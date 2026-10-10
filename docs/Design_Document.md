# Freelief — Design Document

The founding design for Freelief. It records what to build and why. The requirements are records
in `docs/fragments/` (`REQ-NNN`). This document does not restate them. It holds the structure, the
narrative and the decisions. Code, records and this document must never disagree.

---

## 0. Document Control

- **Version:** 1.4, 2026-10-10. The Change Log (section 15) says what each version changed. This line
  does not name an app version, because the design changes in many units (AUD-095).
- **Owner:** EffigyMedia.
- **Status:** living. The owner signed off v1.0 on 2026-10-07, and Initialize was done the same
  day. Since then each slice and each owner decision has changed this document in the same unit of
  work, with a dated Decision Log entry.
- **One-line pitch:** Freelief is a free, open-source, offline web app that helps anyone through a
  panic attack or acute anxiety in the moment, with breathing and gentle distraction.
- **Tier:** Standard.
- **Routing posture:** `ROUTING_BIAS: 2` (quality). People use Freelief in a crisis, so a wrong
  word or a broken screen costs more than rework.
- **Origin:** the owner's request of 2026-10-07, kept in `docs/provisional/FREELIEF_OWNER_REQUEST.md`.
  The folder is kept on purpose: it holds the owner's own words, and every decision in it is now
  in the Decision Log below, so it is a record and not a draft. The premise stub (`PREMISE.md`) was an unfilled template; this document supersedes it and the
  stub is removed.

<!-- BEGIN srs-references - written by the interview, read by the generators -->
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 2023 — the
  accessibility target (AA in full, AAA where a criterion can be met).
- W3C, *Web Application Manifest* and WHATWG *Service Workers* — the installable offline web app.
- GitHub Pages documentation — the host.
- The published research for each technique, one source or more per technique, kept as a record in
  `docs/research/sources.md`. The app shows no research page and makes no claim from it (RLG-056).
<!-- END srs-references -->

---

## 1. Vision & Purpose

A panic attack is sudden and frightening. The person has a racing heart, short breath and the
feeling that something terrible will happen. It passes, usually within minutes, but in that moment
the person has little attention, shaky hands, and often no one to help. The self-help techniques
that help — slow breathing and gentle distraction — are simple, but they are
hard to remember and do alone while panic takes over.

The apps that offer these techniques often ask for an account, ask questions before they help,
need a network, play an advertisement or a subscription offer, or collect data about the person's
worst moments. Many do
not work with a screen reader or a keyboard.

Freelief opens on a short menu with breathing first and one tap away, works with no network, asks nothing of the person,
collects nothing, and works for everyone. Success, a year after release, is a tool that people
recommend to each other in a crisis because it simply works and is free.

<!-- BEGIN srs-purpose - written by the interview, read by the generators -->
Freelief helps a person through a panic attack or acute anxiety at the moment it happens. It gives
self-help techniques studied in clinical research — paced breathing and gentle distraction
activities — and a fast route to a crisis line for a person who
may be in danger. It is for anyone, at no cost, with no account, no network and no data collection.
<!-- END srs-purpose -->

<!-- BEGIN prd-problem - written by the interview, read by the generators -->
During a panic attack a person cannot easily recall or perform the techniques that would calm them.
The tools that exist put obstacles in the way at the worst moment: a sign-up, questions to
answer first, a loading screen, a network that is not there, an advertisement, or a screen that a screen reader or a
keyboard cannot use. Many also record the person's crises as data. A person in distress needs help
that starts at once, works for them as they are, and asks for nothing.
<!-- END prd-problem -->

<!-- BEGIN srs-product-overview - written by the interview, read by the generators -->
Freelief is a progressive web app: plain HTML, CSS and JavaScript served from GitHub Pages. It
installs to the home screen of a phone or a desktop and then works fully offline. When it opens,
it shows the menu at once, with no account, question or notice before it. Breathe, a paced
breathing guide, is the first item; one tap or key press reaches it, the distraction activities (a
bubble field, Zen Garden, the Unblock puzzle, a ripple pond and mandala coloring) and the Visualizer
(music, rain or waves with soft shapes). Every screen has a "Need urgent help?" control that shows crisis
lines for the person's region. Supporting pages give the self-help disclaimer, the standards
Freelief meets with the research behind each technique, and a feedback page that opens a pre-filled
GitHub issue or email. Freelief has no server, no account and no analytics. It stores only the
person's settings, on the device.
<!-- END srs-product-overview -->

---

## 2. Users & Success Criteria

One user type: **a person in the moment.** An adult or a teen who has a panic attack or acute
anxiety now, or who is close to one. The context is often a phone at night or in a public place,
sometimes a desktop with a keyboard, sometimes with a screen reader or reduced motion switched on.
They are not technical, they are not forgiving, and they have little attention.

Two secondary groups use the project, not the app in a crisis:
- **Community volunteers** who check accessibility and report problems through the feedback page.
- **The owner**, who maintains the crisis-line list and the releases.

<!-- BEGIN prd-users - written by the interview, read by the generators -->
- **A person in the moment** — anyone who has a panic attack or acute anxiety now. They want the
  panic to pass. They use a phone or a computer, often at night, sometimes with a screen reader, a
  keyboard only, or reduced motion. They have little attention and shaky hands, and they must not
  be asked for anything before help starts.
- **A community volunteer** — a person who checks Freelief with a screen reader or a keyboard, or
  who reports a problem. They want to report with little effort, through GitHub or email.
- **The owner** — maintains the crisis-line list, accepts volunteer checks, and releases versions.
<!-- END prd-users -->

<!-- BEGIN prd-success - written by the interview, read by the generators -->
- From a cold launch, the menu is visible within 1 second on a mid-range phone, installed and
  offline, with nothing to answer first, and breathing is one tap away (REQ-018, REQ-026).
- After install, an automated test with the network disabled shows every screen working, and a
  network log shows no request to any origin (REQ-008, REQ-015).
- The automated accessibility check reports zero WCAG 2.2 A and AA violations on every page, on
  every release.
- At least one dated manual check with a screen reader and one with a keyboard alone is recorded
  in RLG-033 before 1.0. *(Changed 2026-10-10, RLG-056: the app shows no standards claim, so
  REQ-029 is withdrawn; the manual checks stay a release condition.)*
- Every crisis line in the app has a last-checked date no older than the release that ships it.
- The whole app is under 250 KB (REQ-028).
- No text in the app says Freelief is clinically proven, treats, cures or diagnoses (REQ-025).
<!-- END prd-success -->

**Quality bar for v1.0:** every "must" requirement is met and tested; every "should" is met or is
absent from the release; the release criteria in Stage 10 hold.

---

## 3. Scope, Principles & Constraints

**Principles (tie-breakers, in order):**
1. **Help first.** Nothing stands between the person and help: no account, question, notice or
   wait. Freelief opens on a short menu with Breathe first and one tap away, and Settings can make it
   open on breathing with no tap (REQ-018; owner, 2026-10-07 and 2026-10-08). The menu asks for
   nothing; it is not an obstacle in the sense of this principle (AUD-088).
2. **Works for everyone.** A screen reader, a keyboard, reduced motion and shaky hands are normal
   use, not edge cases.
3. **Ask nothing, keep nothing.** No account, no data, no network.
4. **True claims only.** Promote what is verified; never more.
5. **Small and boring.** Fewer moving parts beat more features.

**Constraints** — all hard, and recorded as `constraint` requirements: the PWA on GitHub Pages,
offline after the first visit (REQ-008); plain HTML, CSS and JavaScript with no framework, no
dependency and no build step (REQ-019); one strings file per language (REQ-017); claim wording
(REQ-025); the MIT license (REQ-031). Budget is zero: no paid service and no paid audit.

**Greenfield.** Freelief builds on no existing code. It copies the delivery model of Effigy Arcade
(GitHub Pages, no build step) but no code from it.

<!-- BEGIN srs-scope - written by the interview, read by the generators -->
Freelief covers self-help for a panic attack or acute anxiety at the moment it happens: paced
breathing, distraction activities, crisis lines by
region, a self-help disclaimer, and a feedback page that hands a
pre-filled report to GitHub or email. It runs in a browser and as an installed offline web app.
The boundary: Freelief does not diagnose, treat, track, or contact anyone. It points to crisis
lines; it does not call them. Its only stored data is the person's settings, on the device.
<!-- END srs-scope -->

<!-- BEGIN prd-out-of-scope - written by the interview, read by the generators -->
Not built (decided 2026-10-07):
- **Accounts, profiles or sign-in** — they add a step before help and store personal data.
- **An episode log, history, mood tracking, reminders or streaks** — they store a person's worst
  moments and add pressure. Freelief is for the moment, not a daily practice.
- **Analytics or usage counts of any kind** — a person's crises are not telemetry.
- **A server, including a relay to file feedback without a GitHub account** — a static site cannot
  keep a token secret, and a server adds a network send and spam handling.
- **Spoken voice guidance** — its quality varies by device and language. Soft tones only.
- **Languages other than English in v1** — the strings file makes a translation a later data change.
- **Location requests** — the region comes from the device language and region setting.
- **Medical claims, diagnosis, or an AI chat or therapist feature** — Freelief is self-help, not
  medical care.
- **Native app-store versions** — the web app installs to the home screen.
- **A paid accessibility audit** — volunteers do the manual checks.
<!-- END prd-out-of-scope -->

---

## 4. Domain Model & Vocabulary

| Term | Meaning |
|---|---|
| **Exercise** | A guided self-help technique: paced breathing. |
| **Activity** | A distraction activity: the bubble field, Zen Garden, Unblock, the ripple pond, mandala coloring, or the Visualizer. No score, no failure, no timer. |
| **Visualizer** | The activity with nothing to do: soft shapes that fade in and out, a full screen and a black screen. It has no sound choice of its own; the sound bar plays sound on every screen. Route `#calm`, module `activities/calm.js`. Its shape loop runs on timers inside the module, but the person sees no countdown, no end and no score, so it keeps the Activity rule. |
| **Breath guide** | The visual of the paced breathing exercise. It grows on the in-breath and shrinks on the out-breath. |
| **Rhythm** | A breathing preset: the length in seconds of each phase (in, hold, out, hold). |
| **Crisis line** | A phone, text or web service for a person in danger. It has a region, a name, how to reach it, and a last-checked date. |
| **Region** | The country taken from the device language and region setting. Never from location. |
| **Settings** | The only stored data, and only the values the person changed: the breathing rhythm, where Freelief opens (the menu or breathing), how long the screen stays on, sound on or off, vibration on or off, the light or dark theme, and the region for urgent help. What sound plays is not stored. On the device only. |
| **Standard** | An external standard Freelief claims to meet, such as WCAG 2.2 AA. It has a level, a check date, and the tester of the manual check. |
| **Source** | A published research citation behind a technique. |

Relations: each Exercise and Activity cites one or more Sources. A Region has zero or more Crisis
lines; a Region with none falls back to the international directory. Settings persist across
restarts on the device (REQ-023, REQ-015).

<!-- BEGIN srs-definitions - written by the interview, read by the generators -->
- **Exercise** — a guided self-help technique: paced breathing.
- **Activity** — a distraction activity with no score, no failure and no timer: the bubble field,
  Zen Garden, Unblock, the ripple pond, mandala coloring, or the Visualizer.
- **Background sound** — music, and rain or waves, chosen with the three buttons of the sound bar
  in the header; it keeps playing on every screen until the person taps its button again.
- **Visualizer** — the activity with nothing to do: soft shapes, a full
  screen and a black screen.
- **Breath guide** — the visual that grows on the in-breath and shrinks on the out-breath.
- **Rhythm** — a breathing preset, given as the seconds of each phase.
- **Crisis line** — a service for a person in danger, with a region, a way to reach it, and a
  last-checked date.
- **Region** — the country taken from the device language and region setting, never from location.
- **Settings** — the only data Freelief stores, and only the values the person changed: the
  breathing rhythm, where Freelief opens, how long the screen stays on, sound on or off, vibration
  on or off, the theme, and the region for urgent help, on the device only.
- **Standard** — an external standard Freelief claims, with its level, check date and tester.
- **Source** — a published research citation behind a technique.
<!-- END srs-definitions -->

---

## 5. Functional Specification

The requirements are every agreed `REQ-` record in `docs/fragments/`; `docs/SRS.md` lists them. Their
priority is the feature list. The
flows below are the structure.

**F1 — Launch to the menu** *(changed 2026-10-07; it was launch to breathing)*. Trigger: the
person opens Freelief. Steps: the shell paints the menu ("What would help right now?") with no
account, question or notice before it; Breathe is the first item, and its card is filled and
larger. A person who set "When Freelief opens: Start breathing at once" in Settings opens straight
on the breath guide instead (2026-10-08). Choosing Breathe starts the
breath guide with the saved rhythm (or the default) and one calm line. Outcome: the person
chooses what helps, and breathing is one tap away. States: *first visit online* — the service
worker installs and caches the app in the background, and the menu does not wait for it; *offline, installed* — served from
cache; *offline, never visited* — the browser cannot load it, which is outside the app's control;
*a screen that cannot load* — the menu shows and the address becomes `#menu`;
*reduced motion* — the guide shows a still shape with a text count instead of growth; *storage
blocked* — the default rhythm is used and nothing fails.

