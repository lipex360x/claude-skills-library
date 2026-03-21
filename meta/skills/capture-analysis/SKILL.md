---
name: capture-analysis
description: Capture skill gaps, workflow frictions, and pattern improvements as structured entries in an analysis file. Use when the user says "/capture-analysis", "analisa isso", "estuda isso", "documenta essa melhoria", "adiciona no analysis", "lessons learned", or wants to record a finding for future skill updates — even if they don't explicitly say "analysis."
user-invocable: true
---

# Analysis

Capture learnings during work sessions as structured, project-agnostic entries in `analysis.md`. This file is a feedback buffer between skill users and skill maintainers — consistent format in, reliable implementation out.

## Steps

### 1. Load or create

Check if `analysis.md` exists at the project root. Run `date "+%H:%M"` for the current timestamp.

- **File exists** → read it, note the last entry number.
- **File doesn't exist** → check `.gitignore` for `analysis.md`. If not present, append `analysis.md` to `.gitignore` (this file contains session-specific learnings, not project code). Then create it with the header:

```markdown
# Lessons Learned for Skill Updates

Source session: <YYYY-MM-DD> ~<HH:MM>
Purpose: project-agnostic learnings to feed back into skills.

---
```

### 2. Parse the input

**Input contract:**
- **No arguments** → prompt the user for what to capture.
- **Free text** → extract the learning (main flow below).
- **`remove <N>` or `remover <N>`** → go to the **Remove entry** flow. `N` must be a positive integer matching an existing entry number. If `N` is not a number, out of range, or the file has no entries, tell the user what went wrong and list valid entry numbers (or state the file is empty).

If `$ARGUMENTS` matches the remove pattern, go to the **Remove entry** flow below.

Otherwise, extract from the user's description:
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

## Remove entry

When the user says `/capture-analysis remove N` or marks an item as implemented:

1. Read the file. If the file doesn't exist or has no entries, tell the user: "No analysis file found (or no entries to remove)." and stop.
2. Validate N: must be a positive integer within the range of existing entries. If invalid, list available entry numbers and stop.
3. Identify and remove entry N.
4. Renumber remaining entries sequentially (no gaps).
5. If no entries remain, delete the file entirely (`rm analysis.md`).
6. Confirm: "Removed entry N: [title]. [M entries remaining / File removed.]"

## Guidelines

- **Project-agnostic content only.** Never reference project-specific files, domain terms, or business logic. Generalize: "when a migration introduces new tables" not "the Supabase migration for the owners table". This file feeds into global skills that work across all projects — project-specific details make entries unusable outside their origin context.

- **Always identify the affected skill.** Every entry must have a `**Skill:**` field after the title. Infer the skill from context — which skill was running when the issue occurred, or which skill the user references. If ambiguous, ask. Format: backtick-wrapped skill name + parenthetical scope hint (e.g., `` `create-diagram` (Phase 3 Excalidraw agent) ``). This makes entries scannable and unambiguous when consumed in a different session.

- **One concern per entry.** If the user describes multiple issues, create multiple entries. Mixed entries are harder to implement and harder to remove when partially done.

- **Actionable proposals.** Every entry must end with something a skill maintainer can implement — a specific change to a specific skill, command, or workflow. "Improve the push skill" is not actionable. "Add a pre-commit check for ARCHITECTURE.md drift to the push skill's Step 3" is.

- **Stale entry awareness.** When loading an existing file, check the `Source session` date. If entries are older than 2 weeks with no action, mention it to the user: "This file has entries from [date] — want to review them before adding more?"

- **Avoid these anti-patterns:**
  - Project-specific content (domain terms, specific file paths from the current project, business logic)
  - Vague entries without concrete proposals ("improve X" without saying how)
  - Duplicate entries — always check existing entries before adding; update if same concern with new context
  - Entries that describe a one-time fix, not a repeatable pattern (if it only happened once and won't recur, it's not worth a skill change)
