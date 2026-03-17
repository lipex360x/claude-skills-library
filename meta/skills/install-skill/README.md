# install-skill

> Install a skill from an npx skills link, with local or global selection.

Handles the full installation flow for skills — from running the npx command to organizing the skill into the correct plugin group in `skills-library/`, creating symlinks, and updating `STRUCTURE.md`.

## Usage

```text
/install-skill <npx-skills-add-command>
```

> [!TIP]
> Also activates when you say "install skill", "add skill", or provide an npx skills command.

## How it works

1. **Ask scope** — If not specified, asks whether to install locally (project) or globally (skills-library/)
2. **Local install** — Runs the npx command with `--copy -a claude-code -y` flags. Skill lands in `.claude/skills/`
3. **Global install** — Runs npx, identifies the installed skill, determines the target plugin group, moves it to `skills-library/<group>/skills/`, creates a symlink in `~/.claude/skills/`, cleans up npx leftovers, and updates `STRUCTURE.md`

> [!NOTE]
> For global installs, the skill automatically determines the correct plugin group (workflow, content, design, database, deploy, meta, tasks) based on the skill's description. If ambiguous, it asks.

## Directory structure

```text
install-skill/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill install-skill
```
