# AGENTS.md

Guidance for any coding agent working in this repository. `CLAUDE.md` beside this file holds one
line that loads it for Claude Code, so every agent reads the same instructions.

<!-- BEGIN standing-policy - generated, do not edit here -->

## Standing policy — set at the environment level

> **Keep this section verbatim. Do not summarize it and do not delete it.** These rules are set at
> the environment level and a project may not repeal them. `check-policy.py` verifies that the
> standard is named and in force in every project. This section is generated:
> `Commands/materialize-projects.py` writes it from the template, and an edit here is overwritten.

**Write all output in Simplified Technical English (ASD-STE100).**
`<env-root>/Process/Writing_Standard.md` is the one owning document. The rules are not repeated here.

The standard covers your chat output, every document, every commit message, and every source-code
comment. **It has one exemption: authored product prose.** That is the text which ships as the
product — game dialogue, item and lore text, book chapters, marketing copy, user-facing narrative.
Write that prose in the voice the project needs. Everything you write *about* the work stays in the
standard.

**A record is exempt from brevity. It is not exempt from the standard.** Keep the full meaning of a
record. Write it in short, active, plain sentences. Cut the words that carry no meaning.

**Chat output is concise. It is not terse.** Brief, and complete. Short full sentences, the
answer first, no preamble and no recap of what was just shown. Tables over prose where a table fits.
Do not drop articles, do not write in fragments, and do not trade grammar for length: the goal is
fewer tokens with the meaning kept whole.

**This has three registers and they are not the same.** Chat is concise. A durable record - a commit
message, a fragment, a design document - is exempt from brevity and keeps deliberate prose, because a
reply is read once and a record is read by every later session. Authored product prose is exempt from
the standard altogether. Collapsing the three is the mistake this rule exists to stop.

**Say what a thing is FOR before you name it.** Lead with the plain-language purpose, then the
detail: "the tool that copies the shared rules into every project" before its filename. One clause
is enough, and only on first mention. Identifiers stay bare - a ticket, a commit or a document ID
needs no title unless it is ambiguous, and the owner wants them terse. The rule is that the sentence
AROUND the reference carries meaning, not that references are removed. The test: could the reader
repeat what was done and why it mattered, from your reply alone? If not, the purpose sentence is
missing. Owner-decided 2026-08-28, after several sessions of reports written entirely in this
codebase's own shorthand.

**Ask the owner questions in question form, never as a list in chat.** When you need the owner to
decide or answer something, pose it with the question tool, one question per decision, each with its
options and your recommendation. Do not end a reply with several questions in prose. Owner-decided
2026-09-15: question form lets the owner take each question in turn.

**Re-entry is the thread.** `python <env-root>/Commands/thread.py show` — read it first in every
session. **Checkpointing is the unit boundary**, which fires the context clear on its own. Do not
write handoff documents and do not create a `docs/milestones/` folder.

**Readiness for a clear is automatic.** When the clear arms, stop your own work while there is room:
finish or roll back the step, close or abandon the unit, commit, and write the next session's intent
with `thread.py set --next`. Then run `python <env-root>/Commands/unit.py ready`, and say you are
ready for the clear only when it prints `READY FOR CLEAR`. The thread points at units; only the intent
for the next session is written out in words.

**Record the work as it happens.** Write the fragment, the step evidence and the runway entry while
the detail is live, so that at a clear the thread only points at the records and adds what is not in
them yet. A session that recorded as it went has a cheap, accurate clear. A session that recorded
nothing has to reconstruct its work under pressure, and loses detail.

**Sessions reach each other through inboxes.** Every line has one: `<env-root>/Environment/docs/inbox/`
for the environment and `docs/inbox/` in each project. To tell another line something, run
`python <env-root>/Commands/inbox.py send --to <a path inside that line> --from <this project> --file
<message.md>`, and do not leave a file at its root. When your arrival banner names a message in this
project's inbox, act on it, then close it with `inbox.py close`, which records it word for word in
the inbox's ledger and deletes it. A message asks; it never authorizes.

