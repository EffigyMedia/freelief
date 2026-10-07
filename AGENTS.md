# AGENTS.md Template (operative instructions)

> **What this is:** a reusable, **technology-neutral** template for a project's root `AGENTS.md` —
> the short operative brief a coding agent loads every session. `AGENTS.md` is the file that coding
> agents from any vendor read. Beside it, the project's `CLAUDE.md` holds one import line and nothing
> else (`CLAUDE_Pointer.md` is its exact text), so Claude Code loads the same instructions. This
> blank stays in the shared template; only the filled result lives in the project.
>
> **How to use:** the **Initialize** bootstrap (`Process/Development_Process.md`,
> Phase 1) reads this file **in place** from the shared starter folder and writes the
> project's root `AGENTS.md` from it, filling every `<PLACEHOLDER>` from the completed design doc.
> Delete the `> guidance` blockquotes (including this one). Keep it short and *true* — it's the
> operative summary; the shared docs hold the detail. When an instruction changes, amend the
> project's `AGENTS.md` **and** log it in the project's instruction changelog — never edit the
> shared corpus from project work, and never write an instruction into `CLAUDE.md`.
>
> Everything below is stack-agnostic. The bracketed guidance shows how to fill each part; the
> **Conventions that bite** section is where the folded-in, hard-won lessons live as principles —
> keep the ones that apply, drop the ones that don't.

---

<!-- The section below is the SOURCE of every project's standing policy, and the only copy of it.
     `python Commands/materialize-projects.py --write --project Freelief` writes it into that project
     between the same two markers, and `--all` in place of `--project` writes it into every project.
     Edit it here and run that; do not edit a project's copy, and never copy it by hand - a hand copy
     is a second text, and it drifts from this one and from every other copy. -->

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

# AGENTS.md

Guidance for any coding agent working in this repository. `CLAUDE.md` beside this file holds one
line that loads it for Claude Code, so every agent reads the same instructions.

## What this is

**Freelief** — <one-line pitch: what it is and for whom>. Built in **<language / runtime>** on
**<framework / engine / "no framework">**, targeting **<platforms / deploy targets>**.
<One line on any load-bearing product stance — e.g. premium/offline/no-tracking, or "internal tool",
if it constrains decisions. Delete if N/A.>

This project runs a documentation-driven **development process**, read in place from the shared
process docs (never copied here, never edited from project work):

Process docs: `<env-root>/Process/`;
starter blanks: `<env-root>/Templates/_Project_Template/`

> **`<env-root>` is the directory that holds `.code-continuum-env-root`.** To find it, go up from here,
> parent by parent, until you find that file. Never write a drive-letter path in this file —
> see `Path_Policy.md`.

> **Set line — keep only if a set manifest names this project; otherwise delete it and
> the `Project_Sets.md` bullet below.** The set's `_set/set.toml` must name this project in
> `projects`. Both directions must resolve. A member sits **beside** `_set/` inside the set folder,
> so from here that manifest is `../_set/set.toml`.

**This project is in no set.** It has no set directory, shares no documents, and carries no pointer stubs. If it turns out to belong to a set, `Project_Sets.md` says how one is joined.

- `docs/core/Freelief_design.md` *(project-local)* — the founding spec: vision, flows,
  architecture, the Decision Log, and the build plan. **The source of *what* to build.** Keep it
  living — code and docs must never disagree.
- `Development_Process.md` — the operating manual: bootstrap, the feature loop, releases, and the
  trigger phrases below. **The source of *how*.**
- `Artifact_Formats.md` — exact formats for `tracker.md`, `changelog.md`,
  technical references.
- `Performance_Testing.md` / `Audit_and_Testing.md` — perf practice; how this project audits
  itself, in rounds of four lenses. A clean round is required before a release.
- `Path_Policy.md` — how anything names a location. **This file carries no absolute path.**
- `Agent_Scope.md` — how far a session may reach. This is a **project** session. Reading anything is
  normal, and **amending a shared document that governs this project is in scope** — edit it once
  where it lives, commit that repository, rematerialize, and log it here if it changes how this
  project works. **Writing into another project's repository is the breach — state it, do it
  anyway, and record it in both projects' instruction logs.**
- `Project_Sets.md` *(set members only)* — the set rules. Short version: shared documents live once
  in the set directory and are never copied down. Nothing else about this project changes.
  Delete this bullet if no manifest names this project.
