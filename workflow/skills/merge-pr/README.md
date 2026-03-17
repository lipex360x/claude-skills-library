# /merge-pr

Merge the current branch's PR, write a detailed implementation summary on the issue, and move the card to Done.

## Triggers

- `/merge-pr`
- "merge pr", "merge this", "land the pr"

## How it works

1. **Find the PR** — locates the open PR for the current branch
2. **Determine target branch** — reads `pr-merge-to` from `.claude/project-settings.json` (default: `main`)
3. **Write implementation summary** — posts a detailed comment on the linked issue covering what was built, key decisions, files changed, test coverage, and verification steps
4. **Merge** — merges with `--delete-branch`
5. **Move card** — moves the issue card to "Done" on the project board
6. **Switch branch** — checks out the target branch and pulls

## Directory structure

```text
merge-pr/
├── SKILL.md
├── README.md
└── references/
    └── project-board-operations.md    # Commands for moving cards on the board
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill merge-pr
```
