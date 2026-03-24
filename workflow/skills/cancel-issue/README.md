# cancel-issue

> Cancel an issue — closes it on GitHub with a reason, moves the card to "Cancelled" on the project board, unblocks dependent issues, and cleans up branches/PRs.

Closes a GitHub issue with a recorded cancellation reason, moves its board card to "Cancelled", notifies and unblocks dependent issues, and optionally cleans up associated branches and pull requests. Preserves the full decision trail in GitHub history.

## Usage

```text
/cancel-issue [issue-number]
```

> [!TIP]
> Also activates when you say "cancel issue", "drop issue", "cancel #N", "won't do", "close as not planned", or want to cancel an issue.

## How it works

1. **Validate and select issue** — Resolve the issue number from arguments or branch name
2. **Ask cancellation reason and close** — Prompt for reason, close as "not planned"
3. **Move card to "Cancelled"** — Update the board card status via GraphQL
4. **Unblock dependent issues** — Notify and update issues that were blocked by this one
5. **Clean up branch and PR** — Optionally close PRs and delete branches
6. **Report** — Summary with closed issue, unblocked issues, and cleanup actions

## Directory structure

```text
cancel-issue/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── project-board-operations.md  # Board GraphQL patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill cancel-issue
```
