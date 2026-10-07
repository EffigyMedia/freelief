# Freelief — Design Document

The founding design for Freelief. It records what to build and why. The requirements are records
in `docs/fragments/` (`REQ-NNN`). This document does not restate them. It holds the structure, the
narrative and the decisions. Code, records and this document must never disagree.

---

## 0. Document Control

- **Version:** 1.0, 2026-10-07.
- **Owner:** EffigyMedia.
- **Status:** signed off by the owner 2026-10-07; ready for Initialize.
- **One-line pitch:** Freelief is a free, open-source, offline web app that helps anyone through a
  panic attack or acute anxiety in the moment, with breathing, grounding, calming words and gentle
  distraction.
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
- The published research for each technique. The list lives on the Standards & research page and
  in `docs/research/` (written in slice 2), one source or more per technique (REQ-024).
<!-- END srs-references -->

---

## 1. Vision & Purpose

A panic attack is sudden and frightening. The person has a racing heart, short breath and the
feeling that something terrible will happen. It passes, usually within minutes, but in that moment
the person has little attention, shaky hands, and often no one to help. The self-help techniques
that work — slow breathing, grounding, calm words, gentle distraction — are simple, but they are
hard to remember and do alone while panic takes over.

The apps that offer these techniques often ask for an account, show a menu, need a network, play an
advertisement or a subscription offer, or collect data about the person's worst moments. Many do
not work with a screen reader or a keyboard.

Freelief opens straight into a breathing guide, works with no network, asks nothing of the person,
collects nothing, and works for everyone. Success, a year after release, is a tool that people
recommend to each other in a crisis because it simply works and is free.

<!-- BEGIN srs-purpose - written by the interview, read by the generators -->
Freelief helps a person through a panic attack or acute anxiety at the moment it happens. It gives
self-help techniques studied in clinical research — paced breathing, 5-4-3-2-1 grounding, calming
statements and gentle distraction activities — and a fast route to a crisis line for a person who
may be in danger. It is for anyone, at no cost, with no account, no network and no data collection.
<!-- END srs-purpose -->

<!-- BEGIN prd-problem - written by the interview, read by the generators -->
During a panic attack a person cannot easily recall or perform the techniques that would calm them.
The tools that exist put obstacles in the way at the worst moment: a sign-up, a menu, a loading
screen, a network that is not there, an advertisement, or a screen that a screen reader or a
keyboard cannot use. Many also record the person's crises as data. A person in distress needs help
that starts at once, works for them as they are, and asks for nothing.
<!-- END prd-problem -->

<!-- BEGIN srs-product-overview - written by the interview, read by the generators -->
Freelief is a progressive web app: plain HTML, CSS and JavaScript served from GitHub Pages. It
installs to the home screen of a phone or a desktop and then works fully offline. When it opens,
a paced breathing guide starts at once. From there, one tap or key press reaches the other
exercises (grounding and calming statements) and the distraction activities (a bubble field, a
shape trace and a colour sort). Every screen has a "Need urgent help?" control that shows crisis
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
- From a cold launch, the breathing guide is visible within 1 second on a mid-range phone,
  installed and offline, with zero taps (REQ-018, REQ-026).
- After install, an automated test with the network disabled shows every screen working, and a
  network log shows no request to any origin (REQ-008, REQ-015).
- The automated accessibility check reports zero WCAG 2.2 A and AA violations on every page, on
  every release.
- At least one dated manual check with a screen reader and one with a keyboard alone, by a
  volunteer, is recorded for the version on the Standards & research page before it shows WCAG
  2.2 AA as met (REQ-029).
- Every crisis line in the app has a last-checked date no older than the release that ships it.
- The whole app is under 150 KB (REQ-028).
- No text in the app says Freelief is clinically proven, treats, cures or diagnoses (REQ-025).
<!-- END prd-success -->

**Quality bar for v1.0:** every "must" requirement is met and tested; every "should" is met or is
absent from the release; the release criteria in Stage 10 hold.

---

## 3. Scope, Principles & Constraints

