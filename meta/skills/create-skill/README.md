# create-skill

> Guide the user through creating, reviewing, or improving Claude Code skills.

Step-by-step guide for building high-quality Claude Code skills — from structuring SKILL.md files to writing effective descriptions, designing progressive disclosure, and launching subagents. Distilled from Anthropic's official skill repository and hands-on experience shipping production skills.

## Usage

```text
/create-skill
```

> [!TIP]
> Also activates when you say "create a skill", "improve a skill", "skill best practices", "how to write a skill", or want to build or review a skill.

## How it works

1. **Understand the intent** — Asks what the skill should do, when it should activate, and whether it's user-invocable or auto-triggered
2. **Design the structure** — Plans the directory layout using progressive disclosure to keep token costs low
3. **Write the description** — Crafts the trigger description using proven patterns that prevent under-triggering
4. **Write the SKILL.md body** — Imperative form, numbered steps, explicit output formats, under 500 lines
5. **Apply quality techniques** — Craftsmanship repetition, anti-patterns lists, and refinement-over-addition steps
6. **Handle subagents** — If applicable, designs prompts and coordination for blank-context subagents
7. **Review against checklist** — Validates every item before finalizing
8. **Generate README.md** — Creates public-facing documentation using the README template

## Directory structure

```text
create-skill/
├── SKILL.md                          # Core instructions for the creation process
├── references/
│   ├── description-patterns.md       # Trigger description examples and the "pushy" technique
│   ├── progressive-disclosure.md     # Three-tier architecture for token efficiency
│   ├── quality-techniques.md         # Craftsmanship repetition, anti-patterns, refinement
│   ├── review-checklist.md           # Validation checklist for finalizing skills
│   └── subagent-patterns.md          # Blank-context coordination and two-phase builds
└── templates/
    └── skill-template.md             # Starter SKILL.md with frontmatter
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-skill
```