**F2 — Change exercise or activity** *(changed 2026-10-07, UNT-030 and the menu decision: "More
ways to calm" and "Back to breathing" are gone)*. Trigger: the person taps or presses "Back to
menu", which every screen except the menu shows at the top, under the header. Steps: the menu, a
short list of large items; the person chooses one; it starts. Outcome: the new exercise or activity
runs. Leaving any screen returns to the menu. No exercise has an end state that asks for
anything.

**F3 — Grounding.** *Withdrawn 2026-10-07 (owner): removed for weak research; see REQ-002 and the
Decision Log.* Steps: five prompts in order (5 things you see, 4 you can touch, 3 you hear,
2 you smell, 1 you taste). The person advances with a large "Next" control or a key. No input is
typed or stored. Outcome: a closing calm line and a return to breathing. Edge: the person can go
back or stop at any step.

**F4 — Calming statements.** *Withdrawn 2026-10-07 (owner): removed for weak research; see REQ-003
and the Decision Log.* Steps: one statement at a time; the person advances when ready. The
statements come from the strings file. Outcome: the person stops when they choose.

**F5 — Distraction activities.** *Bubble field:* bubbles drift slowly; a tap or a key press pops the
focused bubble with a soft visual (and a soft pop if sound is on). *Zen Garden (REQ-038,
added 2026-10-10, replacing the shape trace, REQ-013):* a tray of sand to rake with a finger or
the arrow keys, with a few stones and small plants to add, move and remove; the sand keeps rings
around each, and the raked lines flow around them; Smooth the sand clears the lines. *Unblock (REQ-035,
added 2026-10-09, replacing the colour sort, REQ-014):* wooden blocks on a 6 by 6 board, each
sliding only along its length; the person slides them to let the blue block out through the gap in
the right edge. A block moves by a drag, by the arrow keys on it, or by choosing it and pressing
the two Slide buttons. Each block is named ("Block 3, down, column 4, rows 1 to 3"). Fifteen boards
go from easy to hard; Undo takes back any move and Start again resets the board. *Ripple
pond (REQ-032, added 2026-10-07):* still water; a touch makes soft rings spread from that point,
and a finger drawn across it leaves a trail of ripples; a key press or a screen reader's activation
makes a ripple at a random place; each ripple plays a soft water drop. The ripples interfere:
the water is a fine grid of dots whose brightness is the sum of every ripple's wave, so it is
brighter where crests meet and fainter where a crest meets a trough. *Mandala coloring (REQ-033,
added 2026-10-07):* six soft colors and a mandala of shapes drawn from formulas; the person chooses
a color, then taps or selects a shape to fill it; arrow keys move around a ring and between rings;
each shape is named ("Ring 2, shape 3 of 12, blank"); New mandala starts the next of eight
designs, blank, and after the last it starts the first again.
States for all: no score, no
failure, no timer; reduced motion slows or stops the drift; a screen reader announces each item
and its action. *Visualizer (added 2026-10-07; named 2026-10-07, UNT-034):* nothing to do; the
soft shapes fade in and out. Sound is not chosen here: the header's sound bar, on every screen,
has a music note, a raindrop and a wave (RLG-049). A tap plays that sound and a second tap stops
it; rain and waves replace each other, and music plays with either. A tap while the speaker is off
turns sound on. The sound keeps playing on every screen; breathing lowers it under its tones, and
it waits while urgent help is open. Nothing about it is stored, so each visit starts silent. Full
screen fills the screen
and keeps its own "Need urgent help?" button. Black screen covers everything in black while the
sound plays; one tap or key brings the screen back. Under reduced motion the shapes only fade. The
screen stays awake while it runs.

**F6 — Need urgent help.** Trigger: the "Need urgent help?" control, present on every screen
(the Visualizer's black screen is the one exception: one tap brings it back).
Steps: the app takes the region saved in Settings, or else reads the device language and region;
it shows a Country list set to that region; a line to call the region's emergency number if in
immediate danger, with a Call button for each emergency number; then the crisis lines for that region, each with a tap-to-call or tap-to-text
link and its last-checked date; then the link to the international directory. The Country list
shows another curated region, or "Another country", for this visit only. Sound waits while the dialog is
open and while the app is hidden.
States: *uncurated region, or a device language with no region set* — the "call your local
emergency number" line and the international directory; *offline* — the curated lines still show; the directory
link and any web chat say they need a network. *(Changed at slice 1, 2026-10-07: the emergency line moved first, and
the other-countries list was added. See the Decision Log.)* *(Changed 2026-10-07, UNT-042: the Country list and the
region in Settings replace the other-countries list.)*

**F7 — Settings.** Rhythm preset, where Freelief opens (the menu or breathing), how long the
screen stays on (10, 30 or 60 minutes with no touch, or always while it runs), theme
override, vibration on or off, and the region for urgent help; sound on or off is the speaker in
the header; the Visualizer's sound choice is kept too. Reset settings puts every value back to its
default. The screen also shows the version, whether it is saved for use with no internet, and
Update now.
Saved on the device at once. Only a setting the person changes is stored, so a setting they never
touched follows the default of the version they run; "a saved rhythm is kept" means a rhythm the
person chose. Storage that fails is ignored and the defaults stand.

**F8 — Disclaimer.** The footer links to the disclaimer page (About), which says what Freelief is
and is not, and that frequent attacks call for a doctor or a mental health professional. *(Changed
2026-10-10, RLG-056: the Standards & research page is removed; the sources are a record in
`docs/research/sources.md`.)*

**F9 — Feedback.** Trigger: the feedback page. Steps: the person chooses "Accessibility check" or
"Report a problem"; the page shows the pre-filled text (app version, browser, device type, and a
checklist for an accessibility check); the person edits it; they choose "Copy message" and then
"Open on GitHub" (a new issue URL with only the template and the title in its query; the person
pastes the message) or "Send by email" (a `mailto:` link with subject and body, opened by their own
mail app). *(Changed 2026-10-08, AUD-055: the message no longer goes into the GitHub URL.)* Outcome: the person's own browser or mail app takes over; the app sends nothing.
Edge: until the owner chooses a public email address, the email button is hidden and GitHub is the
only route; REQ-030 makes the email route optional (changed 2026-10-08, AUD-020).

**Integrations.** None at run time. The only outbound links are ones the person chooses: phone,
text, the crisis directory, GitHub and email. If GitHub is down, the issue page does not load. While
the email route is hidden (F9), the page names no other route; the owner's choice of a public email
address is the step that adds the fallback for a person with no GitHub account. *(Corrected
2026-10-10, AUD-128: this sentence said the email route remains.)*

**Permissions and auth.** N/A — no accounts and no roles. Anyone may use every part of the app.

---

## 6. Experience & Interface

**Interaction principles.** Help first: the menu is the first and default screen, with nothing to
answer before it, and Breathe is its first item. One clear
action per screen. Large targets (at least 44 by 44 CSS pixels, larger for the main actions). No
timer, no score, no failure, no surprise sound, no sudden motion. Every control works by touch, by
keyboard and by screen reader, with a visible focus ring. The "Need urgent help?" control is always
in the same place.

**Visual direction.** Soft and dim. A deep night-blue or slate background with one soft accent and
large rounded type. Dark by default, and it follows the device light or dark setting, with an
override in Settings. AAA contrast for text. No images in v1: shapes are drawn with CSS or SVG.
The implementer shows the owner variants before the look is fixed. *(The owner confirmed the current
look on 2026-10-08, after changes from the phone: see the Decision Log.)*

**Tone of voice.** Warm, steady, short and plain. Second person, present tense: "Breathe in." "You
are safe right now." Never clinical, never cheerful, never blaming. Errors are calm and say what
still works.

**Accessibility and internationalization.** WCAG 2.2 AA in full and AAA where a criterion can be
met (REQ-016), keyboard and screen reader (REQ-009), reduced motion (REQ-010), no time limits
(REQ-011), contrast and theme (REQ-021). English only, with one strings file per language
(REQ-017).

---

## 7. Technology Discovery

| # | Item | Decision | Rationale | Rejected |
|---|---|---|---|---|
| 1 | Platform | A progressive web app, phone first, that works on desktop with a keyboard. Supported browsers: the current and previous major versions of Chrome (Android and desktop), Safari (iPhone and Mac) and Firefox (owner, 2026-10-08). | Reaches every device with no store, installs to the home screen, works offline. | Native apps (cost, review, two codebases). |
| 2 | Language and runtime | HTML, CSS and modern JavaScript (ES modules) in the browser. | Runs everywhere with nothing to install or build. | TypeScript (needs a build step). |
| 3 | Frameworks and libraries | None. No third-party code ships. | Smallest download, fastest load, nothing to break or update. | Preact or any framework (a dependency and a build step). |
| 4 | Persistence | `localStorage` for Settings only, behind one module, with every access in try/catch. | Settings are small and on-device; nothing else is stored. | IndexedDB (more than needed). |
| 5 | External services | None at run time. | No network after install, no data sent. | Analytics, a feedback relay. |
| 6 | Content and assets | Text in `strings/en.json`, owner-approved. Crisis lines in `data/crisis-lines.json`, curated and dated. Research sources in `docs/research/`. Tones generated with Web Audio at run time, so no audio files. The system font stack, so no font files. | Small, licence-free, offline. | Recorded audio; web fonts; image assets. |
| 7 | Deployment | GitHub Pages serves the `live` branch of the public repository `EffigyMedia/freelief`. Pushing `main` deploys nothing; moving `live` is the deploy (before 1.0 with the owner's yes, from 1.0 only at a release that cleared the audit gate). Rollback moves `live` back to the previous tag (`preview-X.Y.Z` before 1.0, `vX.Y.Z` from 1.0); see the incident rule in section 9. *(Changed 2026-10-07, AUD-003: it first served `main`.)* The service worker cache name carries the app version. | Free for a public repository; HTTPS, which a service worker needs. | Netlify or another host (no need). |
| 8 | Testing toolchain | Python 3 and Playwright, from a project-local `.venv`, as in Effigy Arcade. axe-core, from the `axe-playwright-python` package in the same venv, runs the automated accessibility check; nothing from it ships. | Real-browser tests, including offline and network-log checks. The Shared Knowledge Base already holds Playwright gotchas. | Node test runners (another toolchain); manual testing only. |
| 9 | Dev environment and commands | `setup`: create `.venv` and install Playwright. `run`: `python -m http.server 8000`. `test`: the Playwright harnesses. `doctor`: check Python, the venv, Playwright, the manifest, the service worker and the JSON files. `build`: none — the repository is the distributable; `build` reports that and checks the size limit. `clean`: remove `output/`. `bench`: the launch-time and size benchmark. | Matches the environment's standard commands with the fewest tools. | A bundler. |
| 10 | Version control | Git. The remote is public. Push `main` freely: it deploys nothing. Moving `live` is the deploy. Before 1.0, `live` moves only with the owner's yes, recorded in the changelog entry of the version it serves; from 1.0 on, it moves only at a release, after `audit-gate.py` prints `GATE CLEAR`, to a tag. *(Changed 2026-10-08, AUD-003: it first said "feature commits stay local; push at a release or for an owner device test".)* | Pages needs a public repository on a free plan; the project is open source. | A private repository. |
| 11 | CI/CD | None in v1. The project commands are enough at this size. | Fewer moving parts. | GitHub Actions (reconsider if volunteers send pull requests). |

**Never commit:** any token, key or password; `.venv/`; `output/`; the content of feedback emails
or any other personal data from a volunteer or a user; licensed material without a licence that
allows redistribution.

---

## 8. Architecture

Each file below is one module with one responsibility.

| Module | Owns | Must not |
|---|---|---|
| `index.html` + `app.js` (**shell**) | The page frame, the screen router, the footer, and the "Need urgent help?" control. | Contain exercise logic or text. |
| `exercises/breathe.js` | The breathing exercise. *(`ground.js` and `statements.js` were removed 2026-10-07.)* | Read storage or the network; hold text. |
| `activities/bubbles.js`, `trace.js`, `unblock.js`, `ripple.js`, `mandala.js` | One activity each. | Keep a score, a timer or a failure state; read storage. |
| `background.js` | The background sound: what plays (off, music, nature, both) and which nature sound, started and stopped through `audio`. The shell tells it what to play. | Touch storage; start a sound by itself. |
| `activities/calm.js` (**the Visualizer**) | The choice of background sound, saved and played by the shell, soft shapes that fade in and out, Full screen with its own "Need urgent help?" button, and the black screen. Its shape loop uses timers inside the module; the person sees none. | Show a countdown, an end or a score; read storage; add shapes or animate while the screen is black. |
| `settings.js` | **The single source of truth for Settings.** The only module that touches `localStorage`. | Hold defaults (those are in `config.json`). |
| `strings.js` + `strings/en.json` | **The single source of all user-facing text.** | Contain logic. |
| `crisis.js` + `data/crisis-lines.json` | The choice of crisis lines from the device region. | Ask for location. |
| `audio.js` | Every sound, made with Web Audio: the breath sound and the hold taps, the activity cues and the background music, rain and waves, which share one volume that a screen can lower. Nothing plays before the first tap or key press. | Play anything while sound is off, while urgent help is open, or while the app is hidden; load an audio file; touch storage except by reading `settings.js` (AUD-117). |
| `haptics.js` | One short vibration from `config.json` → `haptics.patterns` for a single triggered event in an activity. A device without the Vibration API gets nothing. | Vibrate for anything continuous (the breath, a drag trail, the trace tone); vibrate while vibration is off; touch storage except by reading `settings.js` (AUD-117). |
| `wakelock.js` | The screen wake lock while breathing or the Visualizer runs, taken again when the page comes back. | Fail when the browser has no wake lock or refuses it; keep the lock after the last screen releases it; touch storage except by reading `settings.js` (AUD-117). |
| `motion.js` | Reduced-motion detection; every animation asks it. | Touch storage except by reading `settings.js` (AUD-117). |
| `fallback.js` | A classic script in `<head>`: it hides the static fallback in `index.html` while the app starts, and shows it if the app has not started in 2 s. The 2 s is a constant in the file. | Depend on `config.json`, a module or the network, because it must work when they fail. |
| `config.json` | **Every tunable**, with its committed default. | — |
| `sw.js` | The offline cache, versioned by the app version. | Fetch from any other origin. |
| `manifest.webmanifest` | Installation: name, icons, colours. | — |
| `screens/menu.js`, `screens/settings.js` | The menu ("What would help right now?"), the first screen, and the Settings screen. The Settings screen changes Settings only through `settings.js`. | Touch `localStorage` directly. |
| `screens/about.js`, `feedback.js` | The disclaimer (About) and Feedback pages. *(First planned as `pages/`; built as screens at slice 4, with the same contract and router. `standards.js` was removed 2026-10-10, RLG-056.)* | Send data. |

**Routing (added at slice 2; the default changed to the menu 2026-10-07).** Each screen has a URL
hash (`#menu`, `#breathe`, `#settings` and one per activity and page); no hash means `#menu`. The
browser Back button therefore works. An unknown hash shows the menu, and a screen that cannot load
falls back to the menu and the address becomes `#menu`. On a change of screen the shell focuses the new screen's
heading, so a screen reader announces where the person is.

**Data and state.** Settings in `localStorage` under one versioned key (`freelief.settings.v2`),
holding only the values the person changed: the breathing rhythm, where it opens, how long the
screen stays on, sound, vibration, the theme and the region for urgent help. A choice of the default value is not stored. Everything else is static files cached by the
service worker. Nothing is created, changed or deleted by the person except those Settings.

**Contracts.** Each exercise and activity exports `start(container, ctx)` and `stop()`. `ctx`
gives the text functions `t` and `list`, `config`, `motion`, `audio`, `haptic`, `keepAwake`, and the
read-only setting values the screen needs (such as `rhythm` and `soundsOn`). No screen writes a
setting except Settings itself; the background sound belongs to the shell's sound bar (RLG-049). The shell owns which screen runs. `crisis.js` exports `linesFor(regionCode)`, which returns the curated lines and the fallback.

**Tunables (`config.json`):** every tunable has its committed default there. The groups are:
`breathing` (rhythms and the default, 4 in and 6 out); `sounds` (every note, level and fade, the
background volume and ducking, the rain and the waves); `haptics`; `wakeLock` (the screen-on
choices); `bubbles`, `trace`, `unblock` (the boards), `ripple` (with its `wave`), `mandala` and
`calm` (the Visualizer and the background sound); `theme`; `settings`; `crisis` (the directory URL
and the freshness window); and `project` (the feedback links, the email address, empty until
decided).

**Hard problems and de-risking.**
1. *Offline install and update.* Proven first, in the walking skeleton, with an offline test and
   an update test.
2. *Accessible activities.* Every activity uses DOM elements, not a canvas, so a screen reader
   and the keyboard reach every item.
3. *Launch in 1 second.* Keep all CSS in one small file, `styles.css`, linked from `index.html`
   (the CSP is `style-src 'self'`, so no style is inline), load only the shell, the menu and urgent
   help at start and every other screen on its first visit, and benchmark from the first slice.
   *(Changed 2026-10-08, AUD-041: it first said "inline the critical CSS"; see the Decision Log.)*

**Cross-cutting targets.** No request to another origin from the app, ever. No console errors.
Every storage access in try/catch, so blocked storage never breaks a screen. No personal data in
any log. Any failure leaves breathing (the static fallback's breathing line, at worst) and the
crisis lines usable.

---

## 9. Quality & Performance Strategy

**Tests (Playwright, real browser):**
- *Smoke:* every page loads with a clean console.
- *Offline:* after one visit, with the network off, every screen works; the network log shows no
  request to any other origin.
- *Accessibility:* axe-core on every screen, on each state a person reaches inside one (the list is
  `STATES` in `tools/tests/test_a11y.py`: a chosen block, a solved board, a chosen garden item, the
  full screen, the black screen, the reset question, the problem report), and on the help dialog for
  every region and "Another country", with zero A and AA violations; a keyboard-only walk through
  every flow. *(Changed 2026-10-10, AUD-152: it said "every page and state" while only each screen's
  first state was checked.)* A new state that a tap or key reveals is added to `STATES`.
- *Reduced motion:* with the media feature set, no element animates.
- *Settings round trip:* save, reload, read, and assert the same values; blocked storage falls back
  to the defaults.
- *Crisis lines:* each sample region shows its lines; an unknown region shows the fallback.
- *Update:* a new cache version replaces the old one.
- *Claims:* a scan of the strings and pages for forbidden claim words (REQ-025).

**Never break:** the menu at launch, with breathing one tap away; the "Need urgent help?" control on every screen;
offline use; keyboard and screen-reader use.

**Manual:** a dated check by the owner or a volunteer with a screen reader (NVDA, VoiceOver or
TalkBack) and with a keyboard alone, recorded in RLG-033 before 1.0. Owner checks on a real phone
for look and feel, which a test cannot see. *(Changed 2026-10-10, RLG-056: no standard is shown.)*

**Performance:** the targets are REQ-026 (1 s to the first screen, the menu), REQ-027 (100 ms response) and
REQ-028 (250 KB). Workload: a cold launch of the installed app, offline, on a mid-range phone, or
a Playwright run with CPU throttled 4x as its stand-in. `bench` records all three per release.

**Size plan (AUD-124, 2026-10-10).** The limit is 250 KB (REQ-028). At v0.8.8 the app ships 229.1 KB
in 32 files, so 20.9 KB is left. Slice 8 spent about 50 KB; slice 9 so far gave back about 10 KB, when
the Standards page and its data were removed and Zen Garden replaced the trace. The largest files
are `styles.css` 26.8 KB, `icons/icon-512.png` 25.5 KB, `app.js` 22.5 KB, `audio.js` 21.3 KB,
`config.json` 14.0 KB and `strings/en.json` 12.8 KB. The rule: a new activity may spend up to
15 KB (its script, its strings, its config and its styles), and a fix or polish unit up to 2 KB.
Each slice records its size at its close in the changelog. When less than 15 KB is left, the next
slice that adds a feature first takes a saving, and the owner chooses which. Known savings, in
order of risk: (1) a smaller 512 px PNG icon, with fewer colors or a lossless re-encode, about
10 to 15 KB; (2) config groups that only the tools read, moved out of the shipped `config.json`;
(3) unused CSS rules, removed after each screen is removed; (4) minified CSS and JavaScript, which
needs a build step and so a change to REQ-019; it is the last choice.

**Security and privacy.** Nothing sensitive is stored or sent. The threats worth defending against
are a supply-chain change (none: no third-party code ships), a tampered crisis line, and a
misleading claim (REQ-025). The control against a tampered crisis line is this: the owner is the
only person who commits; a crisis line is added or changed only with a source checked in the same
session (AGENTS.md); and a repository test pins each crisis number, and the directory link, to
its record, so a changed number or link fails the tests unless its record changes too
(`test_every_crisis_number_is_pinned`; the directory since AUD-076). No
enforced review of a commit exists. *(Changed 2026-10-08, AUD-007: it first said "every change goes
through a reviewed commit", a control that did not exist.)*

The Content Security Policy (`'self'` for every resource type, no inline script or style) limits
what Freelief's own page loads and connects to: no script, style, image or request from another
origin. It backs up the no-network rule. It does not protect Freelief's storage. **Known trust
dependency:** Freelief shares the origin `https://effigymedia.github.io` with the owner's other
GitHub Pages sites (Effigy Arcade, Tiny Arcade and Drinax Ref Console on 2026-10-07). Cache Storage
and `localStorage` belong to the origin, not to the path, so a page on any of those sites can read
and write Freelief's offline cache and its settings. A defect or a compromise in a sibling site can
therefore replace a cached file, such as `index.html` or `data/crisis-lines.json`, until the next
version replaces the cache. For the CSP, `'self'` is that shared origin, so it also allows a script
from a sibling path. The owner chose to stay on the shared origin (Decision Log, 2026-10-07 and
2026-10-08); an origin of its own (a custom domain or a dedicated account) removes this dependency.

**Incidents (AUD-105, owner 2026-10-09).** A defect in the live release, such as a wrong crisis
number or a broken start-up, is an incident. The owner may move `live` back to the previous tag at
once, with no audit round, and records the move and its reason the same day. Before 1.0 every move
of the preview is tagged `preview-X.Y.Z` (each earlier move was tagged on 2026-10-10), and from 1.0
each release is tagged `vX.Y.Z`, so the target always has a name (AUD-121). A rollback keeps the
person's settings: `settings.js` writes back every stored value that the running version cannot
read, so the older version keeps a newer version's choices, and they apply again after the fix. Installed copies
get the rollback at their next open, because the older `version.js` names another cache. A fix
forward is a release whose round covers only the lenses the fix touches.

**Moving or retiring the site (AUD-111).** Installed copies answer from their cache, so they never
learn of a change by themselves. To move Freelief to a new address: publish it there first; then
publish one last version at the old address whose start screen says where Freelief now lives, with a
link, and keep that version there for at least a year. To retire Freelief: publish one last version
that keeps the breathing guide and the urgent-help dialog, says plainly that the crisis lines are no
longer checked and that the international directory is the route, and then leave it in place. Do not
delete the site while installed copies can still open: a deleted site cannot tell them anything. The
environment's `Process/Teardown_Policy.md` governs the repository itself.
*(Corrected 2026-10-08, AUD-004: it first said the CSP "allows only the app's own origin".)*

---

## 10. Delivery Plan

**Slice 1 — walking skeleton: breathe, help, offline.**
- *Assumption tested:* a plain PWA on GitHub Pages can install, work offline, start the breath
  guide within 1 second, and be fully usable by keyboard and screen reader.
- *In:* the shell, the breath guide with the default rhythm, the "Need urgent help?" control with
  the first curated crisis lines and the directory fallback, the self-help line, the manifest, the
  service worker, `config.json`, `strings/en.json`, the test harness and `bench`.
- *Out:* other exercises, activities, tones, presets, Settings, the supporting pages.
- *Done when:* the offline, accessibility, smoke and crisis tests pass; `bench` meets REQ-026 and
  REQ-028; the owner has checked it on a phone; then the public repository is created (with the
  owner's yes) and pushed.

**Slice 2 — exercises.** Grounding, calming statements, rhythm presets, Settings, soft tones, and
the research sources for each technique. *(Grounding and calming statements were removed
2026-10-07.)*

**Slice 3 — distraction.** The bubble field and the shape trace.

**Slice 4 — trust pages.** The disclaimer page, the Standards & research page, the feedback page,
and the GitHub issue templates. *(The Standards & research page was removed 2026-10-10, RLG-056.)*

**Slice 5 — colour sort.** Built last, as the hardest to make accessible. It ships only if it passes.

**Slice 6 — owner polish, new activities, safety and settings fixes (v0.5.1 to v0.6.0).** *Added
2026-10-08 by the owner's ruling on AUD-068: the work after slice 5 is one named slice.* It covers
the owner's changes from the phone (menu first, layout, sounds, colors, logo), the removal of
grounding and calming words, the ripple pond, mandala coloring and the Visualizer, vibration, the
country list and saved region, the sources for every activity, and the fixes from design audit round
UNT-051. Done when: the round's safety, bug, records and polish fixes the owner chose are built and
tested, and the version is bumped to 0.6.0. Round UNT-051 is this slice's audit. Later work is
planned as named slices, each closed by an audit round and a minor bump.

**Slice 7 — clear the audit backlog (v0.6.4 to v0.7.0).** *Added 2026-10-08 by the owner's choice.*
The open findings from rounds before UNT-051 (2 High, 20 Medium and 25 Low on 2026-10-08) are
checked against the code: a stale finding is closed with the quote that shows the fix, a real one is
fixed as its own unit, High first, and an owner decision is put to the owner. Done when: every open
finding is built, declined by the owner, or waiting on the environment, and a design audit round
closes the slice; then 0.7.0.

**Slice 8 — new play and the round UNT-082 findings (v0.7.4 to v0.8.0).** *Planned 2026-10-09 by the
owner.* Owner features: Puzzle replaces Sort colors, a calm puzzle with no losing state at all, its
kind chosen by the owner from proposals first (RLG-040); ripples that interfere (RLG-041); more
mandala designs (RLG-042); crashing waves in the Visualizer, a Nature button and a rain-or-waves
setting (RLG-043), and music and nature sound that persist across screens until turned off, the
Visualizer's name and design rethought, with the owner choosing from proposals first (RLG-045);
every sound diatonic to the music's key, C major, with a test (RLG-046);
Standards and research rewritten for them, every source checked in the session
(RLG-044). Then the 37 findings of round UNT-082 (AUD-076 to AUD-112), Medium first, and a review of
every screen with the web-interface-review skill. Done when: those are built or ruled on, a design
audit round closes the slice, and the version is 0.8.0.
*Closed 2026-10-09: round UNT-104 closed the slice, and its High and Medium findings (AUD-113 to
AUD-117) were fixed before 0.8.0 by the owner's choice.*

**Slice 9 — the open findings (from v0.8.0).** *Planned 2026-10-09 (AUD-116).* The Low findings of
round UNT-104 (AUD-118 to AUD-128). The findings that rounds re-opened and no plan named: AUD-028
(Firefox has no test run), AUD-032, AUD-033, AUD-045, AUD-057 (an update under a second window),
AUD-071 and AUD-093. The interface review's open items (RLG-047), with the owner's ruling on the
mandala's target size first. The owner's phone checks (RLG-033). Each is fixed or ruled on by the
owner. Done when: none is open without a ruling, and a design audit round closes the slice.

**Definition of done per slice:** it works, `test` is green, `bench` is spot-checked, the design
document and records agree with the code, `docs/README.md` describes what a person sees (when the
slice adds or changes a feature that users see), and it is committed. *(README added 2026-10-08,
AUD-040.)*

**Release criteria for 1.0:** every "must" requirement is met; every success criterion in Stage 2
holds; an audit round clears the gate (`audit-gate.py` prints `GATE CLEAR`); every crisis line is
re-checked; the manual screen-reader and keyboard checks in RLG-033 are reported; the app makes no
standards claim and no health claim (REQ-025). *(Changed 2026-10-10, RLG-056: the Standards &
research page is removed.)*

---

## 11. Risks, Assumptions & Open Questions

| Risk | Mitigation |
|---|---|
| A person in danger uses the app instead of getting help. | The "Need urgent help?" control is on every screen, and the self-help line is on the main screen. |
| A crisis line in the list goes out of service. | Each line has a last-checked date; a release re-checks every line; the international directory is the fallback. |
| A claim overstates the evidence and breaks health-claim rules. | REQ-025 fixes the wording; each technique cites its research (REQ-024); a test scans for forbidden words. |
| ~~A standard is promoted that the app does not meet.~~ | *Withdrawn 2026-10-10 (RLG-056): the app makes no standards claim, and REQ-029 is withdrawn.* |
| No volunteer comes forward for the manual check. | The owner or a volunteer does it before 1.0 (RLG-033); the owner can ask in accessibility communities. *(Changed 2026-10-10, RLG-056.)* |
| A movement or a sound makes a person feel worse. | Reduced motion is honoured (REQ-010); sounds are soft and on by default, and the speaker button in the header fades them out over 0.6 s and then stops them (REQ-007; Decision Log, UNT-053 and UNT-078); sound waits while urgent help is open; nothing is timed or scored. |
| ~~The colour sort cannot be made fully accessible.~~ | *Withdrawn 2026-10-09: Unblock replaced the colour sort (REQ-014 withdrawn, REQ-035).* |
| Unblock is hard to use without sight or with shaky hands. | Three ways to move: a drag, arrow keys on a focused block, and choose then Slide buttons; Undo takes back any move; no score, count or timer; tests solve every board by keyboard. The manual screen-reader check is owed in RLG-033. *(Added 2026-10-10, AUD-126.)* |
| The background sound plays on after a person wants quiet, or surprises them on another screen. | The sound bar in the header shows it on every screen and turns it off in one tap; the speaker button holds every sound; a reset never starts it; only a choice on the Kaleidoscope starts it (REQ-036). *(Added 2026-10-10, AUD-126.)* |
| The shipped size reaches the 250 KB limit under release pressure. | The size plan in section 9 sets what each slice may spend and lists known savings; `build` fails over the limit (REQ-028). *(Added 2026-10-10, AUD-124.)* |
| The offline cache serves an old version after an update. | The cache name carries the version; an update test covers it. |

<!-- BEGIN srs-assumptions - written by the interview, read by the generators -->
- The crisis lines in the curated list stay in service between checks. Each line carries a
  last-checked date, and a release re-checks them.
- The owner or community volunteers will do the manual accessibility checks before 1.0 (RLG-033).
  The app makes no standards claim either way (RLG-056).
- GitHub Pages stays free for a public repository and serves the app over HTTPS, which an
  installable offline web app needs.
- A mid-range phone can show the menu within 1 second of a cold offline launch with a
  plain HTML, CSS and JavaScript app under 250 KB.
- The device language and region setting is a good enough guide to the person's country for
  choosing crisis lines.
<!-- END srs-assumptions -->

**Open questions.**
- **The public feedback email address.** The owner chooses it when they want the email route. It
  does not block a release: REQ-030 makes email optional, so until then the button is hidden and
  GitHub is the route (changed 2026-10-08, AUD-020).

---

## 12. Decision Log

All owner-decided 2026-10-07 in the design interview unless a line says otherwise.

- **"Accessible like Effigy Arcade" means both readings: reachable and usable in distress.** — A
  person in a panic attack needs the app to load at once with no network, and also needs it to work
  with shaky hands, a screen reader, a keyboard or reduced motion. — Rejected: only one reading. —
  2026-10-07
- **The first version offers paced breathing, 5-4-3-2-1 grounding, calming statements and
  distraction activities.** — These are the common self-help techniques for acute panic, and
  distraction was the owner's explicit addition. — Rejected for now: an episode log, because it
  stores personal data. — 2026-10-07 *Amended 2026-10-07 (owner, UNT-032): grounding and calming
  statements are removed; see the entry below.*
- **Ground yourself (5-4-3-2-1 grounding) and Calming words are removed.** — The owner did not like
  them, and their research was weak: the one grounding study was small, uncontrolled and about test
  anxiety, and the support for calming statements was indirect (coping self-talk as one part of
  stress inoculation training and of cognitive therapy). Freelief offers only techniques it can
  back. Interactive activities take their places (a ripple pond and mandala coloring, tracked as
  RLG-013 and RLG-014). — Rejected: keep them with a weaker claim. — 2026-10-07 (owner; UNT-032)
- **The distraction activities are a bubble field, a shape trace and a colour sort.** — Each one
  has no score, no failure and no timer. — Rejected: a counting task. The colour sort is "should"
  and not "must", because a keyboard and screen-reader path for it is the hardest to build. —
  2026-10-07 *Superseded 2026-10-10 (AUD-093, UNT-118): the activities are now Pop Bubbles, Zen
  Garden, Ripple Pond, Color Mandalas, Unblock and Kaleidoscope. Unblock replaced the colour sort
  (2026-10-09, UNT-096) and Zen Garden replaced the shape trace (2026-10-10, UNT-115); see those
  entries.*
- **A "Need urgent help?" control on every screen opens crisis lines by region, chosen from the
  device language and region setting.** — A person who may be in danger must reach a human fast,
  and asking for location adds a prompt and a privacy cost. — Rejected: one fixed line; an
  emergency number only. — 2026-10-07
- **The self-help statement is one quiet line on the main screen, with the full text on the
  disclaimer page.** — Nothing may stand between the person and help. — Rejected: a first-run
  notice; About page only. — 2026-10-07
- ~~**The disclaimer page lists every standard Freelief meets, with its level and the date of the
  last check, and lists only verified ones.**~~ — 2026-10-07. *Superseded the same day by the
  "Standards & research" page below.*
- **A "Standards & research" page promotes every verified standard, with its level and the date of
  the last check, and cites research for each technique.** — The owner wants the standards used as
  a selling point. A claim that a check has not proven would mislead. — Rejected: a section of the
  disclaimer page; a pop-up window, which is harder to make accessible. — 2026-10-07 *Superseded
  2026-10-10 (owner, UNT-114): see "No Standards and research page".*
- **Only clinically researched techniques. Claims say "built on techniques studied in clinical
  research" and never "clinically proven", "treats" or "cures".** — In most markets a health claim
  for an app is regulated (FTC and FDA in the US, ASA and MHRA in the UK). Freelief itself has had
  no clinical study. A review or certification, such as by a clinician or ORCHA, may be claimed only
  after it is granted. — Rejected: stronger wording such as "clinically proven to reduce panic". —
  2026-10-07
- ~~**Soft tones mark the breath, off by default. No spoken voice.**~~ — 2026-10-07. *Superseded the
  same day by the owner: sounds on by default, see below. No spoken voice still stands.*
- **Freelief collects no personal data and makes no network call after install.** — A person's
  worst moments are not telemetry. — Rejected: anonymous usage counts. — 2026-10-07 *Amended
  2026-10-08 (owner, AUD-025): the browser's check for a new version still reaches GitHub Pages when
  the person is online. It carries nothing about the person. The privacy text and REQ-015 now say
  so; see "The privacy text names the update check".*
- **Accessibility target: WCAG 2.2 AA in full, and AAA wherever a criterion can be met.** — The
  users are in distress, so the stricter bar fits. — Rejected: AA only; no named standard. —
  2026-10-07
- **English only in the first version, with all text in one strings file per language.** — This
  keeps the first version small and makes a later translation a data change. — Rejected: English
  and Spanish at launch; English with no translation structure. — 2026-10-07
- **Freelief is for anyone, in the moment: no sign-up, no profile, no history.** — Rejected: a daily
  practice with reminders or streaks, which add stored data and pressure; a clinician-shaped tool.
  — 2026-10-07
- ~~**On launch, the breathing guide starts at once.**~~ — 2026-10-07. *Superseded the same day by the
  owner: Freelief opens on the menu, see below.*
- **Plain HTML, CSS and JavaScript as a progressive web app on GitHub Pages, with no framework, no
  dependency and no build step.** — It gives the smallest download, the fastest load and nothing to
  break, as in Effigy Arcade. — Rejected: a small framework such as Preact. — 2026-10-07
- **Tier: Standard.** — Rejected: Utility. — 2026-10-07
- **Routing posture: 2 (quality).** — People use Freelief in a crisis, so a wrong word or a broken
  screen costs more than rework. — Rejected: 1 (balanced). — 2026-10-07
- **Look: soft and dim. A dark calm theme by default that follows the device light or dark setting,
  with AAA text contrast.** — It does not glare at night, when many attacks happen. — Rejected: light
  and airy; nature imagery, which needs assets and contrast care. — 2026-10-07
- **Crisis lines: a small curated list in the app, each line with a last-checked date, plus a link
  to an international directory.** — The common lines work offline, and a dated entry shows when it
  needs a check. — Rejected: a directory link only, which needs a network in a crisis; a large
  built-in list, which goes stale. — 2026-10-07
- **Breathing rhythm: presets, with 4-in 6-out as the default, a slower rhythm and box breathing.**
  — Rejected: one fixed rhythm; full sliders, which are too much to choose in distress. — 2026-10-07
  *Amended 2026-10-07 (owner, UNT-031): box breathing is the default and is listed first. A device
  that already saved a rhythm keeps it. Balban 2023 studied box breathing as one of its arms.*
  *Amended 2026-10-08 (owner, UNT-050): back to 4-in 6-out as the default. The source check found
  that in Balban 2023 an exhale-focused method gave a larger mood gain than box breathing, and the
  owner asked for the longer breath out if it does better. Of the three presets, 4-in 6-out is the
  closest to that method. A saved rhythm is kept.* *Corrected 2026-10-08 (AUD-061, UNT-052): that
  reading was wrong. Balban 2023 compared each breathing method only with mindfulness; only cyclic
  sighing beat it significantly, the methods were not compared with each other, and no arm used a
  plain long out-breath. The owner kept 4-in 6-out on other grounds: every preset is slow breathing
  under 10 breaths a minute, which Zaccaro 2018 supports, and it was the original design choice.*
- **Strict performance targets: the breathing guide is visible within 1 s of a cold, offline launch
  on a mid-range phone; every input responds within 100 ms; the whole app is under 150 KB.** — In a
  panic attack every second of wait is felt. — Rejected: looser targets (3 s, 500 KB). — 2026-10-07
  *Amended 2026-10-07 (owner): the size limit is 250 KB, and the 1 s target is to the menu (REQ-026);
  see the entries below. Restated in Stages 2, 9 and 11 on 2026-10-08 (AUD-065).*
- **The walking skeleton is breathing, help and offline: an installable offline web app on GitHub
  Pages, the breathing guide at launch, the "Need urgent help?" crisis list, the self-help line, and
  a full keyboard and screen-reader path.** — It proves the riskiest parts end to end. — Rejected:
  breathing only; all exercises in a rough form. — 2026-10-07
- **Accessibility claims are checked by an automated tool on every page and by a dated manual pass
  with a screen reader and a keyboard. The manual pass comes from community volunteers, for example
  from Reddit.** — Freelief is a free, open-source tool with no budget for a paid audit. Automated
  tools find only part of the WCAG issues, so a claim needs the manual pass too. — Rejected:
  automated only; a paid external audit. — 2026-10-07
- **Freelief is free and open source under the MIT license.** — The owner's stance: a free relief
  tool. MIT is short and lets anyone reuse the code with credit. — Rejected: GPL-3.0; MIT for code
  with CC BY for the text. — 2026-10-07
- **A feedback page in the app opens a pre-filled GitHub issue, or a pre-filled email for people
  with no GitHub account.** — Volunteers can report checks and problems with little effort. The
  person sees and edits every word, and the app itself sends nothing. — Rejected: the app writes to
  the repository directly, because a static site cannot keep a GitHub token secret, so anyone could
  take it and misuse the repository; a relay server, because it adds a server, a network send and
  spam handling; GitHub only. — 2026-10-07
- **The GitHub repository EffigyMedia/freelief is created, public, when the first slice is ready.**
  — Public, so that GitHub Pages is free and the source is open. — Rejected: create it now, private
  or public. — 2026-10-07
- **The first curated crisis lines cover the US, the UK, Canada, Australia and Ireland.** — These
  are the main English-speaking regions, which matches the English-only first version. Every other
  region gets the international directory. — Rejected: US only; a wider list, which has more lines
  to keep checked. — 2026-10-07
- **The feedback email address is decided later; the email button stays hidden until then.** —
  Owner's choice. — 2026-10-07 *Amended 2026-10-08 (owner, AUD-020): REQ-030 now makes the email
  route optional. GitHub is the route; the pre-filled email is offered once the owner chooses an
  address. A release with the email button hidden meets REQ-030.*
- ~~**Testing: Python and Playwright from a project-local venv, with axe-core vendored for tests
  only.**~~ — 2026-10-07. *Superseded the same day at Initialize by the entry below.*
- **Testing: Python and Playwright from a project-local venv, with axe-core from the
  `axe-playwright-python` package.** — Real-browser tests, including offline and network-log
  checks, with the same toolchain as Effigy Arcade. The package bundles axe-core, so no file is
  downloaded and copied by hand, and nothing from it ships, so REQ-019 holds. — Rejected: axe-core
  copied into `tools/vendor/` (a manual download to keep current); Node test runners; manual testing
  only. — 2026-10-07
- **The design document stays at `docs/Design_Document.md`, and the repository root holds no
  `.md` file except `AGENTS.md` and `CLAUDE.md`.** — `srs.py` and `prd.py` read the design document
  only at that path; `Development_Process.md` says to move it, and the two shared documents
  disagree. — Rejected: a move to `docs/core/Freelief_design.md`. — 2026-10-07 (Initialize)
- **The project commands are one script, `tools/freelief.py`, and the version lives in
  `version.js`.** — One script is one place to read. `version.js` is plain script, so the page
  loads it with a script tag and the service worker with `importScripts`, and the cache name always
  matches the app. — Rejected: the version in `config.json` (that file is tunables) or in the
  manifest (no standard field). — 2026-10-07 (Initialize)
- **The urgent-help dialog puts the emergency number first and adds a closed "Lines in other
  countries" list.** — In immediate danger, the emergency number is the first thing to see. The
  device language can name the wrong country (a visitor, or a phone left on `en-US`), so every
  curated line stays one tap away. — Rejected: the directory and the emergency line only for an
  uncurated region, as first written in F6. — 2026-10-07 (slice 1, implementer; the owner checks it
  on the phone)
- **The international directory is Find A Helpline (findahelpline.com)** — free, run by
  ThroughLine, more than 175 countries, checked 2026-10-07. — Rejected: Befrienders Worldwide
  (narrower: befriending centres only). — 2026-10-07 (slice 1, implementer; **confirmed by the owner
  2026-10-07**)
- **The colour sort is choose-then-swap, not drag; every tile names its hue and shade; the tiles
  stay in one row.** — One method serves touch, mouse, keyboard and screen reader, and the shade
  names make the task possible without sight. A row that wrapped would break the left-to-right
  order, so the tiles shrink to fit (never under 44 pixels). It passed every automated check, so
  under REQ-014's rule it ships. — Rejected: drag with a separate keyboard mode (two methods to
  learn; drag is hard with shaky hands). — 2026-10-07 (slice 5, implementer; **REQ-014 was edited,
  and the owner confirms or asks for drag as an addition**). *Amended 2026-10-07: the owner asked
  for drag as an addition; see the next entry.* *Corrected 2026-10-08 (owner, AUD-015): "under
  REQ-014's rule it ships" was wrong. REQ-014 has no such rule. The colour sort shipped under
  RLG-005's rule, which requires the automated checks and a manual accessibility check. The
  automated checks passed, and the keyboard-only solve is an automated test; no person has done a
  manual screen-reader check. The owner kept Sort colors in the menu. The manual screen-reader and
  keyboard check is owed before 1.0 and is listed in RLG-033.* *Superseded 2026-10-09 (owner,
  UNT-096): Unblock replaced the colour sort; see "Unblock replaces Sort colors". The owed manual
  check moved to Unblock (RLG-033).*
- **Drag is added to the colour sort beside choose-then-swap, not in place of it.** — Freelief is
  a mobile web app, and on a phone a person expects to drag a tile. Choose-then-swap stays, so the
  keyboard, the screen reader and a person with shaky hands keep one method that needs no fine
  movement. A drop on another tile swaps the two, so both methods do the same thing and the live
  line says the same words. A movement under `sort.dragThreshold` pixels is a tap, not a drag, and
  a drop off the tiles changes nothing. — Rejected: drag that inserts and shifts the other tiles (a
  second rule to learn); drag only (no path without sight). — 2026-10-07 (owner; UNT-029)
  *Superseded 2026-10-09 (owner, UNT-096): Unblock replaced the colour sort, and its drag carries
  over as a drag on a block; see "Unblock replaces Sort colors".*
- **About credits the maker: "Made by", the Effigy Media logo (a 200 x 120 copy of the owner's own
  logo from Effigy Arcade, 26 KB) and a link to https://www.effigymedia.com.** — Owner request. The link
  is one the person chooses; the app still sends nothing. — 2026-10-07 (owner) *Amended 2026-10-07
  (owner, UNT-038): the PNG is replaced by the logo's six bars drawn as inline SVG; see the entry
  below.*
- **The Effigy Media logo on About is its six bars, drawn as inline SVG, in the theme's text color,
  with no lettering.** — The owner asked whether a vector logo would cut the size and chose to draw
  the bars and omit the "EFFIGYMEDIA" text, because the attribution line already names Effigy
  Media. The bars are measured from the PNG (each 26 units thick with 8-unit gaps). They take
  `--text`, so they are soft white in the dark theme and soft black in the light theme, and the
  metallic gradient goes. The shipped size fell from 178.1 KB to 152.5 KB. — 2026-10-07 (owner;
  UNT-038)
- **The shipped size limit is 250 KB, raised from 150 KB.** — The app reached 148.2 KB; the owner chose
  room for more features over trimming. The 1-second launch target stays the guard on speed. —
  2026-10-07 (owner)
- **The app icon is a brushed ensō (the Zen circle) around a soft breath glow, on the night-blue
  background; its opening sits at the upper right so it never reads as a power button.** — The owner
  asked for "something zen" and chose this one of three drafts (`tools/icon_drafts.py`). — 2026-10-07
  (owner)
- **Buttons outside the header are centred. The footer line no longer mentions breathing. The glass
  trace's volume follows speed from a quiet floor, and its trail runs from the loop's start to the
  finger, clearing each loop. On Settings, Back to menu sits at the top. Calm has Full screen (the
  browser's full screen where it exists, a full-viewport stage everywhere), a slowly drifting soft
  background colour, and softly pulsing shape colours.** — Owner requests from the phone. — 2026-10-07
  (owner) *Amended 2026-10-07: Back to menu now sits at the top of every screen; see the next entry.*
- **Back to menu sits at the top of every screen that has it, under the header. A line divides the
  header from the screen, and another divides the footer from it. The version line on About is
  centred.** — Owner requests. The way back is always in the same place, so a person in distress
  never has to scroll to find it. The menu has no Back to menu, so the row is hidden there. —
  2026-10-07 (owner; UNT-030)
- **An activity shows no instruction text above it; the instruction stays for a screen reader.**
  — The owner found the text extraneous: the activities explain themselves to a person who can
  see them. A screen-reader user cannot see them, so each intro stays in the page as visually
  hidden text after the heading, and the colour sort's row still names it with
  `aria-describedby`. — Rejected: delete the text, which leaves a screen-reader user without the
  method. — 2026-10-07 (owner; UNT-033)
- **All user-facing text uses American spelling, and the Calm screen is named "Visualizer".** —
  Owner's decision. "Visualizer" says what the screen is: sound with soft moving shapes, with
  nothing to do. The route stays `#calm`, and code names (`calm.js`, `config.json` → `calm`, string
  keys such as `sort.newColours`) are unchanged, because a person never sees them. This document and
  the code comments keep their existing spelling; `test_repo.py` guards only the text a person
  sees. — 2026-10-07 (owner; UNT-034) *Amended 2026-10-10 (owner, RLG-057 and RLG-058): the
  person now sees the name "Kaleidoscope"; the route stays `#calm`.*
- **The Visualizer's rain is softer, and a third sound mode, Both, plays the music and the rain
  together.** — Owner request. The rain is quieter (volume 0.05 to 0.035), duller (low-pass 2600
  to 1800 Hz) and its drops are fainter, lower and rounder (volume 0.07 to 0.035, 2400 to 1700 Hz,
  a 90 ms decay and a wider band). Both plays the pads at 0.9 and the rain at 0.6 of their own
  levels (`config.json` → `calm.bothMix`), so the rain sits under the music. — 2026-10-07 (owner;
  UNT-035)
- **A ripple pond is added as a distraction activity.** — The owner chose it to take one of the
  places of the removed grounding and calming words. The pond is one real button, so touch, mouse,
  keyboard and screen reader all reach it; a key press makes a ripple at a random place because a
  keyboard has no point to touch. A drag leaves a ripple every `ripple.trailSpacing` pixels, and at
  most `ripple.maxRipples` show at once. Under reduced motion a ring fades at a middle size and
  does not spread. Its research is the same as for the other distraction activities; it has none
  of its own, and the Standards page does not claim any. — Rejected: a canvas (the architecture
  rule). — 2026-10-07 (owner; UNT-037)
- **Mandala coloring is added as a distraction activity.** — The owner chose it for the other
  removed screen. It has the closest research of the options offered: coloring a mandala lowered
  anxiety more than free drawing in Curry and Kasser (2005), already cited. The mandala is SVG
  drawn from ring formulas in `config.json` (petal, band, dot), so no image ships. Each shape is a
  focusable button with a name, with one tab stop for the whole mandala and arrow keys inside it,
  as in the colour sort. Every shape in every design is at least 24 px at a 360 px width (WCAG
  2.5.8); the swatches are 48 px. A tap replaces a fill; there is no eraser and no end. — Rejected:
  a canvas (the architecture rule); a fixed image (size, and no names). — 2026-10-07 (owner;
  UNT-040) *Amended 2026-10-09 (owner, RLG-047; UNT-107): every shape is now at least 44 px; see
  the entry on mandala target size.*
- **While urgent help is open, the page under it does not scroll.** — The owner reported that the
  app under the open dialog still took touches. Taps were already blocked by the modal dialog, but
  a swipe on the backdrop scrolled the page under it, and a scroll past the end of the help list
  could move the page too. The shell now sets `overflow: hidden` on the page while the dialog is
  open, and the dialog has `overscroll-behavior: contain`. — 2026-10-07 (owner report; UNT-041)
- **Urgent help shows one region at a time, chosen from Settings or the device, with a country
  list to change it.** — The owner found the long list of every country hard to use and asked for
  a dropdown or a saved default, and chose both. Settings has "Region for urgent help": Automatic
  (the device language and region, as before) or a curated country, saved only on the device. The
  dialog opens on that region and has a Country list of the curated regions plus "Another country"
  (the general emergency line and the directory). A choice in the list holds for one visit and
  does not change the setting. A saved code that is no longer curated falls back to the general
  route. Freelief still never asks for location. — Rejected: the long list (owner); saving the
  dialog's choice (a person helping someone else would change the owner's default). — 2026-10-07
  (owner; UNT-042)
- **The installed app is portrait only.** — Owner request. The manifest sets `"orientation":
  "portrait"`, which a phone applies to the installed app. A browser tab cannot be locked to an
  orientation (the Screen Orientation API locks only in full screen), and a desktop ignores the
  setting, so in a tab and on a desktop the app still works in any shape. — Rejected: a "turn your
  phone" screen in landscape, which would block help in a crisis. — 2026-10-07 (owner; UNT-045)
- **A short vibration marks each single event in an activity; nothing continuous vibrates.** — The
  owner asked for haptic feedback, on by default with a Settings switch, for triggered events
  only. `haptics.js` sends one short pattern from `config.json` → `haptics.patterns` for a pop, a
  choice, a swap, a finished sort, a finished loop, a ripple from a touch or a key, and a fill. The
  breathing guide, a drag trail in the pond and the glass tone of the trace never vibrate. The
  Vibration API is missing in Safari, including every browser on iPhone, so the Settings hint says
  plainly that it does not work there; on such a device nothing happens and nothing fails. —
  *Amended 2026-10-08 (UNT-047): checked on caniuse.com (Vibration API) in this session. Safari on
  macOS and iOS has no support, so no browser on iPhone does; Firefox dropped it at 129 and
  Firefox for Android has none; Chrome and Samsung Internet on Android support it. The hint now
  names where it works and where it does not.* —
  Rejected: vibration on the breath (continuous, by the owner's rule). — 2026-10-07 (owner;
  UNT-046)
- **Standards and research cites sources for every activity, each in its own section, and states
  how strong its evidence is.** — Owner request. A research agent checked every source in the
  session (Crossref, Europe PMC, PMC or the paper itself) and the session spot-checked three on
  Crossref. Where no study tested the activity, the section names the closest research and says
  "No study has tested this activity itself": bubbles (distraction; video games and stress),
  trace (working-memory tasks and upsetting images), sort (Tetris and intrusive memories), ripple
  (water scenes; nature sounds). Mandala coloring and music have direct, small or mixed evidence.
  The breathing text now says that box breathing gave a smaller gain than an exhale-focused
  method in Balban 2023. A last section keeps the caveat on distraction, reworded to "the
  evidence for that is mixed" as Helbig-Lang 2010 says. — 2026-10-08 (owner; UNT-049)
- **Sound is switched on and off from a speaker button in the header, not in Settings.** — The
  owner asked for it after the design review found that sound starts on its own on Breathe and the
  Visualizer, which can startle a person in public. The speaker sits between "Need urgent help?"
  and the gear on every screen; it is crossed out when off, and it is a toggle button named
  "Sound". Off suspends the audio at once, mid-note; on allows the next sound and restarts the
  Visualizer's music. Sounds stay on by default. On a phone narrower than 430 px the header is
  tighter (16 px help label, 44 px round buttons), so "Need urgent help?" stays on one line from
  360 px. — Rejected: off by default; a switch only in Settings. — 2026-10-08 (owner; UNT-053)
  *Amended 2026-10-08 (owner, UNT-078): Off now fades over 0.6 s and then suspends; see the next
  entry on the fade.*
- **The speaker button fades sound out over 0.6 s, not at once.** — The owner found the hard cut
  jarring (RLG-034). Off ramps the master volume to zero over `sounds.muteFadeSeconds` (0.6 s) and
  then suspends the audio; On resumes it and fades in. A sound stopped while the audio is paused is
  cut off, so no frozen tail plays later. 0.6 s still meets the risk "a sound makes a person feel
  worse": the sound starts to drop at once and is gone in well under a second. — 2026-10-08 (owner;
  UNT-078) *Recorded 2026-10-09 (AUD-090): this entry was missing.*
- **Safety fixes from the design review and round UNT-051.** — The owner chose to fix safety first.
  (1) The emergency number is a Call button, the first tap target in urgent help; the numbers come
  from the region's own emergency text, so "112 or 999" gives two buttons, and no number is guessed
  for an uncurated country. (2) Sound waits while urgent help is open and while Freelief is hidden,
  for example during a call to a line, and comes back only if sound is on (AUD-074). (3) Breathing
  and the Visualizer hold a screen wake lock, so the phone does not dim or lock mid-breath; a
  browser without the API lets the screen sleep. (4) The Visualizer's full screen has its own "Need
  urgent help?" button, which leaves full screen and opens help (AUD-075). (5) The black screen is
  the one state without the help control; one tap or key brings the screen and the control back,
  and while it is black no shape is added and the stage does not animate, which saves power. —
  2026-10-08 (owner; UNT-054)
- **Settings stores only what the person changed, under a new key, `freelief.settings.v2`.** — The
  audit (AUD-062) found that every save wrote every value, so a default froze as if chosen and the
  new long out-breath default never reached anyone who had changed any setting. The v1 store is
  read once and removed: a value carries over only if it differs from today's default, and a
  stored "box" rhythm is dropped, because box was the default from 2026-10-07 to 2026-10-08 and was
  most likely never chosen. The implementer chose this rule because the box period was a few
  hours of a public preview; a person who did choose box chooses it again in Settings. —
  2026-10-08 (implementer, owner-delegated fix order; UNT-055)
- **"Update now" removes nothing until the network is shown to work.** — The audit (AUD-056) found
  that it deleted the offline copy and the worker first, so on a dead or captive connection the app
  was gone until the device was online. Now `registration.update()` fetches the worker from the
  network first; if that fails, everything stays and the screen says "Could not update. This
  version still works offline." A new version installs in its own cache and takes over; only when
  the version is already current is the copy refreshed in full. — 2026-10-08 (UNT-056) *Amended
  2026-10-10 (AUD-133, UNT-127): the refresh replaces the copy only when every file arrived; see
  "Update now replaces a current copy only when the new one is whole".*
- **A new version waits until it is safe to take over.** — The audit (AUD-057) found that after a
  touch, a new version took over mid-session and served its new screens to the old page. Now the
  worker installs and waits; the page lets it take over only before the first touch (and then
  reloads once) or when the person presses Update now. After a touch the page keeps its own
  version, files and all, and the next open gets the new one. A screen that cannot load falls back
  to the menu and the address becomes `#menu`, so the failed screen's link works again. —
  2026-10-08 (UNT-057) *Amended 2026-10-09 (AUD-107, UNT-098): a running breathing screen also
  counts as in use, so with "Start breathing at once" an update found at launch waits for the next
  open and does not restart the breath.*
- **The Breathe card stands out, and Settings can make Freelief open on breathing.** — The design
  review found that, since the app opens on the menu, a person in panic must read and choose before
  any help starts. The owner kept the menu as the default and chose two polish items: the Breathe
  card is filled and larger, and Settings has "When Freelief opens: Show the menu / Start breathing
  at once" (`openOn`, saved only when changed). Only an open with no address follows it; a link to
  a screen opens that screen. — Rejected: breathing as the default again (the owner's 2026-10-07
  decision stands). — 2026-10-08 (owner; UNT-061)
- **On an exercise or activity, the footer shows only its calm line.** — The design review found
  that the full footer (the calm line, the self-help line and three links) took about a quarter of a
  phone screen under the exercise. On Breathe and the six activities only "You are safe right now.
  Take your time." shows; the menu and the info pages keep the full footer. *(Amended 2026-10-09
  (owner, RLG-051): the line is now "You are safe right now."; "Take your time" is removed.)* The self-help line
  stays on the main screen, the menu (REQ-006), and the links stay one tap away through Back to
  menu. — 2026-10-08 (owner; UNT-062)
- **The trace marker is about 44 px across on a phone.** — The design review found it about 25 px,
  small for shaky hands, though a touch anywhere on the shape already moves it. Its radius is a
  tunable (`trace.markerRadius`, 22 units); the panel has a small padding and the drawing may
  overflow into it, so the marker is never clipped at a shape's edge. — 2026-10-08 (owner; UNT-063)
- **The breathing screen shows its rhythm under the circle, such as "In 4 · Out 6".** — The design
  review found that a first-time user sees a count that goes up with no stated end. The line is
  built from the rhythm's own numbers and the short phase names in the strings file, so it always
  matches the rhythm that runs. This closes slice 6 at version 0.6.0. — 2026-10-08 (owner; UNT-064)
- **Feedback keeps the person's words out of the GitHub web address; a Copy button carries them.**
  — The audit (AUD-055) found that "Open on GitHub" put the whole message in the URL, so it reached
  browser history and GitHub when the link opened, before the person pressed Submit. The owner
  chose the Copy button: the link carries only the template and the title, and "Copy message"
  copies the text for the person to paste; where the browser refuses, the text is selected for a
  manual copy. The email link is unchanged, because it opens the person's own mail app. — Rejected:
  keep the body in the URL with a warning. — 2026-10-08 (owner; UNT-065)
- **A screen that fails as it starts falls back to the menu, and a late start-up failure brings back
  the static fallback.** — The audit (AUD-008, AUD-002) found that a failed data load on a deep link
  to Standards stopped the router, because the address listener was added after the first screen,
  and could leave a frozen copy of the last screen. The shell now listens before the first screen,
  clears the old screen before a new one starts, and falls back to the menu (with the address
  `#menu`) when a screen's start fails, as it already did when a screen could not load. Standards
  checks both of its data loads. If the menu itself cannot start after the shell is built, the
  static fallback from `index.html` is put back. — 2026-10-08 (UNT-069)
- **The ripple pond tells a touch's click from a key press by a flag, not by time.** — A click
  within 600 ms of a touch was ignored, but a slow drag lasts longer, so its click counted as a key
  press and added a random ripple. Now a touch sets a flag that its click clears; a key press or a
  cancelled touch clears it too. `ripple.clickAfterPointerMs` is removed. Found when the suite ran on
  a slower machine. — 2026-10-08 (UNT-070)
- **Urgent help uses only a region the person set, and says that web chat needs the internet.** —
  The audit (AUD-026) found that a bare language such as "en" was expanded to the US, so the dialog
  said "call 911" to someone who may not be in the US. Now only an explicit region counts; with
  none, the dialog shows the general route ("call your local emergency number") and the directory,
  and the Country list and Settings can still pick a region. A line's "Chat online" button now
  says it needs an internet connection; calls and texts work offline (AUD-052). — 2026-10-08
  (UNT-071)
- **Feedback says that a GitHub issue is public, and points a person in danger to urgent help.** —
  The audit (AUD-006, AUD-053) found no warning that an issue is public and no word for someone in
  danger who writes feedback. The page now says, above the buttons, that feedback is not watched
  around the clock and that a person in danger should use "Need urgent help?" or call their local
  emergency number; the GitHub hint says issues are public. Both issue templates carry the same two
  lines as comments, seen while editing. The in-app message text stays free of them, because the
  person copies it into the public issue. The owner's response rule for an issue from a person in
  danger is still to be stated. — 2026-10-08 (UNT-072)
- **No response rule beyond the warning for an issue from a person in danger.** — The owner ruled
  (AUD-053) that the Feedback page's line, that feedback is not watched around the clock and that
  a person in danger should use "Need urgent help?" or call their local emergency number, is the
  handling. GitHub issues are answered when the owner sees them, with no promise of time. —
  Rejected: a reply-with-help-routes rule and a safety label. — 2026-10-08 (owner)
- **The current look is confirmed.** — The owner confirmed the soft dark and light themes, the
  rounded buttons and the calm blue accent, as they stand after the changes made from the phone on
  2026-10-07 and 2026-10-08 (AUD-048). No separate variants were shown; the owner chose by using the
  app. — 2026-10-08 (owner)
- **Freelief supports Chrome, Safari and Firefox, and the never-break paths are tested in WebKit.** —
  The audit (AUD-028) found no stated baseline and a suite that ran only in Chromium, though many
  phones use Safari. The owner named the current and previous major versions of Chrome, Safari and
  Firefox. The whole suite runs in Chrome; `test_engines.py` runs the never-break paths (menu,
  breathing, urgent help, three activities, the sound button) in Playwright's WebKit, Safari's
  engine. Firefox's engine cannot start on the development machine until the Microsoft Visual C++
  runtime is installed, which is the owner's step (RLG-033); `doctor` warns until then. —
  2026-10-08 (owner; UNT-081)
- **The header is frozen at the top; the page scrolls under it.** — Owner request. The header
  (Freelief, "Need urgent help?", the sound button and the gear) is sticky with its own background,
  so the way to help is always one tap away on a long page. `body` now grows with its content, which
  a sticky header needs. The Visualizer's full screen and black screen still sit above it. —
  2026-10-08 (owner; UNT-083)
- **Each mandala color has its own note, played as a rain chime; the trace's glass is softer.** —
  Owner requests. Choosing a color and filling a shape play that color's note (C, D, E, G, A and
  high C, a pentatonic scale, so any two sound well together) as a small struck chime: inharmonic
  sine partials that fade at their own rates, with a quieter second strike, like a chime touched by
  rain (`sounds.chime`, `mandala.palette[].note`). The old step cue, now unused, is removed. The
  trace's crystal glass is 40% quieter (`sounds.glass.volume` 0.035 to 0.021). — 2026-10-08 (owner;
  UNT-084) *Superseded in part 2026-10-10 (owner, UNT-115): the trace and its glass sound are
  removed; see "Zen Garden replaces Trace a shape". The mandala chime holds.*
- **A sound that stops while sound is off, or while the off-fade runs, is cut off at once.** — The
  owner found that muting in the Visualizer, leaving it and unmuting played the music again and then
  faded it. Muting pauses the audio clock after its fade, so a sound's own fade-out froze partway
  and resumed with the sound. Now each fading sound is registered, and is cut off silently just
  before the audio pauses; a sound stopped while the audio is already paused is cut off at once. —
  2026-10-08 (owner report; UNT-085)
- **Sort colors shows the order with an arrow under the tiles.** — Owner request. A horizontal arrow
  points right, from "Light" under its left end to "Dark" under its right end, so a person who can
  see the tiles knows the task without reading. It is hidden from a screen reader, because the
  intro already says the order. — 2026-10-08 (owner; UNT-086) *Superseded 2026-10-09 (owner,
  UNT-096): the arrow went with Sort colors; see "Unblock replaces Sort colors".*
- **The mandala has eight designs and five shape kinds.** — Owner request (RLG-042): more designs.
  Five designs are added to the three, and two shape kinds are added to petal, band and dot: a
  scallop (a sector with a rounded outer edge) and a diamond (four straight sides, widest at the
  middle). The designs are still data in `config.json`, so no image ships. Every shape in every
  design stays at least 24 px at a 360 px width, and a test keeps two diamonds side by side from
  overlapping, because a shared edge is hard to tap. — Rejected: designs from image files (size,
  and no names for the shapes). — 2026-10-09 (owner; UNT-091)
- **Every pitched sound that plays with the music is in its key, C major.** — Owner request
  (RLG-046). The pads play C, Am, F and G, so the key is C major (C D E F G A B). Every fixed note
  was already in the key. The rain's drops had a random pitch (a narrow noise band at 1190 to
  2210 Hz); each drop now takes one of five C-major notes (D6, E6, G6, A6, C7,
  `sounds.rain.dropNotes`). A test checks every pitch in `config.json` to within 5 cents of a
  C-major note, and another records the rain's drops as they play. The bubble pop and the ripple's
  water drop keep their random pitch, because they are natural sounds, and the test excludes them
  by name. Filter corners, the rain's swell and the glass's beat are not notes. — Rejected: C-major
  notes for the pop and the water drop (owner). — 2026-10-09 (owner; UNT-093)
