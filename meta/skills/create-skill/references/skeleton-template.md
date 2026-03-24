# Canonical Skill Skeleton

Every skill follows this 13-section structure. Sections are never omitted — when a section does not apply, mark it as Skipped with a reason. An absent section is ambiguous; a Skipped section is explicit.

## Table of contents

- [Section order](#section-order)
- [Section reference](#section-reference)
- [Progressive disclosure rules](#progressive-disclosure-rules)
- [XML tag usage](#xml-tag-usage)
- [Depth-adaptive examples](#depth-adaptive-examples)

## Section order

| # | Section | Format | XML tag | Skippable |
|---|---------|--------|---------|-----------|
| 1 | Frontmatter | YAML between `---` | — | No |
| 2 | Title + Intro | `#` heading + 1-2 sentences | — | No |
| 3 | Input contract | Table | `<input_contract>` | Yes |
| 4 | Output contract | Table | `<output_contract>` | Yes |
| 5 | External state | Table | `<external_state>` | Yes |
| 6 | Pre-flight | Numbered list | `<pre_flight>` | **No** |
| 7 | Steps | Numbered `###` headers | — | No |
| 8 | Next action | 1-3 lines | — | Yes |
| 9 | Self-audit | Numbered list | `<self_audit>` | **No** |
| 10 | Content audit | Numbered list or criteria | `<content_audit>` | Yes |
| 11 | Error handling | Table | — | Yes |
| 12 | Anti-patterns | Bullet list | — | **No** |
| 13 | Guidelines | Bullet list | — | **No** |

**Never-skip sections:** Pre-flight, Self-audit, Anti-patterns, and Guidelines always have content — every skill validates something, audits its own execution, has failure modes to avoid, and has principles to follow.

## Section reference

### 1. Frontmatter

YAML metadata between `---` delimiters. Mandatory fields:

```yaml
---
name: verb-subject              # Required. Lowercase + hyphens, verb-subject pattern
description: >-                 # Required. Pushy trigger description — WHAT + WHEN + "even if"
  [Action summary] — [key details]. Use when the user says "[trigger 1]",
  "[trigger 2]", "[trigger 3]", or wants to [action] — even if they don't
  explicitly say "[keyword]."
user-invocable: true            # Required. true for /commands, false for auto-triggered
allowed-tools:                  # Required. Explicit list — omitting means all tools available
  - Read
  - Edit
  - Bash
argument-hint: [hint]           # Optional. Shows in autocomplete: /skill-name <hint>
---
```

`allowed-tools` is mandatory because it signals intent and prevents unintended tool usage. A read-only skill should never have `Write` or `Bash` access.

### 2. Title + Intro

```markdown
# Skill Title

One-line summary of what this skill does and why it exists.
```

The intro sets context in a single sentence. It is not a description duplicate — it explains the skill's value, not its triggers.

### 3. Input contract

What the skill receives, how it validates, and what happens on invalid input.

```markdown
## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `issue-number` | $ARGUMENTS | yes | Positive integer | AUQ with open issues list |
| `--confirm` | $ARGUMENTS | no | Flag presence | — |

</input_contract>
```

**When to skip:**

```markdown
## Input contract

> _Skipped: "No input — operates on current directory state."_
```

### 4. Output contract

What the skill produces, where, and whether it persists beyond the session.

```markdown
## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| GitHub issue | GitHub API | yes | Markdown body |
| Board card | GitHub Projects | yes | Status field update |
| Report | stdout | no | Markdown |

</output_contract>
```

**When to skip:**

```markdown
## Output contract

> _Skipped: "No persistent output — conversational only."_
```

### 5. External state

Resources the skill reads or writes outside its own directory. This documents the skill's footprint — what it touches in the wider system.

```markdown
## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Project board | GitHub Projects API | R/W | GraphQL |
| Issue body | `gh issue view` | R/W | Markdown |
| Config | `.claude/project-settings.json` | R | JSON |

</external_state>
```

**When to skip:**

```markdown
## External state

> _Skipped: "N/A — self-contained, no external reads or writes."_
```

### 6. Pre-flight

Validations before any work begins. This section is **never skipped** — every skill validates something before starting.

```markdown
## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
3. Working tree has changes → if clean: "Nothing to push." — stop.

</pre_flight>
```

Common pre-flight checks by skill type:

| Skill type | Pre-flight checks |
|---|---|
| GitHub workflow | `gh` installed + authenticated, repo exists, board exists |
| File generation | Target directory exists, template files readable |
| Content creation | Voice profile exists, draft directory exists |
| Codebase analysis | Source files exist, project has sufficient complexity |
| MCP-dependent | Required MCP tools available |
| Conversational | Sufficient conversation context (3+ substantive messages) |

### 7. Steps

The core workflow. Always numbered `###` headers. The **last numbered step is always Report**.

```markdown
## Steps

### 1. Gather state

Run these in parallel:
...

### 2. Analyze and group

...

### N. Report

Present concisely:
- **What was done** — actions taken, artifacts created
- **Audit results** — self-audit + content audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")
```

Guidelines for steps:
- **Imperative form.** "Parse the config", "Read the template" — not "You should parse..."
- **Explain the why.** "Avoid X because Y" works better than rigid "NEVER do X" — Claude 4.6 handles edge cases better when it understands the reasoning.
- **One concern per step.** Each step should represent a focused work session.
- **Report is always last.** It summarizes what happened, includes audit results, and closes the skill execution.

### 8. Next action

What the user should do after this skill completes. Even simple suggestions help with workflow continuity.

```markdown
## Next action

Run `/open-pr` when all issue checkboxes are complete.
```

**When to skip:**

```markdown
## Next action

> _Skipped: "Session complete — no follow-up needed."_
```

### 9. Self-audit

Process verification that runs before the Report step. This section is **never skipped** — every skill verifies its own execution.

```markdown
## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — all validations green, or user approved override
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — verify artifacts were created/modified as declared in Output contract
4. **Anti-patterns clean?** — scan execution for violations of the Anti-patterns section
5. **Approval gates honored?** — all required user confirmations obtained

If any check fails, note it in the Report. Do not block — report the gap and let the user decide.

</self_audit>
```

### 10. Content audit

Verification of generated output accuracy and quality. Applies to skills that produce verifiable content (lessons, posts, diagrams, issue plans, skill files).

```markdown
## Content audit

<content_audit>

Before finalizing output, verify:

1. **Facts correct?** — WebSearch to confirm claims against authoritative sources
2. **Format matches contract?** — output follows the structure declared in Output contract
3. **References valid?** — all paths and URLs cited exist and are accessible
4. **Quality bar met?** — content meets skill-specific quality criteria

Audit is scoped to content generated in THIS session. Full re-audit is `/audit-skill`'s job.

</content_audit>
```

Read `references/content-audit-patterns.md` for the audit type taxonomy and concrete examples.

**When to skip:**

```markdown
## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (read-only / state management)."_
```

### 11. Error handling

Declared strategy per failure type. When a skill calls external tools, APIs, or reads dependencies, it should declare how it handles failures.

```markdown
## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Network error | Report error with details → stop (no silent retry) |
| File not found | Report path and suggest fix → stop |
| Partial completion | Report what succeeded, suggest manual fix for remainder |
```

**When to skip:**

```markdown
## Error handling

> _Skipped: "No external calls — no error surface."_
```

### 12. Anti-patterns

Specific failure modes to avoid. This section is **never skipped** — every skill has traps. Named "Anti-patterns" (not "Avoid these", "What doesn't work", or inline in Guidelines). Always its own section.

```markdown
## Anti-patterns

- **Force-pushing.** Rewrites shared history — because others pulling the branch will get conflicts or lose work.
- **Amending after hook failure.** The failed commit never landed, so `--amend` modifies the *previous* commit — because this potentially destroys unrelated work.
- **Staging secrets.** `.env`, `*.key`, `*.pem` files with real values — because pre-commit hooks are the second line of defense, not the first.
```

Format: **Bold name.** Description with consequence — because reason.

### 13. Guidelines

Principles and reasoning that guide the skill's behavior. Separate from Anti-patterns (which name what to avoid). Guidelines name what to pursue and why.

```markdown
## Guidelines

- **No gates by default.** The default flow is fully automated. Only stop and ask when something unexpected happens — because unnecessary confirmation steps break flow and train users to click "approve" reflexively.

- **Graceful degradation.** If `gh` is not available, skip the issue update step. If the branch has no issue, skip it — because the core job (commit + push) should always complete even when optional steps fail.
```

Format: **Bold principle.** Explanation with reasoning — because context.

## Progressive disclosure rules

The SKILL.md body must stay under 500 lines. When content grows, use the three-tier architecture:

| Tier | Content | Size | When loaded |
|------|---------|------|-------------|
| **Metadata** | `name` + `description` | ~100 tokens | Always in context |
| **SKILL.md body** | Skeleton sections | <500 lines | When skill activates |
| **Resources** | references/, templates/, scripts/ | Unlimited | On demand via Read tool |

### Overflow rules

When a skeleton section exceeds **~15 lines** of content, extract to a reference file:

1. Keep the **top 3-5 most critical items** inline in SKILL.md
2. Add a Read pointer to the full reference:
   ```markdown
   Read `references/anti-patterns.md` for the full list.
   ```
3. Information lives in **ONE place** — either SKILL.md or the reference, never duplicated in both

### Large references (>300 lines)

Include a table of contents at the top so the agent can navigate efficiently. For references >10k words, include grep search patterns in SKILL.md:

```markdown
Read `references/guide.md` — search for "## CDP Setup" for setup steps,
"## Troubleshooting" for common issues.
```

### Scripts as tier 3

Scripts in `scripts/` can be **executed without loading into context** — the most token-efficient tier 3 resource. Extract deterministic bash logic to scripts when possible.

## XML tag usage

XML tags create explicit boundaries that improve Claude's parsing of structured data. Use them for **contracts and audit blocks** — not for prose or sequential steps.

| Content type | Use XML | Use Markdown |
|---|---|---|
| Contract tables (input, output, external state) | `<input_contract>` | — |
| Audit checklists (pre-flight, self-audit, content audit) | `<pre_flight>` | — |
| Report structure | `<report>` | — |
| Subagent context injection | `<checklist>`, `<context>` | — |
| Sequential workflow steps | — | Numbered `###` headers |
| Prose explanations | — | Paragraphs and bullets |
| Anti-patterns and guidelines | — | Bold + bullet format |

Read `references/xml-tag-patterns.md` for the full pattern catalog and Claude 4.6 language guidance.

## Depth-adaptive examples

### Simple skill: clean-tasks (~35 lines)

```markdown
---
name: clean-tasks
description: >-
  Remove completed tasks from the task visibility board, keeping pending and
  in-progress items. Use this skill when the user says "clean tasks", "remove
  done tasks", "clear completed", "tv clean", or wants to tidy up the task
  list — even if they don't explicitly say "clean."
user-invocable: true
allowed-tools:
  - TaskList
  - TaskUpdate
---

# Clean Tasks

Remove completed tasks from the task list. Keep pending and in-progress tasks untouched.

## Input contract

> _Skipped: "No input — operates on current task list state."_

## Output contract

> _Skipped: "No persistent output — task deletions are immediate."_

## External state

> _Skipped: "N/A — operates only on the task system."_

## Pre-flight

<pre_flight>

1. Task list has completed tasks → if none: "No completed tasks to clean." — stop.

</pre_flight>

## Steps

### 1. Find completed tasks

Use TaskList to identify all tasks with status `completed`.

### 2. Delete completed tasks

Use TaskUpdate with status `deleted` for each completed task.

### 3. Report

- **Removed:** {count} completed tasks
- **Remaining:** {count} pending/in-progress tasks (list briefly)

## Next action

> _Skipped: "Session complete — no follow-up needed."_

## Self-audit

<self_audit>

1. Pre-flight passed? — completed tasks existed
2. Steps completed? — all completed tasks deleted
3. Anti-patterns clean? — no pending/in-progress tasks touched

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content."_

## Error handling

> _Skipped: "No external calls — no error surface."_

## Anti-patterns

- **Deleting pending or in-progress tasks.** Only completed tasks are cleaned — because active tasks represent work the user needs to track.

## Guidelines

- **Silent execution.** No user confirmation needed — cleaning completed tasks is a safe, reversible operation.
```

### Complex skill overflow pattern (add-lesson style, ~490 lines)

When a complex skill approaches 500 lines, sections overflow to references:

```markdown
## Anti-patterns

Read `references/anti-patterns.md` for the full list (22 items). Key traps:

- **Generating all content at once.** Each section is a conversation — because bulk generation produces generic output with no user input on quality.
- **Skipping CDP validation.** Never consider a lesson complete without screenshots — because layout breaks on mobile are the most common failure mode.
- **Text-only lessons.** Every lesson needs at least one visual element — because pure text is visually poor and fails to illustrate abstract concepts.
```

The full 22-item list lives in `references/anti-patterns.md`. SKILL.md has the top 3 inline for quick scanning. This keeps the body under 500 lines while all detail remains accessible.