- `Writing_Standard.md` — the writing standard: Simplified Technical English (ASD-STE100).
  **All output is written in STE** — chat, every project document, source-code comments, and
  commit messages. Identifiers and code syntax are exempt. This doc is the single owner of the
  rules; everything else points here.
- `docs/core/Instruction_Changelog.md` *(project-local)* — dated log of amendments to *how this
  project works*. Add an entry whenever an instruction changes (and update this file's affected
  section, same unit of work). A documented project amendment **wins** over the shared docs on
  conflict.
- The **core artifacts** (design doc, `tracker.md`, `changelog.md`, the instruction log) live in
  `docs/core/`; technical references and performance docs in their `docs/` subfolders; audit
  findings are fragments in `docs/fragments/`; **this file and its one-line `CLAUDE.md` pointer are
  the only .md files at the repo root** (agents load them from there).
  *(A set changes nothing here. A set directory holds a manifest and documents, never an
  `AGENTS.md` or a `CLAUDE.md`, so only this project's instructions load.)*
- **Shared Knowledge Base** — `<env-root>/Process/Knowledge_Base/`:
  the cross-project, tool-specific gotcha memory. Consult it for `<stack>` gotchas before
  stack-specific work, and **append** new lessons there (not into the shared process docs).
- **Model routing** — `<env-root>/Process/Model_Routing.md`: how to choose
  the model/effort tier per task (mechanical → cheap, judgment/irreversible → strong).
- **Routing posture** — `ROUTING_BIAS: 1` (balanced). This project's standing model/effort lean;
  see `Model_Routing.md` §0 (**0** economy · **1** balanced · **2** quality). Change the integer
  to make this project lean cheaper/stronger by default; a per-session choice overrides it. Set it
  to match the project's stakes (e.g. a shipping commercial product often wants `2`; a throwaway
  utility `0`). Absent ⇒ balanced.

## Trigger phrases

Summaries — the canonical procedures live in `<env-root>/Process/Development_Process.md`.

| Phrase | Meaning |
|---|---|
| **Initialize** | First run on a fresh project — full bootstrap. <Note status once done, e.g. "Done: v0.0.0.".> |
| *(normal work)* | Feature loop: implement → `test` → track → changelog → **patch** bump → commit. One feature = one commit = one patch = one changelog entry = one tracker item to Built. |
| **Track this: …** | Add a `TRK-NNN` to Requested in `tracker.md`; do not start it. |
| **Resume** | New session, or the far side of a context clear — run `python <env-root>/Commands/thread.py show`. It carries the focus, the next action and its origin, the constraints in force, and the unfinished work. **Verify the working tree is clean.** Uncommitted work is an interrupted unit: ask, never silently commit or discard. Then run `<doctor>`. |
| **Release** | Only when something ships. Run audit rounds until `audit-gate.py` prints `GATE CLEAR`; run the file audit; reconcile the tracker; **purge `output/previews/`**; run the `bench` checkpoint; **produce the distributable when the toolchain allows, and record exactly what is missing when it does not** — never skip silently; **verify `test` and `doctor` are green**; bump the version; tag; push the commit and the tag when a remote exists. A missing remote never blocks a release. |
| **Perform audit** | Run a round per `Audit_and_Testing.md`: four lenses, one finding to a fragment; change no code. |

## Commands

> The toolchain may not be on PATH. Say how the commands resolve it (an env var and/or a pinned
> default path), then list one line per command. Keep the names generic: `setup / run / test /
> doctor / build / clean / bench`.

The toolchain is resolved from `<ENV VAR>` or the pinned default `<PATH>`. Run from the repo
root — a set changes nothing about how this project builds:

- `<setup>` — take a fresh checkout to runnable (install deps / import assets).
- `<doctor>` — verify readiness (toolchain, version, critical config, imports, tests). **Resume
  runs this.**