**Principles (tie-breakers, in order):**
1. **Help first.** Nothing stands between the person and help: no question, menu, notice or wait.
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
breathing, 5-4-3-2-1 grounding, calming statements, three distraction activities, crisis lines by
region, a self-help disclaimer, a Standards & research page, and a feedback page that hands a
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
| **Exercise** | A guided self-help technique: paced breathing, 5-4-3-2-1 grounding, or calming statements. |
| **Activity** | A distraction activity: the bubble field, the shape trace, or the colour sort. No score, no failure, no timer. |
| **Breath guide** | The visual of the paced breathing exercise. It grows on the in-breath and shrinks on the out-breath. |
| **Rhythm** | A breathing preset: the length in seconds of each phase (in, hold, out, hold). |
| **Calming statement** | One short, steady line of text, shown one at a time. |
| **Crisis line** | A phone, text or web service for a person in danger. It has a region, a name, how to reach it, and a last-checked date. |
| **Region** | The country taken from the device language and region setting. Never from location. |
| **Settings** | The only stored data: the chosen rhythm, tones on or off, and the light or dark choice if overridden. On the device only. |
| **Standard** | An external standard Freelief claims to meet, such as WCAG 2.2 AA. It has a level, a check date, and the tester of the manual check. |
| **Source** | A published research citation behind a technique. |

Relations: each Exercise and Activity cites one or more Sources. A Region has zero or more Crisis
lines; a Region with none falls back to the international directory. Settings persist across
restarts on the device (REQ-023, REQ-015).

<!-- BEGIN srs-definitions - written by the interview, read by the generators -->
- **Exercise** — a guided self-help technique: paced breathing, 5-4-3-2-1 grounding, or calming
  statements.
- **Activity** — a distraction activity with no score, no failure and no timer: the bubble field,
  the shape trace, or the colour sort.
- **Breath guide** — the visual that grows on the in-breath and shrinks on the out-breath.
- **Rhythm** — a breathing preset, given as the seconds of each phase.
- **Crisis line** — a service for a person in danger, with a region, a way to reach it, and a
  last-checked date.
- **Region** — the country taken from the device language and region setting, never from location.
- **Settings** — the only data Freelief stores: rhythm, tones, and theme, on the device only.
- **Standard** — an external standard Freelief claims, with its level, check date and tester.
- **Source** — a published research citation behind a technique.
<!-- END srs-definitions -->

---

## 5. Functional Specification

The requirements are the records `REQ-001` to `REQ-031`. Their priority is the feature list. The
flows below are the structure.

**F1 — Launch to breathing.** Trigger: the person opens Freelief. Steps: the shell paints; the
breath guide starts with the saved rhythm (or the default) and one calm line. Outcome: the person
breathes with the guide. States: *first visit online* — the service worker installs and caches the
app in the background, and the guide does not wait for it; *offline, installed* — served from
cache; *offline, never visited* — the browser cannot load it, which is outside the app's control;
*reduced motion* — the guide shows a still shape with a text count instead of growth; *storage
blocked* — the default rhythm is used and nothing fails.

**F2 — Change exercise or activity.** Trigger: the person taps or presses "More ways to calm".
Steps: a short list of large items; the person chooses one; it starts. Outcome: the new exercise
runs. Leaving any exercise returns to the breath guide. No exercise has an end state that asks for
anything.

**F3 — Grounding.** Steps: five prompts in order (5 things you see, 4 you can touch, 3 you hear,
2 you smell, 1 you taste). The person advances with a large "Next" control or a key. No input is
typed or stored. Outcome: a closing calm line and a return to breathing. Edge: the person can go
back or stop at any step.

**F4 — Calming statements.** Steps: one statement at a time; the person advances when ready. The
statements come from the strings file. Outcome: the person stops when they choose.

**F5 — Distraction activities.** *Bubble field:* bubbles drift slowly; a tap or a key press pops the
focused bubble with a soft visual (and a soft tone if tones are on). *Shape trace:* a looping shape;
the person follows it with a finger or moves along it with the arrow keys. *Colour sort:* calm
colour tiles to order by drag, or by keyboard (select, then move). States for all: no score, no
failure, no timer; reduced motion slows or stops the drift; a screen reader announces each item
and its action.

