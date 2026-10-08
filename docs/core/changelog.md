# Changelog

The append-only index of what shipped and when, keyed to version. One short dated entry per feature
commit. Newest on top. **An entry is never edited after the fact.**

Each entry links to the fragment that holds the full record. This project keeps no `tracker.md`:
the fragment store is the tracker, so a link points at the fragment file itself:
`[RLG-001](../fragments/RLG-001.md)`. Both directions must resolve, and that is verified at every
audit.

---

<a id="v0-5-29"></a>
## [0.5.29] - 2026-10-07
- **Ripple pond**: the water drop is softer and more muted: lower, quieter, and filtered.
  [RLG-021](../fragments/RLG-021.md). 106 tests.
- Correction to 0.5.28: that version had 105 tests, not 107.

<a id="v0-5-28"></a>
## [0.5.28] - 2026-10-07
- **Need urgent help?** now shows one country at a time, with a **Country** list to see another,
  in place of the long list of every country.
- **Settings** has a **Region for urgent help**: Automatic, or a country you choose. It is saved
  only on this device. [RLG-020](../fragments/RLG-020.md). 107 tests.

<a id="v0-5-27"></a>
## [0.5.27] - 2026-10-07
- Fixed: with **Need urgent help?** open, a swipe could scroll the app behind it. The app behind
  now stays still until the window closes. [RLG-019](../fragments/RLG-019.md). 103 tests.

<a id="v0-5-26"></a>
## [0.5.26] - 2026-10-07
- New activity: **Color a mandala**. Choose a soft color, then tap a shape to fill it. Three
  designs; the arrow keys and Enter work too, and every shape has a name for a screen reader.
  [RLG-014](../fragments/RLG-014.md), [REQ-033](../fragments/REQ-033.md). 102 tests.

<a id="v0-5-25"></a>
## [0.5.25] - 2026-10-07
- **About**: "Alexander Steele, Effigy Media." now sits on its own line under "Freelief is made
  by". [RLG-017](../fragments/RLG-017.md). 96 tests.

<a id="v0-5-24"></a>
## [0.5.24] - 2026-10-07
- The Effigy Media logo on **About** is now drawn in code: its six bars, soft white on dark and soft
  black on light. The app is 25.6 KB smaller (152.5 KB). [RLG-016](../fragments/RLG-016.md). 96 tests.

<a id="v0-5-23"></a>
## [0.5.23] - 2026-10-07
- New activity: the **Ripple pond**. Touch still water, or draw a finger across it, and soft
  ripples spread out with a quiet water drop. A key press makes a ripple too.
  [RLG-013](../fragments/RLG-013.md), [REQ-032](../fragments/REQ-032.md). 95 tests.

<a id="v0-5-22"></a>
## [0.5.22] - 2026-10-07
- **Visualizer**: the rain is softer, with quieter, rounder drops.
- A new sound choice, **Both**, plays the music with the rain under it.
  [RLG-015](../fragments/RLG-015.md). 89 tests.

<a id="v0-5-21"></a>
## [0.5.21] - 2026-10-07
- The app now uses American spelling everywhere ("Sort colors", "Colors" in Settings).
- **Calm** is renamed **Visualizer**. [RLG-010](../fragments/RLG-010.md). 88 tests.

<a id="v0-5-20"></a>
## [0.5.20] - 2026-10-07
- The activities no longer show instruction text above them. A screen reader still reads how to
  use each one. [RLG-011](../fragments/RLG-011.md). 87 tests.

<a id="v0-5-19"></a>
## [0.5.19] - 2026-10-07
- **Ground yourself** and **Calming words** are removed. Their research was weak, and Freelief
  offers only what it can back. Standards & research no longer lists them.
  [RLG-012](../fragments/RLG-012.md). 86 tests.

<a id="v0-5-18"></a>
## [0.5.18] - 2026-10-07
- **Box breathing** (in 4, hold 4, out 4, rest 4) is now the default rhythm and is listed first in
  Settings. A rhythm you already chose stays. [RLG-009](../fragments/RLG-009.md). 88 tests.

<a id="v0-5-17"></a>
## [0.5.17] - 2026-10-07
- **Back to menu** is now at the top of every screen, just under the header.
- A thin line now divides the header and the footer from the rest of the app.
- The version line on **About** is centred. [RLG-008](../fragments/RLG-008.md). 88 tests.

<a id="v0-5-16"></a>
## [0.5.16] - 2026-10-07
- **Sort colours**: drag a tile onto another tile to swap the two, by touch or mouse. Choosing a
  tile and then the tile to swap it with still works, by touch, mouse or keyboard.
  [RLG-007](../fragments/RLG-007.md). 87 tests.

<a id="v0-5-15"></a>
## [0.5.15] - 2026-10-07
- **About** credits the maker by name: "Freelief is made by Alexander Steele, Effigy Media."

<a id="v0-5-14"></a>
## [0.5.14] - 2026-10-07
- **About** now credits the maker: "Made by" with the Effigy Media logo and a link to
  effigymedia.com. 82 tests.

<a id="v0-5-13"></a>
## [0.5.13] - 2026-10-07
- New app icon, as the owner chose: a brushed **ensō** around a soft breath glow, for the browser
  tab and the home screen.

