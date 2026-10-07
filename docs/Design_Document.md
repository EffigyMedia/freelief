# Design Document — Conversational Blueprint

> **What this is:** the template for a project's founding design document — but it is
> **not a form to fill in**. It is an interview script for an AI design partner.
>
> **Who reads this:** Claude Chat (or any conversational AI acting as solution architect),
> together with the project owner, during **Phase 1 — Planning**.
>
> **What it produces:** two things at once. A completed **`docs/Design_Document.md`** — this
> file, with the interview guidance removed and real content in its place — and a **requirement
> record for every obligation agreed along the way**. The document is the single source of
> truth that Claude Code implements from in **Phase 2**; the records are what the
> specification and the product document are generated from.
>
> **The filename is fixed and is not a style choice.** `srs.py` and `prd.py` read
> `docs/Design_Document.md` by that exact path. They do not search for a design-looking file,
> because a search would find an old draft or another product's notes and lift narrative out
> of it into a document whose first line says it was generated from this line's records.
> Rename this file and both generators quietly stop finding anything.

---

# Part I — Instructions for the Interviewer

You (the AI reading this) are acting as a **senior solution architect running a discovery
session**. The owner has a rough idea; your job is to transform it into an
implementation-ready specification through conversation. You are not a stenographer — you
are a collaborator with opinions, experience, and the obligation to say "that's a risk"
out loud.

## Ground Rules

1. **One theme at a time.** Work through the stages in Part II conversationally. Never
   dump a wall of questions; ask 2–4 related questions, digest the answers, follow up.
2. **Explain why before asking.** Each stage's *Why this matters* is there to be shared —
   an owner who understands why a question matters gives better answers.
3. **Never assume technology.** No language, framework, engine, database, cloud, SDK,
   AI model, ide, VCS workflow, CI/CD pipeline, build system, or testing framework is a
   default. Every technology enters the document through Stage 7 (Technology Discovery)
   as an explicit, justified decision.
4. **Recommend — with tradeoffs.** When the owner is unsure, don't just list options:
   name a recommendation, give the honest tradeoffs, and let them decide. Record what was
   rejected and why, not just what won.
5. **Classify everything you capture** as one of:
   - **Requirement** — the software *shall* do this. It becomes a record immediately, not a
     line in this document. See *Recording As You Go*.
   - **Decision** — settled; goes in the Decision Log with rationale.
   - **Assumption** — taken as true but unverified; flagged in Stage 11.
   - **Open question** — genuinely undecided; parked in Stage 11 so nobody silently guesses.
6. **Capture rationale, not just answers.** "PostgreSQL" is an answer; "PostgreSQL,
   because we need relational integrity across orders and inventory, and the owner already
   operates one" is a decision. The rationale is what prevents relitigating later.
7. **Challenge constructively.** Probe scope creep ("does v1 really need accounts?"),
   missing edge cases ("what happens when the file is empty?"), unstated constraints
   ("who pays for hosting?"), and optimistic estimates. The interview is the cheapest
   place in the entire project to find a problem.
8. **Play back before recording.** At the end of each stage, summarize what you're about
   to record and get confirmation. Corrections at this point are free.
9. **Skip explicitly, never silently.** If a stage doesn't apply (a CLI has no visual
   design), record `N/A — <one-line reason>` in the document rather than deleting the
   section. A visible N/A tells the implementer the topic was considered.
10. **Adopt the owner's vocabulary.** The words the owner uses for domain concepts become
    the project's vocabulary (Stage 4). Don't rename their world.
11. **Don't declare done until the Readiness Checklist (Stage 13) passes.** An incomplete
    design doc costs ten times more during implementation than one more hour of interview.

## Recording As You Go

Two kinds of thing leave this conversation, and they leave it by different routes. Getting
this right is what makes the specification and the product document generate themselves
instead of being written a second time by hand.

### A requirement becomes a record the moment it is agreed

**Do not collect requirements in prose and write them up afterwards.** The moment the owner
agrees that the software *shall* do something, write it as a record, in the conversation,
before moving on. Then say so, in one line, so the owner can correct it while it is cheap.

```
python Commands/fragment.py new --kind requirement --title "<the requirement, in one sentence>" \
    --category function --verification test --priority must --status proposed
```

Four fields, and none of them is optional thinking:

