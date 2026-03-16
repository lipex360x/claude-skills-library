# Claude Skills Library

> Production-ready skills and commands for Claude Code — workflow automation, project scaffolding, design systems, and more.

## Contents

- [Installation](#installation)
- [Skills](#skills)
- [Commands](#commands)
- [Adding new skills](#adding-new-skills)

## Installation

Install all skills:

```bash
npx skills add lipex360x/claude-skills-library --all
```

Install a specific skill:

```bash
npx skills add lipex360x/claude-skills-library --skill create-skill
```

## Skills

Skills are intelligent, context-aware automations triggered by natural language or `/slash-commands`. Each skill lives in its own directory under `skills/` with a `SKILL.md` and supporting references.

| Skill | Command | Description |
|-------|---------|-------------|
| [analysis](./skills/analysis/) | `/analysis` | Capture skill gaps, workflow frictions, and pattern improvements |
| [backlog-start](./skills/backlog-start/) | `/backlog-start` | Pull a backlog issue and start implementation with expanded plan |
| [create-command](./skills/create-command/) | `/create-command` | Guide for creating or improving Claude Code slash commands |
| [create-hook](./skills/create-hook/) | `/create-hook` | Guide for creating or improving Claude Code hooks |
| [create-readme](./skills/create-readme/) | `/create-readme` | Generate or review a project README.md |
| [create-skill](./skills/create-skill/) | `/create-skill` | Guide for creating, reviewing, and improving Claude Code skills |
| [drawio](./skills/drawio/) | `/drawio` | AI-powered Draw.io diagram creation with YAML design system |
| [find-skills](./skills/find-skills/) | `/find-skills` | Discover and install agent skills from the ecosystem |
| [myvoice](./skills/myvoice/) | `/myvoice` | Capture the user's writing voice for authentic content generation |
| [prompt-continue](./skills/prompt-continue/) | `/prompt-continue` | Generate continuation prompts for seamless session handoffs |
| [push](./skills/push/) | `/push` | Commit, push, and auto-update GitHub issue checkboxes |
| [readme-blueprint-generator](./skills/readme-blueprint-generator/) | `/readme-blueprint-generator` | Generate README from project documentation structure |
| [skill-creator](./skills/skill-creator/) | `/skill-creator` | Create, modify, benchmark, and optimize skills |
| [start-new-project](./skills/start-new-project/) | `/start-new-project` | Plan and scaffold projects with structured GitHub issues |
| [supabase-postgres-best-practices](./skills/supabase-postgres-best-practices/) | — | Postgres performance optimization and best practices |
| [system-design](./skills/system-design/) | `/system-design` | Extract design systems from reference images into artboards |
| [vercel-cli](./skills/vercel-cli/) | `/vercel-cli` | Deploy and manage projects on Vercel from the CLI |
| [written](./skills/written/) | `/written` | Create compelling written content and marketing copy |

> [!TIP]
> Each skill has its own README with trigger phrases, workflow details, and usage examples. Click any skill link above to learn more.

[Back to top](#claude-skills-library)

## Commands

Commands are lightweight slash commands — single `.md` files in `commands/` that perform focused operations.

| Command | Description |
|---------|-------------|
| `/backlog-add` | Create a backlog issue in the project's Backlog milestone |
| `/backlog-list` | List open backlog issues with numbered summary for selection |
| `/issues-list` | List all open issues grouped by milestone with priority sorting |
| `/post-approve` | Approve draft, generate EN translation, publish to local files and Google Drive |
| `/pr-create` | Create a PR from the current branch, linking to the open issue |
| `/pr-merge` | Merge the open PR for the current branch and switch to main |
| `/skill-install` | Install a skill from an npx skills link |
| `/skill-uninstall` | Uninstall a skill by name (local or global) |
| `/tv-clean` | Remove completed tasks from the task visibility board |
| `/tv-close` | Close the task visibility board and stop task tracking |
| `/tv-open` | Reopen the task visibility board and resume task tracking |

[Back to top](#claude-skills-library)

## Adding new skills

New skills created with `/create-skill` automatically generate a README following the standard [template](./templates/skill-readme.md).
