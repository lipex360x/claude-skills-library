# install-skill

> Install a skill from an npx skills link, with local or global selection.

Handles the full installation flow — from running the npx command to organizing the skill into the correct plugin group in `skills-library/`, creating symlinks, updating indexes, and pushing to GitHub. Local installs are a single command; global installs include full registration.

## Usage

```text
/install-skill <npx-skills-add-command>
```

> [!TIP]
> Also activates when you say "install skill", "add skill", "skill install", or provide an npx skills command.

## How it works

1. **Ask scope** — If not specified, asks local (project) or global (skills-library/) via AUQ
2. **Execute local install** — Runs npx with `--copy -a claude-code -y` flags; skill lands in `.claude/skills/`
3. **Sync skills-library** — (global) Pulls latest from remote before installing
4. **Check for duplicates** — (global) Warns if skill already exists; asks to reinstall or cancel
5. **Run npx** — (global) Executes the install command
6. **Validate installed skill** — (global) Confirms SKILL.md exists with valid frontmatter
7. **Determine target plugin group** — (global) Classifies skill into workflow/content/design/database/deploy/meta/tasks
8. **Move skill to skills-library** — (global) Moves from `.claude/skills/` to the target plugin directory
9. **Register and clean up** — (global) Runs `setup.sh` for symlinks, cleans npx artifacts
10. **Update indexes** — (global) Updates STRUCTURE.md, skill README, and root README
11. **Verify before pushing** — (global) End-to-end verification of symlink, SKILL.md, STRUCTURE.md, and READMEs
12. **Push to GitHub** — (global) Commits and pushes all changes
13. **Report** — Shows skill name, scope, plugin group, artifacts, and push status

## Directory structure

```text
install-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill install-skill
```
