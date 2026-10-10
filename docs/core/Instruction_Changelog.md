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

## 2026-10-10

### Sweep a removed or renamed screen from every place that names it
- **Instruction:** a removed or renamed screen is swept in the same unit from the design (module
  table, tunables, F-flows, vocabulary, risk table), the technical references, the `config.json`
  groups, the strings, the issue templates, `docs/README.md` and RLG-033. `test_repo.py` fails on a
  retired screen name in a shipped string or a template, and when the GitHub accessibility template
  and the in-app checklist differ.
- **Why:** AUD-143 and the sweep findings of round UNT-124 (AUD-138 to AUD-145): the removals of
  Sort colors, the trace, the Standards page and the Visualizer's name were each swept once and
  missed clauses.
- **Encoded in:** `AGENTS.md` (Architecture, beside the four-list rule); `tools/tests/test_repo.py`.
- Agent, 2026-10-10.

### The changelog allows one later addition: the line that records a live move
- **Instruction:** a changelog entry is never edited after the fact, except that the line recording
  a move of the live preview is added to the entry of the version it serves, on the day of the move.
  `docs/README.md` names no version; the newest `preview-` tag says what the preview serves.
- **Why:** AUD-149 and AUD-144: the move rule added lines to entries that the header said were never
  edited, and the README's version went stale at every move.
- **Encoded in:** `docs/core/changelog.md` (header); `docs/README.md`; design section 7 row 10.
- Agent, 2026-10-10.

### Every live move runs bench; a run is valid only near the baseline's load
- **Instruction:** each move of `live` runs `bench` and records the run in the performance log from
  `output/bench-log-draft.md`. A bench run is valid, and compared with the baseline, only when its
  busiest CPU load is at most the baseline's load plus 5 points, and never over 35%.
- **Why:** AUD-134 and AUD-135. The urgent-help response crossed its target with no bench run
  between v0.7.13 and round UNT-124, and runs at 33% to 35% load were compared with a baseline taken
  at 22% to 27%.
- **Encoded in:** `AGENTS.md` (Conventions, the remote); `docs/performance/baseline.md` (Baseline
  load); `tools/bench.py` (`COMPARABLE_MARGIN_POINTS`, `write_log_draft`).
- Agent, 2026-10-10.

### Tag every move of the live preview
- **Instruction:** each move of `live` before 1.0 tags its commit `preview-X.Y.Z` and pushes the
  tag. An incident rolls `live` back to the previous `preview-` tag before 1.0, and to the previous
  release tag from 1.0.
- **Why:** AUD-121. The Incident row named a release tag that did not exist, and a stale local
  `live` branch pointed at v0.5.0, so a hurried rollback had no safe target.
- **Encoded in:** `AGENTS.md` (the Incident row; Conventions, the remote); `docs/Design_Document.md`
  (section 7 row 7; section 9, Incidents).
- Agent, 2026-10-10.

### Retire an owner check when its screen is removed
- **Instruction:** when a screen is removed, its owed checks in RLG-033 are retired or moved in the
  same unit, each by name with its successor.
- **Why:** AUD-127. RLG-033 held checks on Sort colors after it was removed, so under its own close
  rule it could never close.
- **Encoded in:** `AGENTS.md` (Conventions, the RLG-033 line); RLG-033 (the note of 2026-10-10).
- Agent, 2026-10-10.

### The design's version must have a Change Log entry
- **Instruction:** Document Control's version has a row in the design's Change Log; `test_repo.py`
  fails when it does not. The size plan in design section 9 sets what each slice may spend.
- **Why:** AUD-045 and AUD-126 (the design named version 1.3 with no row, twice); AUD-124 (the size
  was at 95% of the limit with no plan).
- **Encoded in:** `docs/Design_Document.md` (sections 9 and 15);
  `tools/tests/test_repo.py` (`test_the_design_version_has_a_change_log_entry`).
- Agent, 2026-10-10.

### No standards claim and no research page
- **Instruction:** the app shows no standards claim and no research page; REQ-020, REQ-024 and
  REQ-029 are withdrawn. The release build no longer checks verified standards.
- **Why:** the owner's ruling, 2026-10-10 (RLG-056): most of the research is limited or indirect.
- **Encoded in:** `AGENTS.md` (What this is; Architecture; Release); `tools/freelief.py`.
- Owner, 2026-10-10.

### The config rule covers the shipped app; tool limits stay in the tools
- **Instruction:** every tunable of the shipped app lives in `config.json`. A development tool keeps
  its limits as named constants at the top of its file; the bench baseline is read from
  `docs/performance/baseline.md`, so it has one source.
- **Why:** AUD-123. The rule read as covering the tools too, and bench's baseline was a second copy
  kept in step by hand.
- **Encoded in:** `AGENTS.md` (Conventions); `tools/bench.py` (`read_baseline`).
- Agent, 2026-10-10.

## 2026-10-09

### The shared helpers' storage rule is restored, and background.js is a helper
- **Instruction:** `audio.js`, `haptics.js`, `wakelock.js` and `motion.js` must not touch storage
  except by reading `settings.js`. `background.js` plays the background sound and never touches
  storage. `python tools/freelief.py files` is listed under Commands.