- **The background sound keeps playing until it is turned off, and a sound bar shows it.** *(The
  bar and the Visualizer's choice were replaced on 2026-10-09 by the three-button bar; see that
  entry.)* — Owner
  request (RLG-045); the owner chose the sound bar from three designs (a header sound menu with the
  Visualizer renamed, and a choice in Settings only, were not chosen). The Visualizer keeps its name
  and gains Off. Its choice is the background sound, owned by the shell through `background.js`:
  it keeps playing when the person leaves, and every other screen shows a slim bar at the foot of
  the header with what plays and a Stop button. Stop is the same as Off and is saved, so the
  Visualizer opens silent after it. The bar sits inside the header, a landmark. Breathing lowers
  the background to `sounds.background.duckLevel` under its tones (`calm.duckRoutes`); urgent help
  and a hidden app pause it, as before. The background does not start when the app opens; it
  starts when the person opens the Visualizer. — 2026-10-09 (owner; UNT-094)
- **Rain becomes Nature, which plays rain or waves.** — Owner request (RLG-043). The waves are
  looping noise under a low-pass filter; each wave swells and opens the filter, then breaks and
  falls back, at uneven gaps (6 to 11 s) and heights. Noise has no pitch, so the key rule (RLG-046)
  holds. Settings chooses rain or waves; a saved "rain" choice from before becomes Nature with
  rain. — 2026-10-09 (owner; UNT-094)