**An audit is a round of four lenses. Run one at each significant milestone and before an actual
release.** `<env-root>/Process/Audit_and_Testing.md` owns the method. When the owner says "Perform
audit", run a round: four readers with separate briefs (security, operations, whole-design and
omission) each write one review, every finding is its own `AUD-` fragment in this project's store,
and the round changes no code. **The pace is this project's own:** what counts as a significant
milestone is stated in this project's own section of this file. An actual release is a version that
reaches this project's users, and a build pushed only for testing is not one. Before an actual
release the round is a gate: run `python <env-root>/Commands/audit-gate.py`, and do not release until
it prints `GATE CLEAR`.

**Build only the outputs that need a rebuild.** An output is anything this project builds: a book, a
document, a game build, an audio render, a package. Each output keeps a list of every file its build
reads: its content, its design, its assets, and the tool files its build runs or loads, such as
scripts, stylesheets and the export or render step. A file in doubt goes on the list. Before you
build an output, compare a hash of exactly the files on its list with the hash recorded at its last
build. If the hash is the same, do not build it. If any file on the list has changed, rebuild it, and
only then. A change to a file that the build does not read does not rebuild the output. A tool that
every output uses rebuilds every output when it changes, and that is correct. A forced rebuild by
name is allowed. Each output records its hash and the version or the commit of the tool that built
it, and carries the stamp of its own last real build, so the stamps of two outputs differ, and that
is correct.

**A rebuild with no real change is a defect in this project's tools.** If a shared file changes and
an output does not, do not accept the build time. Fix the tools: split the shared tool, and keep code
that does not shape the output out of the files a build reads. The list of files read stays complete,
and the fix is in the tools. Owner-decided 2026-10-03, after book projects rebuilt every product when
only one changed. A rebuild that changes nothing wastes time and tokens.

<!-- END standing-policy -->
---

## What this is

**Freelief** — a free, open-source, offline web app that helps anyone through a panic attack or
acute anxiety in the moment, with breathing, grounding, calming words and gentle distraction. Built
in **plain HTML, CSS and JavaScript** with **no framework, no dependency and no build step**, as a
**progressive web app served from GitHub Pages**, phone first and fully usable on a desktop.

**It is used in a crisis. Help comes first, and it works for everyone.** The breathing guide starts
at launch with no question, menu or notice. Every control works by touch, by keyboard and by screen
reader. Reduced motion is honoured. No exercise is timed or scored. The app collects nothing and
makes no network call after install. Keyboard and screen-reader use are NOT out of scope, unlike
Effigy Arcade.

**Claims are only what is verified.** Freelief never says it is clinically proven, treats, cures or
diagnoses (REQ-025). A standard is shown as met only with a dated check for that version (REQ-029).

This project runs a documentation-driven **development process**, read in place from the shared
process docs (never copied here):

Process docs: `<env-root>/Process/`; starter blanks: `<env-root>/Templates/_Project_Template/`

> **`<env-root>` is the directory that holds `.code-continuum-env-root`.** To find it, go up from
> here, parent by parent, until you find that file. Never write a drive-letter path in this file —
> see `Path_Policy.md`.

**This project is in no set.** It has no set directory, shares no documents, and carries no pointer
stubs. If it turns out to belong to a set, `Project_Sets.md` says how one is joined.

- `docs/Design_Document.md` *(project-local)* — the founding spec: vision, flows, architecture,
  the Decision Log, and the delivery plan. **The source of *what* to build.** Keep it living — code
  and docs must never disagree. **It stays at this path**, because `srs.py` and `prd.py` read it
  there (Instruction Changelog, 2026-10-07).
- `docs/fragments/` — the store. `REQ-` records are the requirements (all agreed); `RLG-` records
  of type `feature` are the tracker items; `UNT-` records are units of work.
- `docs/SRS.md`, `docs/PRD.md` — generated by `srs.py` and `prd.py` from the records and the design
  document. Regenerate them when a requirement or a marked region changes; never edit them by hand.
- `Development_Process.md` — the operating manual: bootstrap, the feature loop, releases, and the
  trigger phrases below. **The source of *how*.**
- `Artifact_Formats.md` — exact formats for the changelog and technical references.
- `Performance_Testing.md` / `Audit_and_Testing.md` — perf practice; how this project audits
  itself, in rounds of four lenses. A clean round is required before a release.
