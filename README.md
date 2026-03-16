# Claude Skills Library

> Production-ready skills for Claude Code — workflow automation, project scaffolding, design systems, and more.

## Installation

Install all skills:

```bash
npx skills add lipex360x/claude-skills-library --all
```

Install a specific skill:

```bash
npx skills add lipex360x/claude-skills-library --skill create-skill
```

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| [create-skill](./create-skill/) | `/create-skill` | Guide for creating, reviewing, and improving Claude Code skills |
| [start-new-project](./start-new-project/) | `/start-new-project` | Plan and scaffold projects with structured GitHub issues |
| [push](./push/) | `/push` | Commit, push, and auto-update issue checkboxes |
| [prompt-continue](./prompt-continue/) | `/prompt-continue` | Generate continuation prompts for seamless session handoffs |
| [system-design](./system-design/) | `/system-design` | Extract design systems from reference images into artboards |

> [!TIP]
> Each skill has its own README with trigger phrases, workflow details, and usage examples. Click any skill link above to learn more.

## Adding new skills

New skills created with `/create-skill` automatically generate a README following the standard [template](./templates/skill-readme.md).