- **The ripples interfere, drawn as a grid of dots in SVG.** — Owner request (RLG-041): brighter
  where rings meet, fainter where they cancel. Each ripple is a wave packet of a few crests that
  travels out and fades; the height of the water at a point is the sum of every packet there
  (`waveHeight` in `activities/ripple.js`, tuned by `ripple.wave`). The water is a grid of small
  SVG dots, 10 px apart, whose opacity is that height over a faint rest level. A frame writes
  only dots that changed visibly, and no frame is drawn while the water is still. A test checks
  that the height is exactly the sum, that crests meeting give about twice one crest, and that a
  crest meeting a trough mostly cancels. Under reduced motion the rings still only fade, with no
  grid. — Rejected: a canvas (the architecture rule); overlapping CSS rings with a blend mode
  (they can brighten but cannot cancel). — 2026-10-09 (owner; UNT-095)
- **Unblock replaces Sort colors.** — Owner request (RLG-040): a calm puzzle that does not even
  seem to have a losing state; the owner rejected a falling-block game. Over three rounds the owner
  saw nine kinds (turn tiles, picture swap, sliding tiles; turn the rings, color field, connect the
  dots, matching pairs; picture logic, shape sudoku, flowing paths) and chose Unblock, a
  sliding-block puzzle, after asking for "something more advanced". Fifteen boards in
  `config.unblock.boards` go from easy (3 moves) to hard (26 moves); they were made by a
  breadth-first solver and a hill-climb, and a test solves every one. The puzzle shows no score,
  no move count and no timer; Undo takes back any move, even the last one. Three ways to move
  serve touch, keyboard and screen reader: a drag (one drag is one move), arrow keys on a focused
  block (each block is a tab stop), and choose then Slide buttons, which a screen reader reaches as
  plain buttons. A drag never chooses; a tap does. REQ-014 is withdrawn and REQ-035 replaces it;
  Sort colors' tests for keyboard, drag, targets and forced colors carry over in that form, and its
  light-to-dark arrow goes with it. — 2026-10-09 (owner; UNT-096)
