# Project Template System — Start Here

> **What this is:** a reusable, technology-agnostic documentation framework for AI-assisted
> software development. Run one design conversation against it, initialize the project, and
> every future phase — implementation, quality audits, performance validation, session
> the unit boundary — has a defined process behind it.
>
> This file is orientation for **you** (the human). The AI reads the other files.
>
> **There is one living process corpus**, spanning two folders: this one (the project-starter
> blanks) and `<env-root>/Process/` (the process docs projects point at). It is edited in
> place and every project reads the current version. There is nothing to pin and nothing to
> migrate. See *One template, pointed at, never copied* at the end.

---

## The Big Idea

Development happens in **two distinct phases with two different AI roles**:

| Phase | Actor | Input | Output |
|---|---|---|---|
| **1. Planning** | Claude Chat (or any conversational AI) | Your rough idea + `Design_Document.md` | A completed `[projectname]_design.md` — an implementation-ready specification |
| **2. Implementation** | Claude Code (or any coding agent) | The completed design doc + `Development_Process.md` | The working project, built one unit at a time |

The planning phase is a **guided interview**, not a form. Claude Chat acts as a senior
solution architect: it asks questions, explains why each answer matters, recommends
technologies with tradeoffs, challenges scope creep, and records every decision *with its
rationale*. Nothing about the stack is assumed — language, framework, storage, deployment,
and tooling are all **discovered and justified** during the conversation.

The implementation phase is **procedural**. Claude Code follows the Development Process:
it bootstraps the project from the design doc, works feature by feature in lockstep with a
tracker and changelog, checkpoints at the unit boundary, and survives context clears through
the thread.

Two additional workflows run **on demand**, outside normal implementation:

- **Audits** (`Audit_and_Testing.md`) — a round of four readers with separate briefs, each
  finding recorded as its own fragment. Run one during design whenever a design settles, and
  before every release, where a clean round is required. It finds problems; it does not fix them.
- **Performance validation** (`Performance_Testing.md`) — baselines and benchmarks
  woven into normal development, so performance is measured continuously instead of
  discovered broken at the end.

---

## How Projects Consume This Template (the distribution model)

**Nothing is copied into a project.** The docs split by who writes them, and each kind
has its own home:

- **Static-shared** — the process/reference docs a project only ever *reads*, living once
  at **`<env-root>/Process/`**: `Development_Process.md`,
  `Artifact_Formats.md`, `Performance_Testing.md`, `Audit_and_Testing.md`, `Writing_Standard.md`,
  `Path_Policy.md`, `Project_Sets.md`, `Agent_Scope.md`. The project's `AGENTS.md` points at them
  there.
- **Blank-consumed** — the project-starter blanks, living **here**
  (`Templates/_Project_Template/`): `Design_Document.md` (filled into
  `[project]_design.md` by the design interview), `AGENTS_Template.md` (filled into the
  root `AGENTS.md` at bootstrap, beside a one-line `CLAUDE.md` copied from
  `CLAUDE_Pointer.md`), `Set_Manifest_Template.toml` (filled into a new set's
  `set.toml`), `Instruction_Changelog.md` (seeded empty as the project's instruction log). The
  blanks stay here; only the filled children live in the project.
- **Project-local** — everything the project's development actually writes, all under the
  project's `docs/` folder: the **core artifacts** (filled design doc, `tracker.md`,
  `changelog.md`, instruction log) in `docs/core/`, plus technical references and
  performance docs in their own subfolders. Audit findings are fragments in `docs/fragments/`.
  The repo root stays clean — its .md files are `AGENTS.md`, which coding agents from any vendor
  read, and a one-line `CLAUDE.md` that loads it for Claude Code.

The project's `AGENTS.md` points at both homes and names no template version, because there is
one living corpus and every project reads it. See *One template, pointed at, never copied* at the
end for how that works in practice.

**Amendments are project-local.** When a project needs to change *how it works*, the
amendment goes in its own `AGENTS.md` and is logged in its instruction log — the shared
docs are never touched. On any conflict, the project's own documented amendment wins over
the shared doc.

### Project sets

A **project set** is a named group of projects that share documents, declared by one `set.toml`
manifest. **A set is a manifest, not a folder** — membership does not decide where a project sits on
disk. Every member keeps its own repository, remote, version, and release cadence. Use a set when
related projects share standing answers: a design language, a brand, a protocol, house conventions.

Two rules govern it:

> **The manifest is the truth.** Pointer stubs and folder layout are views, generated from it.
>
> **A shared document lives once, in the set directory. A member points at it, and never holds a
> copy.**

A set **includes** other sets, so an answer lives at the level where it is true. The Audio set owns
what is true for every piece of Effigy audio software; the dsp set, which Audio includes, owns what
is true only for DAW-inserted plugins. A dsp project is a member of both, and it is named in one
manifest.

**Nothing else about a member changes** — it is a whole project exactly as it was before joining,
which is why joining and leaving are both cheap. To leave, delete one manifest line; nothing moves
on disk. The failure a set prevents is drift: when each project holds its own copy of a shared note,
the copies diverge and nobody can say which is current.

| You have | Say |
|---|---|
| Projects that should become a set | **"Create set `<Name>`"** |
| An existing project that should join a set | **"Add `<Project>` to set `<Set>`"** |
| A new project that should start in a set | **"Initialize into set `<Set>`"** |

The rules and the step-by-step procedures live in
`<env-root>/Process/Project_Sets.md`. **A project that no manifest names ignores all
of this** — sets change nothing for it.

