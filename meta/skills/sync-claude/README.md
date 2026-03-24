# sync-claude

> Synchronize the Claude Code environment (skills-library + .brain) across machines.

Pulls latest from both `skills-library` and `.brain` repos, rebuilds all symlinks via `setup.sh`, and verifies the installation. Handles dirty working trees and diverged branches gracefully with user-driven choices.

## Usage

```text
/sync-claude
```

> [!TIP]
> Also activates when you say "sync claude", "sync skills", "sync brain", "pull skills", "update claude code", "update skills", "atualiza skills", "sincroniza", or want to bring your environment up to date.

## How it works

1. **Check working tree status** — Detects uncommitted changes in each repo; offers stash-and-pull, skip, or abort
2. **Pull latest** — Runs `git pull` on both repos; handles diverged branches with rebase/skip/abort options
3. **Rebuild symlinks** — Executes `setup.sh` to recreate all skill symlinks after both pulls complete
4. **Verify sync** — Checks for broken symlinks, unmanaged directories, and wrong targets in `~/.claude/skills/`
5. **Report** — Shows per-repo status (commits pulled, branch), symlink count, and any discrepancies

## Directory structure

```text
sync-claude/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill sync-claude
```
