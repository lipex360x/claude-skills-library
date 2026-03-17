# /merge-pr

Merge the current branch's PR, write a detailed implementation summary on the issue, notify unblocked issues, and move the card to Done.

## Triggers

- `/merge-pr`
- "merge pr", "merge this", "land the pr"

## How it works

1. **Find the PR** — locates the open PR for the current branch
2. **Determine target branch** — reads `pr-merge-to` from `.claude/project-settings.json` (default: `main`)
3. **Write implementation summary** — posts a detailed comment on the linked issue covering what was built, key decisions, files changed, test coverage, and verification steps
4. **Move card** — Ready to PR → merge → Done
5. **Notify unblocked issues** — scans for `Blocks #N` in the issue body, comments on unblocked issues and moves their cards to "Ready"
6. **Milestone check** — reports milestone progress or completion
7. **Switch branch** — checks out the target branch and pulls

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