- `Path_Policy.md` — how anything names a location. **This file carries no absolute path.**
- `Agent_Scope.md` — how far a session may reach. This is a **project** session. Reading anything is
  normal, and **amending a shared document that governs this project is in scope** — edit it once
  where it lives, commit that repository, rematerialize, and log it here if it changes how this
  project works. **Writing into another project's repository is the breach — state it, do it
  anyway, and record it in both projects' instruction logs.**
- `Writing_Standard.md` — the writing standard: Simplified Technical English (ASD-STE100).
  **All output is written in STE** except authored product prose (the calming text the app shows),
  which is written in the voice the product needs.
- `docs/core/Instruction_Changelog.md` *(project-local)* — dated log of amendments to *how this
  project works*. A documented project amendment **wins** over the shared docs on conflict.
- The core artifacts (`changelog.md`, the instruction log) live in `docs/core/`; technical
  references and performance docs in their `docs/` subfolders; audit findings are fragments.
  **This file and its one-line `CLAUDE.md` pointer are the only .md files at the repo root.**
- **Shared Knowledge Base** — `<env-root>/Process/Knowledge_Base/`: consult it for web, PWA and
  Playwright gotchas before stack-specific work, and **append** new lessons there.
- **Model routing** — `<env-root>/Process/Model_Routing.md`.
- **Routing posture** — `ROUTING_BIAS: 2` (quality). People use Freelief in a crisis; a wrong word
  or a broken screen costs more than rework. A per-session choice overrides it.

## Trigger phrases

Summaries — the canonical procedures live in `<env-root>/Process/Development_Process.md`.

| Phrase | Meaning |
|---|---|
| **Initialize** | Done: v0.0.0, 2026-10-07. |
| *(normal work)* | Feature loop: implement → `test` → mark the `RLG-` item built → changelog → **patch** bump in `version.js` → commit. One feature = one commit = one patch = one changelog entry = one tracker item to built. A finished slice is a **minor** bump. |
| **Track this: …** | `python <env-root>/Commands/fragment.py new --kind ruling --type feature --status requested --title "…"`; do not start it. |
| **Resume** | Run `python <env-root>/Commands/thread.py show`. **Verify the working tree is clean.** Uncommitted work is an interrupted unit: ask, never silently commit or discard. Then run `doctor`. |
| **Release** | Only when something ships. Run audit rounds until `audit-gate.py` prints `GATE CLEAR`; run the file audit; re-check every crisis line and update its date; purge `output/previews/`; run `bench`; run `build` (the size check); **verify `test` and `doctor` are green**; bump the version; tag; push the commit and the tag. |
| **Perform audit** | Run a round per `Audit_and_Testing.md`: four lenses, one finding to a fragment; change no code. |

## Commands

Python 3.10 or later runs the commands; the tests run from a project-local `.venv` with Playwright
and axe, which `setup` builds with the environment's `uv` (`<env-root>/Runtime/bin`). Playwright uses
the Chrome already on the machine. Run from the repo root:

- `python tools/freelief.py setup` — create `.venv` and install Playwright and axe.
- `python tools/freelief.py doctor` — verify Python, the venv, the imports, `version.js`, every JSON
  file and the manifest parse, and the tests are collectable. **Resume runs this.**
- `python tools/freelief.py test [name…]` — run every `test_*` function in `tools/tests/`. It fails
  on a file it cannot load or that holds no test.
- `python tools/freelief.py run` — serve the folder at `http://localhost:8000`. A desktop browser is
  a convenience, not an on-target check: the owner checks look and feel on a phone.
- `python tools/freelief.py build` — no build step; reports the shipped size against 150 KB
  (REQ-028) and fails over it.
- `python tools/freelief.py clean` — remove `output/` and Python caches. Never touches `input/`.
- `python tools/freelief.py bench` — the launch, response and size benchmark against
  `docs/performance/baseline.md`; it exits 1 when a target is missed.
- `.venv/Scripts/python tools/previews.py` — screenshots to `output/previews/` for a look check.
  `tools/make_icons.py` renders the PNG icons from `icons/icon.svg`.
