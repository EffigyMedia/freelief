"""The performance benchmark (Performance_Testing.md): REQ-026, REQ-027 and REQ-028.

Workload: the installed app, offline, cold-launched in a fresh page, with the CPU throttled 4x
as the stand-in for a mid-range phone. Each figure is the median of RUNS launches.
Writes output/bench.json and prints a table. Exit 1 if a target is missed. Exit 2 if the machine
was busy, because a timing taken on a busy machine is not valid either way (AUD-079).

Run:  python tools/freelief.py bench
"""

import json
import os
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))
import freelief  # noqa: E402
from harness import ROOT, base_url, browser, wait_until  # noqa: E402

RUNS = 7
CPU_SLOWDOWN = 4
LAUNCH_TARGET_MS = 1000
RESPONSE_TARGET_MS = 100

# The recorded baseline (docs/performance/baseline.md) and its tolerance. Over tolerance prints FLAG
# but does not fail: a flagged metric goes into docs/performance/log.md, and only a missed target
# fails (AUD-058). Keep these in step with baseline.md when it is re-baselined.
def read_baseline() -> dict:
    """The baseline figures from docs/performance/baseline.md, its one source (AUD-123)."""
    import re
    text = (ROOT / "docs" / "performance" / "baseline.md").read_text("utf-8")
    rows = {"launch_ms": "REQ-026", "response_ms": "REQ-027", "size_kb": "REQ-028"}
    found = {}
    for key, req in rows.items():
        line = next(l for l in text.splitlines() if l.startswith("|") and f"({req})" in l)
        found[key] = float(re.search(r"([0-9.]+)\s*(?:ms|KB)", line.split("|")[3]).group(1))
    return found


BASELINE = read_baseline()
TIMING_TOLERANCE = 0.25  # +25% for the two timings; any size growth is flagged
# A quiet machine is a condition of the measurement (Performance_Testing.md section 2). Above this
# CPU load, sampled before and after every run, the result is not valid (AUD-079).
BUSY_LOAD_PERCENT = 35

# Response: from a click on "Need urgent help?" (on every screen) to the moment after the frame that
# shows the dialog is painted. A requestAnimationFrame callback runs before that paint, so the probe
# ends on a message posted from it, which runs after the paint (AUD-087).
RESPONSE_PROBE = """() => new Promise(resolve => {
  const button = document.querySelector('.help-open');
  const dialog = document.querySelector('dialog.help');
  const start = performance.now();
  new MutationObserver((_, observer) => {
    observer.disconnect();
    requestAnimationFrame(() => {
      const channel = new MessageChannel();
      channel.port1.onmessage = () => resolve(performance.now() - start);
      channel.port2.postMessage(0);
    });
  }).observe(dialog, { attributes: true });
  button.click();
})"""


def cpu_load(seconds: float = 1.0) -> float | None:
    """The machine's CPU load in percent over `seconds`, or None where it cannot be read.

    On Windows it reads the kernel's idle, kernel and user times twice (GetSystemTimes) and takes the
    busy share between the readings. An earlier probe started PowerShell for each sample and mostly
    measured its own start-up, so every run read as busy (AUD-079, round UNT-104)."""
    import time
    if os.name == "nt":
        import ctypes
        from ctypes import wintypes

        def times():
            idle, kernel, user = wintypes.FILETIME(), wintypes.FILETIME(), wintypes.FILETIME()
            if not ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
                return None
            value = lambda ft: (ft.dwHighDateTime << 32) | ft.dwLowDateTime
            return value(idle), value(kernel), value(user)

        first = times()
        time.sleep(seconds)
        second = times()
        if not first or not second:
            return None
        idle = second[0] - first[0]
        total = (second[1] - first[1]) + (second[2] - first[2])  # kernel time includes idle time
        return round(100 * (total - idle) / total, 1) if total else None
    if hasattr(os, "getloadavg"):
        return 100 * os.getloadavg()[0] / (os.cpu_count() or 1)
    return None


def main() -> int:
    context = browser().new_context(viewport={"width": 390, "height": 844}, service_workers="allow")
    page = context.new_page()
    page.goto(base_url())
    page.evaluate("navigator.serviceWorker.ready")
    page.reload()
    wait_until(page, "navigator.serviceWorker.controller !== null")
    page.close()
    context.set_offline(True)

    launches, responses, loads = [], [], []
    for _ in range(RUNS):
        loads.append(cpu_load())
        page = context.new_page()
        cdp = context.new_cdp_session(page)
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": CPU_SLOWDOWN})
        page.goto(base_url())
        wait_until(page, "performance.getEntriesByName('freelief-ready').length > 0")
        launches.append(page.evaluate("performance.getEntriesByName('freelief-ready')[0].startTime"))
        responses.append(page.evaluate(RESPONSE_PROBE))
        page.close()
        loads.append(cpu_load())
    context.close()
    known = [load for load in loads if load is not None]
    busiest = max(known) if known else None

    size_kb = sum(f.stat().st_size for f in freelief.shipped_files()) / 1024
    result = {
        "version": freelief.read_version(),
        "workload": f"installed, offline, cold launch, CPU {CPU_SLOWDOWN}x slower, median of {RUNS}",
        "launch_ms": round(statistics.median(launches), 1),
        "response_ms": round(statistics.median(responses), 1),
        "launch_worst_ms": round(max(launches), 1),
        "response_worst_ms": round(max(responses), 1),
        "response_spread_ms": round(statistics.pstdev(responses), 1),
        "size_kb": round(size_kb, 1),
        "busiest_cpu_load_percent": busiest,
    }
    out = ROOT / "output" / "bench.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", "utf-8")

    checks = [
        ("Launch to first screen (REQ-026)", "launch_ms", LAUNCH_TARGET_MS, "ms", TIMING_TOLERANCE),
        ("Input to visible response (REQ-027)", "response_ms", RESPONSE_TARGET_MS, "ms", TIMING_TOLERANCE),
        ("Shipped size (REQ-028)", "size_kb", freelief.SIZE_LIMIT_BYTES / 1024, "KB", 0.0),
    ]
    print(f"Freelief {result['version']} - {result['workload']}")
    failed = False
    for label, key, target, unit, tolerance in checks:
        value, baseline = result[key], BASELINE[key]
        ok = value <= target
        failed |= not ok
        change = (value - baseline) / baseline
        flagged = ok and change > tolerance
        status = "FAIL" if not ok else ("FLAG" if flagged else " OK ")
        print(f"[{status}] {label}: {value} {unit} (target {target:g} {unit}; "
              f"baseline {baseline:g} {unit}, {change:+.0%})")
    print("A FLAG does not fail: record it in docs/performance/log.md (AUD-058).")
    print(f"Response spread {result['response_spread_ms']} ms; worst {result['response_worst_ms']} ms; "
          f"busiest CPU load {busiest if busiest is not None else 'unknown'}%.")
    if busiest is None:
        print("[WARN] the CPU load could not be read, so the quiet-machine condition is not checked")
    elif busiest > BUSY_LOAD_PERCENT:
        print(f"[BUSY] the CPU load reached {busiest:g}%, over {BUSY_LOAD_PERCENT}%: this run is not valid, "
              "pass or fail. Close other work and run it again.")
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
