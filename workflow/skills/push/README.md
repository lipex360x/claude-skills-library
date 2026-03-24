# push

> Commit, push, and update GitHub issue checkboxes in one command.

Zero-gate-by-default workflow: analyzes changes, groups by concern into separate Conventional Commits, stages specific files (with secrets scanning), manages husky hooks (first commit runs hooks, subsequent commits in the same push skip them), pushes, and updates the related GitHub issue checkboxes automatically. Two optional flags add control: `--confirm` for commit message approval, `-nh` to skip husky entirely. Suggests `/open-pr` when all issue checkboxes are complete.

## Usage

```text
/push [flags]
```

> [!TIP]
> Also activates when you say "push", "commit and push", "ship it", or want to finalize work and sync issue tracking.

### Examples

```text
/push                  # commit, push, and update issue checkboxes
/push --confirm        # require commit message approval before pushing
/push -nh              # skip husky pre-commit hooks
/push --confirm -nh    # both — approve message and skip hooks
```

## How it works

1. **Gather state** — Run `git status`, `git diff`, `git log`, and `git branch` in parallel
2. **Analyze and group changes** — Group by concern, draft separate Conventional Commits messages (feat/fix/refactor/chore/test/docs/style)
3. **Stage and commit** — Stage specific files (never `git add -A`), scan for secrets (`.env`, `*.key`, `*.pem`, `credentials.json`), commit with husky management and ARCHITECTURE.md drift detection
4. **Push** — Push to remote, setting upstream if needed; never force-push
5. **Update issue checkboxes** — Find the related GitHub issue from branch name, match completed work against unchecked boxes, update via `gh issue edit`
6. **Suggest PR (if all checkboxes done)** — Offer to run `/open-pr` when all tasks are complete
7. **Report** — Summary with commit hashes, push result, checkboxes updated, and remaining count

[↑ Back to top](#push)

## Directory structure

```text
push/
├── SKILL.md              # Core skill instructions (7 steps, 0 default approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── issue-update-guide.md  # Issue checkbox matching and update patterns
```

[↑ Back to top](#push)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill push
```
