"""The performance benchmark (Performance_Testing.md): REQ-026, REQ-027 and REQ-028.

Workload: the installed app, offline, cold-launched in a fresh page, with the CPU throttled 4x
as the stand-in for a mid-range phone. Each figure is the median of RUNS launches.
Writes output/bench.json and prints a table. Exit 1 if a target is missed.

Run:  python tools/freelief.py bench
"""

import json
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

RESPONSE_PROBE = """() => new Promise(resolve => {
  const button = document.querySelector('.pause');
  const start = performance.now();
  new MutationObserver((_, observer) => {
    observer.disconnect();
    requestAnimationFrame(() => resolve(performance.now() - start));
  }).observe(button, { attributes: true, childList: true, characterData: true, subtree: true });
  button.click();
})"""


def main() -> int:
    context = browser().new_context(viewport={"width": 390, "height": 844}, service_workers="allow")
    page = context.new_page()
    page.goto(base_url())
    page.evaluate("navigator.serviceWorker.ready")
    page.reload()
    wait_until(page, "navigator.serviceWorker.controller !== null")
    page.close()
    context.set_offline(True)

    launches, responses = [], []
    for _ in range(RUNS):
        page = context.new_page()
        cdp = context.new_cdp_session(page)
        cdp.send("Emulation.setCPUThrottlingRate", {"rate": CPU_SLOWDOWN})
        page.goto(base_url())
        wait_until(page, "performance.getEntriesByName('freelief-ready').length > 0")
        launches.append(page.evaluate("performance.getEntriesByName('freelief-ready')[0].startTime"))
        responses.append(page.evaluate(RESPONSE_PROBE))
        page.close()
    context.close()

    size_kb = sum(f.stat().st_size for f in freelief.shipped_files()) / 1024
    result = {
        "version": freelief.read_version(),
        "workload": f"installed, offline, cold launch, CPU {CPU_SLOWDOWN}x slower, median of {RUNS}",
        "launch_ms": round(statistics.median(launches), 1),
        "response_ms": round(statistics.median(responses), 1),
        "launch_worst_ms": round(max(launches), 1),
        "response_worst_ms": round(max(responses), 1),
        "size_kb": round(size_kb, 1),
    }
    out = ROOT / "output" / "bench.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", "utf-8")

    checks = [
        ("Launch to breathing guide (REQ-026)", result["launch_ms"], LAUNCH_TARGET_MS, "ms"),
        ("Input to visible response (REQ-027)", result["response_ms"], RESPONSE_TARGET_MS, "ms"),
        ("Shipped size (REQ-028)", result["size_kb"], freelief.SIZE_LIMIT_BYTES / 1024, "KB"),
    ]
    print(f"Freelief {result['version']} - {result['workload']}")
    failed = False
    for label, value, target, unit in checks:
        ok = value <= target
        failed |= not ok
        print(f"[{' OK ' if ok else 'FAIL'}] {label}: {value} {unit} (target {target:g} {unit})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
