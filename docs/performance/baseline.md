# Performance Baseline
Established: 2026-10-07 (v0.1.0, slice 1)

## Environment
Desktop stand-in for a mid-range phone: AMD Ryzen 7 3800X, Windows 11 Pro, Chrome 154 driven by
Playwright 1.63, with the CPU throttled 4x through the Chrome DevTools Protocol. Phone viewport
390 x 844. The figures are a stand-in, not a measurement on a real phone; the owner's phone check
is the on-target confirmation.

## Workload
`tools/bench.py`, run by `python tools/freelief.py bench`. The app is installed (one online visit
lets the service worker cache it), then the browser context goes offline. Each run opens a fresh
page, cold, and measures:
- **Launch:** from navigation start to the `freelief-ready` mark that `app.js` sets after the
  breathing guide is on screen.
- **Response:** from a click on the Pause control to the next frame after its label changes.
- **Size:** the bytes of every shipped file (`build` uses the same list).

Seven runs; the median and the worst are recorded. Results go to `output/bench.json`.

## Metrics
| Metric | Target (design doc) | Baseline median | Baseline worst | Tolerance |
|---|---|---|---|---|
| Launch to breathing guide (REQ-026) | < 1000 ms | 110 ms | 112 ms | +25%, and never over target |
| Input to visible response (REQ-027) | < 100 ms | 10 ms | 11 ms | +25%, and never over target |
| Shipped size (REQ-028) | < 150 KB | 41.3 KB | — | any growth is noted in the log |

The tolerance is wide because a millisecond-scale figure moves with machine load. The targets are
hard limits whatever the tolerance says.
