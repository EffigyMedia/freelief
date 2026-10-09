# Trust pages: About, Standards and research, Feedback

The owning document for `screens/about.js`, `screens/standards.js`, `screens/feedback.js`,
`data/research.json`, `data/standards.json` and `.github/ISSUE_TEMPLATE/`. Design:
`docs/Design_Document.md` flows F8 and F9; REQ-006, REQ-020, REQ-024, REQ-025, REQ-029, REQ-030.

## Reaching them
Three footer links: `#about`, `#standards` and `#feedback`. The menu and these pages show the full
footer. The exercise and activity screens show only the calm line, so the links are one step away
there, through "Back to menu". They are ordinary routes. The router awaits a screen's `start()`
(Standards loads its data first) and sets `main[data-shown]` when the screen is drawn. Tests wait
on `data-shown`, not on `data-screen`. If Standards cannot load its data, `start()` rejects and the
shell falls back to the menu (AUD-008).

## About and disclaimer
All text is in `strings/en.json` under `about.*`: the self-help statement, privacy, the open
licence and "Made by". The version comes from `self.FREELIEF_VERSION`. The source link is
`config.json` → `project.sourceUrl`, and the maker's website link is `project.makerUrl`. The maker
logo is inline SVG with an accessible name. Every value from `config.json` that goes into HTML is
escaped (AUD-033).

## Standards and research
- **Standards.** `data/standards.json` → `verified` is a list of
  `{name, level, version, checked, tester, issue}`, where `version` is the version checked. The
  page shows an entry when `version` is the running version or an earlier one (AUD-102, owner
  2026-10-09). A check holds until a release changes the interface: a screen, the styles, the text
  or the shell (`INTERFACE` in `tools/freelief.py`). `claim_outdated()` finds the commit that
  introduced the checked version and looks for an interface change since. Then
  `test_a_verified_standard_holds_until_the_interface_changes` and `build --release` fail, doctor
  warns, and the entry must be removed until people check again. With no entry to show, the page
  shows `standards.none`. That text says what Freelief is built to, and that no standard is claimed
  yet.
- **How a check becomes a recorded standard (AUD-054).** Add an entry only under REQ-029:
  1. The automated axe test (`tools/tests/test_a11y.py`) passes on every screen in both themes for
     the exact version, in a `test` run on a clean tree.
  2. A person checks every screen of that version with a screen reader and with a keyboard alone,
     with the accessibility checklist, and posts it as a GitHub issue from the Feedback page. The
     issue names the version, the browser, the device, the screen reader and its version, and the
     input used, and ticks every screen.
  3. The owner reads the issue. If every screen passed, the owner adds the entry with `version`
     (the checked version), `checked` (the issue's date), `tester` (as the tester asks to be
     named) and `issue` (the issue URL). This is its own unit, with the version bump, and it cites
     the test run. The entry ships in the next version and shows there, because a version bump and
     the standards file are not interface changes.
  4. A failed screen is a finding, not an entry.
- **Research.** `data/research.json` lists the techniques, each with its source ids, and each
  source's citation, URL and checked date. The page shows one section per technique: breathing,
  each activity, and distraction in general. The evidence summaries are translatable text in
  `strings/en.json` (`standards.technique.*` and `standards.evidence.*`). The full notes, with the
  strength of each source, are in `docs/research/sources.md`. Keep the three in step:
  `test_repo.py` fails when a source in `research.json` is not in `sources.md` (AUD-063). Citations
  are quoted as published, so `research.json` is exempt from the claim-wording scan.

## Feedback
The page has two kinds: "Accessibility check" and "Report a problem". It fills a textarea from
`feedback.template.<kind>` with the version, the browser (`navigator.userAgentData` brands, or the
user agent) and the device type. The person can read and change all of it. Switching the kind
refills the box only when its text is still the untouched template, so no typed words are lost.

The person sends the message in one of two ways:
- **Copy message, then Open on GitHub.** "Copy message" writes the text to the clipboard and says
  so in a polite live line. If the browser refuses, the page selects the text and tells the person
  to copy it. "Open on GitHub" is a link to `project.newIssueUrl`, and the person pastes the
  message into the new issue.
- **Send by email.** A `mailto:` link to `project.feedbackEmail`, with the subject and the message
  as the body. It opens the person's own mail app. The choice stays `hidden` while
  `project.feedbackEmail` is empty. Set the address there and the button appears.

**Privacy rule: the GitHub link carries only the template and the title. It never carries the
message (AUD-055).** A web address is kept in browser history and reaches GitHub as soon as it
opens, before the person decides to post. Thus the link has only the `template` and `title` query
parameters. Do not add a `body` parameter, or any other part of the person's words, to that link.
`test_slice4.py` checks this. The note under the GitHub button says that issues are public and asks
the person not to include health or personal details.

Freelief itself makes no request. The person's browser or mail app does.

The issue templates in `.github/ISSUE_TEMPLATE/` match the two kinds by file name
(`project.issueTemplates`: `accessibility-check.md` and `problem-report.md`). `.github/` does not
ship (`NOT_SHIPPED` in `tools/freelief.py`).
