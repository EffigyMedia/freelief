# Trust pages: About, Standards and research, Feedback

The owning document for `screens/about.js`, `screens/standards.js`, `screens/feedback.js`,
`data/research.json`, `data/standards.json` and `.github/ISSUE_TEMPLATE/`. Design:
`docs/Design_Document.md` flows F8 and F9; REQ-006, REQ-020, REQ-024, REQ-025, REQ-029, REQ-030.

## Reaching them
Three footer links on every screen: `#about`, `#standards`, `#feedback`. They are ordinary routes;
the router awaits a screen's `start()` (Standards loads its data first) and sets
`main[data-shown]` when it is drawn. Tests wait on `data-shown`, not `data-screen`.

## About and disclaimer
All text is in `strings/en.json` under `about.*`. The version comes from `self.FREELIEF_VERSION`.
The source link is `config.json` → `project.sourceUrl`; it resolves once the public repository
exists.

## Standards and research
- **Standards.** `data/standards.json` → `verified` is a list of
  `{name, level, version, checked, tester, issue}`. The page shows an entry only while `version`
  equals the running `FREELIEF_VERSION` (AUD-023), so an update clears a claim until the new version
  is checked. Empty, or no entry for this version, means the page shows `standards.none`, which says
  what Freelief is built to and that no standard is claimed yet.
- **How a check becomes a recorded standard (AUD-054).** Add an entry only under REQ-029:
  1. The automated axe test (`tools/tests/test_a11y.py`) passes on every screen in both themes for
     the exact version, in a `test` run on a clean tree.
  2. A person checks every screen of that version with a screen reader and with a keyboard alone,
     using the accessibility checklist, and posts it as a GitHub issue from the Feedback page. The
     issue names the version, the browser, the device, the screen reader and its version, and the
     input used, and ticks every screen.
  3. The owner reads the issue. If every screen passed, the entry is added with `version` (the
     checked version), `checked` (the issue's date), `tester` (as the tester asks to be named),
     and `issue` (the issue URL), in its own unit with the version bump, citing the test run.
  4. A failed screen is a finding, not an entry.
- **Research.** `data/research.json` lists techniques and their source ids, and each source's
  citation, URL and checked date. The evidence summaries are translatable text in
  `strings/en.json` (`standards.evidence.*`). The full notes, with the strength of each source, are
  in `docs/research/sources.md`; keep the three in step. Citations are quoted as published, so this
  file is exempt from the claim-wording scan (`test_repo.py`).

## Feedback
The page fills a textarea from `feedback.template.<kind>` with the version, the browser
(`navigator.userAgentData` brands, or the user agent) and the device type. The GitHub link is
`project.newIssueUrl` with `template`, `title` and `body` query parameters, rebuilt on every edit,
so the link always carries exactly what the person sees. Switching the kind refills the box only
when its text is still the untouched template. The email choice stays `hidden` while
`project.feedbackEmail` is empty; set the address there and the button appears, with a `mailto:`
link built the same way. Freelief itself makes no request: the person's browser or mail app does.

The issue templates in `.github/ISSUE_TEMPLATE/` match the two kinds by file name
(`project.issueTemplates`). `.github/` does not ship (`NOT_SHIPPED` in `tools/freelief.py`).
