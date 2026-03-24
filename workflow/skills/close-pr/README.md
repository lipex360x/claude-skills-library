# close-pr

> Merge the open pull request for the current branch, write a detailed implementation summary on the issue, and move the card to Done.

Ten-step merge workflow that closes the full development loop: writes a detailed implementation summary comment on the linked issue (with file paths, key decisions, and verification steps), updates ARCHITECTURE.md with new routes/patterns/schema changes, moves the board card to "Done", and notifies all issues that were blocked by the merged work. Includes a review gate before the merge to prevent accidental merges.

## Usage

```text
/close-pr
```

> [!TIP]
> Also activates when you say "close pr", "merge pr", "merge pull request", "merge this", "land the pr", or want to finalize and merge the current branch's PR.

### Examples

```text
/close-pr              # merge the current branch's open PR
"merge this PR"        # same effect via model invocation
"land the pr"          # same effect via model invocation
```

> [!WARNING]
> This skill merges the PR and deletes the feature branch via `gh pr merge --merge --delete-branch`. The merge is permanent — once merged, the branch is removed from the remote. The board card moves to "Done" and blocked issues are notified and unblocked.

## How it works

1. **Find the PR** — Locate the open PR for the current branch via `gh pr view`
2. **Determine target branch** — Check `.claude/project-settings.json` for `pr-merge-to`, default to `main`
3. **Write implementation summary on the issue** — Post a structured comment with What was built, Key decisions, Files changed, Test coverage, and How to verify
4. **Update ARCHITECTURE.md** — Reflect new routes, patterns, schema changes, dependencies, or layers
5. **Review gate** — Present summary of all pending actions for user approval before merge
6. **Merge the PR** — Execute `gh pr merge --merge --delete-branch`
7. **Move card to "Done"** — Update the board card status via GraphQL
8. **Notify unblocked issues** — Forward and reverse dependency scan, post unblock comments, clean references, move cards to "Ready"
9. **Switch to base branch** — Checkout and pull the target branch locally
10. **Report** — Summary with merge result, implementation summary status, ARCHITECTURE.md changes, board status, and unblocked issues

[↑ Back to top](#close-pr)

## Directory structure

```text
close-pr/
├── SKILL.md              # Core skill instructions (10 steps, 1 approval gate)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── project-board-operations.md  # Board GraphQL mutation patterns and field IDs
```

[↑ Back to top](#close-pr)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill close-pr
```