**F6 — Need urgent help.** Trigger: the "Need urgent help?" control, present on every screen.
Steps: the app reads the device language and region; it shows a line to call the region's
emergency number if in immediate danger; then the crisis lines for that region, each with a
tap-to-call or tap-to-text link and its last-checked date; then the link to the international
directory; then a closed "Lines in other countries" list with every other curated region.
States: *uncurated region* — the "call your local emergency number" line, the international
directory and the other-countries list; *offline* — the curated lines still show; the directory
link says it needs a network. *(Changed at slice 1, 2026-10-07: the emergency line moved first, and
the other-countries list was added. See the Decision Log.)*

**F7 — Settings.** Rhythm preset, tones on or off, theme override. Saved on the device at once.
Storage that fails is ignored and the defaults stand.

**F8 — Disclaimer, Standards & research.** The footer links to the disclaimer page and to the
Standards & research page. The Standards & research page shows each verified standard with its
level, check date and tester, the sources for each technique, and a link to the feedback page.

**F9 — Feedback.** Trigger: the feedback page. Steps: the person chooses "Accessibility check" or
"Report a problem"; the page shows the pre-filled text (app version, browser, device type, and a
checklist for an accessibility check); the person edits it; they choose "Open on GitHub" (a new
issue URL with the template, title and body in its query) or "Send by email" (a `mailto:` link with
subject and body). Outcome: the person's own browser or mail app takes over; the app sends nothing.
Edge: until the public email address is decided, the email button is hidden.

**Integrations.** None at run time. The only outbound links are ones the person chooses: phone,
text, the crisis directory, GitHub and email. If GitHub is down, the issue page does not load and
the email route remains.

**Permissions and auth.** N/A — no accounts and no roles. Anyone may use every part of the app.

---

## 6. Experience & Interface

**Interaction principles.** Help first: the breath guide is the first and default screen. One clear
action per screen. Large targets (at least 44 by 44 CSS pixels, larger for the main actions). No
timer, no score, no failure, no surprise sound, no sudden motion. Every control works by touch, by
keyboard and by screen reader, with a visible focus ring. The "Need urgent help?" control is always
in the same place.

