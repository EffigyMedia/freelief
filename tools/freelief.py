"""freelief - the project commands: setup, doctor, test, run, build, clean, bench.

Run from the repository root:  python tools/freelief.py <command>

The app itself has no build step and no dependency (REQ-019). Python and Playwright exist only to
test it, in a project-local `.venv` that `setup` creates. Nothing here ships.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENV = ROOT / ".venv"
VENV_PY = VENV / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
TESTS = ROOT / "tools" / "tests"
OUTPUT = ROOT / "output"
VERSION_FILE = ROOT / "version.js"
PORT = 8000

# The size limit of everything that ships (REQ-028).
SIZE_LIMIT_BYTES = 250 * 1024  # raised from 150 KB by the owner, 2026-10-07 (REQ-028)

# Tracked paths that are NOT part of the app a visitor downloads.
NOT_SHIPPED = ("docs/", "tools/", "input/", ".claude/", ".github/", ".gitignore", ".gitattributes",
               "AGENTS.md", "CLAUDE.md", "config.toml", "tools.toml", "LICENSE", ".nojekyll")

# Pinned, so a test run means the same thing on every machine (AUD-032). Raise them on purpose.
# The packages they pull in are pinned as well, so every machine installs the same set (AUD-032).
PIP_PACKAGES = ("playwright==1.63.0", "axe-playwright-python==0.1.8",
                "greenlet==3.5.6", "pyee==13.0.1", "typing-extensions==4.16.0")


def uv() -> str | None:
    """The environment's uv, found by walking up to the env root."""
    for parent in ROOT.parents:
        if (parent / ".code-continuum-env-root").is_file():
            for name in ("uv.cmd", "uv.exe", "uv"):
                candidate = parent / "Runtime" / "bin" / name
                if candidate.is_file():
                    return str(candidate)
    return shutil.which("uv")


def read_version() -> str | None:
    """The one authoritative version, from version.js."""
    if not VERSION_FILE.is_file():
        return None
    match = re.search(r'FREELIEF_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', VERSION_FILE.read_text("utf-8"))
    return match.group(1) if match else None


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout


def is_shipped(path: str) -> bool:
    return bool(path) and not path.startswith(NOT_SHIPPED)


def shipped_files() -> list[Path]:
    """Every tracked file that a visitor's browser can download: what GitHub Pages deploys from a
    commit, not what happens to be in the working tree (AUD-011)."""
    return [ROOT / p for p in git("ls-files", "--cached").split("\n")
            if is_shipped(p) and (ROOT / p).is_file()]


def uncommitted_shipped() -> list[str]:
    """Shipped paths that are new or changed in the working tree, so not what a commit deploys."""
    lines = git("status", "--porcelain", "--untracked-files=all").splitlines()
    return [line[3:] for line in lines if is_shipped(line[3:])]


VERSION_LINE = r'FREELIEF_VERSION\s*=\s*"(\d+\.\d+\.\d+)"'


def changed_since_version_bump(cwd: Path = ROOT) -> list[str]:
    """Shipped files committed after the last commit that changed the version number (AUD-010). An
    installed app keeps its cache until the version changes, so such a file would never reach it. The
    bump is the last commit whose diff touches the FREELIEF_VERSION line, so a change to a comment in
    version.js is not a bump (AUD-136)."""
    bump = git("log", "-1", "--format=%H", "-G", r"FREELIEF_VERSION\s*=", "--", "version.js", cwd=cwd).strip()
    if not bump:
        return []
    return [p for p in git("diff", "--name-only", bump, "HEAD", cwd=cwd).split("\n") if is_shipped(p)]


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def version_not_raised(cwd: Path = ROOT) -> list[str]:
    """A problem when HEAD's version is not higher than the version at the last preview or release
    tag (AUD-136). HEAD at the tagged commit itself is no new release, so it passes."""
    try:
        tag = git("describe", "--tags", "--abbrev=0", "--match", "preview-*", "--match", "v*", cwd=cwd).strip()
    except subprocess.CalledProcessError:
        return []
    if git("rev-list", "-n", "1", tag, cwd=cwd).strip() == git("rev-parse", "HEAD", cwd=cwd).strip():
        return []

    def at(ref: str) -> str | None:
        match = re.search(VERSION_LINE, git("show", f"{ref}:version.js", cwd=cwd))
        return match.group(1) if match else None

    tagged, head = at(tag), at("HEAD")
    if tagged and head and version_key(head) <= version_key(tagged):
        return [f"version {head} is not higher than {tagged} at {tag}"]
    return []


