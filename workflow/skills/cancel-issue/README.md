# cancel-issue

> Cancel an issue — closes it on GitHub with a reason, moves the card to "Cancelled" on the project board, unblocks dependent issues, and cleans up branches/PRs.

Six-step cancellation workflow that preserves the full decision trail: records the reason as a structured comment, moves the board card to "Cancelled", runs both forward and reverse dependency scans to find and unblock dependent issues, and optionally closes associated PRs and deletes branches with user confirmation at each destructive step.

## Usage

```text
/cancel-issue [issue-number]
```

> [!TIP]
> Also activates when you say "cancel issue", "drop issue", "cancel #N", "won't do", "close as not planned", or want to cancel an issue.

### Examples

```text
/cancel-issue 42     # cancel issue #42 directly
/cancel-issue #42    # same — accepts both formats
/cancel-issue        # detect from branch name, or pick from open issues
```

> [!WARNING]
> This skill permanently closes the issue on GitHub as "not planned" and moves the board card to "Cancelled". While the issue remains in GitHub history, the closure and board state change cannot be undone from within the skill. Branch and PR deletion (if approved) are also irreversible.

## How it works

1. **Validate and select issue** — Resolve the issue number from arguments, branch name, or interactive list
2. **Ask cancellation reason and close** — Prompt for reason (no longer needed, superseded, out of scope, or custom), close as "not planned", post structured cancellation comment
3. **Move card to "Cancelled"** — Update the board card status via GraphQL (batch fetch, single update)
4. **Unblock dependent issues** — Forward scan (`Blocks #N`) and reverse scan (`Depends on #N`) to find blocked issues, post unblock comments, clean dependency references, move unblocked cards to "Ready"
5. **Clean up branch and PR** — Optionally close open PRs and delete remote branches (user confirms each)
6. **Report** — Summary with closed issue, unblocked issues, cleanup actions, and audit results

[↑ Back to top](#cancel-issue)

## Directory structure

```text
cancel-issue/
├── SKILL.md              # Core skill instructions (6 steps, 3 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── project-board-operations.md  # Board GraphQL mutation patterns and field IDs
```

[↑ Back to top](#cancel-issue)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill cancel-issue
```
