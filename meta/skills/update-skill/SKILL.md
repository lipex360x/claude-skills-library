---
name: update-skill
description: >-
  Scoped edits to existing Claude Code skills — reads skill-meta.json for instant
  context, modifies only affected sections, runs scoped content audit, and verifies
  skeleton compliance after every edit. Use when the user says "update skill",
  "edit skill", "fix skill", "modify skill", "change this skill", "improve skill",
  "ajusta a skill", or wants to modify an existing skill — even if they don't
  explicitly say "update."
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
argument-hint: "<skill-name> [change description]"
---

# Update Skill

Surgical edits to existing skills — instant context via `skill-meta.json`, scoped changes, and skeleton compliance verification after every modification.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `skill-name` | $ARGUMENTS | yes | Skill directory exists in skills-library | AUQ with skill list from STRUCTURE.md |
| `change-description` | $ARGUMENTS or conversation | yes | Non-empty string describing what to change | AUQ: "What change do you want to make?" |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Modified SKILL.md | `<plugin>/skills/<name>/SKILL.md` | yes | Markdown with YAML frontmatter |
| Updated skill-meta.json | `<plugin>/skills/<name>/skill-meta.json` | yes | JSON per spec |
| Modified references | `<plugin>/skills/<name>/references/*.md` | yes | Markdown |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Target skill-meta.json | `<plugin>/skills/<name>/skill-meta.json` | R/W | JSON |
| Target SKILL.md | `<plugin>/skills/<name>/SKILL.md` | R/W | Markdown |
| Target references | `<plugin>/skills/<name>/references/` | R/W | Markdown files |
| STRUCTURE.md | `skills-library/STRUCTURE.md` | R | Markdown |
| Skeleton template | `references/skeleton-template.md` | R | Markdown |
| Review checklist | `references/review-checklist.md` | R | Markdown |
| Scoped audit mapping | `references/scoped-audit-mapping.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Current directory is `skills-library/` → if not: "Run from skills-library root." — stop.
2. Target skill directory exists → if not: AUQ with skill list from STRUCTURE.md for selection.
3. Target `SKILL.md` is readable → if not: "SKILL.md not found at expected path." — stop.
4. Working tree is clean (no uncommitted changes in target skill) → if dirty: warn but continue — the user may have in-progress work.

</pre_flight>

## Steps

### 1. Load context

Read the target skill's `skill-meta.json` if it exists. Extract: `lineCount`, `skeleton` section states, `references[]`, `steps`, `skeletonVersion`.

If `skill-meta.json` does not exist, fall back to manual discovery:
- Read `SKILL.md` and count lines
- Scan for the 13 skeleton section headers
- List files in `references/`
- Count numbered step headers

Store the loaded context — this is the baseline for scoped operations.

### 2. Parse change request

Identify which skeleton sections the requested change affects. A change to anti-patterns affects only the Anti-patterns section. A change to the workflow affects the Steps section. A new reference file affects External state and potentially Steps.

If the change is ambiguous, use AskUserQuestion to clarify scope before proceeding.

### 3. Capture before-state

Record the current state of each affected section:
- Line count of the section
- Number of items (anti-patterns, guidelines, steps, checklist items)
- Section presence flag

This before-state enables the diff-based content audit in Step 6 — comparing what changed rather than re-auditing everything.

### 4. Apply scoped changes

Modify only the affected sections. Leave all other sections untouched — do not reformat, reorder, or "improve" content outside the change scope.

If the change requires a new reference file, create it in the skill's `references/` directory. If it modifies an existing reference, use Edit for surgical changes rather than rewriting the file.

### 5. Verify skeleton compliance

Read `references/skeleton-template.md` for the canonical structure.

Check all 13 sections are present with canonical names in the correct order:
1. Frontmatter, 2. Title + Intro, 3. Input contract, 4. Output contract, 5. External state, 6. Pre-flight, 7. Steps, 8. Next action, 9. Self-audit, 10. Content audit, 11. Error handling, 12. Anti-patterns, 13. Guidelines

Verify never-skip sections (Pre-flight, Self-audit, Anti-patterns, Guidelines) have content. Verify skipped sections have `> _Skipped: "reason"_`. Verify the last numbered step is "Report". Verify XML tags on contracts and audit blocks.

If compliance fails, fix the issue before continuing — do not defer skeleton fixes.

### 6. Run scoped content audit

Read `references/scoped-audit-mapping.md` to determine which checklist categories apply to the modified sections.

For each affected section, verify:
- New content is accurate and consistent with the skill's existing behavior
- No contradictions introduced between modified and unmodified sections
- References cited in the modified content exist and are accessible
- Modified anti-patterns follow the format: **Bold name.** Description with consequence

### 7. Run scoped review checklist

Read `references/review-checklist.md`. Run only the categories identified by the scoped audit mapping, plus the two always-check categories (Skeleton compliance, Progressive disclosure).

Present results as the standard markdown table:

```markdown
**Scoped Review — <skill-name> (modified: <section list>):**