- **Standards and research cite Vytal 2012 for Unblock and Buxton 2021 for the waves.** — RLG-044.
  Unblock is backed by a laboratory study in which a hard task, unlike an easy one, reduced induced
  anxiety (vytal2012), and by the review of video games already cited (pallavicini2021). The Tetris
  sources (holmes2009, james2015) were about intrusive memories and are no longer cited; their
  notes stay in `docs/research/sources.md`. The Visualizer adds a meta-analysis of natural sounds
  (buxton2021) and says its rain and waves are imitations. Every DOI was checked on Crossref in the
  session, and the two new abstracts were read on PubMed. — 2026-10-09 (owner request; UNT-097)
  *Superseded 2026-10-10 (owner, UNT-114): the Standards and research page is removed; the sources
  stay in `docs/research/sources.md`. See "No Standards and research page".*
- **The screen may sleep after a time with no touch, chosen in Settings.** — AUD-103: a person who
  falls asleep on Breathe or the Visualizer left the screen on for hours. The owner chose a default
  of 30 minutes and a setting of 10, 30 or 60 minutes ("Keep the screen on", `awakeMinutes`,
  `config.wakeLock`). After that time with no touch or key the wake lock is released and the
  exercise goes on; the next touch takes it back. No countdown is shown, so REQ-011 holds. Pausing
  breathing releases the lock at once. A lock granted after the screen stopped wanting it is
  released at once (AUD-081). — 2026-10-09 (owner; UNT-098)
