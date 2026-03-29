---
name: capture-analysis
description: >-
  Capture skill gaps, workflow frictions, and pattern improvements as structured
  entries in an analysis file. Use when the user says "/capture-analysis",
  "analisa isso", "estuda isso", "documenta essa melhoria", "adiciona no
  analysis", "lessons learned", or wants to record a finding for future skill
  updates — even if they don't explicitly say "analysis."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
---

# Capture Analysis

Capture learnings during work sessions as structured, project-agnostic entries in `analysis.md`. This file is a feedback buffer between skill users and skill maintainers — consistent format in, reliable implementation out.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `action` | $ARGUMENTS | no | One of: free text, `remove <N>`, empty | AUQ: "What do you want to capture?" |
| `entry number` | $ARGUMENTS (remove flow) | conditional | Positive integer matching existing entry | List valid entry numbers and stop |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Analysis entry | `./analysis.md` | yes | Markdown (numbered entry) |
| .gitignore update | `./.gitignore` | yes | Text append |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Analysis file | `./analysis.md` | R/W | Markdown |
| Gitignore | `./.gitignore` | R/W | Text |

</external_state>

## Pre-flight

<pre_flight>

1. If `$ARGUMENTS` matches remove pattern (`remove <N>` or `remover <N>`) → switch to Remove entry flow.
2. If `$ARGUMENTS` is empty → AUQ: "What do you want to capture?" — stop if no response.
3. Run `date "+%H:%M"` for the current timestamp.

</pre_flight>

## Steps

### 1. Load or create

Check if `analysis.md` exists at the project root.

- **File exists** → read it, note the last entry number.
- **File doesn't exist** → check `.gitignore` for `analysis.md`. If not present, append `analysis.md` to `.gitignore` (this file contains session-specific learnings, not project code). Then create it with the header:

```markdown
# Lessons Learned for Skill Updates

Source session: <YYYY-MM-DD> ~<HH:MM>
Purpose: project-agnostic learnings to feed back into skills.

---
```

### 2. Parse the input

Extract from the user's description:
- **What happened** — the concrete trigger situation
- **What's missing or broken** — current vs expected behavior
- **What should change** — proposal with enough detail to implement

If the description is too vague to fill these three parts, ask ONE clarifying question — no more. Keep the flow fast.

Before writing, scan existing entries for the same concern. If found, **update** the existing entry with the new context instead of creating a duplicate.

### 3. Write entry

Append the entry to `analysis.md`. Continue numbering from the last entry. Each entry follows this structure:

```markdown
## N. [Concise title — what needs to change]

**Skill:** `skill-name` (specific section or phase affected)

### The problem
[Concrete trigger situation — what happened, not what should happen]

### The gap
[Current behavior vs expected behavior — be specific]

### Proposed solution
[Concrete proposal. Enough detail for a skill maintainer to implement without asking questions. Name the skill, the section, the change.]

### Why it matters
[Impact — cost of not fixing, benefit of fixing. 2-3 sentences max.]
```

### 4. Update timestamp

Update the `Source session:` line in the header to the current date and time.

### 5. Confirm

Tell the user: entry number, title, and total entry count. One line.

### 6. Remove entry (conditional flow)

When the user says `/capture-analysis remove N` or marks an item as implemented:

1. Read the file. If the file doesn't exist or has no entries, tell the user: "No analysis file found (or no entries to remove)." and stop.
2. Validate N: must be a positive integer within the range of existing entries. If invalid, list available entry numbers and stop.
3. Identify and remove entry N.
4. Renumber remaining entries sequentially (no gaps).
5. If no entries remain, delete the file entirely (`rm analysis.md`).
6. Confirm: "Removed entry N: [title]. [M entries remaining / File removed.]"

### 7. Report

<report>

Present concisely:
- **Action:** entry added, updated, or removed
- **Entry:** number and title
- **Total entries:** current count in `analysis.md`
- **Audit results:** self-audit summary
- **Errors:** issues encountered (or "none")

</report>

## Next action

Review accumulated entries periodically and feed them into skill updates via `/update-skill`.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — input source identified, timestamp obtained
2. **Steps completed?** — entry written or removed as requested
3. **Output exists?** — `analysis.md` updated with correct entry number and structure
4. **No duplicates?** — existing entries scanned before writing
5. **Anti-patterns clean?** — entry is project-agnostic, actionable, and identifies affected skill

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Project-agnostic?** — no project-specific file paths, domain terms, or business logic in the entry
2. **Skill identified?** — `**Skill:**` field present with backtick-wrapped name and scope hint
3. **Actionable proposal?** — proposed solution names a specific skill, section, and change
4. **One concern per entry?** — no mixed issues in a single entry

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `analysis.md` not found (remove flow) | Report "No analysis file found" → stop |
| Invalid entry number | List valid entry numbers → stop |
| `.gitignore` not found | Create it with `analysis.md` entry |
| Vague input | Ask ONE clarifying question, then proceed |

## Anti-patterns

- **Project-specific content.** Domain terms, specific file paths from the current project, business logic — because entries must be reusable across all projects that consume the skill.
- **Vague entries without proposals.** "Improve X" without saying how — because skill maintainers cannot implement without concrete changes to specific sections.
- **Duplicate entries.** Adding a new entry when the same concern exists — because duplicates create confusion and waste review time. Always scan and update instead.
- **One-time fixes as entries.** Recording something that happened once and won't recur — because analysis entries should capture repeatable patterns, not incidents.

## Guidelines

- **Project-agnostic content only.** Never reference project-specific files, domain terms, or business logic. Generalize: "when a migration introduces new tables" not "the Supabase migration for the owners table" — because this file feeds into global skills that work across all projects.

- **Always identify the affected skill.** Every entry must have a `**Skill:**` field. Infer the skill from context — which skill was running when the issue occurred. Format: backtick-wrapped skill name + parenthetical scope hint — because this makes entries scannable and unambiguous when consumed in a different session.

- **One concern per entry.** If the user describes multiple issues, create multiple entries — because mixed entries are harder to implement and harder to remove when partially done.

- **Actionable proposals.** Every entry must end with something a skill maintainer can implement — a specific change to a specific skill section — because "improve the push skill" is not actionable while "add a pre-commit check to push Step 3" is.

- **Stale entry awareness.** When loading an existing file, check the `Source session` date. If entries are older than 2 weeks, mention it: "This file has entries from [date] — want to review them before adding more?" — because stale entries lose context and may no longer be relevant.