**Visual direction.** Soft and dim. A deep night-blue or slate background with one soft accent and
large rounded type. Dark by default, and it follows the device light or dark setting, with an
override in Settings. AAA contrast for text. No images in v1: shapes are drawn with CSS or SVG.
The implementer shows the owner variants before the look is fixed.

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
| 1 | Platform | A progressive web app, phone first, that works on desktop with a keyboard. | Reaches every device with no store, installs to the home screen, works offline. | Native apps (cost, review, two codebases). |
| 2 | Language and runtime | HTML, CSS and modern JavaScript (ES modules) in the browser. | Runs everywhere with nothing to install or build. | TypeScript (needs a build step). |
| 3 | Frameworks and libraries | None. No third-party code ships. | Smallest download, fastest load, nothing to break or update. | Preact or any framework (a dependency and a build step). |
| 4 | Persistence | `localStorage` for Settings only, behind one module, with every access in try/catch. | Settings are small and on-device; nothing else is stored. | IndexedDB (more than needed). |
| 5 | External services | None at run time. | No network after install, no data sent. | Analytics, a feedback relay. |
| 6 | Content and assets | Text in `strings/en.json`, owner-approved. Crisis lines in `data/crisis-lines.json`, curated and dated. Research sources in `docs/research/`. Tones generated with Web Audio at run time, so no audio files. The system font stack, so no font files. | Small, licence-free, offline. | Recorded audio; web fonts; image assets. |
| 7 | Deployment | GitHub Pages serves `main` of the public repository `EffigyMedia/freelief`. A push deploys. Rollback is a revert commit. The service worker cache name carries the app version. | Free for a public repository; HTTPS, which a service worker needs. | Netlify or another host (no need). |
| 8 | Testing toolchain | Python 3 and Playwright, from a project-local `.venv`, as in Effigy Arcade. axe-core, from the `axe-playwright-python` package in the same venv, runs the automated accessibility check; nothing from it ships. | Real-browser tests, including offline and network-log checks. The Shared Knowledge Base already holds Playwright gotchas. | Node test runners (another toolchain); manual testing only. |
| 9 | Dev environment and commands | `setup`: create `.venv` and install Playwright. `run`: `python -m http.server 8000`. `test`: the Playwright harnesses. `doctor`: check Python, the venv, Playwright, the manifest, the service worker and the JSON files. `build`: none — the repository is the distributable; `build` reports that and checks the size limit. `clean`: remove `output/`. `bench`: the launch-time and size benchmark. | Matches the environment's standard commands with the fewest tools. | A bundler. |
| 10 | Version control | Git. Feature commits stay local; push at a release or for an owner device test. The remote is public. | Pages needs a public repository on a free plan; the project is open source. | A private repository. |
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
| `exercises/breathe.js`, `ground.js`, `statements.js` | One exercise each. | Read storage or the network; hold text. |
| `activities/bubbles.js`, `trace.js`, `sort.js` | One activity each. | Keep a score, a timer or a failure state; read storage. |
| `settings.js` | **The single source of truth for Settings.** The only module that touches `localStorage`. | Hold defaults (those are in `config.json`). |
| `strings.js` + `strings/en.json` | **The single source of all user-facing text.** | Contain logic. |
| `crisis.js` + `data/crisis-lines.json` | The choice of crisis lines from the device region. | Ask for location. |
| `audio.js` | The soft tones with Web Audio. | Play anything when tones are off. |
| `motion.js` | Reduced-motion detection; every animation asks it. | — |
| `config.json` | **Every tunable**, with its committed default. | — |
| `sw.js` | The offline cache, versioned by the app version. | Fetch from any other origin. |
| `manifest.webmanifest` | Installation: name, icons, colours. | — |
| `screens/menu.js`, `screens/settings.js` | The "More ways to calm" list, and the Settings screen. The Settings screen changes Settings only through `settings.js`. | Touch `localStorage` directly. |
| `pages/` | The disclaimer, Standards & research, and feedback pages. | Send data. |

**Routing (added at slice 2).** Each screen has a URL hash (`#breathe`, `#menu`, `#ground`,
`#statements`, `#settings`); no hash means `#breathe`. The browser Back button therefore works, and
an unknown hash falls back to breathing. On a change of screen the shell focuses the new screen's
heading, so a screen reader announces where the person is.

**Data and state.** Settings in `localStorage` under one versioned key. Everything else is static
files cached by the service worker. Nothing is created, changed or deleted by the person except
their Settings.

**Contracts.** Each exercise and activity exports `start(container, ctx)` and `stop()`. `ctx`
gives `strings`, `settings` (read-only), `config`, `motion` and `audio`. The shell owns which one
runs. `crisis.js` exports `linesFor(regionCode)`, which returns the curated lines and the fallback.

**Tunables (`config.json`):** rhythm presets and the default (4-in, 6-out); tone frequencies and
volume; bubble count and drift speed; shape-trace speed; colour-sort tile count; the international
directory URL; the feedback repository URL and the email address (empty until decided).

**Hard problems and de-risking.**
1. *Offline install and update.* Proven first, in the walking skeleton, with an offline test and
   an update test.
2. *Accessible activities.* The bubble field and the colour sort use DOM elements, not a canvas,
   so a screen reader and the keyboard reach every item. The colour sort is built last.
3. *Launch in 1 second.* Inline the critical CSS, defer everything but the breath guide, and
   benchmark from the first slice.

**Cross-cutting targets.** No request to another origin from the app, ever. No console errors.
Every storage access in try/catch, so blocked storage never breaks a screen. No personal data in
any log. Any failure leaves the breath guide and the crisis lines usable.

---

## 9. Quality & Performance Strategy

**Tests (Playwright, real browser):**
- *Smoke:* every page loads with a clean console.
- *Offline:* after one visit, with the network off, every screen works; the network log shows no
  request to any other origin.