- **Freelief asks the browser to keep its offline copy.** — AUD-080: best-effort storage can be
  evicted on a full phone, and then the app does not open offline. After the start, Freelief calls
  `navigator.storage.persist()` where the browser decides with no question (Chromium, Safari). It
  does not call it in Firefox, which asks the person, because the app opens with no question
  (REQ-018). The call never holds up the start. — 2026-10-09 (UNT-098)
- **Nothing wakes the audio while it is held silent.** — AUD-082: a breathing tone resumed the
  paused audio behind urgent help. While sound is off, help is open or the app is hidden, no sound
  is made and the audio is not resumed. A failed crisis-lines load and a failed offline install
  are now logged with their reason (AUD-084, AUD-085). — 2026-10-09 (UNT-098)
- **A verified standard holds until the interface changes.** — AUD-102: the record of a check
  ships in the version after the one checked, and the page showed only entries for the running
  version, so no check could ever show. The owner chose this rule: an entry names the version
  checked and shows in that version and later ones, until a release changes a screen, the styles,
  the text or the shell (`INTERFACE` in `tools/freelief.py`). `claim_outdated()` finds the commit
  that introduced the version and compares the interface since; the tests and `build --release`
  fail on an outdated entry, and doctor warns. REQ-029 is changed with its history. — Rejected:
  record the entry in the same commit as the checked version. — 2026-10-09 (owner; UNT-099)
  *This supersedes the AUD-023 rule that a claim holds only for the exact running version.*
  *Superseded 2026-10-10 (owner, UNT-114): there is no standards claim and no `claim_outdated()`;
  see "No Standards and research page".*
- **Settings can be reset, and a default choice is not stored.** — AUD-110: a stored value had no
  end. Reset settings puts every setting back to its default, and choosing the default value again
  removes the stored value, so it follows a later default. Settings also says whether this version
  is saved for use with no internet (AUD-112): the offline copy is written all at once, so its cache
  exists only when it is complete. — 2026-10-09 (UNT-099)
- **Doctor warns about stale crisis lines and outdated claims.** — AUD-104: freshness was checked
  only at a release. Doctor, which every Resume runs, now warns when a crisis line or the directory
  is older than `crisis.maxCheckAgeDays`, and when a verified standard is outdated. — 2026-10-09
  (UNT-099)
- **The Effigy Media name and logo are reserved.** — AUD-077: they shipped under the MIT license.
  The owner chose to reserve them: `LICENSE` and the README say the code is MIT and the name and
  logo are not licensed for reuse. — 2026-10-09 (owner; UNT-099)
- **An incident rolls back at once; a fix forward runs a scoped round.** — AUD-105: after 1.0 a wrong
  crisis number or a broken start-up had no fast path, because `live` moves only after a full round.
  The owner chose: the owner may move `live` back to the previous release tag at once, with no
  round (`git push --force origin vPREVIOUS:live`). The move is recorded the same day in the
  changelog and a fragment, with the reason. A rollback reaches installed copies: the older
  `version.js` names another cache, so its worker installs and takes over at the next open, as any
  update does. A fix forward is a release with a scoped round: only the lenses the fix touches. —
  2026-10-09 (owner; UNT-101)
- **The crisis data keeps its own names and hours.** — AUD-101: REQ-017 gained a second exception
  in UNT-077 (AUD-039) without the owner's acceptance. The owner accepted it: the crisis-line names,
  the country names and the hours stay in `data/crisis-lines.json`, beside each line's dated source.
  — 2026-10-09 (owner; UNT-101)
- **The network wording names the update and the repair.** — AUD-098: the app also downloads its
  own missing files to repair the offline copy. The owner chose to name both: the only things that
  reach the internet are the browser's check for a newer version and the download of Freelief's own
  files to update or repair it, and nothing about the person is sent. REQ-015, About and AGENTS.md
  say this. — 2026-10-09 (owner; UNT-101)
- **The Visualizer and the wake lock have their own requirements.** — AUD-109: REQ-036 (the
  Visualizer and the background sound) and REQ-037 (the screen wake lock and its idle setting),
  agreed by the owner from the earlier requests. — 2026-10-09 (owner; UNT-101)
- **The interface review is part of a slice, and its fixes follow the stress checks.** — The
  environment's `web-interface-review` skill (AUD-097) ran on every screen on 2026-10-09 and found no
  High finding. The fixes: Reset settings asks once more; a cover (black screen, full screen) makes
  the rest of the page inert; any key ends the black screen, as its label says; the help dialog's
  emergency line is a polite live region; `scroll-padding-top` keeps a focused control below the
  sticky header; every edge honours the safe-area insets; the trace loop has 3 to 1 contrast; links
  that stand alone are 44 px targets; Open on GitHub opens a new tab. What was not fixed, and why,
  is in RLG-047. — 2026-10-09 (UNT-103)
- **The background sound stops while sound is held, and a reset never starts it.** — Round UNT-104
  found that the background loops kept scheduling notes into the paused audio clock while urgent help
  was open or the app was hidden, so every queued chord played at once on return (AUD-113, High).
  `background.hold()` now stops the loops when sound is held, and `restart()` starts the chosen sound
  again on return. The round also found that Reset settings started the music and turned sound back
  on (AUD-114). Now only a choice on the Visualizer starts a sound (Off and Stop end it from
  anywhere), and a reset keeps the speaker's sound setting. — 2026-10-09 (owner chose to fix before
  0.8.0; UNT-105)
