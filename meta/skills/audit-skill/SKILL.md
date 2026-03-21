---
name: audit-skill
description: Evaluate existing skills against the quality review checklist and produce structured audit reports. Use this skill when the user says "audit this skill", "review skill quality", "check skill health", "audita a skill X", "como está a skill Y", "skill quality check", "what's the quality of", "how good is this skill", or wants to assess skill compliance — even if they don't explicitly say "audit."
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

## Input contract

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `target` | arg[1] or AUQ | yes | Must match: a skill name in skills-library, a plugin name, or literal `"all"` | AUQ with discovered options: list all skills and plugins |

## Workflow

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

List all available skills and plugins:

```bash
Glob: skills-library/*/skills/*/SKILL.md
```

Parse results into a list of `plugin: [skill1, skill2, ...]` entries. Present with `AskUserQuestion` offering plugin names and `"all"` as options (not individual skills — 30+ options overload the prompt). If the user selects a plugin, then offer the individual skills within that plugin as a follow-up AUQ.

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
- **✅ pass** — fully meets the standard
- **❌ fail** — missing or clearly below standard
- **⚠️ partial** — partially implemented, needs improvement
- **N/A** — not applicable to this skill

Be specific in findings — cite what you found (or didn't find) with line numbers or quotes. Vague findings like "could be better" are a failure mode.

### 4. Produce per-skill report

Generate the report using the template structure from `templates/per-skill-report.md`:

```markdown
# Audit Report: <skill-name>

Plugin: <plugin>
Audited: <ISO-8601 date>
Checklist version: <date of review-checklist.md or commit>

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 6 trigger phrases, 2 anti-triggers |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action + multiple triggers |
| ... | ... | ... | ... |

## Score: N/M

## Priority fixes (ordered by impact)

1. **<fix title>** — <specific finding>
2. **<fix title>** — <specific finding>

## Recommended action

- [ ] Run `/create-skill <skill-name>` with this report to apply fixes
```

Save the report to `<plugin>/skills/<name>/audit-report.md`.

### 5. Batch mode (plugin or library-wide)

**Plugin mode** — evaluate all skills in the plugin sequentially in the current session. Produce a per-skill report for each, then a consolidated summary.

**Library-wide mode (`all`)** — spawn one `Agent` per plugin. Each agent receives:
- The full review checklist content
- The list of skills to audit in its assigned plugin
- Instructions to produce per-skill reports and return a summary

Agent prompt template:

```
You are auditing all skills in the <plugin> plugin for quality compliance.

Review checklist:
<full checklist content>

Skills to audit:
<list of skill paths>

For each skill:
1. Read SKILL.md, references/, templates/, README.md
2. Evaluate against every checklist item
3. Save the per-skill report to <plugin>/skills/<name>/audit-report.md

After all skills are audited, return a summary table:
| Skill | Score | Critical gaps |

Do NOT modify any skill files — only create audit-report.md files.
```

**Guardrails:**
- Maximum one agent per plugin
- If an agent fails, log the error and continue with remaining plugins
- Collect all agent results before producing the consolidated report

### 6. Produce consolidated report (batch mode only)

When auditing multiple skills, produce a summary saved to `skills-library/audit-report-<date>.md`:

```markdown
# Skills Library Audit — <date>

## Summary

| Skill | Plugin | Score | Critical gaps |
|-------|--------|-------|---------------|
| /push | workflow | 3/12 | input contract, allowed-tools, error handling |
| /tdd | workflow | 9/12 | allowed-tools |
| ... | ... | ... | ... |

## Fix batches (grouped by fix type)

### Batch 1: <fix type> (N skills)
skill1, skill2, skill3, ...

### Batch 2: <fix type> (N skills)
...

## Top 5 most critical skills to fix

1. **<skill>** (score N/M) — <reason>
2. ...
```

Use the template from `templates/consolidated-report.md`.

### 7. Present results

Display to the user:
- Per-skill scores with pass/fail breakdown
- Top 5 most critical skills to fix (by score)
- Suggested fix batches (grouped by fix type for efficient remediation)
- Prompt: "Run `/create-skill <skill-name>` with the audit report to apply fixes"

## Output contract

| Artifact | Path | Persists? |
|----------|------|-----------|
| Per-skill report | `<plugin>/skills/<name>/audit-report.md` | yes (deleted after fixes applied) |
| Consolidated report | `skills-library/audit-report-<date>.md` | yes |

## Guidelines

- **Read-only is non-negotiable.** This skill reads SKILL.md, references/, templates/, and produces reports. It never edits, renames, or restructures the audited skill. If you find yourself wanting to "just fix this one thing" — stop. That's `/create-skill`'s job.
- **Checklist is the source of truth.** Every evaluation must trace back to a specific checklist item. Don't invent new criteria mid-audit — if something is missing from the checklist, flag it as a checklist improvement suggestion in the report, not as a skill failure.
- **Specific findings only.** "Description could be improved" is not a finding. "Description has 2 trigger phrases but no anti-triggers and missing 'even if' pattern" is a finding. Cite line numbers, quote text, count items.
- **Score honestly.** Don't inflate scores to avoid uncomfortable results. A skill with 3/12 needs to know it's 3/12 so the fix effort is properly prioritized.
- **Batch by fix type, not by skill.** The consolidated report groups fixes by type (e.g., "add allowed-tools") because fixing the same issue across 20 skills is more efficient than fixing one skill at a time.

## Anti-patterns

- Modifying audited skills (the skill is read-only)
- Using a hardcoded copy of the review checklist instead of reading it at runtime
- Vague findings without specific evidence ("needs improvement")
- Spawning agents for single-skill mode (unnecessary overhead)
- Auditing `create-skill`, `plan-skill`, or `audit-skill` (they are the tools, not the subjects)
- Presenting 30+ individual skills in a single AUQ (use plugin-level selection with drill-down instead)
- Inflating scores to avoid flagging issues
- Skipping categories as "N/A" without verifying they truly don't apply
