# Changelog

The append-only index of what shipped and when, keyed to version. One short dated entry per feature
commit. Newest on top. **An entry is never edited after the fact.**

Each entry links to the fragment that holds the full record. This project keeps no `tracker.md`:
the fragment store is the tracker, so a link points at the fragment file itself:
`[RLG-001](../fragments/RLG-001.md)`. Both directions must resolve, and that is verified at every
audit.

---

<a id="v0-5-0"></a>
## [0.5.0] - 2026-10-07
- Slice 5, the colour sort [RLG-005](../fragments/RLG-005.md): put five soft tiles in order from
  lightest to darkest by choosing a tile, then the tile to swap it with, by touch, mouse or
  keyboard. Every tile names its shade, so it works with a screen reader; the row is one tab stop
  with arrow keys inside; "New colours" changes the palette. It passed every automated check, so it
  ships. REQ-014 changed from "drag or keyboard" to this method and waits for the owner's
  confirmation. All five delivery slices are now built. 48 tests; bench 132 ms, 9 ms, 95 KB.

<a id="v0-4-0"></a>
## [0.4.0] - 2026-10-07
- Slice 4, trust pages [RLG-004](../fragments/RLG-004.md): footer links on every screen to
  **About and disclaimer** (self-help not medical care, when to see a professional, privacy, the
  open license, the version), **Standards and research** (what Freelief is built to, no standard
  claimed until people verify it, and every technique with its sources and an honest strength of
  evidence), and **Feedback** (a pre-filled, editable GitHub issue; the email choice waits for an
  address). Two GitHub issue templates. `docs/README.md` for the public repository. The
  claim-wording test now has one named exemption for the disclaimer's denial. 43 tests; bench
  132 ms, 9 ms, 89 KB.

<a id="v0-3-0"></a>
## [0.3.0] - 2026-10-07
- Slice 3, distraction [RLG-003](../fragments/RLG-003.md): "Pop bubbles" (soft bubbles that
  drift slowly, popped by tap or key, replaced a moment later, with a control to stop the drifting
  and no movement under reduced motion) and "Trace a shape" (a figure eight to follow with a finger
  or the arrow keys, read by a screen reader as a slider). No score, no failure, no timer. A soft
  pop tone when tones are on. Three distraction sources added to `docs/research/sources.md`,
  including the caveat that distraction can act as a safety behaviour. Fixed on the way: bubbles
  could overlap and cover each other's touch targets. 33 tests; bench 124 ms, 9 ms, 70 KB.

<a id="v0-2-0"></a>
## [0.2.0] - 2026-10-07
- Slice 2, the exercises [RLG-002](../fragments/RLG-002.md): "More ways to calm" leads to
  5-4-3-2-1 grounding, calming words (ten statements, one at a time) and Settings. Settings has
  three breathing rhythms (calm 4-6, slower 5-7, box 4-4-4-4), soft tones per breath (off by
  default), and a colour choice that can override the device. Settings stay on the device and
  survive blocked storage. Screens have their own address, so the browser Back button works.
  Research sources for each technique are in `docs/research/sources.md`, with an honest note on
  the weak evidence for grounding. Fixed on the way: a breathing timer could run after its screen
  was left. 27 tests; bench 123 ms launch, 10 ms response, 58 KB.

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