def stale_crisis_checks(max_age_days: int, today=None) -> list[str]:
    """Crisis lines and the directory last checked longer ago than the window (AUD-024)."""
    import datetime
    import json
    today = today or datetime.date.today()
    data = json.loads((ROOT / "data" / "crisis-lines.json").read_text("utf-8"))
    entries = [("directory", data["directory"].get("checked"))]
    for code, region in data["regions"].items():
        entries += [(f"{code}: {line['name']}", line.get("checked")) for line in region["lines"]]
    stale = []
    for name, checked in entries:
        try:
            age = (today - datetime.date.fromisoformat(checked)).days
        except (TypeError, ValueError):
            stale.append(f"{name} (no valid date)")
            continue
        if age < 0:
            # A date after today is a typing error, and it would pass every age check (AUD-137).
            stale.append(f"{name} (checked {checked}, in the future)")
        elif age > max_age_days:
            stale.append(f"{name} (checked {checked}, {age} days ago)")
    return stale


# --- commands -------------------------------------------------------------------------------

def cmd_setup(_: argparse.Namespace) -> int:
    tool = uv()
    if tool is None:
        print("[FAIL] uv not found: not in <env-root>/Runtime/bin and not on PATH")
        return 1
    if not VENV_PY.is_file():
        subprocess.run([tool, "venv", str(VENV)], cwd=ROOT, check=True)
    subprocess.run([tool, "pip", "install", "--python", str(VENV), *PIP_PACKAGES], cwd=ROOT, check=True)
    # WebKit runs the never-break paths, and doctor requires it (AUD-086). Chrome is the one on the
    # machine; Firefox needs a Windows runtime first (RLG-033), so it is not installed here.
    subprocess.run([str(VENV_PY), "-m", "playwright", "install", "webkit"], cwd=ROOT, check=True)
    print("[ OK ] setup complete")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    problems: list[str] = []

    def check(ok: bool, label: str, fix: str = "") -> None:
        print(f"[{' OK ' if ok else 'FAIL'}] {label}" + ("" if ok else f" - {fix}"))
        if not ok:
            problems.append(label)

    check(sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (3.10 or later)")
    check(VENV_PY.is_file(), "project .venv exists", "run: python tools/freelief.py setup")
    if VENV_PY.is_file():
        probe = subprocess.run([str(VENV_PY), "-c", "import playwright, axe_playwright_python"],
                               capture_output=True, text=True)
        check(probe.returncode == 0, "Playwright and axe import in .venv",
              "run: python tools/freelief.py setup")
        # Every package is the pinned version (AUD-032).
        listed = subprocess.run([str(VENV_PY), "-c",
                                 "import importlib.metadata as m; print('\\n'.join(f'{d.metadata[\"Name\"].lower()}=={d.version}' for d in m.distributions()))"],
                                capture_output=True, text=True).stdout.split()
        # Package names compare with "_" and "-" as the same, as pip does.
        norm = lambda text: text.lower().replace("_", "-")
        installed = {norm(line.split("==")[0]): norm(line) for line in listed}
        wrong = [pin for pin in PIP_PACKAGES if installed.get(norm(pin.split("==")[0])) != norm(pin)]
        check(not wrong, f"the {len(PIP_PACKAGES)} test packages are the pinned versions",
              "differs: " + ", ".join(wrong) + "; run: python tools/freelief.py setup")
        # The browser the tests, bench and icon tool drive: the installed Chrome, or Playwright's
        # own Chromium (AUD-012). Launched once, so a missing browser shows here, not mid-suite.
        launch = subprocess.run([str(VENV_PY), "-c",
                                 "import sys; sys.path.insert(0, 'tools/tests'); import harness; "
                                 "b = harness.browser(); print(b.version)"],
                                cwd=ROOT, capture_output=True, text=True)
        check(launch.returncode == 0, f"a browser launches for the tests ({launch.stdout.strip() or 'none'})",
              "install Google Chrome, or run: .venv python -m playwright install chromium")
        # The supported-browser engines (AUD-028). WebKit is required; Firefox is reported until its
        # engine can start here (it needs the Microsoft Visual C++ runtime on Windows; RLG-033).
        for name, required in (("webkit", True), ("firefox", False)):
            probe = subprocess.run([str(VENV_PY), "-c",
                                    "import sys; sys.path.insert(0, 'tools/tests'); import harness; "
                                    f"print(harness.engine('{name}').version)"],
                                   cwd=ROOT, capture_output=True, text=True)
            ok = probe.returncode == 0
            if required or ok:
                check(ok, f"{name} launches for the browser tests ({probe.stdout.strip() or 'none'})",
                      f"run: .venv python -m playwright install {name}")
            else:
                print(f"[WARN] {name} cannot start here, so its browser tests do not run "
                      "(install the Microsoft Visual C++ runtime; see RLG-033)")
    check(read_version() is not None, "version.js holds FREELIEF_VERSION = \"X.Y.Z\"")
    import json
    # Every JSON file that ships; a missing one fails, it is not skipped (AUD-035).
    for name in ("manifest.webmanifest", "config.json", "strings/en.json", "data/crisis-lines.json",
                ):
        path = ROOT / name
        if not path.exists():
            check(False, f"{name} exists", "the app needs it")
            continue
        try:
            json.loads(path.read_text("utf-8"))
            check(True, f"{name} parses")
        except ValueError as error:
            check(False, f"{name} parses", str(error))
    # The worker: it imports version.js, and every file it caches exists (AUD-036).
    worker = ROOT / "sw.js"
    if worker.is_file():
        source = worker.read_text("utf-8")
        listed = re.findall(r'^\s+"([^"]+)",$', source.split("const FILES = [", 1)[-1].split("];", 1)[0], re.M)
        missing = [f for f in listed if f != "./" and not (ROOT / f).is_file()]
        check('importScripts("version.js")' in source and listed and not missing,
              f"sw.js imports version.js and its {len(listed)} cached files exist",
              "missing: " + ", ".join(missing) if missing else "check sw.js")
    else:
        check(False, "sw.js exists", "the offline copy needs it")
    # Each test file compiles; a file with a syntax error fails here, not only in `test` (AUD-034).
    collected = sorted(TESTS.glob("test_*.py"))
    broken = []
    for file in collected:
        try:
            compile(file.read_text("utf-8"), str(file), "exec")
        except SyntaxError as error:
            broken.append(f"{file.name}: {error.msg}")
    check(bool(collected) and not broken, f"{len(collected)} test file(s) in tools/tests compile",
          "; ".join(broken) or "no test files")
    # Things a release would refuse, seen at every Resume and not only at a release (AUD-104,
    # AUD-102). They warn: the tree works, but the owner has a duty to do.
    # A broken data file was reported above; these warnings then cannot run, and say so (AUD-119).
    try:
        config = json.loads((ROOT / "config.json").read_text("utf-8"))
        window = config["crisis"]["maxCheckAgeDays"]
        for line in stale_crisis_checks(window):
            print(f"[WARN] crisis data checked more than {window} days ago, re-check it: {line}")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"[WARN] the crisis-line freshness check could not run: {error}")
    print(f"\n{'READY' if not problems else f'NOT READY: {len(problems)} problem(s)'}")
    return 0 if not problems else 1


