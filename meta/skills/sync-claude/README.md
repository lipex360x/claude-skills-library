# sync-claude

> Synchronize the Claude Code environment (skills-library + .brain) across machines.

One-command environment sync that pulls both repos (`skills-library` and `.brain`), rebuilds all symlinks via `setup.sh`, and runs a 3-check verification (broken symlinks, unmanaged directories, wrong targets). Handles dirty working trees with stash-and-pull and diverged branches with rebase — all user-driven via AUQ choices.

## Usage

```text
/sync-claude
```

> [!TIP]
> Also activates when you say "sync claude", "sync skills", "sync brain", "pull skills", "update claude code", "update skills", "atualiza skills", "sincroniza", or want to bring your environment up to date.

### Examples

```text
/sync-claude               # pull both repos, rebuild symlinks, verify
```

Also triggered by natural language:

```text
"sync my skills"           # same effect via model invocation
"update claude environment" # same effect via model invocation
```

> [!NOTE]
> Requires both `~/www/claude/skills-library/` and `~/www/claude/.brain/` directories. If either is missing, offers to clone it or skip.

## How it works

1. **Check working tree status** — Detects uncommitted changes in each repo; offers stash-and-pull, skip, or abort via AUQ
2. **Pull latest** — Runs `git pull` on both repos; handles diverged branches with rebase/skip/abort options. Tracks commits pulled per repo
3. **Rebuild symlinks** — Executes `setup.sh` to recreate all skill symlinks after both pulls complete
4. **Verify sync** — Runs 3 checks against `~/.claude/skills/`: broken symlinks, unmanaged directories (non-symlinks), and symlinks pointing outside skills-library
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
