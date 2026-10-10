# Trust pages: About and Feedback

The owning document for `screens/about.js`, `screens/feedback.js` and `.github/ISSUE_TEMPLATE/`.
Design: `docs/Design_Document.md` flows F8 and F9; REQ-006, REQ-025, REQ-030.

## Reaching them
Two footer links: `#about` and `#feedback`. The menu and these pages show the full
footer. The exercise and activity screens show only the calm line, so the links are one step away
there, through "Back to menu". They are ordinary routes. The router awaits a screen's `start()`
and sets `main[data-shown]` when the screen is drawn. Tests wait on `data-shown`, not on
`data-screen`. A screen whose `start()` rejects falls back to the menu (AUD-008).

## About and disclaimer
All text is in `strings/en.json` under `about.*`: the self-help statement, privacy, the open
licence and "Made by". The version comes from `self.FREELIEF_VERSION`. The source link is
`config.json` → `project.sourceUrl`, and the maker's website link is `project.makerUrl`. The maker
logo is inline SVG with an accessible name. Every value from `config.json` that goes into HTML is
escaped (AUD-033).

## Standards and research (removed)
The page was removed on 2026-10-10 (owner, RLG-056), with its route, footer link, data files and
claim tooling. The app makes no standards claim. The sources stay in `docs/research/sources.md`.

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