| Field | What it is | Why it is asked now |
|---|---|---|
| `--category` | `function`, `performance`, `usability`, `interface`, `database`, `constraint` or `attribute` | It decides which clause of the specification the requirement is printed under. A requirement with no category has nowhere to go. |
| `--verification` | `inspection`, `analysis`, `demonstration` or `test` | How this will be shown to be met. A requirement whose verification is "we will look at it" is one nobody has thought about. |
| `--priority` | `must`, `should` or `could` | What will not be built is a **Non-Goal** and belongs in Stage 3, not a record with a priority that reads as a plan. |
| `--status` | `proposed` until the owner agrees, then `agreed` | A `proposed` requirement is still a question. Nothing proposed reaches the specification, which is what stops the document claiming an obligation the owner never accepted. |

**One requirement, one record, stating it as it stands.** A requirement that changes is
edited in place with its history beneath it. Do not write a second record about the same
obligation: a reader who finds two has to work out which one is true.

**The design document does not restate them.** A stage that produces requirements says so
and moves on. Copying the requirement back into this document creates a second place for it
to be true, and the two disagree the first time one is edited.

### Narrative goes in a marked region

Some of what a specification needs is not a requirement and no record can hold it: a
purpose, a scope statement, the measure of success, a glossary. Those live in **marked
regions** in this document, and the generators lift them out.

A region looks like this, and the words go between the two comment lines:

    <!-- BEGIN <region-name> - written by the interview, read by the generators -->
    <!-- END <region-name> -->

**The name in that example is a placeholder on purpose.** An example carrying a real region
name would BE a region: it is a comment line holding the key, it sits above the stage that
owns that name, and the reader takes the first one it finds. The specification would then
report the clause as present and empty, and the interview's real answer, further down this
file, would never be read. The first draft of this template did exactly that.

Three rules, each earning its place:

1. **Write inside the markers, never around them.** Everything outside them is yours and is
   not read.
2. **An empty region is reported as empty.** Leaving one blank is not the same as never
   having been asked, and the generated document says which it was. So fill it, or say in
   it why it is empty.
3. **Do not delete a region you are not using.** `N/A — <reason>` inside it tells the
   implementer the topic was considered. A deleted region reads as a document that predates
   the question.

Each region below appears at the stage whose answers fill it. You do not need to know which
clause of which document it feeds; the name is the whole of the contract.

---

## Calibrating Depth

Ask early: *roughly how big is this?* Then scale the interview:

| Tier | Feels like | Interview depth |
|---|---|---|
| **Utility** | Hours–days of build; single purpose; one user (often the owner) | Stages 1–3, 5, 7, **9 (brief)**, 10, 12–13 required; others usually N/A. Stage 9 may be minimal: the test approach plus an explicit, reasoned call on whether performance matters (a reasoned N/A is fine; silence is not). Aim for a document a few pages long. |
| **Standard** | Weeks of build; real users; several subsystems | All stages, moderate depth. This is the default assumption. |
| **Complex** | Months+; many users; integrations, compliance, or novel technical risk | All stages, full depth; expect multiple sessions and revisit stages as understanding grows. |

Depth calibration changes *how much* you explore, never *whether decisions get rationale*.

## The Interview Arc

The stages in Part II are ordered so each builds on the last: **what and why → for whom →
how big → in what language (domain) → doing what → feeling how → built with what → shaped
how → verified how → delivered in what order → what could go wrong**. Follow the order by
default, but the conversation may loop back — a technology constraint discovered in
Stage 7 may legitimately reshape scope in Stage 3. When that happens, update the earlier
stage and note the change in the Decision Log.

## Producing the Final Document

When the checklist passes:

1. Write the completed document **in place, as `docs/Design_Document.md`** — same numbered
   sections, guidance blocks removed, real content in place, every marked region filled or
   carrying its `N/A — <reason>`. Keep decisions, rationale, and rejected alternatives
   visible. Do not rename it and do not write it somewhere else: the generators read that
   path and nothing else.
2. Move every agreed requirement from `proposed` to `agreed`. Until that happens the
   specification is empty by design, because a proposed requirement is still a question.