### The shared Knowledge Base (lives at the projects root)

The **tool-specific** gotcha knowledge base across **all** projects lives once at
`<env-root>/Process/Knowledge_Base/`, a sibling to every project.
Consult it for stack gotchas; append whenever a new lesson is paid for. (Generalizable
*process* lessons get folded into the shared process corpus instead.)

### The Godot mobile skeleton (sibling folder, for Godot games)

Godot mobile games don't scaffold the project from scratch — the runnable skeleton lives
once at `<env-root>/Templates/_Godot_Template/` (portrait
`project.godot`, a studio splash + credits, the `Audio` autoload, GUT, the `tools/`
commands, and a `plugins/` library). Initialize copies it, then runs the **plugin picker**
(`Development_Process.md` → Bootstrap → Scaffold): it presents
`_Godot_Template/plugins/plugins.json` and installs the chosen addons with
`tools/install-plugins.py`. Non-Godot projects ignore this and scaffold from the design
doc as usual.

---

## Quickstart — Starting a New Project

1. **Create an empty project folder** under `Projects/In-Dev/`. Copy nothing from here.

2. **Run the design interview.** Open a conversation with Claude Chat, attach or paste
   this generation's `Design_Document.md`, and say something like:

   > *"I want to design a new software project using this template. Here's my rough idea:
   > […]. Interview me until the design is complete."*

   Claude Chat will work through the stages — vision, scope, technology discovery,
   architecture, quality strategy, delivery plan — asking questions and recommending
   options. Expect this to take a real conversation, not five minutes. It's the highest
   -leverage hour of the whole project.

3. **Save the result** as `docs/core/[projectname]_design.md` (lowercase, e.g.
   `docs/core/deadweight_design.md`) in the project folder — create the folders if they
   don't exist yet (if you save it at the root instead, bootstrap moves it there). The
   interview isn't done until the Implementation Readiness Checklist at the end of the
   template passes.

4. **Open the folder in Claude Code** and say:

   > **Initialize** — using the project template at
   > `<env-root>/Templates/_Project_Template/`

   Claude Code reads the design doc and the process docs
   (`Process/`) **in place**, stands up the environment, scaffolds the
   project, creates the standard project commands, generates the project's root
   `AGENTS.md` from this folder's `AGENTS_Template.md` (populated from the design doc)
   and the one-line `CLAUDE.md` that loads it,
   seeds the tracker, changelog, and instruction log,
   sets up version control, and builds the first vertical slice.

---

## The Day-to-Day Rhythm (cheat sheet)

Condensed for orientation — the canonical trigger definitions live in
`Process/Development_Process.md`.

| You say | What happens |
|---|---|
| **Initialize** | First run — bootstrap the whole project from the design doc |
| *(normal work)* | Build features; each one is tested, committed, versioned, changelogged, and tracked automatically |
| **Track this: …** | Capture an idea into the tracker without building it now |
| **Resume** | New session, or the far side of a context clear — read the thread, verify the tree is clean, run `doctor` |
| **Perform audit** | Run a round per `Audit_and_Testing.md`: four lenses, one finding to a fragment, no code changed |
| **Release** | Ship it: full validation, version bump, tag, distributable |

**You do not schedule a checkpoint.** A unit of work opens before the first edit and closes when the
work is done, and the context clear fires at that boundary on its own. The environment measures what
a unit costs and arms the clear early enough that one more unit fits — so pacing is derived from
measurement rather than from a number you have to remember.

---

## Design Principles of This System

These templates deliberately **never assume** a language, framework, engine, database,
AI model, SDK, cloud provider, ide, VCS workflow, CI/CD pipeline, build system, testing
framework, or methodology. Those are *project decisions*, discovered and recorded during
the design interview. The process documents refer to them symbolically ("the project's
`test` command", "the VCS chosen in the design doc") so the same process works for a
game, an API, a CLI tool, or an embedded system.

Other load-bearing principles, learned from real projects built with earlier generations:

- **Decisions over descriptions.** Every significant choice is recorded with its rationale
  and the alternatives rejected, so it never gets silently relitigated.
- **Documentation duties are procedural, not aspirational.** Docs update in the *same
  commit* as the code they describe — that's the only thing that keeps them true.
- **One source of truth per fact.** Version lives in one place; each subsystem has one
  owning technical reference; the tracker is the only feature record — and each process
  rule has one owning doc, with summaries elsewhere deferring to it.
- **Re-entry is the thread.** The thread carries the focus, the next action and where it came
  from, the constraints in force, and the unfinished work, so nothing in flight drops silently
  when the context clears. Read it first in every session.
- **Findings before fixes.** Audits and reviews produce findings; changes flow through the
  normal tracked feature loop, never as invisible side effects.
- **Performance is continuous.** Baselines start at the walking skeleton and every release
  compares against them, so there are no end-of-project surprises.

---

## One template, pointed at, never copied

**These files are the template.** There is no version directory to resolve and nothing for a project
to pin. A project's `AGENTS.md` names no template version, because there is one.

- **Improve the corpus in place.** Edit the file that owns the rule, and every project has the change
  at once. That is what pointing rather than copying is for.
- **Record what you changed in `../TEMPLATE_CHANGELOG.md`.** It is the only place that says what
  moved and when, and every project you have picked the change up the moment you saved it.
- **Nothing is migrated and nothing is re-pinned.** There is no migration step, because there are no
  two versions for a project to be between.
