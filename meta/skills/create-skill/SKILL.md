---
name: create-skill
description: >-
  Guide the user through creating high-quality Claude Code skills — from
  structuring SKILL.md files to writing effective descriptions, designing
  progressive disclosure, and launching subagents. Use this skill whenever
  the user mentions "create a skill", "new skill", "skill quality", "skill
  best practices", "how to write a skill", or wants to build a /command —
  even if they don't explicitly say "skill."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - Skill
argument-hint: "[spec-file]"
---

# Create Skill

Step-by-step factory for building structurally consistent Claude Code skills. Every output follows the 14-section canonical skeleton.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `spec-file` | $ARGUMENTS | no | Valid `/plan-skill` spec with required headers | Fall back to interactive flow (Step 1.0a) |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path (global) | Path (local) | Persists | Format |
|----------|---------------|--------------|----------|--------|
| SKILL.md | `<plugin>/skills/<name>/SKILL.md` | `<project>/.claude/skills/<name>/SKILL.md` | yes | Markdown with YAML frontmatter |
| skill-meta.json | `<plugin>/skills/<name>/skill-meta.json` | `<project>/.claude/skills/<name>/skill-meta.json` | yes | JSON per `references/skill-meta-spec.md` |
| README.md | `<plugin>/skills/<name>/README.md` | `<project>/.claude/skills/<name>/README.md` | yes | Markdown |
| References | `<plugin>/skills/<name>/references/*.md` | `<project>/.claude/skills/<name>/references/*.md` | yes | Markdown |
| Templates | `<plugin>/skills/<name>/templates/*` | `<project>/.claude/skills/<name>/templates/*` | yes | Various |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Mode | Format |
|----------|------|--------|------|--------|
| Symlinks | `~/.claude/skills/` | Write | global only | Symlink via `setup.sh` |
| Library structure | `skills-library/STRUCTURE.md` | Write | global only | Markdown |
| Library README | `skills-library/README.md` | Write | global only | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. **Detect mode:**
   - If current directory is `skills-library/` or a subdirectory → **global mode** (skill will live in `skills-library/<plugin>/skills/<name>/`).
   - Otherwise → **local mode** (skill will live in `<project>/.claude/skills/<name>/`). Confirm target project directory via AUQ.
2. **Global mode only:** Target plugin directory exists under `skills-library/` → if not: list available plugins via AUQ.
3. Skill name follows verb-subject pattern (e.g., `create-skill`, `review-postgres`) → if not: suggest correction.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Understand the intent

#### 1.0 Spec detection (automatic)

Check if a `/plan-skill` spec is available:

1. **Check args** — If the user passed a file path, read it as a spec.
2. **Check downloads/** — If no args, glob for `downloads/*-spec.md`. Multiple matches → AUQ to pick.
3. **Validate** — Must contain: `## Meta`, `## Purpose`, `## Trigger`, `## Workflow`, `## Guardrails`, `## Decisions Log`.

When valid, present summary table and AUQ: `["Confirm — use this spec", "Reject — start fresh"]`.

Read `references/spec-contract.md` for the full mapping of spec sections to steps.

#### 1.0a Normal flow (no spec)

Ask the user:
- What should the skill do? (the core action)
- When should it activate? (trigger contexts)
- Is it user-invocable or auto-triggered?

Use AUQ with concrete options when clarifying ambiguous decisions.

#### 1.1 Classify scope

When the request contains multiple actions, break into discrete steps and classify each as mandatory or optional via AUQ with `multiSelect: true`. Skip for single, unambiguous actions.

### 2. Design the structure

```
skill-name/
├── SKILL.md              # Required. <500 lines
├── templates/            # Optional. Output formats
├── references/           # Optional. Detailed docs on demand
├── scripts/              # Optional. Executable code
└── assets/               # Optional. Static resources
```

Only SKILL.md is required. Read `references/progressive-disclosure.md` for the three-tier architecture.

Skill names follow the **verb-subject** pattern: `create-skill`, `review-postgres`, `check-gmail`. Lowercase, hyphens, verb first. Name must match the directory name.

### 3. Write the description

The description is the single most important design decision — Claude activates a skill based solely on `name` + `description`.

Read `references/description-patterns.md` for examples and the "pushy" technique.

### 4. Write the SKILL.md body

Read `references/skeleton-template.md` — the mandatory starting point. Every skill follows the 14-section skeleton:

Frontmatter → Title+Intro → Input contract → Output contract → External state → Pre-flight → Steps (Report always last) → Post-flight → Next action → Self-audit → Content audit → Error handling → Anti-patterns → Guidelines

**Model selection in frontmatter:** Evaluate if the skill is operational (follows a clear script, calls APIs, processes structured data, runs CLI commands) or analytical/creative (requires deep reasoning, architecture analysis, creative writing, nuanced judgment). Operational skills get `model: sonnet` in the frontmatter. Analytical/creative skills omit `model:` (defaults to opus). When in doubt, omit — it's safer to use opus than to underpower a complex skill.

**Writing rules:**

- Sections are never omitted — use `> _Skipped: "reason"_` when not applicable
- Four never-skip sections: Pre-flight, Self-audit, Anti-patterns, Guidelines
- XML tags on contracts and audits (read `references/xml-tag-patterns.md`)
- Imperative form; explain the why behind constraints
- Explicit output formats with concrete examples
- Error handling for skills with external calls (read `references/error-handling-patterns.md`)

**Depth adaptation:** When a section exceeds ~15 lines, extract to `references/` with top 3-5 items inline and a Read pointer. One source of truth — never duplicate between SKILL.md and references.

**Content audit evaluation:** Determine if the skill generates verifiable content (read `references/content-audit-patterns.md`). If yes → define audit criteria. If no → mark as Skipped with reason.

Read `references/anthropic-patterns.md` for prompt engineering patterns.

For editing existing skills, use `/update-skill` — this skill handles creation only.

### 5. Apply quality techniques

Read `references/quality-techniques.md` for the full set. Key techniques:

- **Craftsmanship repetition.** Repeat quality expectations at multiple points.
- **Anti-patterns list.** Name specific failure modes.
- **Refinement over addition.** Build in a "polish, don't add" step.

### 6. Handle subagents (if applicable)

Subagents start with a blank context. Read `references/subagent-patterns.md` for patterns, race conditions, and the two-phase build approach.

### 7. Verify skeleton compliance and review

**Skeleton compliance gate** — verify before running the full review:

1. All 14 sections present in correct order
2. Skipped sections have explicit justification
3. Never-skip sections have real content
4. XML tags on contracts and audit blocks
5. Report is the last numbered step

Fix any failures before proceeding.

**Review checklist** — Read `references/review-checklist.md` and validate every item. Present results as a markdown table.

### 8. Register and generate metadata

**Register (global mode only):** Run `bash ~/.brain/scripts/setup.sh` to create the symlink. Local skills are discovered automatically by Claude Code — no registration needed.

**Generate skill-meta.json:** Create alongside SKILL.md per `references/skill-meta-spec.md`. Fill all fields: skeleton section states, step count, approval gates, references, dependencies.

### 8b. Test the skill

1. **Functional test** — Run with realistic input. Verify it follows steps and produces expected output.
2. **Activation test** — 3+ natural trigger phrases. All must activate. If any fails, revise description (Step 3).
3. **Edge case** — One input outside scope. Verify graceful handling.

### 9. Update READMEs

Run `/create-readme` targeting:

1. The skill's directory
2. **Global mode only:** The `skills-library/` root

### 10. Update STRUCTURE.md

**Global mode only.** Update `skills-library/STRUCTURE.md` if the skill was created, moved, renamed, or deleted. Skip for local skills and content-only edits.

### 11. Push to GitHub

Push using `/push`. **Global mode:** if `.brain/` files were modified, push that repo too. **Local mode:** push only the project repo.

### 12. Report

<report>

- **What was done** — skill created, files generated, registration status
- **Audit results** — skeleton compliance + review checklist + content audit summary
- **Errors** — issues encountered or "none"

</report>

## Post-flight

<post_flight>

After presenting the Report, verify external state:

1. **Symlink resolves?** — `ls -L ~/.claude/skills/<name>/SKILL.md` must succeed (dereference through symlink).
2. **skill-meta.json valid?** — `python3 -c "import json; json.load(open('<path>/skill-meta.json'))"` must pass.
3. **References exist on disk?** — for each entry in skill-meta.json `references` array, `test -f <skill-dir>/references/<filename>` must succeed.
4. **Registered in STRUCTURE.md?** (global mode only) — `grep '<skill-name>' skills-library/STRUCTURE.md` must find the skill.
5. **Registered in README.md?** (global mode only) — `grep '<skill-name>' skills-library/README.md` must find the skill in the plugin table.
6. **README.md exists?** — `test -f <skill-dir>/README.md` must succeed.

If any check fails, report the specific failure and the fix command.
7. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all post-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</post_flight>

## Next action

Run `/audit-skill <skill-name>` for a full structural audit, or start using the skill.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — directory and plugin validated
2. **Steps completed?** — list any skipped steps with reason
3. **Skeleton compliance?** — all 13 sections present, correct order, XML tags applied
4. **skill-meta.json generated?** — exists alongside SKILL.md with correct schema
5. **Under 500 lines?** — SKILL.md line count checked, overflow applied if needed
6. **Anti-patterns clean?** — no cross-skill deps, no duplicate content, no missing contracts
7. **Approval gates honored?** — scope classification questions asked

</self_audit>

## Content audit

<content_audit>

Before finalizing, verify the generated skill:

1. **Skeleton structure valid?** — all 13 sections in correct order, Skipped sections justified, never-skip sections populated
2. **Contracts accurate?** — Input/Output/External state match actual behavior
3. **Read pointers resolve?** — every `Read references/...` points to an existing file
4. **skill-meta.json consistent?** — skeleton booleans match section states, references list matches files
5. **Line count compliant?** — under 500 lines, no section >15 lines without overflow

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Spec file not found | Fall back to interactive flow (Step 1.0a) |
| Plugin directory missing (global) | AUQ: list available plugins or create new |
| `.claude/skills/` missing (local) | Create the directory automatically |
| SKILL.md exceeds 500 lines | Extract sections >15 lines to references |
| `setup.sh` fails | Report error, suggest manual run |
| Review checklist has FAILs | Fix before proceeding |

## Anti-patterns

- **Skipping the skeleton.** Writing SKILL.md freeform produces inconsistent structure — because the skeleton template is the mandatory starting point, not a suggestion.
- **Omitting sections instead of skipping.** An absent section is ambiguous; `> _Skipped: "reason"_` is explicit — because `/audit-skill` checks for presence and treats missing sections as failures.
- **Cross-skill dependencies.** Referencing or importing from other skills creates fragile coupling — because each skill loads independently with no guaranteed load order.
- **`@` imports in SKILL.md.** Only works in CLAUDE.md files — because SKILL.md is loaded by the skill runner, which doesn't resolve `@` imports. Use Read tool instructions.
- **Duplicating content.** Information in both SKILL.md and references drifts apart — because the agent doesn't know which copy is authoritative. One source of truth.
- **Undocumented external state.** Reading or writing shared resources without declaring them — because one skill's update silently breaks another when neither documented the dependency.

## Guidelines

- **Skeleton is the factory standard.** Every skill follows the canonical 14-section skeleton — this is the structural guarantee that makes the library consistent and auditable.
- **Depth adaptation over truncation.** Extract to references with inline summaries rather than cutting content — because token efficiency and completeness are both achievable through progressive disclosure.
- **Reasoning over rigid rules.** "Avoid X because Y" works better than "NEVER do X" — because Claude 4.6 handles edge cases better with reasoning, and aggressive emphasis causes overtriggering.
- **Description is the activation mechanism.** Invest more time here than any other element — because a skill with perfect structure but a weak description never fires when needed.
- **Test before shipping.** A skill that passes review but fails on real input erodes trust — because users learn to distrust the factory after one bad experience.