3. Generate both documents and read them:

   ```
   python Commands/srs.py --line <this line>
   python Commands/prd.py --line <this line>
   ```

   **Read what they say is missing.** A clause reading *Not supplied* names the stage its
   content should have come from, and a clause saying the region exists and is empty means
   the interview reached that heading and left it blank. Both are the interview telling you
   where it stopped, while the owner is still in the room.
4. Remind the owner: this document is **living**. During implementation, settled answers to
   new questions land in the Decision Log; scope changes update Non-Goals; a requirement
   that changes is edited in its own record and a requirement that is dropped becomes
   `withdrawn` rather than deleted. The document, the records, and the code must never
   disagree.

---

# Part II — The Design Document Structure

Each stage below has: **Why this matters** (share it), **Explore** (the questions —
adapt, don't recite), and **Record** (the fields the final document must contain).

---

## 0. Document Control *(required)*

**Record:**
- Version / date, owner, status (draft → interview complete → in build → stable)
- **One-line pitch** — the whole project in a sentence: what it is and who it's for.
- Tier (Utility / Standard / Complex) — set during depth calibration.
- **Routing posture** — the project's default model/effort bias (`ROUTING_BIAS`: **0** economy
  / **1** balanced / **2** quality; see `Process/Model_Routing.md` §0). Derive it from
  the project's stakes, don't guess: a shipping/commercial product where rework is costly or
  changes are hard to reverse leans **quality (2)**; a throwaway or exploratory utility leans
  **economy (0)**; most projects sit **balanced (1)**. It's a default, tunable later and
  overridable per session — but recording it here means bootstrap sets it right instead of
  defaulting blindly. (Loose mapping, not a rule: Utility→often 0, Standard→1, Complex→often 2.)


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-references`* — The documents this specification depends on - a standard, a protocol, a supplier's sheet, another project's design. One per line, each findable by what is written here. No record carries these, so a project that depends on none says that here.

<!-- BEGIN srs-references - written by the interview, read by the generators -->
<!-- END srs-references -->

---

## 1. Vision & Purpose *(required)*

**Why this matters.** Every downstream decision — features, stack, architecture — is
judged against the purpose. A fuzzy purpose produces a project that does many things
poorly.

**Explore.**
- What problem does this solve? For whom? What do they do today instead, and why is that
  inadequate?
- Why does this deserve to be built — what's the payoff if it works?
- Is there an existing product/tool that almost solves it? What's the gap?
- What does wild success look like a year after release?

**Record.** Problem statement; status quo and its inadequacy; the core insight or
opportunity; what success looks like.


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-purpose`* — Why this software exists, in a few sentences: the problem it solves and who for. This is the first thing a reader of the specification meets.

<!-- BEGIN srs-purpose - written by the interview, read by the generators -->
<!-- END srs-purpose -->

*`prd-problem`* — The problem itself, stated so that somebody who knows nothing about the solution understands it. Not the feature that answers it - the thing that is wrong today.

<!-- BEGIN prd-problem - written by the interview, read by the generators -->
<!-- END prd-problem -->

*`srs-product-overview`* — What the product is, where it sits, and what it works with. The paragraph you would give somebody before they read a single requirement.

<!-- BEGIN srs-product-overview - written by the interview, read by the generators -->
<!-- END srs-product-overview -->

---

## 2. Users & Success Criteria *(required)*

**Why this matters.** "Who is this for" decides platform, UX depth, error-message tone,
performance targets, and how much polish v1 needs. Success criteria become the acceptance
bar the implementation is verified against.

**Explore.**
- Who are the distinct user types? What's each trying to accomplish, in what context
  (desk, phone, terminal, another program calling an API)?
- How technical are they? How forgiving?
- How will you *know* it's working — what would you measure or observe? Push for concrete,
  testable criteria ("I can process a week's invoices in under 10 minutes" beats "it's fast").
- What's the difference between *usable*, *good*, and *done* for this project?

**Record.** User types with goals and context; concrete success criteria (each one
verifiable); explicit quality bar for v1.


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`prd-users`* — Who it is for. The distinct user types, what each is trying to accomplish, and in what context.

<!-- BEGIN prd-users - written by the interview, read by the generators -->
<!-- END prd-users -->

*`prd-success`* — How we will know it worked. A measure, not a feeling: each line something somebody could check and disagree with.

<!-- BEGIN prd-success - written by the interview, read by the generators -->
<!-- END prd-success -->

---

## 3. Scope, Principles & Constraints *(required)*

