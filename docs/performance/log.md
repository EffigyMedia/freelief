# Performance Log

Append-only, newest on top. Format: `Performance_Testing.md` §7.

## 2026-10-08 — Slice 6 checkpoint and re-baseline (v0.6.2)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 155 ms | 178 ms | +15% | OK; RE-BASELINED |
| Response: Need urgent help? opens | 69 ms | 74 ms | +8% | OK; RE-BASELINED; 26 ms of headroom |
| Shipped size | 130.3 KB | 188.7 KB | +45% | FLAG, expected; RE-BASELINED; 61 KB of budget left |
Notes: two runs agreed (177.3 and 177.7 ms; 74.7 and 74.2 ms). Slice 6 added the ripple pond,
mandala coloring and the Visualizer, vibration, the screen wake lock, the country list, the header
sound button, the research sources for every activity and longer strings; the SVG logo saved 25.6
KB. The audit round's 207.8 ms (AUD-058) was a single run on a busy machine. bench now flags a
metric over tolerance (AUD-058). Watch the response: the help dialog grew with the Call buttons.

## 2026-10-07 — Re-baseline (v0.5.10)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 155 ms | 155 ms | new | RE-BASELINED |
| Response: Need urgent help? opens | 69 ms | 69 ms | new | RE-BASELINED; 31 ms of headroom |
| Shipped size | 130.3 KB | 130.3 KB | new | RE-BASELINED; 20 KB of budget left |
Notes: the owner made the menu the first screen, and the Pause control is no longer on it, so the
response probe now opens the urgent-help dialog. Opening a modal dialog with every crisis line is
heavier than toggling a label; it is the control that matters most, so it is the one to measure.

## 2026-10-07 — RLG-006 fixed (v0.5.7)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 132–146 ms | +20% to +33% | BORDERLINE: two runs, one over the +25% tolerance; far inside the 1 s target (was 224 ms) |
| Input to visible response | 10 ms | 10 ms | 0% | OK |
| Shipped size | 41.3 KB | 122.0 KB | +195% | OK; 28 KB of budget left |
Notes: the cause was the static fallback (AUD-002), painted before the app ran; `fallback.js` now
hides it until a start fails. Lazy loading of the non-breathing screens gave about 10 ms more.
The two runs differ by 14 ms on the same build, so machine load moves this figure; watch it at the
next checkpoint before more work on it.

## 2026-10-07 — Checkpoint (v0.5.6, after sounds, shapes and Calm)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 224 ms | +104% | REGRESSION → RLG-006 (within the 1 s target) |
| Input to visible response | 10 ms | 11 ms | +10% | OK |
| Shipped size | 41.3 KB | 120.2 KB | +191% | OK, expected; 30 KB of budget left |
Notes: two runs, 231 ms and 224 ms. Every screen is imported before the first paint. The fix is the
planned lazy loading of the non-breathing screens.

## 2026-10-07 — Slice 5 checkpoint (v0.5.0)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 132 ms | +20% | OK, within tolerance |
| Input to visible response | 10 ms | 9 ms | -10% | OK |
| Shipped size | 41.3 KB | 95.0 KB | +130% | OK, expected |
Notes: all five slices are in. 55 KB of the 150 KB budget remain. Launch is near the +25%
tolerance; lazy loading of the non-breathing screens is the planned remedy if it crosses.

## 2026-10-07 — Slice 4 checkpoint (v0.4.0)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 132 ms | +20% | OK, within tolerance |
| Input to visible response | 10 ms | 9 ms | -10% | OK |
| Shipped size | 41.3 KB | 88.6 KB | +115% | OK, expected |
Notes: three page modules, two data files and about 9 KB more text. The launch loads every module
before the first paint, so each new screen adds a little to it. If a later slice crosses the +25%
tolerance, load the non-breathing screens lazily (dynamic `import()` on first visit).

## 2026-10-07 — Slice 3 checkpoint (v0.3.0)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 124 ms | +13% | OK |
| Input to visible response | 10 ms | 9 ms | -10% | OK |
| Shipped size | 41.3 KB | 70.2 KB | +70% | OK, expected |
Notes: two activity modules, their strings and styles. 80 KB of the 150 KB budget remain for slices
4 and 5.

## 2026-10-07 — Slice 2 checkpoint (v0.2.0)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 123 ms | +12% | OK |
| Input to visible response | 10 ms | 10 ms | 0% | OK |
| Shipped size | 41.3 KB | 57.9 KB | +40% | OK, expected |
Notes: five new modules (two exercises, two screens, settings, audio) and the larger strings file.
The launch now loads every module before the first paint; still far inside 1 s.

## 2026-10-07 — Baseline (v0.1.0, slice 1)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to breathing guide | 110 ms | 110 ms | 0% | OK |
| Input to visible response | 10 ms | 10 ms | 0% | OK |
| Shipped size | 41.3 KB | 41.3 KB | 0% | OK |
Notes: the two PNG icons are 31 KB of the 41 KB. They are needed for home-screen install.
