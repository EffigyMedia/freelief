# Changelog

The append-only index of what shipped and when, keyed to version. One short dated entry per feature
commit. Newest on top. **An entry is never edited after the fact.**

Each entry links to the fragment that holds the full record. This project keeps no `tracker.md`:
the fragment store is the tracker, so a link points at the fragment file itself:
`[RLG-001](../fragments/RLG-001.md)`. Both directions must resolve, and that is verified at every
audit.

---

<a id="v0-8-0"></a>
## [0.8.0] - 2026-10-09
**Slice 8 is complete.** Since 0.7.3: Unblock in place of Sort colors, ripples that interfere,
eight mandala designs, background music, rain or waves that keep playing until you stop them, a
Keep the screen on setting, Reset settings, every sound in the music's key, rewritten Standards and
research, the fixes from audit round UNT-082 and from an interface review of every screen, and
design audit round UNT-104.
- Fixed before release (round UNT-104): after urgent help was open for a while, the background
  music could play a burst of queued notes at once; it now stops while help is open and starts
  again after. Reset settings no longer starts the music or turns sound back on. The help dialog
  opens with less work. [AUD-113](../fragments/AUD-113.md), [AUD-114](../fragments/AUD-114.md),
  [AUD-115](../fragments/AUD-115.md).
- Tools and records: bench reads the CPU load correctly and is re-baselined (response 77 ms of
  100 ms); the shared helpers' storage rule is restored in AGENTS.md; slice 9 plans the open
  findings. [AUD-079](../fragments/AUD-079.md), [AUD-116](../fragments/AUD-116.md),
  [AUD-117](../fragments/AUD-117.md). 181 tests.
- The live preview moved to 0.8.0 on 2026-10-09, with the owner's yes in chat ("Keep going until
  you're done and the new slice is live").

<a id="v0-7-13"></a>
## [0.7.13] - 2026-10-09
- Fixes from an interface review of every screen: **Reset settings** asks once more first; the
  page under the black screen and the full screen cannot be reached by Tab or a screen reader, and
  any key ends the black screen; choosing a country in urgent help announces the new emergency
  number; a focused control is never hidden under the header; the edges of a phone with a notch are
  kept clear; the trace loop and the pond's edge are easier to see; source links are larger
  targets; Open on GitHub opens a new tab, so the typed message is kept; the freed Unblock block
  leaves the Tab order and the page does not scroll sideways; the blue block also has an arrow.
  The rest is tracked in [RLG-047](../fragments/RLG-047.md). 178 tests.

<a id="v0-7-12"></a>
## [0.7.12] - 2026-10-09
- **About**: the privacy text now says that, besides the update check, Freelief downloads its own
  files to update or repair itself, and nothing about you is sent.
  [AUD-098](../fragments/AUD-098.md).
- Records: the documentation findings of audit round UNT-082 are fixed: the Release order and an
  Incident rule, the file audit command, the design's principles, settings, contracts and
  superseded entries, the technical references, REQ-007, REQ-015 and REQ-017, and new REQ-036 (the
  Visualizer) and REQ-037 (the wake lock). New tests tie the fallback's copies to their source and
  every activity to the menu. 176 tests.

<a id="v0-7-11"></a>
## [0.7.11] - 2026-10-09
- **Settings**: a **Reset settings** button, and a line that says whether this version is saved for
  use with no internet. Choosing a default again no longer pins it.
  [AUD-110](../fragments/AUD-110.md), [AUD-112](../fragments/AUD-112.md).
- **Standards and research**: a verified standard now stays shown in later versions until a
  release changes the interface (REQ-029 changed). [AUD-102](../fragments/AUD-102.md).
- The Effigy Media name and logo are reserved; the code stays MIT.
  [AUD-077](../fragments/AUD-077.md).
- Tools: doctor warns about stale crisis lines and outdated claims, and setup installs WebKit.
  [AUD-104](../fragments/AUD-104.md), [AUD-086](../fragments/AUD-086.md). 173 tests.

<a id="v0-7-10"></a>
## [0.7.10] - 2026-10-09
- **Keep the screen on**: a new setting. During breathing and the Visualizer, the screen may turn
  off after 10, 30 (the default) or 60 minutes with no touch; the exercise goes on. Pausing
  breathing lets the screen sleep at once. [AUD-103](../fragments/AUD-103.md),
  [AUD-081](../fragments/AUD-081.md).
- Freelief asks the browser to keep its offline copy, so it still opens offline on a full phone.
  [AUD-080](../fragments/AUD-080.md).