**Why this matters.** The Non-Goals list is the single most valuable section for an AI
implementer — it prevents scope creep and gold-plating. Principles break ties when two
good options compete. Constraints are the walls the design must fit inside.

**Explore.**
- What are you deliberately **not** building — now, or ever? (Propose candidates: does v1
  need auth? multi-user? mobile? offline? localization? Push each one out unless it earns
  its place.)
- What 3–6 principles should break ties? (e.g. "speed of use beats feature breadth",
  "never lose user data", "boring technology over novel".)
- Hard limits: budget, timeline, team, target platforms/OS/hardware, legal/compliance,
  data residency, systems that must be integrated with, skills the owner wants to use or
  avoid.
- Greenfield or not: does this build on or integrate with code that already exists? If
  existing: where it lives, what state it's in, and what must not break.

**Record as requirements.** A HARD constraint is a record with `--category constraint` - a
design decision imposed from outside rather than derived from a need. A preference is not: it
is a principle, and it belongs in this document where a tie-break can read it. A Non-Goal is
neither, and never becomes a record: a requirement that will not be built is a plan nobody
has, which is why `--priority` has no fourth value.

**Record.** North-star principles (3–6); Non-Goals (explicit, dated); constraints
(each marked *hard* or *preference*); greenfield, or the existing-code baseline (what it
builds on and what must not break).


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-scope`* — What this software covers - what it does, what it does not, and where the boundary runs.

<!-- BEGIN srs-scope - written by the interview, read by the generators -->
<!-- END srs-scope -->

*`prd-out-of-scope`* — What is deliberately not being built, and why. The Non-Goals list in prose. A reader should finish it knowing what NOT to ask for.

<!-- BEGIN prd-out-of-scope - written by the interview, read by the generators -->
<!-- END prd-out-of-scope -->

---

## 4. Domain Model & Vocabulary *(required for Standard+; brief for Utility)*

**Why this matters.** The core "nouns" of the system and their relationships become the
shared language of the code, UI, docs, and database. Consistent naming here prevents the
implementer from inventing synonyms across the codebase — a real and expensive failure mode.

**Explore.**
- What are the 5–15 things this system is *about*? For each: what is it, what are its key
  attributes, what's its lifecycle (created how, changed by what, deleted when)?
- How do they relate? ("An Order has many Items; a User owns many Orders.")
- Are there terms the owner uses that have a precise meaning in their world? Capture the
  precise meaning, not the dictionary one.

**Record as requirements.** What must PERSIST, and what must stay true of it, is a record with
`--category database` - a retention period, a uniqueness rule, a thing that survives a restart.
The entity list itself stays here: it is vocabulary, and vocabulary is not an obligation.

**Record.** Entity list with definitions, key attributes, and relationships; a
relationship summary (prose or simple diagram); any term with a project-specific meaning.


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-definitions`* — The terms this project uses with a precise meaning, defined. The nouns from the domain model, in the owner's words rather than the dictionary's.

<!-- BEGIN srs-definitions - written by the interview, read by the generators -->
<!-- END srs-definitions -->

---

## 5. Functional Specification *(required)*

**Why this matters.** This is *what the software does* — the section the implementer
returns to most. Numbered flows let the build plan and tracker reference them precisely.
Edge cases spelled out here don't become bugs later.

**Explore.**
- **Flows:** what do users (or calling systems) actually do, step by step? Trigger →
  steps → outcome, happy path plus the important alternates. Number them (F1, F2 …).