def cmd_test(args: argparse.Namespace) -> int:
    """Run every test_* function in tools/tests/test_*.py. Fails loudly on a file it cannot load."""
    if not VENV_PY.is_file():
        print("[FAIL] no .venv - run: python tools/freelief.py setup")
        return 1
    if Path(sys.executable).resolve() != VENV_PY.resolve():
        # Re-run inside the venv, where Playwright lives.
        return subprocess.run([str(VENV_PY), __file__, "test", *args.pattern], cwd=ROOT).returncode

    sys.path.insert(0, str(TESTS))
    files = sorted(TESTS.glob("test_*.py"))
    if args.pattern:
        files = [f for f in files if any(p in f.name for p in args.pattern)]
    if not files:
        print("[FAIL] no test files collected")
        return 1

    passed = failed = 0
    for file in files:
        spec = importlib.util.spec_from_file_location(file.stem, file)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            print(f"[FAIL] {file.name}: could not load")
            traceback.print_exc()
            failed += 1
            continue
        tests = [(n, f) for n, f in vars(module).items() if n.startswith("test_") and callable(f)]
        if not tests:
            print(f"[FAIL] {file.name}: holds no test_ function")
            failed += 1
            continue
        for name, function in tests:
            try:
                function()
                print(f"[ OK ] {file.name}::{name}")
                passed += 1
            except Exception as error:
                print(f"[FAIL] {file.name}::{name}: {error}")
                if not isinstance(error, AssertionError):
                    traceback.print_exc()
                failed += 1
    print(f"\n{passed} passed, {failed} failed")
    # Firefox is a supported browser, so a run without it says so plainly (AUD-028).
    if not firefox_starts():
        print("[WARN] Firefox did not run: its engine cannot start on this machine (see RLG-033)")
    return 0 if failed == 0 else 1


