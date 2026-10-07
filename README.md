# Project Template

The generic, technology-agnostic project template. **One living corpus** — it is edited in place,
and every project gets each improvement, which is what pointing rather than copying was always for.

It spans **two homes**:

- **`Process/`** — the static process docs projects *point at* during development
  (`Development_Process.md`, `Artifact_Formats.md`, `Performance_Testing.md`,
  `Audit_and_Testing.md`, `Writing_Standard.md`, `Path_Policy.md`, `Project_Sets.md`,
  `Agent_Scope.md`).
- **This folder** — the project-*starter* material: orientation (`START_HERE.md`) and the blanks
  consumed at project creation (`Design_Document.md`, `AGENTS_Template.md`, `CLAUDE_Pointer.md`,
  `Instruction_Changelog.md`, `Set_Manifest_Template.toml`).

**Starting a new project?** Read [`START_HERE.md`](START_HERE.md).

**Changing the template?** Edit it here and record the change in
[`TEMPLATE_CHANGELOG.md`](TEMPLATE_CHANGELOG.md). Every project picks it up; there is nothing to
migrate and nothing to re-pin.

> **These files are the template.** There is no version folder to resolve and nothing for a project
> to pin, so an improvement you make here reaches every project at once. `START_HERE.md` explains how
> a project consumes it.

Related shared singletons:
- `Process/Knowledge_Base/` — cross-project, tool-specific gotchas.
- `Process/Model_Routing.md` — model/effort routing per task.
- `Templates/_Godot_Template/` — the runnable Godot mobile skeleton.