<a id="v0-5-12"></a>
## [0.5.12] - 2026-10-07
- As the owner asked: buttons outside the header are centred; the footer reads "You are safe right
  now. Take your time."; the singing glass grows from quiet to full with your speed, and its trail runs
  from where the loop began to your finger and clears each loop; Settings has Back to menu at the top;
  **Calm** has **Full screen**, a slowly drifting soft background colour and softly pulsing shape
  colours. 81 tests.

<a id="v0-5-11"></a>
## [0.5.11] - 2026-10-07
- Fix: the owner could not load v0.5.10. The offline worker looked in every cache, so an older
  version's cache could serve old files. It now reads only its own version's cache, and a new version
  that arrives at launch reloads the page once, before you touch anything. **Settings** now shows the
  **version** and an **Update now** button. 78 tests.

<a id="v0-5-10"></a>
## [0.5.10] - 2026-10-07
- As the owner asked: Freelief now **opens on the menu** ("What would help right now?"), with Breathe
  first; **every screen has Back to menu**; **Settings is a gear** at the top right of every screen.
  [REQ-018](../fragments/REQ-018.md) and [REQ-026](../fragments/REQ-026.md) changed. 75 tests.

<a id="v0-5-9"></a>
## [0.5.9] - 2026-10-07
- **Standards and research** now covers what was added since slice 4: the colour sort under
  distraction, and a new entry for Calm music and rain with two checked sources (a meta-analysis of
  104 trials on music and stress; one small study on nature sounds), each with an honest note on the
  strength of the evidence. 74 tests.

<a id="v0-5-8"></a>
## [0.5.8] - 2026-10-07
- Softer sounds everywhere, as the owner asked: lower notes, slow swells, long fades and lower
  volume (the grounding chime was abrasive). The bubble pop is now a soft percussive pop. **Calm** has
  a **Music** or **Rain** choice, remembered on the device. Activity buttons are centred. 74 tests.

<a id="v0-5-7"></a>
## [0.5.7] - 2026-10-07
- Faster start again ([RLG-006](../fragments/RLG-006.md)): the breathing guide is ready in about 132 ms
  (was 224 ms). The safety fallback no longer paints on every launch; it shows only if the start
  fails. Other screens load on their first visit. A link such as `#constructor` now opens breathing
  ([AUD-005](../fragments/AUD-005.md)). 72 tests.

<a id="v0-5-6"></a>
## [0.5.6] - 2026-10-07
- New **Calm** screen, as the owner asked: slow musical pads, soft geometric shapes that fade in and
  out like a screen saver, and a **Black screen** button (one tap brings the screen back; the music
  keeps playing). Fixed in the tests: the test server refused connections when the service worker
  fetched every file at once, which made one test fail at random. 71 tests.

<a id="v0-5-5"></a>
## [0.5.5] - 2026-10-07
- **Trace a shape** now has twelve shapes: figure eight, circle, ripple, flower, star, heart, petal,
  trefoil knot, weave, soft square, egg and clover. **New shape** moves to the next one, and each
  shape sings on its own note. 64 tests.

<a id="v0-5-4"></a>
## [0.5.4] - 2026-10-07
- Sounds, as the owner asked ([REQ-007](../fragments/REQ-007.md) changed): subtle sounds are on by
  default, with one **Sounds** switch in Settings. Each breathing tone now lasts its whole phase and
  stops on Pause. New cues: a chime on Next in grounding and calming words, a singing crystal glass
  while tracing a shape (louder with speed, fading when you stop), a two-note chime per loop, and a
  click and a rising phrase in the colour sort. Nothing plays before your first tap. Also: a stored
  rhythm name such as "constructor" no longer passes the settings check. 63 tests.

<a id="v0-5-3"></a>
## [0.5.3] - 2026-10-07
- From the owner's phone test: the urgent-help window has a **Back** button at the top that stays
  visible while you scroll, and the phone's back gesture closes the window without leaving the app
  ([AUD-044](../fragments/AUD-044.md)). Every exercise and activity now offers **More ways to calm**
  as well as **Back to breathing**. 58 tests.

<a id="v0-5-2"></a>
## [0.5.2] - 2026-10-07
- Fix (audit [AUD-002](../fragments/AUD-002.md)): if Freelief cannot start, the page no longer
  stays blank. A static fallback shows how to breathe, says to call the local emergency number, and
  links the helpline directory, even with JavaScript off. If only the crisis-lines file fails, the
  app runs and the help dialog keeps the emergency line and the directory. Start-up errors are
  logged. Restored the `crisis` section of `config.json`, lost in slice 2. 55 tests.

<a id="v0-5-1"></a>
## [0.5.1] - 2026-10-07
- Fix (audit [AUD-001](../fragments/AUD-001.md), [AUD-014](../fragments/AUD-014.md),
  [AUD-013](../fragments/AUD-013.md)): Freelief's offline copy repairs itself after another app on
  the shared `effigymedia.github.io` origin deletes it; Freelief no longer deletes other apps'
  caches; the offline copy is always fetched fresh, past the browser's HTTP cache. Three new tests,
  including a real version update. 51 tests.

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
