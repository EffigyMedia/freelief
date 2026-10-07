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
SIZE_LIMIT_BYTES = 150 * 1024

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


def shipped_files() -> list[Path]:
    """Every tracked or new file that a visitor's browser can download."""
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    return [ROOT / p for p in listed
            if p and not p.startswith(NOT_SHIPPED) and (ROOT / p).is_file()]


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


def cmd_build(_: argparse.Namespace) -> int:
    """No build step: the repository is the distributable. This checks that it is shippable."""
    files = shipped_files()
    total = sum(f.stat().st_size for f in files)
    print(f"No build step: GitHub Pages serves the repository as it is (REQ-019).")
    print(f"Shipped: {len(files)} file(s), {total / 1024:.1f} KB of {SIZE_LIMIT_BYTES / 1024:.0f} KB (REQ-028)")
    if total > SIZE_LIMIT_BYTES:
        print("[FAIL] over the size limit")
        return 1
    print("[ OK ] shippable")
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
    for name in ("setup", "doctor", "run", "build", "clean", "bench"):
        sub.add_parser(name)
    test = sub.add_parser("test")
    test.add_argument("pattern", nargs="*", help="run only test files whose name holds one of these")
    args = parser.parse_args()
    return globals()[f"cmd_{args.command}"](args)


if __name__ == "__main__":
    sys.exit(main())
