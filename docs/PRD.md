# Product Requirements — In-Dev/Freelief

> **Generated, never authored.** Every requirement below is a record in this line's fragment store. Edit the record, not this file: the next run overwrites it.
>
> This is the companion to the Software Requirements Specification, not a summary of it. The specification says what the software must do; this says what is decided, what is not, and where the work has got to.
>
> Store stamp `ab5c48f2deb2f8d3` · 31 requirement(s) recorded

## The problem

During a panic attack a person cannot easily recall or perform the techniques that would calm them.
The tools that exist put obstacles in the way at the worst moment: a sign-up, a menu, a loading
screen, a network that is not there, an advertisement, or a screen that a screen reader or a
keyboard cannot use. Many also record the person's crises as data. A person in distress needs help
that starts at once, works for them as they are, and asks for nothing.

## Who it is for

- **A person in the moment** — anyone who has a panic attack or acute anxiety now. They want the
  panic to pass. They use a phone or a computer, often at night, sometimes with a screen reader, a
  keyboard only, or reduced motion. They have little attention and shaky hands, and they must not
  be asked for anything before help starts.
- **A community volunteer** — a person who checks Freelief with a screen reader or a keyboard, or
  who reports a problem. They want to report with little effort, through GitHub or email.
- **The owner** — maintains the crisis-line list, accepts volunteer checks, and releases versions.

## How we will know it worked

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

## What is deliberately out of scope

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

## What is still undecided

*Nothing. Every requirement in this line's store is agreed, verified or withdrawn.*

## What we are building

### Must have

- **REQ-001** — Freelief offers a paced breathing exercise with a visual breath guide.
- **REQ-002** — Freelief offers a 5-4-3-2-1 sensory grounding exercise that the person steps through at their own pace.
- **REQ-003** — Freelief offers calming statements, shown one at a time, that the person advances at their own pace.
- **REQ-004** — Freelief offers interactive calming activities whose purpose is to distract the person from panic.
- **REQ-005** — Every screen shows a 'Need urgent help?' control that opens a list of crisis lines chosen from the device language and region setting, without a request for location.
- **REQ-006** — The main screen shows one short line that says Freelief is self-help and not medical care, and the About page gives the full statement. Neither blocks access to an exercise.
- **REQ-008** — Freelief is a progressive web app served from GitHub Pages that installs to the home screen and works with no network after the first visit.
- **REQ-009** — Every control is reachable and usable with a keyboard alone and with a screen reader.
- **REQ-010** — When the device asks for reduced motion, Freelief replaces every animation with a still or gentle equivalent.
- **REQ-011** — No exercise or activity requires the person to act within a time limit.
- **REQ-012** — Freelief offers a bubble field: the person pops slow, soft bubbles by touch or by key, with no score, no failure and no timer.
- **REQ-013** — Freelief offers a shape trace: the person slowly follows a looping shape with a finger or the arrow keys.
- **REQ-015** — Freelief collects no personal data and sends nothing over the network after install. Only the person's settings are stored, and only on the device.
- **REQ-016** — Freelief meets WCAG 2.2 level AA in full, and level AAA wherever a criterion can be met.
- **REQ-017** — All user-facing text lives in one strings file per language, so a translation can be added without a code change. English is the only language in the first version.
- **REQ-018** — When Freelief opens, the paced breathing guide starts at once, with no account, sign-up, menu or question before it.
- **REQ-019** — Freelief is plain HTML, CSS and JavaScript with no framework, no third-party dependency and no build step.
- **REQ-020** — A "Standards & research" page, linked from the footer and the disclaimer page, promotes every standard Freelief meets, such as WCAG 2.2 AA, with its level and the date it was last verified. It lists only standards that a check has verified.
- **REQ-021** — Freelief uses a dark, calm theme by default and follows the device light or dark setting. All text meets WCAG AAA contrast (7:1, or 4.5:1 for large text).
- **REQ-022** — Freelief ships a curated list of national crisis lines, each with a last-checked date, and a link to an international directory for every other region.
- **REQ-024** — Every technique in Freelief is one studied in published clinical research, and the Standards & research page cites at least one source for each technique.
- **REQ-025** — Freelief makes no claim that it is clinically proven, treats, cures or diagnoses anything. It may say only that its techniques are studied in clinical research, and may claim a review or certification only after it is granted.
- **REQ-026** — On a mid-range phone, installed and offline, the breathing guide is visible within 1 second of a cold launch.
- **REQ-027** — Every tap or key press gets a visible response within 100 milliseconds on a mid-range phone.
- **REQ-028** — The whole app, with every file the offline cache stores, is under 150 KB.
- **REQ-029** — A standard is shown as met only when an automated check of every page passes and a manual check with a screen reader and with a keyboard alone is recorded, with its date and tester, for the version shown. The manual check may come from community volunteers.
- **REQ-030** — A feedback page opens a pre-filled GitHub issue (accessibility check or problem report) and, as a second choice, a pre-filled email to the public project address. The pre-filled text holds only the app version, browser and device type, and the person sees and can edit all of it before they send. The app itself sends nothing.
- **REQ-031** — Freelief's source code is published under the MIT license.

### Should have

- **REQ-007** — Freelief can play soft tones that mark breath in and breath out. The tones are off by default and the person can turn them on.
- **REQ-014** — Freelief offers a colour sort: the person puts calm colours into gradient order by drag or by keyboard, with no score and no failure.
- **REQ-023** — The person can choose a breathing rhythm from presets (4-in 6-out by default, a slower rhythm, and box breathing), and the choice is remembered on the device.


## Where it stands

| | Count |
|---|---|
| Verified — shown to be met | 0 |
| Agreed — specified, not yet shown | 31 |
| Proposed — waiting on a decision | 0 |
| Withdrawn — no longer required | 0 |

Of the 31 requirement(s) in the specification, 0 (0%) have had their verification carried out.

## What has to land before what

*No requirement in this line blocks another. That is a fact and not an error: sequencing is recorded as a `blocks` relation between requirements, and nothing here has one.*

## What we dropped

*Nothing has been withdrawn.*

---

Generated 2026-10-07T13:13:54-04:00 by `Commands/prd.py`. The specification is generated beside it by `Commands/srs.py`, from these same records.