- **Why:** AUD-117. A sed edit in UNT-094 (v0.7.6) deleted the rule and doubled a half-line, and
  the background.js addition had no entry here.
- **Encoded in:** `AGENTS.md` (Architecture; Commands); the design, section 8 module table;
  `tools/tests/test_repo.py` (`test_agents_md_repeats_no_line`).
- Agent, 2026-10-09.

### The Release row runs in order: prepare, validate, gate, tag, deploy last
- **Instruction:** the crisis-line re-check and the version bump come first, then the file audit,
  bench, `build --release`, `test` and `doctor`, then the audit rounds to `GATE CLEAR`, then the tag
  and the push, and `live` moves last. A fix for a round goes back to the start, so the tagged commit
  is the audited commit.
- **Why:** AUD-078. The old row moved `live` right after the gate and before the tag existed, and
  changed shipped files after `GATE CLEAR`.
- **Encoded in:** `AGENTS.md` (trigger phrases: Release).
- Agent, 2026-10-09.

### The file audit is a command
- **Instruction:** "the file audit" is `python tools/freelief.py files`: it lists every shipped file
  and fails when the offline copy and the shipped files disagree.
- **Why:** AUD-108. The Release row named a step that nothing defined.
- **Encoded in:** `tools/freelief.py` (`files`); `AGENTS.md` (Release).
- Agent, 2026-10-09.

### An incident may roll back at once
- **Instruction:** the owner may move `live` back to the previous release tag at once, with no round,
  and records it the same day. A fix forward runs a scoped round.
- **Why:** AUD-105, owner's ruling 2026-10-09.
- **Encoded in:** `AGENTS.md` (trigger phrases: Incident); the design, sections 7 and 9 and the
  Decision Log.
- Owner, 2026-10-09.

### A new screen goes into four lists
- **Instruction:** `ROUTES` and `QUIET_FOOTER` in `app.js`, `FILES` in `sw.js`, and `ITEMS` in
  `screens/menu.js`. Tests check all four.
- **Why:** AUD-100. AGENTS.md named two.
- **Encoded in:** `AGENTS.md` (Architecture); `tools/tests/test_repo.py`.
- Agent, 2026-10-09.

### The network claim names the update and the repair
- **Instruction:** after install, only the update check and the download of Freelief's own files to
  update or repair it reach the internet.
- **Why:** AUD-098, owner's ruling 2026-10-09. AGENTS.md said "no network call after install".
- **Encoded in:** `AGENTS.md` (What this is); REQ-015; `about.privacy1`.
- Owner, 2026-10-09.

### Recorded late: three instruction changes of 2026-10-08
- **Instruction:** (1) pending owner checks live in `RLG-033`, appended with `fragment.py append`,
  and it closes only when the owner reports them all (AUD-017); (2) the routing posture is read from
  `config.toml` `[routing] bias` (AUD-022); (3) the test command names the supported browsers and
  the WebKit run in `test_engines.py` (AUD-028).
- **Why:** AUD-096. They were made in UNT-079 and UNT-081 without an entry here.
- **Encoded in:** `AGENTS.md` (Conventions; Routing posture; Commands); `config.toml`.
- Agent, 2026-10-09.

## 2026-10-08

### doctor checks more, and says what it checks
- **Instruction:** AGENTS.md's doctor line now names every check: a browser launches for the tests,
  every shipped JSON file exists and parses, `sw.js` imports `version.js` and lists only files that
  exist, and every test file compiles.
- **Why:** audit findings AUD-012, AUD-034, AUD-035 and AUD-036 (round UNT-051, fixed in UNT-075).

### The Release row runs `build --release`
- **Instruction:** at a release, run `build --release`. It fails on uncommitted shipped files, on a
  shipped file changed after the last version bump, and on crisis data checked more than
  `crisis.maxCheckAgeDays` days ago.
- **Why:** audit findings AUD-010, AUD-011 and AUD-024 (round UNT-051, fixed in UNT-074).

### AGENTS.md says Freelief opens on the menu, and names every shipped module
- **Instruction:** Freelief opens on the menu ("What would help right now?"), with Breathe first and
  one tap away. `#menu` is the default route, and a screen that cannot load falls back to it. The
  Architecture section names the Visualizer (`activities/calm.js`), the shared helpers `audio.js`,
  `haptics.js`, `wakelock.js` and `motion.js`, and `fallback.js`, each with what it must not do.
- **Why:** audit findings AUD-064 and AUD-069 (round UNT-051). The owner decided on 2026-10-07 to
  open on the menu (REQ-018, Decision Log), but AGENTS.md still said, as a crisis rule, that the
  breathing guide starts at launch and that `#breathe` is the default. A later session that followed
  it could reverse the owner's decision. Three shipped modules had no stated owner or limit.
- **Encoded in:** `AGENTS.md` (What this is; Architecture); `docs/Design_Document.md` (F1, F2, F5,
  Stages 2, 4, 6 and 8, the Decision Log notes); `docs/README.md`.
- Agent, 2026-10-08.

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