- Fixed: a breathing tone no longer wakes the audio behind urgent help. An update found while
  breathing runs waits for the next open. Failed loads are logged. The directory link is pinned in
  the tests, and the Visualizer and the pond no longer keep old timer ids.
  [AUD-082](../fragments/AUD-082.md), [AUD-107](../fragments/AUD-107.md),
  [AUD-084](../fragments/AUD-084.md), [AUD-085](../fragments/AUD-085.md),
  [AUD-076](../fragments/AUD-076.md), [AUD-083](../fragments/AUD-083.md). 171 tests.

<a id="v0-7-9"></a>
## [0.7.9] - 2026-10-09
- **Standards and research**: rewritten for Unblock and the waves. Unblock cites a study in which a
  hard task lowered anxiety, and the Visualizer cites a review of natural sounds. Every source was
  checked again on 2026-10-09. [RLG-044](../fragments/RLG-044.md). 163 tests.

<a id="v0-7-8"></a>
## [0.7.8] - 2026-10-09
- **Unblock** replaces Sort colors: slide wooden blocks along their length to let the blue block
  out. Fifteen boards from easy to hard, every one solvable. Drag a block, press the arrow keys on
  it, or choose it and use the Slide buttons. Undo takes back any move; there is no score, no move
  count and no timer. [RLG-040](../fragments/RLG-040.md), [REQ-035](../fragments/REQ-035.md).
  163 tests.

<a id="v0-7-7"></a>
## [0.7.7] - 2026-10-09
- **Ripple pond**: the ripples interfere, like real water. Where two rings meet the water is
  brighter, and where a crest meets a trough it is fainter. [RLG-041](../fragments/RLG-041.md).
  163 tests.

<a id="v0-7-6"></a>
## [0.7.6] - 2026-10-09
- **Background sound**: the Visualizer's music, nature sound or both keeps playing when you leave
  it. Every other screen shows a slim bar under the header with what plays and a **Stop** button.
  The Visualizer has a new **Off** choice. Breathing lowers the background sound under its tones.
  [RLG-045](../fragments/RLG-045.md).
- **Waves**: **Rain** is now **Nature**, which plays rain or waves. Choose which in Settings.
  [RLG-043](../fragments/RLG-043.md). 161 tests.

<a id="v0-7-5"></a>
## [0.7.5] - 2026-10-09
- **Visualizer**: the rain's drops are tuned to the notes of the music's key, C major. The bubble
  pop and the ripple's water drop keep their natural, random pitch.
  [RLG-046](../fragments/RLG-046.md). 156 tests.

<a id="v0-7-4"></a>
## [0.7.4] - 2026-10-09
- **Color a mandala**: five new designs, eight in all, with two new shapes: a scallop with a rounded
  edge and a diamond. [RLG-042](../fragments/RLG-042.md). 154 tests.

<a id="v0-7-3"></a>
## [0.7.3] - 2026-10-08
- **Sort colors**: an arrow under the tiles shows the order, with **Light** on the left and **Dark**
  on the right. [RLG-039](../fragments/RLG-039.md). 153 tests.
- The live preview moved to 0.7.3 on 2026-10-08, with the owner's yes in chat ("Yes, move live").

<a id="v0-7-2"></a>
## [0.7.2] - 2026-10-08
- Fixed: muting the Visualizer, leaving it and unmuting no longer plays its music again before it
  fades. [RLG-038](../fragments/RLG-038.md). 152 tests.

<a id="v0-7-1"></a>
## [0.7.1] - 2026-10-08
- **Color a mandala**: each color has its own note, played like a rain chime when you choose the
  color and when you fill a shape.
- **Trace a shape**: the crystal glass sound is softer. [RLG-036](../fragments/RLG-036.md),
  [RLG-037](../fragments/RLG-037.md). 151 tests.

<a id="v0-7-0"></a>
## [0.7.0] - 2026-10-08
- **Slice 7 is complete.** The audit backlog from rounds before UNT-051 is cleared: every finding is
  built, ruled on by the owner, or waiting on the environment (AUD-072). Design audit round UNT-082
  closed the slice; its 37 new findings (AUD-076 to AUD-112) are the work queue for slice 8.
  150 tests.
- The live preview moved to 0.7.0 on 2026-10-08, with the owner's yes in chat ("Yes, move live").

<a id="v0-6-16"></a>
## [0.6.16] - 2026-10-08
- The header now stays at the top while the page scrolls under it, so **Need urgent help?** is
  always in reach. [RLG-035](../fragments/RLG-035.md). 150 tests.

<a id="v0-6-15"></a>
## [0.6.15] - 2026-10-08
- Internal: the supported browsers are Chrome, Safari and Firefox, and the core paths are now also
  tested in Safari's engine. [AUD-028](../fragments/AUD-028.md). 149 tests.
