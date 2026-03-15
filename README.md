# Claude Skills Library

Curated collection of Claude Code skills.

## Installation

Install all skills:

```bash
npx skills add lipex360x/claude-skills-library --all
```

Install a specific skill:

```bash
npx skills add lipex360x/claude-skills-library -s create-skill
```

## Available Skills

| Skill | Description |
|-------|-------------|
| [create-skill](./create-skill/) | Guide for creating, reviewing, and improving Claude Code skills |
| [prompt-continue](./prompt-continue/) | Generate continuation prompts for seamless session handoffs |
| [system-design](./system-design/) | Extract design systems from reference images into artboards |
| [start-new-project](./start-new-project/) | Plan and scaffold projects with structured GitHub issues |
| [push](./push/) | Commit, push, and auto-update issue checkboxes |

Each skill has its own [README.md](./create-skill/README.md) with trigger phrases, how it works, usage examples, and installation instructions. Click any skill link above to see its documentation.

## Skill documentation

Every skill in this library includes a `README.md` in its directory. New skills created with the `create-skill` skill automatically generate a README following the standard [template](./templates/skill-readme.md).
