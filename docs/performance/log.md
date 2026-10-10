# Performance Log

Append-only, newest on top. Format: `Performance_Testing.md` §7.

## 2026-10-10 — Round UNT-124 health step (v0.8.14), recorded late (AUD-135)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 154 ms | 206.2 to 211.8 ms | +34% to +38% | FLAG, under target |
| Response: Need urgent help? opens (to after paint) | 77 ms | 100.1 to 102.9 ms | +30% to +34% | FAIL (AUD-131) |
| Shipped size | 239.8 KB | 233.1 KB | -3% | OK |
Notes: four valid runs of six at the 35% limit then in force (33.1%, 33.7%, 33.9%, 34.9% busiest
load); two were BUSY (40.5%, 55.2%). Under the rule of AUD-134 (baseline load 27% plus 5 points) none
of the four would be comparable. The response failure was not seen at the version that caused it,
because no bench ran between v0.7.13 and this round; every live move now runs one (AUD-135). Fixed in
v0.8.15 (AUD-131).

## 2026-10-10 — The help dialog is warmed after the first paint (v0.8.15), NOT VALID: busy machine
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 154 ms | 242.7 to 264.1 ms | +58% to +71% | FLAG, under target; not valid |
| Response: Need urgent help? opens (to after paint) | 77 ms | 27.9 to 29.3 ms | -62% to -64% | OK; not valid |
| Shipped size | 239.8 KB | 233.9 KB | -2% | OK |
Notes: AUD-131. Round UNT-124 measured the response at 100.1 to 102.9 ms on valid runs (33% to
35% load). A probe split it: the click handler took about 90 ms, and showModal() took 78 to 93 ms of
that, because the first open styled and laid out the dialog's content from nothing. An empty dialog
took 17 ms. app.js now lays the dialog out once, unseen, just after the first paint (warmHelp). In
the same probe, at 4x CPU and before the bench, the response fell from 107.9 ms to 23.9 ms (median of
7) and the launch was unchanged (230.7 and 232.7 ms). Warming before the ready mark was tried and
rejected: it moved the launch to 409 ms. All four bench runs above had 81% to 96.5% load, so none is
valid; the launch rise is load, as the same probe showed no change. A quiet re-baseline is owed
(RLG-033, AUD-134).

## 2026-10-09 — Slice 8 close and re-baseline (v0.7.13)
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 178 ms | 154 ms | -13% | OK; RE-BASELINED |
| Response: Need urgent help? opens (to after paint) | 74 ms (old end point) | 77 ms | n/a | OK; RE-BASELINED; 23 ms of headroom |
| Shipped size | 188.7 KB | 239.8 KB | +27% | FLAG, expected; RE-BASELINED; 10 KB of budget left |
Notes: the first valid runs since AUD-087 moved the end point. The load probe was fixed in round
UNT-104 (AUD-079): it now reads kernel CPU times and agreed with the system counter (14% to 17%
idle). Runs at 22.2%, 26.6% and 25.9% busiest load gave 79.7, 77.6 and 76.8 ms; the last two follow
a change that skips redrawing the help dialog when its region is unchanged (AUD-115). Size is near
its limit (AUD-124): the next slice must plan against the 10 KB left.

## 2026-10-09 — Slice 8 checkpoint (v0.7.11), NOT VALID: busy machine
| Metric | Baseline | Now | Δ | Verdict |
|---|---|---|---|---|
| Launch to first screen (the menu) | 178 ms | 186.4 ms | +5% | OK, but the run is not valid |
| Response: Need urgent help? opens | 74 ms | 96.5 ms | +30% | FLAG, under target; not valid; new end point |
| Shipped size | 188.7 KB | 232.8 KB | +23% | FLAG, expected; 17 KB of budget left |
Notes: the busiest CPU load sample was 58%, over the 35% limit that bench now enforces (AUD-079),
so the two timings are not evidence either way. The response probe now ends after the dialog's
frame is painted (AUD-087), so it is not comparable with the 74 ms baseline. The size is exact and
valid: slice 8 added Unblock and its fifteen boards, the background sound and waves, the
interfering pond and the five mandala designs. A re-baseline on a quiet machine is owed before a
release (RLG-033). The response is the metric to watch: on this busy run it had 3.5 ms of headroom.

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
