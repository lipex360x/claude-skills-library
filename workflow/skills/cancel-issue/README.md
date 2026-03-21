# /cancel-issue

Cancel an issue — closes it on GitHub with a reason, moves the card to "Cancelled" on the project board, unblocks dependent issues, and cleans up branches/PRs.

## Triggers

- `/cancel-issue <number>`
- "cancel issue", "drop issue", "cancel #N", "won't do", "close as not planned"

## How it works

1. **Select issue** — from argument or current branch name
2. **Ask reason** — presents common cancellation reasons via selectable options
3. **Close issue** — closes on GitHub with `--reason "not planned"` and posts a cancellation comment
4. **Move card** — moves to "Cancelled" column on the project board
5. **Unblock dependents** — scans for `Blocks #N` annotations and reverse dependencies, notifies blocked issues, moves unblocked cards to "Ready"
6. **Clean up** — prompts to close open PRs and delete associated branches
7. **Summary** — reports all actions taken

## Directory structure

```text
cancel-issue/
├── SKILL.md
├── README.md
└── references/
    └── project-board-operations.md    # Commands for moving cards on the board
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill cancel-issue
```