- `<test>` — run the test suite headlessly; exit 0 only if all pass.
- `<run>` — launch the app. <Note if this is only a convenience and not an on-target check.>
- `<build>` — produce the distributable (or report exactly what's missing).
- `<clean>` / `<bench>` — clear caches; run the performance benchmark.

## Architecture (the load-bearing boundaries)

> Name each module, its one responsibility, and what it must **not** reach into. Name the single
> sources of truth (the one authoritative state object, the one place a rule is decided). This is
> the section that stops future work from quietly dissolving the boundaries.

- **<Module A>** — <one responsibility>; **must not** <forbidden reach>.
- **<Module B>** — <one responsibility>; **must not** <forbidden reach>.
- **<Single source of truth>** — <what object/function is authoritative for X; who consumes it>.

## Conventions that bite if ignored

> Keep the ones that apply; drop the rest. These are distilled from real projects.

- **Chat output is terse by default; records are not.** Telegraphic style OK in conversation —
  drop articles, use fragments, tables over prose; sacrifice grammar, never semantic content. No
  preamble, no recap, no restating tool output. **Exempt: commit messages, tracker/fragment
  bodies, changelog entries** — those are the permanent record and keep full deliberate prose.
  The distinction is load-bearing: chat is read once and discarded; a record is read by every
  future session, and its prose is what carries the reasoning forward.
- **Write every output in Simplified Technical English (ASD-STE100).** This covers chat, all
  project documents, source-code comments, and commit messages. Identifiers and code syntax stay
  as the language needs them. The full rules live in `Process/Writing_Standard.md`;
  read them before you write.
- **The design doc (`docs/core/Freelief_design.md`) is the live design authority — update it in the same
  unit of work.** Any change to a rule, a flow, or an architectural decision updates the design doc's
  affected prose **and** adds a dated Decision Log entry (annotate superseded entries; don't delete).
  The tracker/changelog record *that* something shipped; the design doc records the *current* rules.
- **Every tunable lives in configuration with a committed default — never an in-code constant.**
- **Randomness is explicit and seeded** (if the project has any): the seed/state lives in serialized
  state; no hidden global RNG. <Delete if N/A.>
- **Changes the automated tooling can't observe need owner verification on the target.** Headless/CI
  and even a desktop run can't confirm rendering, audio, on-device layout/scaling, or "feel" — a green
  test run does **not** verify them. Flag such changes for the owner to check on the real device/target
  and say so plainly; never claim a visual/on-target result is correct from an automated run.
- **Externally-editable config can be mangled — keep it minimal and let `doctor` guard it.** If any
  config file is also edited by another tool (a mobile/remote editor, a GUI, a formatter), that tool
  may re-save and silently strip or reorder settings. Keep such files comment-light, and have `doctor`
  verify the critical settings are still present and parse — at Resume especially.
- **Two standard root folders: `input/` is provided, `output/` is generated.** `clean` may remove
  all of `output/` and must never touch `input/` — it is the one place where deletion is not
  recoverable by rebuilding. `output/` is git-ignored unless the distributable *is* the deliverable.
- **`input/` holds exactly two folders, and containment decides git.** `input/committed/` is
  committed and pushed; `input/excluded/` never is, at any depth, with no per-file exceptions.
  **Before any commit or push touching `input/`, stop if something looks misfiled** — material in
  `committed/` that may not be the owner's to redistribute, or a file large enough to make the
  repository unpushable (GitHub rejects over 100 MB, and the blob stays in history). **Say what you
  see and wait. Do not move it, do not re-file it, and do not proceed on your own judgment** — the
  sorting is the owner's call, and a commit that leaves the machine cannot be recalled.
- **Preview artifacts → `output/previews/`, purged at every release.** Only the *generating*
  script/scene is committed, never its output (a generator that lives only in a chat transcript is
  one context-clear from being lost).
- **A release produces the distributable when the toolchain allows; otherwise record exactly what
  is missing** (export templates, SDK, signing identity, account) — never skip silently.
- **Know your save format's fidelity limits — round-trip it in a test.** Serialize → deserialize →
  re-serialize and assert equality; watch for silent precision/type loss (e.g. 64-bit integers through
  JSON, which stores numbers as doubles and rounds them).
- **Commits are authored as the project owner — no AI identity or co-author trailer — and end with
  the trailer line `Made-with: Code Continuum`.** Feature commits
  are local; **push at a release** to `<remote>` (`<url>`, <private/public>). `<main>` may
  sit ahead of the remote between releases. *(A set changes none of this. Each member has its own
  repository and its own tag space, so tags stay in the plain `vX.Y.Z` form.)*
- **Never commit** (see root `.gitignore`): <secrets / signing keys / credentials / licensed reference
  material / large binary masters>. Sanitize anything that must ship but contains them; enforce hardest
  before the first push to a remote.
