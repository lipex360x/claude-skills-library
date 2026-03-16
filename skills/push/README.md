# push

> Commit, push, and update GitHub issue checkboxes in one command.

Analyzes changes, drafts a conventional commit message, and syncs issue tracking — all with a single approval gate.

## Usage

```text
/push
/push -y
/push -y -nh
```

| Flag | Description |
|------|-------------|
| `-y` | Auto-approve the commit message, skip the confirmation gate |
| `-nh` | Skip husky entirely (uses `--no-verify`) |

> [!TIP]
> Also activates when the user says "commit and push", "ship it", or wants to finalize work and sync issue tracking — even without mentioning the issue.

## How it works

1. **Gather state** — runs `git status`, `git diff`, `git log`, and `git branch` in parallel
2. **Analyze and group changes** — groups by concern, drafts separate Conventional Commits messages (one per topic)
3. **Approval gate** — presents the commit plan for user approval (skipped with `-y`)
4. **Stage and commit** — stages specific files (never `git add -A`), scans for secrets, commits with husky management
5. **Push** — pushes to remote, setting upstream if needed
6. **Update issue checkboxes** — finds the related GitHub issue, parses checkboxes, and marks completed items

> [!NOTE]
> The commit message is the only approval point. Everything else — staging, pushing, issue updates — is fully automated.

## Directory structure

```text
push/
├── SKILL.md              # Core instructions
└── references/           # Issue checkbox update guide
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill push
```
