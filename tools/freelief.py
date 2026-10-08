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

PIP_PACKAGES = ("playwright", "axe-playwright-python")


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


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


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


def changed_since_version_bump() -> list[str]:
    """Shipped files committed after the last commit that changed version.js (AUD-010). An installed
    app keeps its cache until the version changes, so such a file would never reach it."""
    bump = git("log", "-1", "--format=%H", "--", "version.js").strip()
    if not bump:
        return []
    return [p for p in git("diff", "--name-only", bump, "HEAD").split("\n") if is_shipped(p)]


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
        if age > max_age_days:
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
    check(read_version() is not None, "version.js holds FREELIEF_VERSION = \"X.Y.Z\"")
    for name in ("manifest.webmanifest", "config.json", "strings/en.json", "data/crisis-lines.json"):
        path = ROOT / name
        if path.exists():
            import json
            try:
                json.loads(path.read_text("utf-8"))
                check(True, f"{name} parses")
            except ValueError as error:
                check(False, f"{name} parses", str(error))
    collected = sorted(TESTS.glob("test_*.py"))
    check(bool(collected), f"tests collectable ({len(collected)} file(s) in tools/tests)")
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
    return 0 if failed == 0 else 1


def cmd_run(_: argparse.Namespace) -> int:
    print(f"Serving {ROOT} at http://localhost:{PORT}  (Ctrl+C stops it)")
    return subprocess.run([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT).returncode


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
    late = changed_since_version_bump()
    config = json.loads((ROOT / "config.json").read_text("utf-8"))
    stale = stale_crisis_checks(config["crisis"]["maxCheckAgeDays"])
    for problem, items in (("not committed, so not what Pages deploys", dirty),
                           ("changed after the last version bump", late),
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
    if not bench.is_file():
        print("[FAIL] no benchmark yet - it is created with the performance baseline after slice 1")
        return 1
    return subprocess.run([str(VENV_PY), str(bench)], cwd=ROOT).returncode


def main() -> int:
    parser = argparse.ArgumentParser(prog="freelief", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("setup", "doctor", "run", "clean", "bench"):
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