- **Every mandala shape is at least 44 px on a phone.** — The interface review found parts of
  about 37 to 40 px in the denser designs, under the stress checks' 44 px rule (RLG-047, AUD-125).
  The owner chose to thin the dense rings rather than accept 24 px. Every design now has the same
  three rings, each 28 units thick (about 46 px at a 360 px width), around a center of 16 units;
  dots and bands get their size from that thickness. Petals and diamonds were widened, and rings
  that were still too small were given fewer parts. The test now asks for 44 px in every design.
  The designs are a little simpler. — Rejected: accept 24 px (WCAG 2.5.8). — 2026-10-09 (owner;
  UNT-107)
- **The header is three centered rows, and the sound bar is three toggle buttons.** — Owner
  requests (RLG-049), chosen step by step with screenshots and mockups. A first reading, one
  centered row, was shown and rejected. The header now has the name on its own line; then the five
  round buttons: a music note, a raindrop and a wave (the sound bar), the speaker and Settings; then
  "Need urgent help?" on its own line. A tap on a sound plays it; a tap on a sound that plays stops
  it; rain and waves replace each other; music plays with either; a tap while the speaker is off
  turns sound on. The bar replaces the Visualizer's Off/Music/Nature/Both choice and the Settings
  choice of rain or waves, so `calmMode` and `natureSound` are no longer stored, and each visit
  starts silent. "Need urgent help?" stays a text button: an icon (the owner asked about "!") would
  make the one control a person in panic must find into a symbol to decode, and "!" reads as an
  error. Tab follows what is seen, so help is the sixth stop. The header is about 160 px tall on a
  phone, and `scroll-padding-top` keeps a focused control below it. — Rejected: one centered row;
  a Play/Stop bar with the last sound remembered (built, then replaced the same day); help as an
  icon; help on line 2 (recommended, not chosen). — 2026-10-09 (owner; UNT-108)
  *This supersedes the sound bar with Stop in the RLG-045 entry and the Visualizer's sound choice.*
- **Keep the screen on has an Always choice.** — Owner request (RLG-048). Beside 10, 30 and 60
  minutes, "Always, while it runs" keeps the screen on for as long as breathing or the Visualizer
  runs (stored as 0 minutes). The default stays 30 minutes, so the AUD-103 protection holds unless
  the person chooses Always; its hint says it uses more battery. — 2026-10-09 (owner; UNT-108)
- **The footer line is "You are safe right now."** — Owner request (RLG-051): "Take your time" is
  removed from the footer; the owner kept the first sentence. — 2026-10-09 (owner; UNT-109)
- **Breathing sounds like breath, and box breathing taps the seconds of a hold.** — Owner request
  (RLG-050): breath noise in place of the tone, sounding different for in and out, and light
  percussive taps for the seconds of a hold. Each in or out phase is soft looping noise that swells
  and fades over the whole phase, through a band filter that rises (in-breath, 700 to 1,500 Hz) or
  falls (out-breath, 900 to 380 Hz). A hold plays one short tap of filtered noise at each second,
  centered on C6, so it stays in the music's key (RLG-046). The calm and slower rhythms have no
  holds, so only box breathing taps. — Rejected: keep the sine tone (the owner's request). —
  2026-10-09 (owner; UNT-110)
- **Owner fixes of 2026-10-10: names and order, a fading ripple, a way back in Unblock, no click.**
  — The menu order and names are the owner's (RLG-058): Breathing, Pop Bubbles, Zen Garden (Trace
  a shape holds its place until it is built, RLG-055), Ripple Pond, Color Mandalas, Unblock and
  Kaleidoscope (the Visualizer's new name, RLG-057); each screen's title matches. A ripple now fades
  to nothing over its last `ripple.wave.endFadeSeconds` (RLG-054). Unblock has Previous board,
  which wraps from the first to the last (RLG-052). The click at the start of an in-breath came from
  stopping the out-breath while its fade-out ramp still ran: cancelScheduledValues dropped the ramp
  and the volume jumped back up. Every stop now holds the current value first (`hold()` in
  audio.js, RLG-053). The exhale's band is a whole step lower (802 to 339 Hz), as the owner asked.
  — 2026-10-10 (owner; UNT-113)
- **No Standards and research page, and no standards claim.** — The owner asked whether the page
  should stay when most of its research is limited or indirect, and chose to remove it, and with it
  the standards claim (RLG-056). `screens/standards.js`, the `#standards` route, the footer link,
  `data/research.json`, `data/standards.json` and the claim tooling (`claim_outdated`) are removed.
  REQ-020, REQ-024 and REQ-029 are withdrawn. The sources stay in `docs/research/sources.md` as the
  record, and REQ-025 (no health claim) still holds. — Rejected: a shorter page with one honest
  lead line; a standards line on About. — 2026-10-10 (owner; UNT-114) *This supersedes the entries
  on the Standards and research page, the verified-standard rule (AUD-102) and the research rewrite
  (RLG-044).*
- **Zen Garden replaces Trace a shape.** — Owner request (RLG-055); the owner chose "Place stones and
  rake" from three kinds. An SVG tray of sand: a drag rakes five parallel lines along its path; the
  arrow keys move a rake and draw as it moves; stones and plants are named buttons that a drag or
  the arrow keys move and Delete or Remove takes away; a mask hides the lines inside the rings
  around each item, so the lines flow around it. It starts with three stones and has room for six
  items. A soft sand sound, filtered noise centered on A5, plays while raking. The trace, its twelve
  shapes and the crystal-glass sound are removed; REQ-013 is withdrawn and REQ-038 replaces it. —
  Rejected: ripples that form around stones by themselves; raking only. — 2026-10-10 (owner;
  UNT-115)
- **The Visualizer is the Kaleidoscope: a slow, full-width kaleidoscope.** — Owner request
  (RLG-057): "more trippy, a full-screen geometric evolving tapestry"; the owner chose a slow
  kaleidoscope with no flashing, and the name Kaleidoscope (RLG-058). One wedge of 18 random soft
  shapes is copied 12 times around the center, every other copy mirrored; the pattern turns once in
  240 s, its colors drift through the hues in 150 s, and every 20 s a new pattern cross-fades in over
  7 s. No brightness changes faster than that fade (WCAG 2.3.1). Under reduced motion nothing turns
  or drifts; only the slow cross-fade remains. Full screen and Black screen are unchanged, and
  nothing new is drawn under the black screen. — Rejected: a tiled woven pattern; bolder, faster
  motion. — 2026-10-10 (owner; UNT-116)
- **The breath sound is softer: a gentle high cut and a lower volume.** — Owner request (RLG-059).
  A low-pass filter at `sounds.breath.lowpassHz` (2200 Hz) follows the whole breath sound, and the
  breath's volume goes from 0.09 to 0.07 and the hold tap's from 0.06 to 0.05. — 2026-10-10 (owner;
  UNT-119)
- **Every move of the preview is tagged, and a rollback keeps newer settings.** — AUD-121: the
  Incident rule named "the previous release tag", but the repository had no tag, and an older
  version's save dropped the settings it could not read. Each move of `live` now tags its commit
  `preview-X.Y.Z`; the twelve earlier moves were tagged from the remote's log. `settings.js` keeps
  stored values it cannot read and writes them back, and a new choice of that setting replaces
  them. The stale local `live` branch (at v0.5.0) is deleted. — Rejected: naming the target only in
  the changelog (a hurried owner needs one command). — 2026-10-10 (UNT-121)
- **Update now replaces a current copy only when the new one is whole.** — AUD-133: with no new
  version, Update now deleted every Freelief cache and unregistered the worker, and then the browser
  had to download the copy again; one failed file left no offline copy and no message. The worker
  now fetches every file into a temporary cache and copies it over only when all arrived; otherwise
  the copy stays and Settings says so. — 2026-10-10 (UNT-127) *This amends the entry on Update now
  of 2026-10-08 (AUD-056).*
- **A page keeps its own version's screens through any takeover.** — AUD-057, re-opened by round
  UNT-124: a takeover that lands after the first touch, in the moment between the page's offer and
  the worker's activation, left a page in use under the new worker, which had deleted the page's
  cache. A page cannot withdraw a takeover that has begun, so the page now asks for each lazy screen
  with its own version (`?v=`), the worker answers from that version's cache, and activation keeps
  the highest other version's cache until the next update. — Rejected: a 'stay' message from the
  page (it cannot stop an activation already under way); a reload after the touch (it interrupts the
  person). — 2026-10-10 (UNT-126)
- **The interface review's low items are fixed or accepted.** — RLG-047. Fixed: a screen title per
  screen (`app.screenTitle`); the `theme-color` meta follows a forced theme; the checked date reads
  as words in the page's language; Pause and the bubbles' drift control change their label and no
  longer carry `aria-pressed`, so a screen reader never says "Resume, pressed"; bubbles sit in the
  page in slot order, and their focus ring is drawn inside; the Feedback checklist names the
  current screens; two strings use curly quotes. Accepted, with the reason: Unblock's blocks still
  move with `left` and `top`, because the board's cell is a percentage of the board, which
  `translate` cannot use (a 0.12 s slide of a few blocks); the sound bar's toggle buttons announce
  their state through `aria-pressed`, so it needs no live region; the black cover shows no focus
  ring by design. No longer apply: the trace slider and the old Visualizer animations (removed).
  — 2026-10-10 (UNT-123)
- **A new version takes over only from Freelief's only window, and a worker stores only its own
  version's files.** — AUD-057 (re-opened by round UNT-082): a fresh second window let a new version
  take over under a window in use, which then loaded the new version's screens. The worker now
  skips waiting only when the page that asks is the only window; otherwise the new version waits
  until every window is closed, and Update now asks the person to close the other window. AUD-120:
  a cache miss or a repair could store a newer deploy's files under the running version's cache;
  the worker now stores a network file only while the network serves its own version. — Rejected:
  serving each window from the cache of the version it loaded (it needs a record of each window
  that outlives the worker). — 2026-10-10 (UNT-122)
- **The worker's update check skips the HTTP cache, and the tests now face real caching.** — The
  test server always sent `no-store`, so no test met GitHub Pages' `max-age=600` (AUD-013). A new
  test serves the app that way, and it found that the update check took `version.js` from the HTTP
  cache, so a new version could take up to ten minutes to reach a device. The worker is now
  registered with `updateViaCache: "none"`, and the test checks that the new version takes over
  and its changed files run offline (AUD-009). Every screen is now checked offline and for outside
  requests (AUD-027); the exact Content Security Policy and every address in shipped code are
  checked (AUD-031); a stored inherited name is checked to be ignored (AUD-030). —
  2026-10-08 (UNT-073)
- **`build --release` checks what a release needs.** — The audit found that build counted untracked
  files though Pages deploys a commit (AUD-011), that nothing checked for a version bump after a
  shipped change, so an installed app could keep an old file (AUD-010), and that nothing checked the
  crisis dates (AUD-024). `build` now counts tracked files only and warns about uncommitted shipped
  files; `build --release` fails on them, on a shipped file changed after the last version bump,
  and on a crisis line or the directory checked more than `crisis.maxCheckAgeDays` (90) days ago.
  A repo test also fails on a shipped change committed without a bump. The AGENTS.md Release row
  names `build --release`. — 2026-10-08 (UNT-074)
- **A recorded standard is shown only for the version that was checked, and the way a check
  becomes a record is written down.** — The audit found that a recorded standard had no version,
  so a claim would outlive the version it was checked on (AUD-023), and that no procedure turned a
  volunteer's check into a record (AUD-054). Each entry in `data/standards.json` now carries
  `version` and `issue`, the page shows an entry only while its version is the running one, and the
  trust pages reference states the four steps from an axe pass and a manual check to an entry. —
  2026-10-08 (UNT-076) *Superseded in part 2026-10-09 (owner, AUD-102; UNT-099): an entry now shows
  in its version and later ones until the interface changes; see that entry.* *Superseded
  2026-10-10 (owner, UNT-114): `data/standards.json` is removed; see "No Standards and research
  page".*
- **The shared origin is a known trust dependency, and the design says what the CSP protects.** —
  The audit (AUD-004) showed that a page on a sibling site of `effigymedia.github.io` can write
  Freelief's Cache Storage and `localStorage`, and that the design claimed a CSP that "allows only
  the app's own origin". The owner chose on 2026-10-07 to stay on the shared origin (the entry
  "Freelief stays on the shared origin" below). Section 9 now records the dependency and says that
  the CSP limits what Freelief's page loads and connects to, and does not stop a sibling site from
  writing its storage. — Rejected for now: a custom domain or a dedicated account (the owner's
  2026-10-07 choice). — 2026-10-08 (AUD-004)
- **All CSS is in one linked file, `styles.css`; no CSS is inline.** — Stage 8 first planned to
  inline the critical CSS for the 1 s launch. The CSP is `style-src 'self'` with no
  `'unsafe-inline'`, so an inline style would be refused, and `index.html` has always linked
  `styles.css`. The launch target is met by loading only the shell, the menu and urgent help at
  start (RLG-006; the menu replaced breathing as the first screen, AUD-091). This reverses the Stage 8 plan. — Rejected: `'unsafe-inline'` or a hash in the
  CSP for an inline block (a weaker policy for a small gain). — 2026-10-08 (AUD-041)
- **The control against a tampered crisis line is the real one: a single committer, a checked
  source, and a test that pins each number.** — The audit (AUD-007) found that the design claimed
  "every change goes through a reviewed commit", but `main` has no protection and no review. The
  owner is the only committer; AGENTS.md lets a crisis line change only with a source checked in
  the same session; and `test_every_crisis_number_is_pinned` in `tools/tests/test_repo.py` fails
  when a number changes without its record. Section 9 now says this. A branch ruleset that needs a
  pull request is not set. — 2026-10-08 (AUD-007)
- **The privacy text names the update check.** — The audit (AUD-025) found that "sends nothing over
  the internet after it is installed" omits the browser's check for a new version: when an online
  person opens the app, the browser asks GitHub Pages for `sw.js` and `version.js`. That request
  carries nothing about the person, but GitHub can see the address and the time. The owner chose the
  wording: "Freelief sends nothing about you. The only thing that reaches the internet is your
  browser's check for a newer version of Freelief, from GitHub Pages." REQ-015 is changed with its
  history. — 2026-10-08 (owner; AUD-025)
- **The worker answers only from its own version's cache; a new version that takes over before the
  person touches anything reloads the page once; Settings shows the version and an `Update now` button
  that drops Freelief's offline copy and reloads from the internet.** — The owner could not load v0.5.10:
  `caches.match()` searched every cache, so an old version's cache served old files. Reloading only
  before the first touch never interrupts an exercise. `Update now` deletes only `freelief-` caches,
  because the origin is shared. — 2026-10-07 (owner reported; implementer fixed) *Amended
  2026-10-08 (AUD-056, UNT-056): Update now removes nothing until the network is shown to work; see
  that entry. Superseded in part (AUD-057): a new version waits until it is safe to take over.*