- The live preview moved to 0.6.15 on 2026-10-08, with the owner's yes in chat ("Yes, move live").

<a id="v0-6-14"></a>
## [0.6.14] - 2026-10-08
- **About** says exactly what reaches the internet: "Freelief sends nothing about you. The only
  thing that reaches the internet is your browser's check for a newer version of Freelief, from
  GitHub Pages."
- Feedback by email is now optional until an address is chosen; GitHub is the route.
- Records: the design matches the deploy model, the shared-origin trust, the stylesheet and the
  crisis-line control; pending owner checks are listed in RLG-033; the quality routing posture is
  in force. [AUD-025](../fragments/AUD-025.md), [AUD-020](../fragments/AUD-020.md),
  [AUD-007](../fragments/AUD-007.md), [AUD-015](../fragments/AUD-015.md), [AUD-003](../fragments/AUD-003.md),
  [AUD-004](../fragments/AUD-004.md), [AUD-040](../fragments/AUD-040.md), [AUD-041](../fragments/AUD-041.md),
  [AUD-042](../fragments/AUD-042.md), [AUD-045](../fragments/AUD-045.md), [AUD-017](../fragments/AUD-017.md),
  [AUD-022](../fragments/AUD-022.md). 148 tests.
- Correction to 0.6.13: that version had 148 tests, not 147.

<a id="v0-6-13"></a>
## [0.6.13] - 2026-10-08
- The **sound button** now fades the sound out and back in, in place of a hard cut. Urgent help
  fades it too. [RLG-034](../fragments/RLG-034.md). 147 tests.

<a id="v0-6-12"></a>
## [0.6.12] - 2026-10-08
- In Windows High Contrast and other forced-color modes, **Sort colors** and **Color a mandala**
  keep their colors, because the colors are the task.
- Internal clean-ups: escaped values, timers that no longer pile up, one more text moved into the
  strings file, a tunable, and dead code removed. [AUD-050](../fragments/AUD-050.md),
  [AUD-033](../fragments/AUD-033.md), [AUD-038](../fragments/AUD-038.md), [AUD-039](../fragments/AUD-039.md),
  [AUD-046](../fragments/AUD-046.md), [AUD-047](../fragments/AUD-047.md). 146 tests.

<a id="v0-6-11"></a>
## [0.6.11] - 2026-10-08
- **Standards and research** shows a checked standard only for the version that was checked, so a
  claim never outlives its check. (None is claimed yet.) [AUD-023](../fragments/AUD-023.md),
  [AUD-054](../fragments/AUD-054.md). 145 tests.

<a id="v0-6-10"></a>
## [0.6.10] - 2026-10-08
- Internal: sturdier project tools. `doctor` checks that a browser launches, that every data file
  exists, the offline file list, and that every test file compiles; `run` serves this machine
  only; the test packages are pinned. No visible change. [AUD-012](../fragments/AUD-012.md),
  [AUD-034](../fragments/AUD-034.md), [AUD-035](../fragments/AUD-035.md), [AUD-036](../fragments/AUD-036.md),
  [AUD-037](../fragments/AUD-037.md), [AUD-029](../fragments/AUD-029.md), [AUD-032](../fragments/AUD-032.md). 145 tests.

<a id="v0-6-9"></a>
## [0.6.9] - 2026-10-08
- Internal: a release check (`build --release`) for a clean tree, a version bump after every
  shipped change, and crisis lines checked in the last 90 days. No visible change.
  [AUD-011](../fragments/AUD-011.md), [AUD-010](../fragments/AUD-010.md), [AUD-024](../fragments/AUD-024.md). 145 tests.

<a id="v0-6-8"></a>
## [0.6.8] - 2026-10-08
- Fixed: a new version of Freelief now reaches an installed app at once; GitHub Pages' caching could
  delay it by up to ten minutes. Stronger tests: every screen offline, the security policy, and
  the update under real caching. [AUD-013](../fragments/AUD-013.md), [AUD-009](../fragments/AUD-009.md),
  [AUD-027](../fragments/AUD-027.md), [AUD-031](../fragments/AUD-031.md), [AUD-030](../fragments/AUD-030.md). 143 tests.

<a id="v0-6-7"></a>
## [0.6.7] - 2026-10-08
- **Feedback** now says that GitHub issues are public, and that feedback is not watched around the
  clock: if you are in danger, use **Need urgent help?** or call your local emergency number.
  [AUD-006](../fragments/AUD-006.md), [AUD-053](../fragments/AUD-053.md). 139 tests.

