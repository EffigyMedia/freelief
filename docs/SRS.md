# Software Requirements Specification — In-Dev/Freelief

> **Generated, never authored.** Every requirement below is a record in this line's fragment store. Edit the record, not this file: the next run overwrites it.
>
> Structure follows **ISO/IEC/IEEE 29148**. A requirement appears here once it is `agreed`; a `proposed` one is still a question for the owner and a `withdrawn` one is history the store keeps.
>
> Store stamp `6f480907bf20f4a1` · 31 requirement(s) specified, 0 not yet

## 1. Introduction

### 1.1 Purpose

Freelief helps a person through a panic attack or acute anxiety at the moment it happens. It gives
self-help techniques studied in clinical research — paced breathing, 5-4-3-2-1 grounding, calming
statements and gentle distraction activities — and a fast route to a crisis line for a person who
may be in danger. It is for anyone, at no cost, with no account, no network and no data collection.

### 1.2 Scope

Freelief covers self-help for a panic attack or acute anxiety at the moment it happens: paced
breathing, 5-4-3-2-1 grounding, calming statements, three distraction activities, crisis lines by
region, a self-help disclaimer, a Standards & research page, and a feedback page that hands a
pre-filled report to GitHub or email. It runs in a browser and as an installed offline web app.
The boundary: Freelief does not diagnose, treat, track, or contact anyone. It points to crisis
lines; it does not call them. Its only stored data is the person's settings, on the device.

### 1.3 Product overview

Freelief is a progressive web app: plain HTML, CSS and JavaScript served from GitHub Pages. It
installs to the home screen of a phone or a desktop and then works fully offline. When it opens,
a paced breathing guide starts at once. From there, one tap or key press reaches the other
exercises (grounding and calming statements) and the distraction activities (a bubble field, a
shape trace and a colour sort). Every screen has a "Need urgent help?" control that shows crisis
lines for the person's region. Supporting pages give the self-help disclaimer, the standards
Freelief meets with the research behind each technique, and a feedback page that opens a pre-filled
GitHub issue or email. Freelief has no server, no account and no analytics. It stores only the
person's settings, on the device.

### 1.4 Definitions

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

## 2 References

- W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation, 2023 — the
  accessibility target (AA in full, AAA where a criterion can be met).
- W3C, *Web Application Manifest* and WHATWG *Service Workers* — the installable offline web app.
- GitHub Pages documentation — the host.
- The published research for each technique. The list lives on the Standards & research page and
  in `docs/research/` (written in slice 2), one source or more per technique (REQ-024).

## 3. Specific requirements

### 3.1 External interfaces

*None. No `agreed` requirement in this line is categorised `interface`.*

### 3.2 Functions

- **REQ-001** *(must)* — Freelief offers a paced breathing exercise with a visual breath guide.
- **REQ-002** *(must)* — Freelief offers a 5-4-3-2-1 sensory grounding exercise that the person steps through at their own pace.
- **REQ-003** *(must)* — Freelief offers calming statements, shown one at a time, that the person advances at their own pace.
- **REQ-004** *(must)* — Freelief offers interactive calming activities whose purpose is to distract the person from panic.
- **REQ-005** *(must)* — Every screen shows a 'Need urgent help?' control that opens a list of crisis lines chosen from the device language and region setting, without a request for location.
- **REQ-006** *(must)* — The main screen shows one short line that says Freelief is self-help and not medical care, and the About page gives the full statement. Neither blocks access to an exercise.
- **REQ-007** *(should)* — Freelief plays subtle sounds: a soft tone that lasts each breathing phase, and short cues for the activities (a bubble pop, a chime on Next, a singing-glass tone while tracing, a click and a rising phrase in the colour sort). Sounds are on by default; one Sounds switch in Settings turns them all off. Nothing plays before the person's first tap or key press.
- **REQ-012** *(must)* — Freelief offers a bubble field: the person pops slow, soft bubbles by touch or by key, with no score, no failure and no timer.
- **REQ-013** *(must)* — Freelief offers a shape trace: the person slowly follows a looping shape with a finger or the arrow keys.
- **REQ-014** *(should)* — Freelief offers a colour sort: the person puts calm colours into order from lightest to darkest by choosing a tile and then the tile to swap it with, by touch, mouse or keyboard, with no score and no failure.
- **REQ-018** *(must)* — When Freelief opens, it shows the menu of exercises and activities at once, with no account, sign-up, notice or question before it. Breathing is the first item, one tap away, and every screen has a Back to menu control.
- **REQ-020** *(must)* — A "Standards & research" page, linked from the footer and the disclaimer page, promotes every standard Freelief meets, such as WCAG 2.2 AA, with its level and the date it was last verified. It lists only standards that a check has verified.
- **REQ-022** *(must)* — Freelief ships a curated list of national crisis lines, each with a last-checked date, and a link to an international directory for every other region.
- **REQ-023** *(should)* — The person can choose a breathing rhythm from presets (4-in 6-out by default, a slower rhythm, and box breathing), and the choice is remembered on the device.
- **REQ-024** *(must)* — Every technique in Freelief is one studied in published clinical research, and the Standards & research page cites at least one source for each technique.
- **REQ-030** *(must)* — A feedback page opens a pre-filled GitHub issue (accessibility check or problem report) and, as a second choice, a pre-filled email to the public project address. The pre-filled text holds only the app version, browser and device type, and the person sees and can edit all of it before they send. The app itself sends nothing.

