---
name: audit-skill
description: >-
  Evaluate existing skills against the quality review checklist and produce
  structured audit reports. Use this skill when the user says "audit this skill",
  "review skill quality", "check skill health", "audita a skill X", "como está
  a skill Y", "skill quality check", "what's the quality of", "how good is this
  skill", or wants to assess skill compliance — even if they don't explicitly
  say "audit."
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - Write
  - Bash
---

# Audit Skill

Evaluate one or more existing skills against the review checklist from `/create-skill` and produce structured, machine-consumable audit reports. This skill is **read-only** — it never modifies the audited skill.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `target` | arg[1] or AUQ | yes | Must match: a skill name in skills-library, a plugin name, or literal `"all"` | AUQ with discovered options: list all skills and plugins |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Per-skill report | `<plugin>/skills/<name>/audit-report.md` | yes (deleted after fixes applied) | Markdown |
| Consolidated report | `skills-library/audit-report-<date>.md` | yes | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Review checklist | `skills-library/meta/skills/create-skill/references/review-checklist.md` | R | Markdown |
| SKILL.md files | `skills-library/*/skills/*/SKILL.md` | R | Markdown with YAML frontmatter |
| skill-meta.json files | `skills-library/*/skills/*/skill-meta.json` | R | JSON |
| Report templates | `templates/per-skill-report.md`, `templates/consolidated-report.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `skills-library/` directory exists and contains plugin directories → if not: "skills-library not found." — stop.
2. Review checklist exists at `skills-library/meta/skills/create-skill/references/review-checklist.md` → if not: "Review checklist missing — cannot audit without standards." — stop.
3. Target argument resolves to at least one skill → if not: AUQ with discovered skills/plugins as options.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Resolve target

Parse the argument to determine audit scope:

**Skill name** (e.g., `push`, `tdd`):

```bash
# Find the skill's SKILL.md
Glob: skills-library/*/skills/<name>/SKILL.md
```

If exactly one match → single-skill mode.

**Plugin name** (e.g., `workflow`, `meta`):

```bash
# Verify plugin exists and collect all skills
Glob: skills-library/<name>/skills/*/SKILL.md
```

If the directory exists and contains skills → plugin mode (audit all skills in that plugin).

**Literal `"all"`**:

```bash
# Collect all skills across all plugins
Glob: skills-library/*/skills/*/SKILL.md
```

→ Library-wide mode (spawns parallel agents, one per plugin).

**No argument provided:**

List all available skills and plugins. Parse results into a list of `plugin: [skill1, skill2, ...]` entries. Present with `AskUserQuestion` offering plugin names and `"all"` as options (not individual skills — 30+ options overload the prompt). If the user selects a plugin, then offer the individual skills within that plugin as a follow-up AUQ.

**Exclusions:** Always exclude `create-skill`, `plan-skill`, and `audit-skill` from audit — they are the evaluation tools, not subjects.

**Validation:** If the target doesn't match any skill or plugin, show an error with the closest matches (fuzzy match against known names) and present `AskUserQuestion` to retry.

### 2. Load review checklist

Read the current review checklist at runtime — never use a hardcoded copy:

```
Read: skills-library/meta/skills/create-skill/references/review-checklist.md
```

This ensures the audit always uses the latest standards. Parse the checklist into evaluation categories.

### 3. Evaluate skill (single-skill mode)

For each skill being evaluated, read its full structure:

```
Read: <plugin>/skills/<name>/SKILL.md
Glob: <plugin>/skills/<name>/references/*
Glob: <plugin>/skills/<name>/templates/*
Read: <plugin>/skills/<name>/README.md (if exists)
```

Evaluate against each checklist category:

| Category | What to check |
|----------|---------------|
| **Description** | Pushy trigger phrases, anti-triggers, "even if" pattern, WHAT + WHEN coverage |
| **SKILL.md body** | Under 500 lines, imperative form, constraints reasoned, numbered steps, output formats, input contract |
| **Quality** | Quality expectations repeated at key points, anti-patterns named, refinement step, error handling |
| **Testing** | Invoked with realistic input, activation tested (3+ trigger phrases), failure modes checked |
| **Subagents** | (if applicable) Agent context complete, tool access explicit, two-phase build, race conditions |
| **Structure** | Standard layout (SKILL.md, references/, templates/), references one level deep, large refs have TOC, self-contained, README generated |
| **Compliance** | CLAUDE.md compliance (frontmatter values, naming conventions, plugin rules) |

For each item, assign a status:
- **pass** — fully meets the standard
- **fail** — missing or clearly below standard
- **partial** — partially implemented, needs improvement
- **N/A** — not applicable to this skill

Be specific in findings — cite what you found (or didn't find) with line numbers or quotes. Vague findings like "could be better" are a failure mode.

### 4. Produce per-skill report

Generate the report using the template structure from `templates/per-skill-report.md`. Save the report to `<plugin>/skills/<name>/audit-report.md`.

### 5. Batch mode (plugin or library-wide)

**Plugin mode** — evaluate all skills in the plugin sequentially in the current session. Produce a per-skill report for each, then a consolidated summary.

**Library-wide mode (`all`)** — spawn one `Agent` per plugin. Each agent receives:
- The full review checklist content
- The list of skills to audit in its assigned plugin
- Instructions to produce per-skill reports and return a summary

**Guardrails:**
- Maximum one agent per plugin
- If an agent fails, log the error and continue with remaining plugins
- Collect all agent results before producing the consolidated report

### 6. Produce consolidated report (batch mode only)

When auditing multiple skills, produce a summary saved to `skills-library/audit-report-<date>.md`. Use the template from `templates/consolidated-report.md`. Group fix batches by fix type, not by skill — fixing the same issue across 20 skills is more efficient than fixing one skill at a time.

### 7. Report

Present concisely:
- **What was done** — skills audited, mode used (single/plugin/library-wide)
- **Scores** — per-skill scores with pass/fail breakdown
- **Top fixes** — top 5 most critical skills to fix (by score)
- **Fix batches** — suggested fix batches grouped by fix type for efficient remediation
- **Audit results** — self-audit summary
- **Errors** — issues encountered (or "none")
- **Next step** — "Run `/update-skill <skill-name>` with the audit report to apply fixes"

## Next action

Run `/update-skill <skill-name>` with the audit report to apply fixes for the lowest-scoring skills first.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — review checklist loaded, target resolved
2. **Steps completed?** — all skills in scope evaluated, reports generated
3. **Output exists?** — audit-report.md files created at declared paths
4. **Anti-patterns clean?** — no audited skills were modified, no vague findings, no inflated scores
5. **Checklist sourced at runtime?** — review checklist was read from disk, not hardcoded

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Findings specific?** — every finding cites line numbers, quotes, or counts — no vague "could be better" entries
2. **Scores accurate?** — each pass/fail/partial maps to a specific checklist item with evidence
3. **Report format matches template?** — output follows per-skill-report.md or consolidated-report.md structure
4. **Fix batches logical?** — grouped by fix type, not by skill, with accurate skill counts

Audit is scoped to reports generated in THIS session.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Review checklist not found | Report path and stop — cannot audit without standards |
| Skill/plugin not found | Fuzzy match against known names, present AUQ to retry |
| Agent failure (library-wide mode) | Log error, continue with remaining plugins, note gap in consolidated report |
| Template file missing | Generate report inline using the expected structure, warn about missing template |
| Malformed SKILL.md (no frontmatter) | Flag as critical finding, continue audit of remaining sections |

## Anti-patterns

- **Modifying audited skills.** The skill is read-only — because modifying while auditing conflates evaluation with remediation and makes audit results unreliable.
- **Hardcoded checklist.** Using a cached copy instead of reading at runtime — because the checklist evolves and stale criteria produce inaccurate audits.
- **Vague findings.** "Needs improvement" without evidence — because non-actionable findings waste remediation effort and erode trust in the audit.
- **Spawning agents for single-skill mode.** Unnecessary overhead — because one skill doesn't need parallelism.
- **Auditing evaluation tools.** `create-skill`, `plan-skill`, and `audit-skill` are the standards, not subjects — because auditing them against themselves creates circular evaluation.
- **AUQ with 30+ options.** Presenting all individual skills overloads the prompt — because plugin-level selection with drill-down is more navigable.
- **Inflating scores.** Avoiding uncomfortable results — because a 3/12 needs to be flagged so fix effort is prioritized correctly.
- **Skipping categories as N/A without verification.** Assuming irrelevance — because most categories apply to most skills; verify before skipping.

## Guidelines

- **Read-only is non-negotiable.** This skill reads SKILL.md, references/, templates/, and produces reports. It never edits, renames, or restructures the audited skill — because mixing evaluation and remediation produces unreliable results. That's `/update-skill`'s job.

- **Checklist is the source of truth.** Every evaluation must trace back to a specific checklist item. Don't invent new criteria mid-audit — if something is missing from the checklist, flag it as a checklist improvement suggestion in the report, not as a skill failure.

- **Specific findings only.** "Description could be improved" is not a finding. "Description has 2 trigger phrases but no anti-triggers and missing 'even if' pattern" is a finding — because actionable findings drive efficient remediation.

- **Score honestly.** Don't inflate scores to avoid uncomfortable results. A skill with 3/12 needs to know it's 3/12 so the fix effort is properly prioritized.

- **Batch by fix type, not by skill.** The consolidated report groups fixes by type (e.g., "add allowed-tools") — because fixing the same issue across 20 skills is more efficient than fixing one skill at a time.