<a id="v0-6-6"></a>
## [0.6.6] - 2026-10-08
- **Need urgent help?** no longer guesses your country from your language alone; with no region
  set, it shows "call your local emergency number" and the directory, and you can pick your country.
- **Chat online** now says it needs an internet connection.
  [AUD-026](../fragments/AUD-026.md), [AUD-052](../fragments/AUD-052.md). 138 tests.

<a id="v0-6-5"></a>
## [0.6.5] - 2026-10-08
- Fixed: in the **Ripple pond**, a slow drag no longer adds a stray ripple somewhere else when you
  lift your finger. [RLG-032](../fragments/RLG-032.md). 136 tests.
- Correction to 0.6.4: that version had 135 tests, not 134.

<a id="v0-6-4"></a>
## [0.6.4] - 2026-10-08
- Fixed: if a screen fails to open, Freelief shows the menu and every link keeps working. If even
  the menu fails, the plain breathing and emergency page comes back.
  [AUD-008](../fragments/AUD-008.md), [AUD-002](../fragments/AUD-002.md). 134 tests.

<a id="v0-6-3"></a>
## [0.6.3] - 2026-10-08
- Internal: the benchmark flags a figure that drifts past its tolerance, and the performance
  baseline is renewed at the end of slice 6 (178 ms launch, 74 ms response, 188.7 KB).
  [AUD-058](../fragments/AUD-058.md). 133 tests.
- The live preview moved to 0.6.3 on 2026-10-08, with the owner's yes in chat ("Yes, move live").

<a id="v0-6-2"></a>
## [0.6.2] - 2026-10-08
- Sturdier offline copy: if the browser's storage fails, Freelief loads from the internet in place
  of showing an error, and a failed self-repair is logged. No visible change.
  [AUD-059](../fragments/AUD-059.md), [AUD-060](../fragments/AUD-060.md). 133 tests.

<a id="v0-6-1"></a>
## [0.6.1] - 2026-10-08
- **Feedback**: a **Copy message** button. Open on GitHub no longer puts your message in the web
  address; you paste it into the issue yourself. [AUD-055](../fragments/AUD-055.md). 132 tests.

<a id="v0-6-0"></a>
## [0.6.0] - 2026-10-08
- **Breathe** shows its rhythm under the circle, for example "In 4 · Out 6".
  [RLG-031](../fragments/RLG-031.md). 131 tests.
- **Slice 6 is complete.** Since 0.5.0: owner polish from the phone, three new activities (ripple
  pond, mandala coloring, the Visualizer), drag in the color sort, vibration, the country list and
  saved region, sources for every activity, and the safety, bug, records and polish fixes from
  design audit round UNT-051.
- The live preview moved to 0.6.0 on 2026-10-08, with the owner's yes in chat ("Yes, move live").

<a id="v0-5-48"></a>
## [0.5.48] - 2026-10-08
- **Trace a shape**: the dot you move is larger and easier to see. [RLG-030](../fragments/RLG-030.md).
  130 tests.

<a id="v0-5-47"></a>
## [0.5.47] - 2026-10-08
- On breathing and the activities, the footer shows only "You are safe right now. Take your time.",
  so the exercise has more room. The menu keeps the full footer. [RLG-029](../fragments/RLG-029.md).
  129 tests.

<a id="v0-5-46"></a>
## [0.5.46] - 2026-10-08
- On the menu, the **Breathe** card stands out.
- **Settings** has "When Freelief opens": show the menu, or start breathing at once.
  [RLG-028](../fragments/RLG-028.md). 128 tests.

<a id="v0-5-45"></a>
## [0.5.45] - 2026-10-08
- Records only. The Delivery Plan names slice 6, which closes at 0.6.0.
- The live preview record, written down late (AUD-073): in the session of 2026-10-07 to 2026-10-08
  the owner said yes in chat to each move of `live`, to v0.5.16, v0.5.25, v0.5.27 and v0.5.34. The
  earlier moves, up to v0.5.15, have no record of a yes beyond UNT-014. The preview serves v0.5.34.
  From now on each move is recorded in the entry of the version it serves.
  [AUD-068](../fragments/AUD-068.md), [AUD-073](../fragments/AUD-073.md). 127 tests.

<a id="v0-5-44"></a>
## [0.5.44] - 2026-10-08
- **About** now names every setting Freelief saves on your device: breathing rhythm, sound,
  vibration, colors, the Visualizer's sound, and your country for urgent help.