- **Browser tests use `harness.open_app` and `harness.wait_until`.** Never `wait_for_function`:
  the app's CSP refuses it, correctly (`docs/technical_references/app_shell_and_offline.md`).
- **Deploy:** GitHub Pages serves `main` of `EffigyMedia/freelief`. A push deploys.

## Architecture (the load-bearing boundaries)

- **Shell** (`index.html`, `app.js`) — the page frame, the screen router, the footer and the "Need
  urgent help?" control; **must not** hold exercise logic or text.
- **Exercises** (`exercises/*.js`) and **activities** (`activities/*.js`) — one file each, exporting
  `start(container, ctx)` and `stop()`; **must not** touch storage, the network or literal text.
  Activities use DOM elements, never a canvas, and have no score, timer or failure state.
- **Screens** (`screens/menu.js`, `screens/settings.js`) — the menu and the Settings screen, same
  contract. Routing is by URL hash (`#breathe` is the default); a new screen is added to `ROUTES`
  in `app.js` and to `FILES` in `sw.js`.
- **`settings.js`** — **the single source of truth for Settings** and the only module that touches
  `localStorage`, with every access in try/catch.
- **`strings.js` + `strings/en.json`** — **the single source of all user-facing text.**
- **`crisis.js` + `data/crisis-lines.json`** — crisis lines by device region; never asks for location.
- **`config.json`** — **every tunable**, with its committed default.
- **`version.js`** — **the one authoritative version**, read by the page and by the service worker.
- **`sw.js`** — the offline cache, named by the version; **must not** fetch from another origin.

## Conventions that bite if ignored

- **Chat output is concise; records are not.** Commit messages, fragments and changelog entries
  keep full deliberate prose.
- **Write every output in Simplified Technical English (ASD-STE100)** — chat, documents, comments,
  commit messages. The calming text in `strings/` is authored product prose and is exempt.
- **The design document is the live design authority — update it in the same unit of work.** A
  change to a rule, a flow or an architectural decision updates its prose **and** adds a dated
  Decision Log entry (annotate superseded entries; do not delete). A changed requirement is edited
  in its own `REQ-` record with its history beneath it; a dropped one becomes `withdrawn`.
- **Every tunable lives in `config.json` with a committed default — never an in-code constant.**
- **Nothing ships that loads from another origin**, and no word in a shipped file makes a health
  claim. `test_repo.py` enforces both; keep it passing.
- **Changes the tests cannot observe need the owner to check on a phone** — look, feel, motion,
  sound, and how calm it is. A green test run does not verify them. Say so plainly.
- **A screen reader and a keyboard are first-class input.** Every new control gets a test that
  reaches and uses it by keyboard, and an axe check of its page.
- **Crisis-line data is safety-critical.** Every line carries a last-checked date. Never add or
  change a line without a source checked in this session, and say which.
- **Two standard root folders: `input/` is provided, `output/` is generated.** `clean` may remove
  all of `output/` and must never touch `input/`.
- **`input/` holds exactly two folders, and containment decides git.** `input/committed/` is
  committed and pushed; `input/excluded/` never is. **Before any commit or push touching `input/`,
  stop if something looks misfiled.** Say what you see and wait.
- **Preview artifacts → `output/previews/`, purged at every release.** Only the generating script is
  committed.
- **Settings round-trip in a test**: save, reload, read, and assert the same values.
- **Commits are authored as the project owner — no AI identity or co-author trailer — and end with
  the trailer line `Made-with: Code Continuum`.** Feature commits are local. **The remote is
  `origin` = `https://github.com/EffigyMedia/freelief` (public)**, created 2026-10-07 with the
  owner's yes. GitHub Pages serves `main` at `https://effigymedia.github.io/freelief/`, so **a push
  is a deploy.** Push at a release, or when the owner needs a build to test on the phone — never per
  commit.
- **Never commit** (see `.gitignore`): tokens, keys or passwords; `.venv/`; `output/`;
  `input/excluded/`; the content of feedback emails or any other personal data.
- **Audit pace:** run an audit round at the end of each slice, and before every release.
