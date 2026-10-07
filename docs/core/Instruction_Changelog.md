# Instruction Changelog

The dated audit trail of amendments to **how we work** — the instructions in `AGENTS.md`, the
design doc, and this project's deviations from the shared process docs (`<env-root>/Process/`)
and trigger phrases. The operative rules live in those docs; this file records *when* and *why*
each instruction changed, and *where* it now lives. Newest on top.

**Rule for this file:** when an instruction changes, add an entry here **and** update the operative
doc it points to in the same unit of work.

**Stack-specific gotchas go elsewhere:** tool / engine / target-device lessons belong in the shared
**Knowledge Base** (`<env-root>/Process/Knowledge_Base/`, one file per tool), not here —
this log is only for changes to *how we work* (process/instructions).

---

<!-- Entry template — copy for each change, newest on top:

## YYYY-MM-DD

### <Short imperative title of the instruction change>
- **Instruction:** <the new rule, stated operatively>.
- **Why:** <what prompted it — owner directive, a bug it prevents, a lesson learned>.
- **Encoded in:** <the operative doc(s) updated in the same unit of work — e.g. AGENTS.md → Conventions;
  a tool script; .gitignore. Never a shared process doc — those are immutable>.
- <Owner | agent>, YYYY-MM-DD.

-->

## 2026-10-07 (later still)

### Pages serves the `live` branch; main no longer deploys
- **Instruction:** GitHub Pages serves `live`. Pushing `main` deploys nothing. Before 1.0, `live` is
  a public preview and moves only with the owner's yes for that move; from 1.0 on it moves only at a
  release, after `audit-gate.py` prints `GATE CLEAR`, to a tag. The README says the app is a preview
  and does not invite installs until 1.0.
- **Why:** audit finding AUD-003. A push to `main` was a public deploy, so the release gate could
  never apply to what users get. The owner chose a separate `live` branch and to keep the site up as
  a marked preview. This replaces "a push deploys" in the entry below.
- **Encoded in:** `AGENTS.md` (Commands: Deploy; Conventions: commits and remote; Release);
  `docs/README.md`; GitHub Pages source set to `live`.
- Owner, 2026-10-07.

## 2026-10-07 (later)

### The remote exists; a push deploys *(replaced by the entry above)*
- **Instruction:** `origin` is the public repository `https://github.com/EffigyMedia/freelief`, and
  GitHub Pages serves `main`. Push only at a release or when the owner needs a phone build.
- **Why:** the owner approved creating and publishing it after all five slices were built. This
  closes the entry below, "Create the GitHub repository when slice 1 is ready, public".
- **Encoded in:** `AGENTS.md` (Conventions: commits and remote); `docs/README.md`.
- Owner, 2026-10-07.

## 2026-10-07

### Keep the design document at `docs/Design_Document.md`
- **Instruction:** the design document stays at `docs/Design_Document.md`. It does not move to
  `docs/core/Freelief_design.md`.
- **Why:** `Development_Process.md` Phase 1 step 6 says to move it to `docs/core/`, but
  `Commands/srs.py` and `prd.py` read only `docs/Design_Document.md`, by a fixed path, on purpose.
  A move would make both generated documents silently lose every narrative section. The shared
  documents disagree; the tool path is the one that breaks if it is wrong. The environment is told
  through its inbox.
- **Encoded in:** `AGENTS.md` (What this is; Conventions).
- Agent, 2026-10-07.

### Create the GitHub repository when slice 1 is ready, public
- **Instruction:** Initialize does not create the remote. The public repository
  `EffigyMedia/freelief` is created when slice 1 is ready, with the owner's yes at that time.
- **Why:** the owner decided this in the design interview (Decision Log, 2026-10-07). It overrides
  `Development_Process.md` Phase 1 step 7, which creates a private remote during Initialize.
- **Encoded in:** `AGENTS.md` (Conventions: commits and remote).
- Owner, 2026-10-07.

### The fragment store is the tracker; there is no `tracker.md`
- **Instruction:** tracker items are `RLG-` fragments of type `feature` in `docs/fragments/`. This
  project keeps no `docs/core/tracker.md`. The changelog links to the fragment files.
- **Why:** `Commands/tracker.py` writes a view whose header describes the environment's own roadmap
  and frozen line, which is false for a project. Effigy Arcade keeps no tracker file for the same
  reason.
- **Encoded in:** `AGENTS.md` (trigger phrases); `docs/core/changelog.md` header.
- Agent, 2026-10-07.

### Root template files removed
- **Instruction:** the repository root holds no `.md` file except `AGENTS.md` and `CLAUDE.md`.
- **Why:** the standup left the template's own `README.md` and `START_HERE.md` at the root. They
  describe the template, not Freelief. A public README for GitHub goes in `docs/README.md` when the
  repository is created.
- **Encoded in:** `AGENTS.md` (What this is).
- Agent, 2026-10-07.