- The accessibility checklist on **Feedback** now lists every screen by its name.
- The project records now match the app (opens on the menu, 250 KB, every module named).
  [AUD-063](../fragments/AUD-063.md), [AUD-064](../fragments/AUD-064.md), [AUD-065](../fragments/AUD-065.md),
  [AUD-067](../fragments/AUD-067.md), [AUD-069](../fragments/AUD-069.md), [AUD-070](../fragments/AUD-070.md). 127 tests.

<a id="v0-5-43"></a>
## [0.5.43] - 2026-10-08
- Internal: the Visualizer gets and saves its sound choice through the app shell, so no activity
  touches Settings or storage. No visible change. [AUD-066](../fragments/AUD-066.md). 124 tests.

<a id="v0-5-42"></a>
## [0.5.42] - 2026-10-08
- Fixed: a new version no longer changes under you once you have started using Freelief. It
  waits for the next time you open it. [AUD-057](../fragments/AUD-057.md). 123 tests.

<a id="v0-5-41"></a>
## [0.5.41] - 2026-10-08
- Fixed: **Update now** checks the connection before it removes anything. On a broken or sign-in
  Wi-Fi it says so, and Freelief keeps working offline. [AUD-056](../fragments/AUD-056.md). 121 tests.

<a id="v0-5-40"></a>
## [0.5.40] - 2026-10-08
- Fixed: Settings now saves only what you change, so a setting you never touched follows the
  app's default. If you chose box breathing in the last day, choose it again in Settings.
  [AUD-062](../fragments/AUD-062.md). 120 tests.

<a id="v0-5-39"></a>
## [0.5.39] - 2026-10-08
- **Need urgent help?** now has a **Call** button for the emergency number, first in the window.
- Sound goes quiet while urgent help is open, and while you are on a call or in another app.
- The screen stays on during breathing and the Visualizer.
- The Visualizer's full screen keeps a **Need urgent help?** button. Under the black screen the
  shapes stop, to save battery. [RLG-027](../fragments/RLG-027.md). 118 tests.

<a id="v0-5-38"></a>
## [0.5.38] - 2026-10-08
- **Sound** is now a speaker button at the top of every screen, crossed out when off. Off is
  silent at once. The switch is no longer in Settings. [RLG-026](../fragments/RLG-026.md). 113 tests.

<a id="v0-5-37"></a>
## [0.5.37] - 2026-10-08
- Corrected: **Standards and research** no longer says that a longer breath out did better than box
  breathing. The trial compared each method only with mindfulness. 4 in, 6 out stays the default,
  because all of Freelief's rhythms are slow breathing, which a review supports.
  Correction to 0.5.36: its entry states that comparison too. [AUD-061](../fragments/AUD-061.md).
  111 tests.

<a id="v0-5-36"></a>
## [0.5.36] - 2026-10-08
- The default rhythm is **4 in, 6 out** again: in a trial, a longer breath out did better than box
  breathing. Standards and research says so. A rhythm you chose stays.
  [RLG-025](../fragments/RLG-025.md). 111 tests.

<a id="v0-5-35"></a>
## [0.5.35] - 2026-10-08
- **Standards and research** now has a section for every activity, each with its own sources and
  a plain note on how strong the evidence is. Eight new sources; every source checked 2026-10-08.
  [RLG-018](../fragments/RLG-018.md). 111 tests.

<a id="v0-5-34"></a>
## [0.5.34] - 2026-10-08
- The **Vibration** hint is shorter and smaller: "A short buzz on taps. Android only (Chrome,
  Samsung Internet), not iPhone." [RLG-024](../fragments/RLG-024.md). 110 tests.

<a id="v0-5-33"></a>
## [0.5.33] - 2026-10-08
- The **Vibration** hint in Settings now says exactly where it works: Chrome and Samsung Internet
  on Android. It does not work on iPhone, in Safari or in Firefox.
  [RLG-024](../fragments/RLG-024.md). 110 tests.

<a id="v0-5-32"></a>
## [0.5.32] - 2026-10-07
- **Vibration**: a short buzz when you pop a bubble, choose or swap a tile, finish a sort or a loop,
  make a ripple or fill a shape. Never for breathing or anything continuous. On by default; turn
  it off in **Settings**. It does not work on iPhone or in Safari.
  [RLG-024](../fragments/RLG-024.md), [REQ-034](../fragments/REQ-034.md). 110 tests.

<a id="v0-5-31"></a>
## [0.5.31] - 2026-10-07
- Installed on a phone, Freelief now stays in portrait. [RLG-022](../fragments/RLG-022.md). 106 tests.

<a id="v0-5-30"></a>
## [0.5.30] - 2026-10-07
- **Visualizer**: the rain is 25% quieter, on its own and in Both. [RLG-023](../fragments/RLG-023.md).
  106 tests.

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
