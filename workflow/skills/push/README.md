# push

> Commit, push, and update GitHub issue checkboxes in one command.

Analyzes changes, drafts a conventional commit message, stages, commits (with husky management), pushes, then reviews and updates the open issue checkboxes for the current branch. Supports `--confirm` flag for commit message approval and `-nh` flag to skip husky.

## Usage

```text
/push
```

> [!TIP]
> Also activates when you say "push", "commit and push", "ship it", or want to finalize work and sync issue tracking.

## How it works

1. **Gather state** — Run `git status`, `git diff`, `git log`, and `git branch` in parallel
2. **Analyze and group changes** — Group by concern, draft separate Conventional Commits messages
3. **Stage and commit** — Stage specific files (never `git add -A`), scan for secrets, commit with husky management
4. **Push** — Push to remote, setting upstream if needed
5. **Update issue checkboxes** — Find the related GitHub issue and mark completed items
6. **Suggest PR (if all checkboxes done)** — Offer to run `/open-pr` when all tasks are complete
7. **Report** — Summary with commits created, push result, and checkbox updates

## Directory structure

```text
push/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── issue-update-guide.md  # Issue checkbox update patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill push
```
