# merge-pr

> Merge the open pull request for the current branch and switch back to main.

Finds the PR for the current branch, merges it with branch deletion, and switches to the base branch.

## Usage

```text
/merge-pr
```

> [!TIP]
> Also activates when the user says "merge pull request", "merge this", "land the pr", or wants to finalize the current branch's PR.

## How it works

1. **Find the PR** — locates the open PR for the current branch via `gh pr view`
2. **Merge** — merges with `--merge --delete-branch` (merge commit, remote branch cleanup)
3. **Switch to base branch** — checks out the base branch and pulls latest
4. **Report** — displays PR number, merge status, and current branch

## Directory structure

```text
merge-pr/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill merge-pr
```
