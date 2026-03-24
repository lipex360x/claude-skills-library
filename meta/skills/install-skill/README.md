# install-skill

> Install a skill from an npx skills link, with local or global selection.

Full installation pipeline from npx command to production-ready skill. Local installs are a single command; global installs include a 13-step flow covering duplicate detection, plugin group classification (7 groups: workflow, content, design, database, deploy, meta, tasks), symlink creation via `setup.sh`, index updates (STRUCTURE.md + both READMEs), end-to-end verification, and git push.

## Usage

```text
/install-skill <npx-skills-add-command>
```

> [!TIP]
> Also activates when you say "install skill", "add skill", "skill install", or provide an npx skills command.

### Examples

```text
/install-skill npx skills add vercel-labs/agent-skills --skill react   # install from a known source
/install-skill npx skills add owner/repo --skill my-tool               # install any skill by command
```

> [!NOTE]
> Requires `npx` (Node.js) for running the install command. Global installs also require `git` and the skills-library repo at `~/www/claude/skills-library/`.

## How it works

1. **Ask scope** — If not specified, asks local (project) or global (skills-library/) via AUQ
2. **Execute local install** — (local) Runs npx with `--copy -a claude-code -y` flags; skill lands in `.claude/skills/`. Done
3. **Sync skills-library** — (global) Pulls latest from remote before installing
4. **Check for duplicates** — (global) Warns if skill already exists; asks to reinstall or cancel
5. **Run npx** — (global) Executes the install command with `--copy -a claude-code -y` flags
6. **Validate installed skill** — (global) Confirms SKILL.md exists with valid frontmatter (name, description, user-invocable)
7. **Determine target plugin group** — (global) Classifies skill into workflow/content/design/database/deploy/meta/tasks based on description and purpose
8. **Move skill to skills-library** — (global) Moves from `.claude/skills/` to the target plugin directory
9. **Register and clean up** — (global) Runs `setup.sh` for symlinks, cleans npx artifacts (empty dirs, lock files)
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
