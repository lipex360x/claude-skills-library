# Progressive Disclosure — The Core Architecture

Skills load in three tiers. This design keeps token costs low and context focused.

| Level | Content | Size | When loaded |
|-------|---------|------|-------------|
| **Metadata** | `name` + `description` | ~100 tokens | Always in context (all sessions) |
| **Instructions** | SKILL.md body | <500 lines | When the skill is activated |
| **Resources** | files in templates/, references/, scripts/ | Unlimited | On demand, when the agent reads them |

## What this means in practice

- The **description** determines whether the skill activates — invest time here.
- The **SKILL.md body** guides execution — keep it lean and processual.
- **Resources** provide depth without bloating the activation payload — use them freely for detailed guidelines, templates, and examples.

## How to reference resources

Use natural language instructions, not special syntax:

```markdown
Read `references/api-patterns.md` for the full endpoint conventions.
```

The agent reads it with the Read tool when it reaches that instruction. Keep file references one level deep — avoid chains where one reference points to another, because it's easy to lose the agent in a reference maze.

## Large references (>300 lines)

Include a table of contents at the top so the agent can navigate efficiently and read only the section it needs.
