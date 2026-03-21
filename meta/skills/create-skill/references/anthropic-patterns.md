# Anthropic Patterns for Skills

Patterns from Anthropic's skill design that improve quality, token efficiency, and predictability. Apply these when creating or reviewing skills.

## Table of contents

- [Allowed tools](#allowed-tools)
- [Few-shot examples](#few-shot-examples)
- [Dynamic context injection](#dynamic-context-injection)
- [Structured output with XML tags](#structured-output-with-xml-tags)

## Allowed tools

Restrict which tools a skill can use via the `allowed-tools` frontmatter field. This prevents skills from calling tools they don't need — reducing accidental side effects and making the skill's capabilities explicit.

```yaml
---
name: list-issues
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---
```

**When to use:**
- Every skill should declare `allowed-tools` because it signals intent and prevents unintended tool usage (e.g., a read-only skill accidentally writing files).

**Guidelines:**
- Include only tools the skill genuinely needs in its workflow.
- Read-only skills (audit, list, inspect): `Read`, `Glob`, `Grep`, `Bash` (for `gh` commands).
- Skills that modify files: add `Edit`, `Write`.
- Skills with user interaction: add `AskUserQuestion`.
- Skills that spawn subagents: add `Agent`.
- Skills that need web access: add `WebSearch`, `WebFetch`.

**Common mistake:** Omitting `allowed-tools` entirely. Without it, the skill has access to all tools — including destructive ones like `Write` and `Bash` that a read-only skill should never touch.

## Few-shot examples

Include concrete input/output examples in the SKILL.md or references to show the model what good output looks like. Few-shot examples are more effective than abstract descriptions because the model pattern-matches against them.

**When to use:**
- Skills that produce structured output (reports, tables, specs, code).
- Skills where output quality varies without a concrete reference point.
- High-frequency skills where consistency matters across invocations.

**How to apply:**

Embed a small example directly in the SKILL.md step that produces the output:

```markdown
### 4. Produce the report

Generate the report in this format:

| Check | Status | Finding |
|-------|--------|---------|
| Input contract | ✅ pass | Required/optional inputs defined with validation |
| Anti-patterns | ❌ fail | No anti-patterns section found |
```

For complex examples, extract to `templates/` and reference with a Read instruction:

```markdown
Read `templates/output-example.md` for the expected format.
```

**Common mistake:** Describing the output format in prose ("produce a markdown table with columns for...") instead of showing the actual table. The model follows shapes more reliably than descriptions.

## Dynamic context injection

Load reference content at runtime using Read tool instructions instead of embedding everything in the SKILL.md. This keeps the main file under 500 lines while making detailed knowledge available on demand.

```markdown
Read `references/quality-techniques.md` for the full set of techniques.
```

**When to use:**
- Content that exceeds 50 lines and isn't needed in every invocation.
- Reference data that changes independently of the main skill logic.
- Detailed examples, templates, or lookup tables.

**Three-tier architecture:**

| Tier | File | Token cost | When loaded |
|------|------|-----------|-------------|
| 1 | SKILL.md | Always | Every invocation |
| 2 | references/*.md | On demand | When a step requires it |
| 3 | templates/*.md | On demand | When producing output |

**Guidelines:**
- SKILL.md contains the workflow, decisions, and quality gates.
- References contain the detailed how-to knowledge.
- Templates contain output shapes and starter structures.
- Each reference should be self-contained — no reference chains (A reads B reads C).

**Common mistake:** Using `@` import syntax in SKILL.md. The `@` import only works in CLAUDE.md files — in SKILL.md, use explicit Read tool instructions.

## Structured output with XML tags

Use XML tags in skill instructions to delimit structured sections that the model should treat as distinct blocks. This improves parsing accuracy and reduces bleed between sections.

**When to use:**
- Agent prompts where multiple pieces of context are injected (checklist + skill list + instructions).
- Skills that pass structured data between steps or to subagents.
- Templates with placeholder sections that the model fills in.

**How to apply in agent prompts:**

```markdown
You are auditing skills for quality compliance.

<checklist>
{full checklist content}
</checklist>

<skills-to-audit>
{list of skill paths}
</skills-to-audit>

For each skill, evaluate against the checklist and produce a report.
```

**How to apply in output templates:**

```markdown
<brief>
- Target: {what is being built}
- Constraints: {key limitations}
- Quality bar: {what "done" looks like}
</brief>
```

**Guidelines:**
- Use descriptive tag names that match the content (`<checklist>`, not `<data>`).
- Keep the content inside tags self-contained — the model should understand each block independently.
- Don't nest XML tags more than one level deep — it adds complexity without clarity.

**Common mistake:** Using XML tags for everything. They add value for structured data boundaries — not for prose instructions. If the content reads naturally as markdown, use markdown.
