# Performance Baseline
Established: 2026-10-07 (v0.1.0, slice 1) — re-baselined: 2026-10-07 (v0.5.10), because the first
screen became the menu (REQ-018 changed) and the response probe moved from Pause to the urgent-help
button, so both figures now measure different things — re-baselined: 2026-10-08 (v0.6.2), at the end
of slice 6, which added three activities, vibration, the wake lock, the country list and more
strings (see the log).

## Environment
Desktop stand-in for a mid-range phone: AMD Ryzen 7 3800X, Windows 11 Pro, Chrome 154 driven by
Playwright 1.63, with the CPU throttled 4x through the Chrome DevTools Protocol. Phone viewport
390 x 844. The figures are a stand-in, not a measurement on a real phone; the owner's phone check
is the on-target confirmation.

**A quiet machine is a condition of every run (AUD-079).** `bench.py` samples the CPU load before
and after each run. If the busiest sample is over 35%, the run is not valid, pass or fail, and
bench exits 2. On 2026-10-09 this machine stayed between 33% and 63% load from other applications,
so the figures below were not re-taken; a re-baseline on a quiet machine is owed (RLG-033).

## Workload
`tools/bench.py`, run by `python tools/freelief.py bench`. The app is installed (one online visit
lets the service worker cache it), then the browser context goes offline. Each run opens a fresh
page, cold, and measures:
- **Launch:** from navigation start to the `freelief-ready` mark that `app.js` sets after the
  first screen (the menu) is on screen.
- **Response:** from a click on `Need urgent help?` to just after the frame that shows the dialog
  is painted (since 2026-10-09, AUD-087: it ended before that paint). The 74 ms baseline used the
  old end point.
- **Size:** the bytes of every shipped file (`build` uses the same list).

Seven runs; the median and the worst are recorded. Results go to `output/bench.json`.

## Metrics
| Metric | Target (design doc) | Baseline median | Baseline worst | Tolerance |
|---|---|---|---|---|
| Launch to first screen (REQ-026) | < 1000 ms | 178 ms | — | +25%, and never over target |
| Input to visible response (REQ-027) | < 100 ms | 74 ms | — | +25%, and never over 100 ms |
| Shipped size (REQ-028) | < 250 KB (was 150 KB until 2026-10-07) | 188.7 KB | — | any growth is noted in the log |

`tools/bench.py` holds these medians in `BASELINE` and prints `FLAG`, without failing, when a timing
is over +25% or the size has grown; only a missed target fails (AUD-058). Keep the two in step.

*Before the re-baseline (v0.1.0): launch to the breathing guide 110 ms; Pause response 10 ms;
41.3 KB. At v0.5.10: 155 ms, 69 ms, 130.3 KB.* The urgent-help response is close to its target: a
35% rise would cross it, so watch it.

The tolerance is wide because a millisecond-scale figure moves with machine load. The targets are
hard limits whatever the tolerance says.
