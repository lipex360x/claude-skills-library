# create-skill

Guide the user through creating, reviewing, or improving Claude Code skills — from structuring SKILL.md files to writing effective descriptions and applying quality techniques.

## Trigger phrases

- `create a skill` / `improve a skill`
- `skill best practices` / `how to write a skill`
- Also activates when the user wants to build a new `/command` or mentions skill quality — even without explicitly saying "skill"

## How it works

1. **Understand the intent** — Asks what the skill should do, when it should activate, and whether it's user-invocable or auto-triggered
2. **Design the structure** — Plans the directory layout using progressive disclosure to keep token costs low
3. **Write the description** — Crafts the trigger description using proven patterns that prevent under-triggering
4. **Write the SKILL.md body** — Follows best practices: imperative form, numbered steps, explicit output formats, under 500 lines
5. **Apply quality techniques** — Adds craftsmanship repetition, anti-patterns lists, and refinement-over-addition steps
6. **Handle subagents** — If applicable, designs prompts and coordination for blank-context subagents
7. **Review against checklist** — Validates every item in the review checklist and presents results before finalizing
8. **Generate README.md** — Creates public-facing documentation using the README template

## Usage

```
/create-skill
```

Tell the skill what you want to build (e.g., "I want a skill that generates changelogs from git history") and it will walk you through the full creation process with structured questions and approval gates.

> [!TIP]
> The skill also works in review mode — point it at an existing skill and it will evaluate it against the built-in checklist with specific improvement suggestions.

## Directory structure

```
create-skill/
├── SKILL.md                # Core instructions for the creation process
├── references/
│   ├── description-patterns.md     # Trigger description examples and the "pushy" technique
│   ├── progressive-disclosure.md   # Three-tier architecture for token efficiency
│   ├── quality-techniques.md       # Craftsmanship repetition, anti-patterns, refinement
│   ├── subagent-patterns.md        # Blank-context coordination and two-phase builds
│   └── review-checklist.md         # Validation checklist for finalizing skills
└── templates/
    └── skill-template.md           # Starter SKILL.md with frontmatter
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-skill
```
