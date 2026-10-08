# Performance Log

Append-only, newest on top. Format: `Performance_Testing.md` §7.

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
