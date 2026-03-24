# Progressive Disclosure — The Core Architecture

Skills load in three tiers. This design keeps token costs low and context focused.

## Table of contents

- [Three-tier architecture](#three-tier-architecture)
- [Tier details](#tier-details)
- [Overflow threshold](#overflow-threshold)
- [Large references](#large-references-300-lines)
- [Grep patterns for navigation](#grep-patterns-for-navigation)
- [Scripts as tier 3](#scripts-as-tier-3)
- [How to reference resources](#how-to-reference-resources)

## Three-tier architecture

| Tier | Content | Size | When loaded |
|------|---------|------|-------------|
| **1. Metadata** | `name` + `description` | ~100 tokens | Always in context (all sessions) |
| **2. SKILL.md body** | Skeleton sections | <500 lines | When the skill is activated |
| **3. Resources** | files in references/, templates/, scripts/ | Unlimited | On demand via Read tool |

## Tier details

**Tier 1 — Metadata (~100 tokens, always in context).** The description determines whether the skill activates. Invest time here because a weak description means the skill never fires when it should, and a broad description means it fires when it shouldn't. The ~100 token budget means every word earns its place.

**Tier 2 — SKILL.md body (<500 lines, when activated).** The body guides execution. Keep it lean and processual — workflow steps, decision points, and quality gates. When a section exceeds the overflow threshold, extract to tier 3 and keep only the top items inline.

**Tier 3 — Resources (unlimited, on demand).** References, templates, and scripts provide depth without bloating the activation payload. Use them freely for detailed guidelines, examples, and lookup tables. The agent reads them with the Read tool when it reaches a pointer instruction.

## Overflow threshold

When a skeleton section exceeds **~15 lines** of content, extract to a reference file:

1. Keep the **top 3-5 most critical items** inline in SKILL.md
2. Add a Read pointer to the full reference:
   ```markdown
   Read `references/anti-patterns.md` for the full list.
   ```
3. Store information in **one place** — either SKILL.md or the reference, never duplicated in both

Example of a section that overflows correctly:

```markdown
## Anti-patterns

Read `references/anti-patterns.md` for the full list (22 items). Key traps:

- **Generating all content at once.** Each section is a conversation — because bulk generation produces generic output.
- **Skipping CDP validation.** Never consider a lesson complete without screenshots — because layout breaks are the most common failure mode.
- **Text-only lessons.** Every lesson needs at least one visual element — because pure text fails to illustrate abstract concepts.
```

The full 22-item list lives in the reference. SKILL.md has the top 3 inline for quick scanning. This keeps the body under 500 lines while all detail remains accessible.

## Large references (>300 lines)

Include a table of contents at the top so the agent can navigate efficiently and read only the section it needs. Structure the TOC with anchored links:

```markdown
## Table of contents

- [Section A](#section-a)
- [Section B](#section-b)
- [Section C](#section-c)
```

## Grep patterns for navigation

For references exceeding ~10k words, include grep search patterns in the SKILL.md pointer so the agent can jump directly to the relevant section without reading the entire file:

```markdown
Read `references/guide.md` — search for "## CDP Setup" for setup steps,
"## Troubleshooting" for common issues.
```

This lets the agent use the Grep tool to locate the exact section before reading, avoiding the token cost of loading the entire file into context.

## Scripts as tier 3

Scripts in `scripts/` can be **executed without loading into context** — the most token-efficient tier 3 resource. The agent runs the script via Bash and reads only the output, never the source code.

Extract deterministic bash logic to scripts when possible:
- Validation checks that inspect files or system state
- Data gathering that aggregates multiple `gh` or `git` calls
- Formatting pipelines that transform structured data

```markdown
### 2. Gather metrics

Run `scripts/collect-metrics.sh` and capture the output.
```

The script does the work; the agent reads the result. Zero tokens spent on implementation detail.

## How to reference resources

Use natural language instructions, not special syntax:

```markdown
Read `references/api-patterns.md` for the full endpoint conventions.
```

The agent reads it with the Read tool when it reaches that instruction. Keep file references one level deep — avoid chains where one reference points to another, because it loses the agent in a reference maze.

For the full skeleton structure and section definitions, see `references/skeleton-template.md`.