- *Accessibility:* axe-core on every page and state, with zero A and AA violations; a keyboard-only
  walk through every flow.
- *Reduced motion:* with the media feature set, no element animates.
- *Settings round trip:* save, reload, read, and assert the same values; blocked storage falls back
  to the defaults.
- *Crisis lines:* each sample region shows its lines; an unknown region shows the fallback.
- *Update:* a new cache version replaces the old one.
- *Claims:* a scan of the strings and pages for forbidden claim words (REQ-025).

**Never break:** the breath guide at launch; the "Need urgent help?" control on every screen;
offline use; keyboard and screen-reader use.

**Manual:** a dated volunteer check with a screen reader (NVDA, VoiceOver or TalkBack) and with a
keyboard alone, before a standard is shown (REQ-029). Owner checks on a real phone for look and
feel, which a test cannot see.

**Performance:** the targets are REQ-026 (1 s to the breath guide), REQ-027 (100 ms response) and
REQ-028 (150 KB). Workload: a cold launch of the installed app, offline, on a mid-range phone, or
a Playwright run with CPU throttled 4x as its stand-in. `bench` records all three per release.

**Security and privacy.** Nothing sensitive is stored or sent. The threats worth defending against
are a supply-chain change (none: no third-party code ships), a tampered crisis line (every change
goes through a reviewed commit), and a misleading claim (REQ-025). A Content Security Policy that
allows only the app's own origin backs up the no-network rule.

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
the research sources for each technique.

**Slice 3 — distraction.** The bubble field and the shape trace.

**Slice 4 — trust pages.** The disclaimer page, the Standards & research page, the feedback page,
and the GitHub issue templates.

**Slice 5 — colour sort.** Built last, as the hardest to make accessible. It ships only if it passes.

**Definition of done per slice:** it works, `test` is green, `bench` is spot-checked, the design
document and records agree with the code, and it is committed.

**Release criteria for 1.0:** every "must" requirement is met; every success criterion in Stage 2
holds; an audit round clears the gate (`audit-gate.py` prints `GATE CLEAR`); every crisis line is
re-checked; the Standards & research page shows only what is verified.

---

## 11. Risks, Assumptions & Open Questions

| Risk | Mitigation |
|---|---|
| A person in danger uses the app instead of getting help. | The "Need urgent help?" control is on every screen, and the self-help line is on the main screen. |
| A crisis line in the list goes out of service. | Each line has a last-checked date; a release re-checks every line; the international directory is the fallback. |
| A claim overstates the evidence and breaks health-claim rules. | REQ-025 fixes the wording; each technique cites its research (REQ-024); a test scans for forbidden words. |
| A standard is promoted that the app does not meet. | REQ-029: a standard is shown only with a dated automated and manual check for that version. |
| No volunteer comes forward for the manual check. | No standard is shown as met; the app still works; the owner can ask in accessibility communities. |
| A movement or a sound makes a person feel worse. | Reduced motion is honoured (REQ-010); tones are off by default (REQ-007); nothing is timed or scored. |
| The colour sort cannot be made fully accessible. | It is "should", not "must", and built last; it ships only when it passes. |
| The offline cache serves an old version after an update. | The cache name carries the version; an update test covers it. |

<!-- BEGIN srs-assumptions - written by the interview, read by the generators -->
- The crisis lines in the curated list stay in service between checks. Each line carries a
  last-checked date, and a release re-checks them.
- Community volunteers will do the manual accessibility checks. If none come forward, no
  standard is shown as met (REQ-029), and the product still works.
- GitHub Pages stays free for a public repository and serves the app over HTTPS, which an
  installable offline web app needs.
- A mid-range phone can show the breathing guide within 1 second of a cold offline launch with a
  plain HTML, CSS and JavaScript app under 150 KB.
- The device language and region setting is a good enough guide to the person's country for
  choosing crisis lines.
<!-- END srs-assumptions -->

**Open questions.**
- **The public feedback email address.** The owner decides, before the first release that shows
  the email button. Until then the button is hidden.