- **Freelief opens on the menu ("What would help right now?"), with Breathe first. Every screen has one
  `Back to menu` control. Settings is a gear, always at the top right, and leaves the menu list. The
  brand name stays plain text, so `Need urgent help?` remains the first stop for the Tab key.** — The
  owner, testing on the phone, asked for the menu as home and a way back to it from every method, and
  for Settings as a gear. REQ-018 and REQ-026 are changed with their history. — Rejected: breathing at
  launch (the first decision). — 2026-10-07 (owner)
- **All sounds are soft: low notes, slow swells with no click, long fades, low volume. The bubble pop
  is a short burst of filtered noise over a falling thump, not a tone. Calm offers Music (pads) or Rain
  (filtered noise with soft drops), remembered on the device.** — The owner found the grounding chime
  abrasive and asked for every sound to be soft and pleasant, a percussive pop, and an atonal rain mode.
  — 2026-10-07 (owner) *Amended: Calm became the Visualizer with a Both mode (UNT-034), and on
  2026-10-09 Rain became Nature with rain or waves, and Off was added (RLG-043, RLG-045).*
- **Only breathing, the shell and urgent help load at start; every other screen loads on its first
  visit. `fallback.js` hides the static fallback while the app starts and shows it if the start fails or
  takes over 2 s.** — The launch had doubled (RLG-006); profiling showed the painted fallback was the
  main cost. The 2 s wait is a constant in `fallback.js`, not in `config.json`, because that script must
  work when `config.json` fails. — 2026-10-07 (implementer, for RLG-006) *Superseded in part
  2026-10-07 (owner): the menu replaced breathing as the first screen, so the shell, the menu and
  urgent help load at start; see "Freelief opens on the menu".*
- **A Calm screen plays slow musical pads (four gentle chords of detuned triangle waves through a
  low-pass filter) while simple geometric shapes fade in and out. A `Black screen` button covers
  everything in black; one tap or key brings the screen back, and the music keeps playing. Under reduced
  motion the shapes only fade.** — The owner asked for a zen sound mode with musical pads, shapes that
  come and go like a screen saver, and a black screen. The black screen is one large button, so touch,
  keyboard and screen readers can all leave it. — 2026-10-07 (owner) *Superseded 2026-10-10
  (AUD-093, UNT-118): Calm became the Visualizer with a Both mode (UNT-035), its sound became the
  background sound and the three-button sound bar (2026-10-09), and its shapes became the
  Kaleidoscope (2026-10-10, UNT-116). The black screen holds. See those entries.*
- **The shape trace offers twelve shapes (figure eight, circle, ripple, flower, star, heart, petal,
  trefoil knot, weave, soft square, egg, clover), one at a time, with a `New shape` control; each shape
  sings on its own note of a C major pentatonic scale.** — The owner asked for many more shapes. The
  shapes are drawn from formulas, so no asset ships. — 2026-10-07 (owner) *Superseded 2026-10-10
  (owner, UNT-115): Zen Garden replaced the shape trace; see "Zen Garden replaces Trace a shape".*
- **Sounds are on by default, with one Sounds switch in Settings. A soft tone lasts each breathing
  phase; the activities have short cues; the shape trace sounds like a singing crystal glass while the
  person moves. Nothing plays before the first tap or key press. No spoken voice.** *(Amended
  2026-10-09 (owner, RLG-050): the breathing tone became a breath sound; see that entry.)* — The owner asked
  for more, subtle sounds, on by default (REQ-007 changed). Browsers block sound before a gesture,
  and creating audio early would log a warning, so the first gesture unlocks it. — Rejected: tones off
  by default (the first decision). — 2026-10-07 (owner) *Amended 2026-10-08 (owner, UNT-053): the
  Sounds switch moved from Settings to the speaker button in the header; sounds stay on by default.*
- **Urgent help has its way out at the top: a `Back` button in a header that stays visible while the
  content scrolls, and the phone's back gesture closes the window without leaving the app. Every
  exercise and activity shows both `More ways to calm` and `Back to breathing`.** — The owner, testing
  on a phone, could not find the Close button at the bottom of the window and asked for a way to
  other methods from every method. — 2026-10-07 (owner) *Superseded the same day (owner, the menu
  decision and UNT-030): `More ways to calm` and `Back to breathing` are gone; every screen except the
  menu has one `Back to menu` control at the top. The `Back` button in urgent help still stands.*
- **GitHub Pages serves a `live` branch, not `main`. Before 1.0, `live` is a public preview that
  moves only with the owner's yes; from 1.0 on, it moves only at a release that cleared the audit
  gate, to a tag. The README calls the app a preview and does not invite installs before 1.0.** —
  A push to `main` was a public deploy, so the release gate never applied to what users got
  (AUD-003). `live` was created at 75e923f, the v0.5.0 already deployed; that build is a preview,
  not a release, so it has no release tag. — Rejected: gating every push to `main`. — 2026-10-07
  (owner)
- **Start-up fails soft. `index.html` holds a static fallback (a breathing line, the emergency
  instruction, the directory link, the self-help line) that shows with JavaScript off or when the app
  cannot start; the app replaces it once it can draw everything. A failed crisis-lines file is not
  fatal: the help dialog keeps the emergency line and the directory from `config.json`.** — Design
  section 8 says any failure leaves the guide and the crisis route usable (AUD-002). The fallback text
  is the first of two exceptions to REQ-017; the second is the crisis data (AUD-039, accepted by the
  owner 2026-10-09). — 2026-10-07 (implementer, for AUD-002; the owner accepted the REQ-017
  exception the same day)
- **Freelief stays on the shared origin `effigymedia.github.io` and repairs its own offline cache.**
  — Other apps on that origin may delete its cache (AUD-001). On each online launch the page asks the
  worker to fetch any missing file, and Freelief deletes only its own `freelief-` caches. — Rejected:
  a free GitHub organization or a custom domain for an origin of its own. Accepted risk: a cache
  deleted while the person is offline cannot be repaired until they are online. — 2026-10-07 (owner)
- **The public repository `EffigyMedia/freelief` exists and GitHub Pages serves `main` *(changed the same day: it serves `live`, see above)* at
  https://effigymedia.github.io/freelief/.** — Created after all five slices were built, with the
  owner's yes, so the app can be checked on a phone over HTTPS. A push is now a deploy. — 2026-10-07
  (owner)
- **The trust pages are screens in the router, reached from three footer links on every screen:
  About and disclaimer, Standards and research, Feedback.** — One router and one contract for
  everything; the pages work offline like the rest. — Rejected: separate HTML files under
  `pages/`, which would need their own shell and cache entries. — 2026-10-07 (slice 4,
  implementer) *Amended 2026-10-10 (owner, UNT-114): the Standards and research link and page are
  removed; the footer links to About and Feedback.*
- **With no verified standard, the Standards page says what Freelief is built to and that no
  standard is claimed yet.** — REQ-029 forbids a claim before a manual check; the owner still wants
  the standards work visible. Verified standards come from `data/standards.json`, which stays empty
  until a volunteer check is recorded. — 2026-10-07 (slice 4, implementer) *Superseded 2026-10-10
  (owner, UNT-114): there is no Standards page; see "No Standards and research page".*
- **The claim-wording test exempts exactly one string (the disclaimer's "does not diagnose or
  treat") and the research citations file, and a second test fails if an exempt string stops
  denying.** — The disclaimer must name what Freelief does not do, and paper titles are quoted as
  published. — Rejected: a looser pattern for the whole app. — 2026-10-07 (slice 4, implementer)
- **Feedback carries only the app version, the browser and the device type, in text the person
  edits; switching the kind of message never erases words the person typed.** — 2026-10-07
  (slice 4, implementer)
- **Bubbles sit one to a slot in a 3 x 3 grid, never at a free random place.** — Random places let
  one bubble cover another's touch target, which the axe target-size check caught at random. —
  Rejected: random placement with an overlap test (more code, same result). — 2026-10-07 (slice 3,
  implementer)
- **Bubble drift has a "Stop the drifting" control, and under reduced motion the bubbles do not
  move at all.** — WCAG 2.2.2 asks that movement lasting over five seconds can be paused. —
  2026-10-07 (slice 3, implementer)
- **The shape trace is a figure eight, and its marker is a `role="slider"` with a percent value.**
  — A slider is the pattern a screen reader already knows for "a position along a track", and the
  arrow keys move it. A pointer is matched to the shape only near the marker, so the crossing in
  the middle cannot make it jump. — 2026-10-07 (slice 3, implementer) *Superseded in part:
  the figure eight became one of twelve shapes, chosen in turn; see the shape-trace entries below.*
  *Superseded 2026-10-10 (owner, UNT-115): Zen Garden replaced the shape trace.*
- **Distraction is offered for the moment, never as a way to overcome panic.** — Research on safety
  behaviours (Helbig-Lang & Petermann 2010) says escape behaviours, which can include distraction,
  may keep an anxiety disorder going. Freelief's activity text says "there is nothing to win" and
  makes no claim. The Standards & research page (slice 4) must say that frequent attacks call for
  treatment. — 2026-10-07 (slice 3, implementer; a design concern for the owner to read) *Amended
  2026-10-10 (UNT-118): the Standards page is removed (UNT-114); About says it
  (`about.selfHelp2`).*
- **Screens are addressed by URL hash, and the menu and Settings live in `screens/`.** — The
  browser Back button works with no extra code, and the exercises stay free of storage: the
  Settings screen is not an exercise, and it writes only through `settings.js`. — Rejected: a
  router with no URL (Back would leave the app); Settings inside an exercise module. —
  2026-10-07 (slice 2, implementer)
- **Grounding and calming words keep focus on the control the person used; the new text is a
  polite live region.** — Moving focus to the text on every step would send a keyboard user back
  to the start of the page each time. — 2026-10-07 (slice 2, implementer) *Both screens were
  removed 2026-10-07 (UNT-032).*
- **The slower rhythm is 5 in, 7 out; box breathing is 4-4-4-4.** — Both stay under 10 breaths a
  minute (Zaccaro 2018); box breathing was one arm of Balban 2023. — 2026-10-07 (slice 2,
  implementer)
- **The breathing guide counts the seconds of each phase and shows the count; a screen reader
  hears only the phase name.** — The count carries the rhythm under reduced motion, and announcing
  every second would be noise. — 2026-10-07 (slice 1, implementer)
- **Activities use DOM elements, not a canvas.** — A screen reader and the keyboard must reach every
  item. — Rejected: a canvas. — 2026-10-07 (proposed by the implementer in Stage 8; confirmed at
  sign-off)

---

## 13. Implementation Readiness Checklist

- [x] The one-line pitch, success criteria, and Non-Goals exist and agree with each other.
- [x] Every flow in Stage 5 has its edge cases and failure states specified.
- [x] Every agreed obligation is a requirement record (`REQ-001` to `REQ-031` at sign-off).
- [x] Every requirement carries a category, a verification method and a priority.
- [x] Every marked region is filled.
- [x] Both generated documents have been produced and read: `docs/SRS.md` and `docs/PRD.md`,
      31 of 31 requirements, no clause *Not supplied*. *(This checklist is the sign-off snapshot of
      2026-10-07. The records now run to REQ-037; the generators report the current count.)*
- [x] Every technology appears in Stage 7 with rationale.
- [x] The never-commit list exists.
- [x] Module boundaries exist and no two modules own the same concern.
- [x] Every performance target has a metric, a threshold, and a workload.
- [x] The walking skeleton is defined tightly enough to build without further questions.
- [x] Every open question is resolved or parked in Stage 11.
- [x] No section is skipped.
- [x] The owner has read the Non-Goals and Decision Log and agrees they are right (2026-10-07).

---

## 14. Glossary

<!-- BEGIN srs-acronyms - written by the interview, read by the generators -->
- **ASA** — Advertising Standards Authority (UK).
- **CBT** — cognitive behavioural therapy.
- **CSP** — Content Security Policy.
- **DBT** — dialectical behaviour therapy.
- **FDA** — Food and Drug Administration (US).
- **FTC** — Federal Trade Commission (US).
- **MHRA** — Medicines and Healthcare products Regulatory Agency (UK).
- **ORCHA** — Organisation for the Review of Care and Health Apps.
- **PWA** — progressive web app.
- **WCAG** — Web Content Accessibility Guidelines.
<!-- END srs-acronyms -->

---

## 15. Change Log

- **v0.1 — 2026-10-07** — Interview started; decisions recorded as they were made.
- **v0.2 — 2026-10-07** — Interview complete. Interview guidance removed; every stage filled;
  `PREMISE.md` superseded. Waiting for the owner's sign-off.
- **v1.0 — 2026-10-07** — The owner signed off. All 31 requirements moved to `agreed`; the SRS and
  PRD generated; the first crisis-line regions decided.
- **v1.1 — 2026-10-07** — Slices 1 to 5 built (app v0.1.0 to v0.5.0), and slice 6 started (app
  v0.5.1 to v0.5.32) with the owner's changes from the phone: the menu became the first screen;
  grounding and calming words were removed; drag was added to the colour sort; the ripple pond,
  mandala coloring, the Visualizer, vibration, the country list and the saved region were added;
  GitHub Pages moved to the `live` branch; the shared origin was accepted with self-repair of the
  cache.
- **v1.2 — 2026-10-08** — Slice 6 finished (app v0.5.33 to v0.6.0): the header sound button, the
  emergency Call buttons, the wake lock, sources for every activity, the "When Freelief opens"
  setting, the quiet footer and the rhythm line. Slice 7 (from app v0.6.4, at v0.6.12 on this date):
  fixes from the audit backlog, among them the feedback Copy button, safe updates, `build
  --release`, versioned standards entries, and corrections to sections 7, 8 and 9 (the deploy
  model, the CSS plan, the shared-origin trust dependency, the crisis-line control and the update
  check in the privacy text).
- **v1.3 — 2026-10-09** — Slice 8 (app v0.7.4 to v0.8.0): Unblock replaced Sort colors (REQ-014
  withdrawn, REQ-035); the ripples interfere; eight mandala designs; the background sound, music and
  nature (rain or waves), plays on every screen until it is turned off; every sound is in C major;
  Settings gained Reset and Keep the screen on; REQ-036 (the Visualizer and the background sound)
  and REQ-037 (the wake lock) were added; the fixes of round UNT-082 and the interface review; and
  slice 9 was planned. *(Entry added 2026-10-10, AUD-045 and AUD-126: version 1.3 had no entry.)*
- **v1.4 — 2026-10-10** — Slice 9 so far (app v0.8.1 to v0.8.8): the mandala's 44 px parts; the
  three-row header and the three-button sound bar; breathing that sounds like breath; the owner's
  menu order and names; the Standards and research page and the standards claim removed (REQ-020,
  REQ-024 and REQ-029 withdrawn); Zen Garden replaced Trace a shape (REQ-013 withdrawn, REQ-038);
  the Visualizer redrawn as the Kaleidoscope. Then the documentation findings (AUD-045, AUD-093,
  AUD-124, AUD-126, AUD-128): superseded Decision Log entries annotated, section 5 no longer names a
  range, the risk table updated, the size plan added to section 9, and the clauses that still named
  the Standards page corrected.