| Item | Status | Notes |
|------|--------|-------|
| ...  | OK/WARN/FAIL | ... |
```

If any item is FAIL, fix it before proceeding. WARN items are reported but do not block.

### 8. Update skill-meta.json

If `skill-meta.json` exists, update the affected fields:
- `lastModified` → today's date
- `lineCount` → current SKILL.md line count
- `skeleton` → refresh booleans for any sections that changed state
- `references[]` → add/remove if reference files changed

If `skill-meta.json` does not exist, generate it from scratch following `references/skill-meta-spec.md`. Read the full SKILL.md to populate all fields accurately.

### 9. Report

<report>

Present concisely:
- **Change applied:** what was modified (sections, references, line count delta)
- **Before → After:** key metrics (line count, anti-pattern count, section states)
- **Scoped review:** summary of checklist results (pass/warn/fail counts)
- **skill-meta.json:** updated or generated
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Run `/push` to commit and sync the changes.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Only affected sections modified?** — diff the file to confirm no changes outside the declared scope
2. **Skeleton intact?** — all 13 sections present with canonical names after edits
3. **skill-meta.json reflects changes?** — `lastModified`, `lineCount`, and `skeleton` fields are current
4. **Under 500 lines?** — SKILL.md line count is within limit
5. **No untouched sections rewritten?** — compare before-state to confirm scope was respected

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Scoped to modified sections only — full skill audit is `/audit-skill`'s job.

1. **New content accurate?** — verify instructions are correct and actionable
2. **Format consistent?** — modified content follows the same patterns as existing content (bullet style, heading level, XML tags)
3. **No contradictions?** — new content does not conflict with unmodified sections
4. **References valid?** — any paths or file references in modified content exist

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `skill-meta.json` missing | Fall back to manual discovery, generate at end |
| `skill-meta.json` has stale data | Correct during update in Step 8, note discrepancy in Report |
| Target SKILL.md not found | AUQ with skill list for re-selection |
| Skeleton compliance fails after edit | Fix immediately — do not defer |
| SKILL.md exceeds 500 lines after edit | Extract overflow content to references, update Read pointers |
| Reference file missing | Create it or remove the reference from SKILL.md |

## Anti-patterns

- **Rewriting untouched sections.** Only modify sections in the change scope — because reformatting or "improving" unrelated sections creates noise in diffs, risks introducing bugs, and violates the scoped-edit principle.
- **Running full checklist on minor edits.** Use `references/scoped-audit-mapping.md` to run only affected categories — because a full 11-category review for a single anti-pattern addition wastes time and teaches the user to skip the review.
- **Re-auditing the entire skill.** Content audit is scoped to modified sections — because full content re-verification is `/audit-skill`'s job, not a side effect of every edit.
- **Forgetting skill-meta.json.** Always update or generate `skill-meta.json` at the end of every session — because stale metadata defeats the purpose of instant context loading for future edits.
- **Using /create-skill for edits.** `/create-skill` regenerates the full skeleton — because applying it to an existing skill risks overwriting carefully tuned content that took multiple iterations to get right.

## Guidelines

- **Scope is king.** The value of `/update-skill` over `/create-skill` is precision. Every decision should minimize the blast radius of changes. When in doubt about whether a section needs updating, leave it alone — the user can always run `/update-skill` again for additional sections.

- **Before-state enables accountability.** Capturing section metrics before changes allows the Report to show concrete diffs ("Anti-patterns: 4 → 5, +1 added"). Without before-state, the Report can only say "changes were made" — which tells the user nothing useful.

- **Graceful fallback when skill-meta.json is missing.** Not all skills have been migrated yet. Manual discovery (reading SKILL.md headers + listing references/) is slower but produces the same context. Generate `skill-meta.json` at the end so the next edit benefits from instant loading.

- **Fix skeleton issues immediately.** If an edit accidentally breaks skeleton compliance (wrong section order, missing section, wrong name), fix it in the same session. Deferring skeleton fixes creates compounding drift that makes future audits harder.