- **Which international crisis directory the fallback links to.** Proposed at slice 1:
  Find A Helpline (findahelpline.com), run by ThroughLine, free, more than 175 countries, checked
  2026-10-07. The owner confirms at the slice 1 phone check.

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
  stores personal data. — 2026-10-07
- **The distraction activities are a bubble field, a shape trace and a colour sort.** — Each one
  has no score, no failure and no timer. — Rejected: a counting task. The colour sort is "should"
  and not "must", because a keyboard and screen-reader path for it is the hardest to build. —
  2026-10-07
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
  disclaimer page; a pop-up window, which is harder to make accessible. — 2026-10-07
- **Only clinically researched techniques. Claims say "built on techniques studied in clinical
  research" and never "clinically proven", "treats" or "cures".** — In most markets a health claim
  for an app is regulated (FTC and FDA in the US, ASA and MHRA in the UK). Freelief itself has had
  no clinical study. A review or certification, such as by a clinician or ORCHA, may be claimed only
  after it is granted. — Rejected: stronger wording such as "clinically proven to reduce panic". —
  2026-10-07
- **Soft tones mark the breath, off by default. No spoken voice.** — Tones need no recorded assets
  and no translation. — Rejected: spoken guidance (quality varies by device and language); silent
  only. — 2026-10-07
- **Freelief collects no personal data and makes no network call after install.** — A person's
  worst moments are not telemetry. — Rejected: anonymous usage counts. — 2026-10-07
- **Accessibility target: WCAG 2.2 AA in full, and AAA wherever a criterion can be met.** — The
  users are in distress, so the stricter bar fits. — Rejected: AA only; no named standard. —
  2026-10-07
- **English only in the first version, with all text in one strings file per language.** — This
  keeps the first version small and makes a later translation a data change. — Rejected: English
  and Spanish at launch; English with no translation structure. — 2026-10-07
- **Freelief is for anyone, in the moment: no sign-up, no profile, no history.** — Rejected: a daily
  practice with reminders or streaks, which add stored data and pressure; a clinician-shaped tool.
  — 2026-10-07
- **On launch, the breathing guide starts at once.** — It asks zero decisions of the person in the
  worst moment. Other exercises are one tap away. — Rejected: a menu first; a question first. —
  2026-10-07
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
- **Strict performance targets: the breathing guide is visible within 1 s of a cold, offline launch
  on a mid-range phone; every input responds within 100 ms; the whole app is under 150 KB.** — In a
  panic attack every second of wait is felt. — Rejected: looser targets (3 s, 500 KB). — 2026-10-07
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
  Owner's choice. — 2026-10-07
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
  (narrower: befriending centres only). — 2026-10-07 (slice 1, implementer; proposed for owner
  confirmation)
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
  the middle cannot make it jump. — 2026-10-07 (slice 3, implementer)
- **Distraction is offered for the moment, never as a way to overcome panic.** — Research on safety
  behaviours (Helbig-Lang & Petermann 2010) says escape behaviours, which can include distraction,
  may keep an anxiety disorder going. Freelief's activity text says "there is nothing to win" and
  makes no claim. The Standards & research page (slice 4) must say that frequent attacks call for
  treatment. — 2026-10-07 (slice 3, implementer; a design concern for the owner to read)
- **Screens are addressed by URL hash, and the menu and Settings live in `screens/`.** — The
  browser Back button works with no extra code, and the exercises stay free of storage: the
  Settings screen is not an exercise, and it writes only through `settings.js`. — Rejected: a
  router with no URL (Back would leave the app); Settings inside an exercise module. —
  2026-10-07 (slice 2, implementer)
- **Grounding and calming words keep focus on the control the person used; the new text is a
  polite live region.** — Moving focus to the text on every step would send a keyboard user back
  to the start of the page each time. — 2026-10-07 (slice 2, implementer)
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
- [x] Every agreed obligation is a requirement record (`REQ-001` to `REQ-031`).
- [x] Every requirement carries a category, a verification method and a priority.
- [x] Every marked region is filled.
- [x] Both generated documents have been produced and read: `docs/SRS.md` and `docs/PRD.md`,
      31 of 31 requirements, no clause *Not supplied*.
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
