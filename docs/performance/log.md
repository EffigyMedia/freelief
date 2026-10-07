# Performance Log

Append-only, newest on top. Format: `Performance_Testing.md` §7.

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
