---
name: push
description: Commit, push, and update GitHub issue checkboxes in one command. Analyzes changes, drafts a conventional commit message, stages, commits (with husky management), pushes, then reviews and updates the open issue for the current branch. Supports --confirm flag to require commit message approval and -nh flag to skip husky. Use when the user says "push", "commit and push", "ship it", "/push", or wants to finalize work and sync issue tracking — even if they don't explicitly mention the issue.
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Push

Stage, commit, push, and update the related GitHub issue — all in one command. Default behavior: draft the commit message and proceed immediately. Only stop and ask when something goes wrong.

## Flags

- **`--confirm`** — require explicit approval of the commit message before committing. Use when you want to review the message before it goes in.
- **`-nh`** — skip husky entirely (uses `--no-verify` on every commit). Without this flag, the default behavior is: husky runs on the first commit of each `/push` invocation, `--no-verify` on subsequent commits within the same push (if multiple commits are grouped by concern).

Flags can be combined: `/push --confirm -nh`

## Steps

### 1. Gather state

Run these in parallel:

```bash
git status
git diff
git diff --cached
git log --oneline -5
git branch -vv
```

If the working tree is clean (no staged or unstaged changes, no untracked files to stage), inform the user and stop. Nothing to push.

### 2. Analyze and group changes

Analyze all changes (staged + unstaged) and group them by concern. If changes touch unrelated topics (e.g., a new feature + a rename + a cleanup), create **separate commits** for each — one commit per concern.

For each group, draft a **Conventional Commits** message in English:
- Prefixes: `feat:`, `fix:`, `refactor:`, `chore:`, `test:`, `docs:`, `style:`
- Focus on **why**, not **what** — the diff shows what changed
- One line subject (under 72 chars), optional body for complex changes

**Default behavior** → proceed directly to step 3 with the drafted messages. No confirmation needed.

**If `--confirm` flag is set** → present the commit plan (which files go in which commit) to the user and **wait for approval** before proceeding.

**If something looks wrong** (e.g., secrets detected, unexpected files, ambiguous grouping), stop and present the issue via `AskUserQuestion` with actionable options. Do NOT proceed silently when there's a problem — but do NOT stop for routine commits.

### 3. Stage and commit

**Staging:**
- Prefer `git add <specific-files>` over `git add -A` or `git add .`
- Scan for secrets before staging — warn and exclude if any of these are found:
  - `.env`, `.env.*` (except `.env.example`)
  - `credentials.json`, `*.key`, `*.pem`, `*.p12`
  - Files containing `API_KEY=`, `SECRET=`, `PASSWORD=` with actual values
- If the user insists on staging a flagged file, warn once more, then respect their decision

**Committing:**
- Use heredoc format for the commit message:
  ```bash
  git commit -m "$(cat <<'EOF'
  feat: add user authentication
  EOF
  )"
  ```
- **`-nh` flag provided** → always use `--no-verify`
- **No `-nh` flag** → when a single `/push` produces multiple commits (grouped by concern), run husky on the first commit. If the hook passes, subsequent commits **in the same push** use `--no-verify` to skip redundant runs. If there's only one commit, husky always runs. Previous `/push` invocations in the conversation do not count — each `/push` resets the hook state
- **If the hook fails** → fix the issue, re-stage, create a **new** commit. Never amend — amending after a hook failure would modify the previous commit, potentially losing work

### 4. Push

```bash
git push
```

- If the branch has no upstream → `git push -u origin <branch>`
- If push fails because the branch is behind remote → explain the situation, suggest `git pull --rebase`, and ask the user how to proceed. Never force-push.

### 5. Update issue checkboxes

Find the related issue for the current branch. Try these patterns in order:

1. **Number in branch name** — `feature/14-chat-backend` → issue #14
2. **Commit references** — scan recent commits for `#N` references
3. **Title match** — compare branch slug against open issue titles

If no issue is found, skip this step gracefully — not every branch has an issue.

If found, read `references/issue-update-guide.md` for the matching and update process, then:

1. Fetch the issue body: `gh issue view <N> --json body -q '.body'`
2. Parse all checkboxes (`- [ ]` and `- [x]`)
3. Match completed work against unchecked boxes
4. **Clear matches** → mark directly (`- [ ]` → `- [x]`)
5. **Ambiguous matches** → ask the user which checkboxes to mark
6. Update: `gh issue edit <N> --body "<updated body>"`
7. Report what was checked off

### 6. Summary

Present concisely:
- Commit hash and message
- Push status (branch, remote)
- Checkboxes updated (if any)
- Remaining open checkboxes count

### 7. Suggest PR (if all checkboxes done)

If an issue was found in Step 5 and **all checkboxes are now checked** (0 remaining), suggest opening a PR:

Use `AskUserQuestion` with options `["Yes, open PR", "No, not yet"]`.

- **"Yes, open PR"** → invoke `/open-pr`. If the skill is unavailable, tell the user to run `/open-pr` manually
- **"No, not yet"** → end normally

If there are still open checkboxes, skip this step entirely.

## Avoid these

- **Force-pushing** — rewrites shared history; others pulling the branch will get conflicts or lose work.
- **Amending after hook failure** — the failed commit never landed, so `--amend` modifies the *previous* commit, potentially destroying unrelated work.
- **Staging secrets** (`.env`, `*.key`, `*.pem`, `credentials.json`, files with `API_KEY=`/`SECRET=`/`PASSWORD=`) — the scan in step 3 catches common patterns; pre-commit hooks are the second line of defense.
- **Committing unrelated files in one commit** — defeats `git bisect` and makes reverts dangerous. Group by concern (step 2).
- **Skipping issue update when the branch has an issue** — the issue is the source of truth for progress. If `gh` is available and an issue exists, always attempt the update.
- **Auto-editing ARCHITECTURE.md** — only add a note to the commit message body (step 6 of Guidelines). The file owner decides what to change.

## Guidelines

- **No gates by default.** The default flow is fully automated — draft message, stage, commit, push, update issue. Only stop and ask via `AskUserQuestion` when something unexpected happens (secrets detected, push rejected, ambiguous checkbox matches). The `--confirm` flag adds an explicit approval step for the commit message when the user wants it.

- **Graceful degradation.** If `gh` is not available, skip the issue update step. If the branch has no issue, skip it. If the issue body can't be parsed, skip it. The core job (commit + push) always completes.

- **ARCHITECTURE.md drift detection.** Before committing, check if staged changes introduce patterns that should be reflected in `ARCHITECTURE.md` (if the file exists):
  - New route (`page.tsx`/`route.ts` in a new directory)
  - New dependency in `package.json`/`Cargo.toml`/`go.mod`
  - New migration file (schema change)
  - New file in a location that doesn't match any documented pattern

  If ARCHITECTURE.md doesn't exist, skip this check entirely. If drift is detected, append a note to the **commit message body** (not the title): `Note: ARCHITECTURE.md may need updating (new route: /payments, new dep: recharts)`. Do NOT auto-edit ARCHITECTURE.md or block the commit — this is informational only.