- **Features, prioritized:** Must / Should / Could (or the owner's scheme). Everything
  "Could" is a candidate Non-Goal — challenge it.
- **States & edge cases:** for each flow — empty state, loading/in-progress, success,
  failure, cancellation. What happens with missing, invalid, huge, or malicious input?
  Concurrent use? Interrupted mid-operation?
- **Inputs/outputs & interfaces:** file formats, validation rules, CLI flags, endpoints,
  function signatures — whatever the system's surface is.
- **Integrations** *(as applicable)*: external services, APIs, hardware, data sources.
  For each: auth model, rate limits, cost, and behavior when it's down.
- **Permissions & auth** *(as applicable)*: who may do what; sensitive operations.

**Record here.** Numbered flows, each with its states and edge cases; the integration list with
what happens when each is down; the permission model or N/A. These are structure - how the
software hangs together - and they belong in this document.

**Record as requirements.** Every *shall* that comes out of this stage is a record, written as
it is agreed and not collected into a list here. The prioritized feature list is NOT written in
this document at all: it is the set of records, and their priorities are the `--priority` field.
Writing it twice makes two places for it to be true.

- What the software does: `--category function`.
- What it exchanges, and in what shape - file formats, CLI flags, endpoints, signatures, the
  surface of each integration: `--category interface`.

An edge case is usually a requirement, not a note. "Rejects a file over 2 GB with a named
error" is verifiable and belongs in a record; "we should think about big files" is neither.

---

## 6. Experience & Interface *(as applicable — anything with a user-facing surface)*

**Why this matters.** "How it should feel" can't be inferred from a feature list. This
applies to CLIs and APIs too — ergonomics is experience. For anything visual, direction
recorded here saves rounds of rework later; for aesthetic decisions, the Development
Process has the implementer present *variants* before committing, and this section is
what those variants are judged against.

**Explore.**
- Interaction model: what does using it feel like? What must be instant, what may be slow?
  What's the information hierarchy — what does the user see first?
- Visual direction *(GUI only)*: look and feel, layout, references/inspiration, design
  system if any.
- Accessibility & internationalization: targets, languages, formats — or an explicit N/A.
- Content & tone: error messages, empty states, naming — who is the software "being"
  when it talks?

**Record here.** Interaction principles; visual direction with references or N/A;
tone-of-voice notes.

**Record as requirements.** An accessibility or internationalization target that somebody
could fail is a record with `--category usability`, not a note: "every control reachable
by keyboard" can be verified and "accessible" cannot. A target with no way to check it
is an aspiration, and the interview is where that difference is cheapest to find.

---

## 7. Technology Discovery *(required — the stage where the stack is chosen, never assumed)*

**Why this matters.** Technology choices are the least reversible decisions in the
project. Made implicitly, they're made badly. Each choice below must be **discovered**
from the requirements above and **justified** — with alternatives named and rejected for
stated reasons. The owner's existing skills, infrastructure, and preferences are
legitimate inputs; silence is not.

**Explore — work through each, in roughly this order, letting earlier answers constrain
later ones:**

1. **Delivery platform(s):** desktop, mobile, web, terminal, server, embedded, plugin —
   where does this run? (Driven by Stage 2's users-in-context.)
2. **Language & runtime:** what fits the platform, the problem domain, the performance
   needs, and the owner's ability to maintain it later?
3. **Frameworks, engines & key libraries:** what does the heavy lifting? What should
   deliberately *not* be used, and why?
4. **Persistence:** does state need to survive restarts? Files, embedded DB, server DB,
   cloud storage — sized to actual need, not habit.
5. **External services & APIs:** anything bought/rented rather than built — including AI
   models/services if the project calls for them. Note cost, keys, quotas, offline behavior.
6. **Content & assets** *(as applicable)*: what non-code content does the product need —
   art, audio, fonts, copy, datasets, reference material? For each kind: who or what
   produces it (owner-made, commissioned, licensed, generated), the pipeline and formats,
   and the **license terms**. Anything licensed or third-party feeds the never-commit
   list (item 10) and must not silently depend on a CDN or external host at runtime.
7. **Deployment & distribution:** how does it reach users — an executable, a package, an
   app store, a hosted service, an internal path? What are the environments (dev / prod /
   others)? What's the release and rollback story?
8. **Testing toolchain:** what will run the tests the Quality stage defines? How will
   tests be invoked reproducibly?
9. **Development environment & tooling:** how are toolchains and dependencies isolated
   and reproduced? (Per-project environments, containerized, system — a *decision*, with
   the owner's machine hygiene preferences as input.) What are the standard project
   commands (`setup` / `run` / `test` / `doctor` / `build` / `clean` — see the Development
   Process) implemented with?
10. **Version control & backup:** which VCS, what workflow (the Development Process
    assumes commit/tag/checkpoint capabilities), where's the offsite copy, and is the
    remote private or public? What must *never* be committed (secrets, PII, licensed
    material) — this drives the ignore rules at bootstrap.
11. **CI/CD** *(as applicable)*: is automation warranted at this scale, or do the
    project commands suffice?

**Interviewer guidance.** Prefer boring, well-documented technology unless the project's
core value demands otherwise. Minimize the count of moving parts. Every "we might need it
later" is a candidate for the Non-Goals list, not the stack.

**Record.** For each numbered item: the **decision**, the **rationale**, and the
**alternatives rejected with reasons**. Plus: pinned versions where relevant; license or
cost constraints; the never-commit list.

---

## 8. Architecture *(required for Standard+; a paragraph may suffice for Utility)*

**Why this matters.** Module boundaries are the single best insurance for steering an AI
on a codebase the owner won't read line-by-line: a failure or change in one module stays
contained. Contracts let modules evolve independently. Naming the hard problems up front
is how they get de-risked instead of discovered.

**Explore.**
- **Modules:** what are the components, what does each own, and what must it *not* reach
  into? (One responsibility per module; one owning module per concern.)
- **Data model & state:** where does state live? Schemas/structures, migrations, data
  lifecycle (created, retained, deleted).
- **Contracts:** the interfaces between modules and to the outside — signatures,
  request/response shapes, error contracts, versioning.
- **Data flow:** how information moves; sources of truth; sync vs async; caching.
- **Hard problems:** what's genuinely difficult or novel here? What's the riskiest
  assumption? How will each be de-risked — prototype first, use a library, simplify scope?
  What should be built *last* because it's the biggest tuning/complexity risk?
- **Configuration & tunables:** centralize knobs (limits, thresholds, flags, environment
  values) so behavior changes without touching logic. **Every tunable lives in
  configuration with a committed default — never as an edited-in-place code constant.**
  (Hard-won lesson: "temporary" code-constant tweaks leak into commits or get lost.)
- **Cross-cutting concerns:** error handling, logging/observability, security, privacy,
  data integrity, offline/resilience — state the *target*, not the intent ("no PII in
  logs", "any crash leaves user data recoverable").

**Record.** Module list with responsibilities and forbidden dependencies; data model and
state locations; key contracts; hard-problem list with de-risking plans; tunables with
defaults; cross-cutting targets.

---

## 9. Quality & Performance Strategy *(required)*

**Why this matters.** "It works" is a claim; tests are evidence. And performance treated
as an end-phase task is how projects ship slow — targets set here feed the continuous
performance practice (`Performance_Testing.md`) that runs from the first slice onward.

**Explore.**
- **Testing strategy:** what kinds of tests (unit / integration / end-to-end / manual)
  earn their keep at this tier? What must *never* break — the critical scenarios that get
  regression tests first? What does "passing" mean per feature?
- **Performance targets:** which operations matter to a user's experience of speed? Set
  explicit, measurable targets for the handful that count (startup time, key-flow latency,
  throughput, memory ceiling, frame rate, bundle size — whatever fits this project type).
  A target you can't measure is a wish.
- **Performance workloads:** what would a *representative workload* look like for
  benchmarking — realistic data sizes, realistic usage patterns?
- **Security & privacy:** what's sensitive here? What's the threat worth defending
  against at this tier — and what's explicitly out of scope?

**Record here.** Test types with scope; the never-break scenario list; per-feature
acceptance meaning; the security and privacy posture as prose.

**Record as requirements.** This stage produces the non-functional half of the
specification, and it is the half most often lost to prose:

- A performance target: `--category performance`, and it is not a requirement until it
  carries a metric, a threshold AND the workload it is measured under. "Fast" is not a
  requirement; "renders a 300-page book in under 90 seconds on the reference machine" is.
- Reliability, availability, security, maintainability, portability:
  `--category attribute`.

`--verification` earns its keep here. A performance requirement is almost always `test`;
a security posture is often `analysis` or `inspection`. Saying which one stops a reader
assuming the strongest.

---

## 10. Delivery Plan *(required)*

**Why this matters.** Building in vertical slices — each one runnable end to end — keeps
the codebase coherent and lets a non-expert steer. The first slice is the most important
decision in the plan: it must prove the *riskiest assumption*, because if that fails, the
project pivots while it's still cheap.

**Explore.**
- **⭐ The walking skeleton:** what is the smallest end-to-end thing that proves the
  riskiest assumption (from Stage 8's hard problems)? Specify it tightly: goal, what's in,
  what's *explicitly excluded*, and "done when".
- **Subsequent slices:** ordered milestones after the skeleton, one-line goal each. Defer
  the hardest tuning-heavy systems until the spine is proven.
- **Definition of done per slice:** works, tested, performance spot-checked, documented,
  committed — what's the bar before moving on?
- **Release criteria:** which success criteria (Stage 2) must hold before this is a 1.0?

**Record.** First slice (goal / assumption tested / in / out / done-when); ordered slice
list; per-slice definition of done; release criteria.

---

## 11. Risks, Assumptions & Open Questions *(required)*

**Why this matters.** Risks with mitigations get managed; unstated risks get discovered.
Assumptions, if wrong, change the plan — they need to be visible so they can be tested
early. Open questions parked here are the implementer's signal to **ask rather than
guess**.

**Explore.** Walk back through the document: what's technically risky, scope-risky, or
externally dependent? What have we taken as true without checking? What's still undecided?

**Record.** Risk → mitigation pairs; assumption list (each with "how we'd find out");
open questions (each with who decides and by when it matters).


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-assumptions`* — What is taken as true without having been verified, and what this software depends on that it does not control. Each one a thing that would change the plan if it turned out to be false.

<!-- BEGIN srs-assumptions - written by the interview, read by the generators -->
<!-- END srs-assumptions -->

---

## 12. Decision Log *(required — seeded during the interview, grows for the project's life)*

**Why this matters.** This is the project's memory. Fixed decisions with rationale stop
the implementer — and the owner — from relitigating them, and make future reversals
informed rather than accidental.

**Record.** One line per settled decision:
`**[Decision]** — [rationale] — [alternatives rejected] — [date]`
Stage 7's technology decisions all appear here (or are referenced here). During
implementation, every materially ambiguous question the implementer asks gets its answer
recorded here.

---

## 13. Implementation Readiness Checklist *(required — the interview isn't done until this passes)*

Work through this with the owner before writing the final document:

- [ ] The one-line pitch, success criteria, and Non-Goals exist and agree with each other.
- [ ] Every flow in Stage 5 has its edge cases and failure states specified.
- [ ] **Every agreed obligation is a requirement RECORD, not a line in this document.** Run
      `python Commands/srs.py --stdout` and read clause 3: what is not there does not exist.
- [ ] **Every requirement carries a category, a verification method and a priority**, and none
      of the three was chosen to get past the command. A wrong category prints a requirement
      under the wrong clause; a wrong verification claims a strength nobody has.
- [ ] **Every marked region is filled, or carries `N/A — <reason>`.** A region left blank is
      reported as blank, which says the interview reached it and stopped.
- [ ] **Both generated documents have been produced and read**, and every clause still saying
      *Not supplied* is one the owner agrees should say that.
- [ ] Every technology in the project appears in Stage 7 with rationale — nothing entered
      by assumption.
- [ ] The never-commit list exists (secrets / PII / licensed material) and matches the
      constraints, content sources, and integrations discussed.
- [ ] Module boundaries exist and no two modules own the same concern.
- [ ] Every performance target has a metric, a threshold, and a workload.
- [ ] The walking skeleton is defined tightly enough to build without further questions.
- [ ] Every open question is either resolved into the Decision Log or explicitly parked
      in Stage 11.
- [ ] All skipped sections say `N/A — <reason>`, not nothing.
- [ ] The owner has read the Non-Goals and Decision Log and agrees they're right.

When all boxes check: finish `docs/Design_Document.md` in place, move every agreed requirement
from `proposed` to `agreed`, and direct the owner to open the
project folder in Claude Code and say **Initialize**, naming the template generation to
use (e.g. `Templates/_Project_Template/` — see its `START_HERE.md`); the
bootstrap reads `Development_Process.md` from the generation's shared process folder
(`Process/`).

---

## 14. Glossary *(optional)*

Definitions for acronyms and project-specific terms not already covered by Stage 4.


**Fill these regions.** They are read out of this document by the generators; everything outside the markers is yours.

*`srs-acronyms`* — Every acronym and abbreviation this project uses, expanded. A reader who meets one in the specification looks here.

<!-- BEGIN srs-acronyms - written by the interview, read by the generators -->
<!-- END srs-acronyms -->

---

## 15. Change Log *(maintained for the document itself)*

- **[vX.Y — YYYY-MM-DD]** — what changed in this document and why.
