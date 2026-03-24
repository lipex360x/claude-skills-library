# close-pr

> Merge the open pull request for the current branch, write a detailed implementation summary on the issue, and move the card to Done.

Merges the current branch's PR with a detailed implementation summary comment on the linked issue, updates ARCHITECTURE.md if needed, moves the board card to "Done", and notifies unblocked issues — closing the full development loop.

## Usage

```text
/close-pr
```

> [!TIP]
> Also activates when you say "close pr", "merge pr", "merge pull request", "merge this", "land the pr", or want to finalize and merge the current branch's PR.

## How it works

1. **Find the PR** — Locate the open PR for the current branch
2. **Determine target branch** — Identify the base branch for the merge
3. **Write implementation summary on the issue** — Post a detailed summary comment
4. **Update ARCHITECTURE.md** — Reflect architectural changes if applicable
5. **Review gate** — Present summary for approval before merging
6. **Merge the PR** — Execute the merge via GitHub CLI
7. **Move card to "Done"** — Update the board card status via GraphQL
8. **Notify unblocked issues** — Comment on issues that are now unblocked
9. **Switch to base branch** — Checkout the target branch locally
10. **Report** — Summary with merge result, issue updates, and board status

## Directory structure

```text
close-pr/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── project-board-operations.md  # Board GraphQL patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill close-pr
```
