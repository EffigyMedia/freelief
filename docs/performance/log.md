# Performance Log

Append-only, newest on top. Format: `Performance_Testing.md` §7.

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
