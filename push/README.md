# push

Commit, push, and update GitHub issue checkboxes in one command. Analyzes changes, drafts a conventional commit message, and syncs issue tracking — all with a single approval gate.

## Trigger phrases

- "push"
- "commit and push" / "ship it"
- `/push`
- Also activates when the user wants to finalize work and sync issue tracking — even without mentioning the issue

## How it works

1. **Gather state** — Runs `git status`, `git diff`, `git log`, and `git branch` in parallel to understand the current working tree
2. **Analyze and group changes** — Groups changes by concern and drafts separate Conventional Commits messages (one commit per unrelated topic)
3. **Approval gate** — Presents the commit plan for user approval (skipped with `-y` flag)
4. **Stage and commit** — Stages specific files (never `git add -A`), scans for secrets, and commits with husky management
5. **Push** — Pushes to remote, setting upstream if needed
6. **Update issue checkboxes** — Finds the related GitHub issue (by branch name, commit refs, or title match), parses checkboxes, and marks completed items

## Usage

```
/push
```

Flags:
- `-y` — Auto-approve the commit message, skip the confirmation gate
- `-nh` — Skip husky entirely (uses `--no-verify`)

```
/push -y -nh
```

## Directory structure

```
push/
├── SKILL.md              # Core instructions
└── references/           # Issue checkbox update guide
```

## Installation

```bash
npx skills add https://github.com/lipex360x/claude-skills-library --skill push
```