def firefox_starts() -> bool:
    probe = subprocess.run([str(VENV_PY), "-c", "import sys; sys.path.insert(0, 'tools/tests'); import harness; "
                            "harness.engine('firefox')"], cwd=ROOT, capture_output=True, text=True)
    return probe.returncode == 0


def run_handler(shipped: set[str]):
    """A request handler that serves only the shipped files, and only to a page on this machine.

    The folder holds more than the app (.git, input/excluded, docs), so a path that does not ship is
    refused (AUD-118). A Host header other than localhost or 127.0.0.1 is refused too, so a web page
    open in the same browser cannot reach the server by DNS rebinding."""
    import http.server
    hosts = {f"localhost:{PORT}", f"127.0.0.1:{PORT}", "localhost", "127.0.0.1"}

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT), **kwargs)

        def send_head(self):
            if self.headers.get("Host", "") not in hosts:
                self.send_error(403, "This server answers only this machine")
                return None
            path = self.path.split("?", 1)[0].split("#", 1)[0].lstrip("/")
            from urllib.parse import unquote
            path = unquote(path) or "index.html"
            if path not in shipped:
                self.send_error(404, "Not a shipped file")
                return None
            return super().send_head()

        def log_message(self, *args):
            pass

    return Handler


def cmd_run(_: argparse.Namespace) -> int:
    # In this process, so stopping it stops the server; there is no child left on the port (AUD-122).
    import http.server
    shipped = {p.relative_to(ROOT).as_posix() for p in shipped_files()}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), run_handler(shipped))
    print(f"Serving the {len(shipped)} shipped files at http://localhost:{PORT}  (this machine only; Ctrl+C stops it)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    """No build step: the repository is the distributable. This checks that it is shippable.
    With --release it also checks what a release needs: a clean tree, a version bump after the
    last shipped change, and crisis lines checked within the window."""
    import json
    files = shipped_files()
    total = sum(f.stat().st_size for f in files)
    print(f"No build step: GitHub Pages serves the committed repository as it is (REQ-019).")
    print(f"Shipped: {len(files)} file(s), {total / 1024:.1f} KB of {SIZE_LIMIT_BYTES / 1024:.0f} KB (REQ-028)")
    failed = total > SIZE_LIMIT_BYTES
    if failed:
        print("[FAIL] over the size limit")
    dirty = uncommitted_shipped()
    late = changed_since_version_bump() + version_not_raised()
    config = json.loads((ROOT / "config.json").read_text("utf-8"))
    stale = stale_crisis_checks(config["crisis"]["maxCheckAgeDays"])
    for problem, items in (("not committed, so not what Pages deploys", dirty),
                           ("changed after the last version bump, or the version not raised", late),
                           (f"crisis data checked more than {config['crisis']['maxCheckAgeDays']} days ago", stale)):
        if not items:
            continue
        if args.release:
            failed = True
            print(f"[FAIL] {problem}: " + "; ".join(items))
        else:
            print(f"[WARN] {problem}: " + "; ".join(items))
    if failed:
        return 1
    print("[ OK ] shippable" + (" for a release" if args.release else ""))
    return 0


def cached_files() -> set[str]:
    """The files sw.js caches for offline use (its FILES list), without the start URL."""
    source = (ROOT / "sw.js").read_text("utf-8")
    block = re.search(r"const FILES = \[(.*?)\];", source, re.DOTALL).group(1)
    return {f for f in re.findall(r'"([^"]+)"', block) if f != "./"}


def cmd_files(_: argparse.Namespace) -> int:
    """The file audit (AUD-108): every shipped file, its size and whether the offline copy holds it.
    It fails when a shipped file is not cached, or a cached file does not ship. sw.js is the one
    shipped file that is not cached: the browser fetches the worker script itself."""
    shipped = {p.relative_to(ROOT).as_posix(): p.stat().st_size for p in shipped_files()}
    cached = cached_files()
    for path, size in sorted(shipped.items()):
        mark = "cached" if path in cached else ("worker" if path == "sw.js" else "NOT CACHED")
        print(f"{size / 1024:7.1f} KB  {mark:10}  {path}")
    missing = sorted(set(shipped) - cached - {"sw.js"})
    extra = sorted(cached - set(shipped))
    print(f"{len(shipped)} shipped file(s), {sum(shipped.values()) / 1024:.1f} KB; {len(cached)} cached.")
    if missing:
        print("[FAIL] shipped but not cached: " + ", ".join(missing))
    if extra:
        print("[FAIL] cached but not shipped: " + ", ".join(extra))
    if missing or extra:
        return 1
    print("[ OK ] the offline copy holds every shipped file")
    return 0


def cmd_clean(_: argparse.Namespace) -> int:
    """Remove output/ and Python caches. Never touches input/."""
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    for cache in (ROOT / "tools").rglob("__pycache__"):
        shutil.rmtree(cache)
    print("[ OK ] clean")
    return 0


def cmd_bench(_: argparse.Namespace) -> int:
    bench = ROOT / "tools" / "bench.py"
    if not VENV_PY.is_file():
        print("[FAIL] no .venv - run: python tools/freelief.py setup")
        return 1
    if not bench.is_file():
        print("[FAIL] no benchmark yet - it is created with the performance baseline after slice 1")
        return 1
    return subprocess.run([str(VENV_PY), str(bench)], cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(prog="freelief", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("setup", "doctor", "run", "clean", "bench", "files"):
        sub.add_parser(name)
    build = sub.add_parser("build")
    build.add_argument("--release", action="store_true",
                       help="also fail on uncommitted shipped files, a missing version bump and stale crisis data")
    test = sub.add_parser("test")
    test.add_argument("pattern", nargs="*", help="run only test files whose name holds one of these")
    args = parser.parse_args()
    return globals()[f"cmd_{args.command}"](args)


if __name__ == "__main__":
    sys.exit(main())
