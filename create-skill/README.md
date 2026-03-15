# create-skill

Guide the user through creating, reviewing, or improving Claude Code skills — from structuring SKILL.md files to writing effective descriptions and applying quality techniques.

## Trigger phrases

- "create a skill"
- "improve a skill"
- "skill best practices" / "how to write a skill"
- Also activates when the user wants to build a new `/command` or mentions skill quality — even without explicitly saying "skill"

## How it works

1. **Understand the intent** — Asks what the skill should do, when it should activate, and whether it's user-invocable or auto-triggered
2. **Design the structure** — Plans the directory layout (SKILL.md, templates, references, scripts, assets) using progressive disclosure to keep token costs low
3. **Write the description** — Crafts the trigger description using proven patterns that prevent under-triggering
4. **Write the SKILL.md body** — Follows best practices: imperative form, numbered steps, explicit output formats, under 500 lines
5. **Apply quality techniques** — Adds craftsmanship repetition, anti-patterns lists, and refinement-over-addition steps
6. **Handle subagents** — If applicable, designs prompts and coordination for blank-context subagents
7. **Review against checklist** — Validates every item in the review checklist and presents results before finalizing

## Usage

```
/create-skill
```

Tell the skill what you want to build (e.g., "I want a skill that generates changelogs from git history") and it will walk you through the full creation process with structured questions and approval gates.

## Directory structure

```
create-skill/
├── SKILL.md              # Core instructions for the creation process
├── references/           # Deep-dive guides (description patterns, quality techniques, subagent patterns, review checklist, progressive disclosure)
└── templates/            # Starter SKILL.md template with frontmatter
```

## Installation

```bash
npx @anthropic-ai/claude-code-skills install lipex360x/claude-skills-library/create-skill --copy
```
