# Changelog

The append-only index of what shipped and when, keyed to version. One short dated entry per feature
commit. Newest on top. **An entry is never edited after the fact.**

Each entry links to the fragment that holds the full record. This project keeps no `tracker.md`:
the fragment store is the tracker, so a link points at the fragment file itself:
`[RLG-001](../fragments/RLG-001.md)`. Both directions must resolve, and that is verified at every
audit.

---

<a id="v0-1-0"></a>
## [0.1.0] - 2026-10-07
- Slice 1, the walking skeleton [RLG-001](../fragments/RLG-001.md): the breathing guide starts at
  launch (4 in, 6 out) with a pause control; "Need urgent help?" opens crisis lines for the device
  region (US, UK, Canada, Australia, Ireland, each checked 2026-10-07), the emergency number, the
  Find A Helpline directory and the other countries; the self-help line; an installable offline
  app with a versioned cache; a soft dark theme that follows the device light setting. 19 browser
  and repository tests; bench baseline 110 ms launch, 10 ms response, 41 KB. Waiting for the
  owner's phone check.

<a id="v0-0-0"></a>
## [0.0.0] - 2026-10-07
- Initialized: the project commands (`tools/freelief.py`), the test environment, the repository
  rules test, the MIT license, and the five delivery slices as requested tracker items
  [RLG-001](../fragments/RLG-001.md) to [RLG-005](../fragments/RLG-005.md). No app yet.