### 3.3 Usability requirements

- **REQ-009** *(must)* — Every control is reachable and usable with a keyboard alone and with a screen reader.
- **REQ-010** *(must)* — When the device asks for reduced motion, Freelief replaces every animation with a still or gentle equivalent.
- **REQ-011** *(must)* — No exercise or activity requires the person to act within a time limit.
- **REQ-016** *(must)* — Freelief meets WCAG 2.2 level AA in full, and level AAA wherever a criterion can be met.
- **REQ-021** *(must)* — Freelief uses a dark, calm theme by default and follows the device light or dark setting. All text meets WCAG AAA contrast (7:1, or 4.5:1 for large text).

### 3.4 Performance requirements

- **REQ-026** *(must)* — On a mid-range phone, installed and offline, the first screen (the menu) is visible within 1 second of a cold launch.
- **REQ-027** *(must)* — Every tap or key press gets a visible response within 100 milliseconds on a mid-range phone.
- **REQ-028** *(must)* — The whole app, with every file the offline cache stores, is under 250 KB.

### 3.5 Logical database requirements

*None. No `agreed` requirement in this line is categorised `database`.*

### 3.6 Design constraints

- **REQ-008** *(must)* — Freelief is a progressive web app served from GitHub Pages that installs to the home screen and works with no network after the first visit.
- **REQ-017** *(must)* — All user-facing text lives in one strings file per language, so a translation can be added without a code change. English is the only language in the first version.
- **REQ-019** *(must)* — Freelief is plain HTML, CSS and JavaScript with no framework, no third-party dependency and no build step.
- **REQ-025** *(must)* — Freelief makes no claim that it is clinically proven, treats, cures or diagnoses anything. It may say only that its techniques are studied in clinical research, and may claim a review or certification only after it is granted.
- **REQ-031** *(must)* — Freelief's source code is published under the MIT license.

### 3.7 Software system attributes

- **REQ-015** *(must)* — Freelief collects no personal data and sends nothing over the network after install. Only the person's settings are stored, and only on the device.
- **REQ-029** *(must)* — A standard is shown as met only when an automated check of every page passes and a manual check with a screen reader and with a keyboard alone is recorded, with its date and tester, for the version shown. The manual check may come from community volunteers.

## 4. Verification

How each requirement above is shown to be met. The method is recorded on the requirement, so this clause cannot disagree with clause 3.

| Requirement | Clause | Method | Status |
|---|---|---|---|
| REQ-001 | 3.2 | test | agreed |
| REQ-002 | 3.2 | test | agreed |
| REQ-003 | 3.2 | test | agreed |
| REQ-004 | 3.2 | demonstration | agreed |
| REQ-005 | 3.2 | test | agreed |
| REQ-006 | 3.2 | inspection | agreed |
| REQ-007 | 3.2 | test | agreed |
| REQ-012 | 3.2 | test | agreed |
| REQ-013 | 3.2 | test | agreed |
| REQ-014 | 3.2 | test | agreed |
| REQ-018 | 3.2 | test | agreed |
| REQ-020 | 3.2 | inspection | agreed |
| REQ-022 | 3.2 | inspection | agreed |
| REQ-023 | 3.2 | test | agreed |
| REQ-024 | 3.2 | inspection | agreed |
| REQ-030 | 3.2 | test | agreed |
| REQ-009 | 3.3 | test | agreed |
| REQ-010 | 3.3 | test | agreed |
| REQ-011 | 3.3 | inspection | agreed |
| REQ-016 | 3.3 | test | agreed |
| REQ-021 | 3.3 | test | agreed |
| REQ-026 | 3.4 | test | agreed |
| REQ-027 | 3.4 | test | agreed |
| REQ-028 | 3.4 | test | agreed |
| REQ-008 | 3.6 | test | agreed |
| REQ-017 | 3.6 | inspection | agreed |
| REQ-019 | 3.6 | inspection | agreed |
| REQ-025 | 3.6 | inspection | agreed |
| REQ-031 | 3.6 | inspection | agreed |
| REQ-015 | 3.7 | inspection | agreed |
| REQ-029 | 3.7 | inspection | agreed |

## 5. Appendices

### 5.1 Assumptions and dependencies

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

### 5.2 Acronyms and abbreviations

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

---

Generated 2026-10-07T22:26:12-04:00 by `Commands/srs.py` from 31 requirement record(s).
