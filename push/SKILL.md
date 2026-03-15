---
name: push
description: Commit, push, and update GitHub issue checkboxes in one command. Analyzes changes, drafts a conventional commit message, stages, commits (with husky management), pushes, then reviews and updates the open issue for the current branch. Supports -y flag to auto-approve commit message and -nh flag to skip husky. Use when the user says "push", "commit and push", "ship it", "/push", or wants to finalize work and sync issue tracking — even if they don't explicitly mention the issue.
user-invocable: true
---

# Push

Stage, commit, push, and update the related GitHub issue — all in one command. Single approval gate: the commit message. Everything else is automated.

## Flags

- **`-y`** — auto-approve the commit message. Skip the confirmation gate — draft the message and commit immediately. Useful for small, obvious changes where review adds no value.
- **`-nh`** — skip husky entirely (uses `--no-verify` on the commit). Without this flag, the default behavior is: husky runs on the first commit of the session, `--no-verify` on subsequent commits.

Flags can be combined: `/push -y -nh`

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

Analyze all changes (staged + unstaged) and group them by concern. If changes touch unrelated topics (e.g., a new feature + a rename + a cleanup), create **separate commits** for each — one commit per concern. This applies even with `-y`.

For each group, draft a **Conventional Commits** message in English:
- Prefixes: `feat:`, `fix:`, `refactor:`, `chore:`, `test:`, `docs:`, `style:`
- Focus on **why**, not **what** — the diff shows what changed
- One line subject (under 72 chars), optional body for complex changes

**If `-y` flag is set** → proceed directly to step 3 with the drafted messages. No confirmation needed.

**Otherwise** → present the commit plan (which files go in which commit) to the user and **wait for approval**. This is the only confirmation gate. The user may edit or reject it.

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
- **No `-nh` flag** → husky runs on the first commit of the session. If this isn't the first commit, use `--no-verify` to skip redundant hook runs
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

## Guidelines

- **Never force-push.** If the push is rejected, explain why and ask the user.

- **Never amend.** Each push creates a new commit. Amending published commits rewrites history others may depend on. Amending after a hook failure modifies the wrong commit.

- **Never stage secrets.** The scan in step 3 catches common patterns. If something slips through, the user's pre-commit hooks are the second line of defense.

- **Single gate.** The commit message (step 2) is the only point where the user must approve — unless `-y` is passed, which skips it entirely. Everything else — staging, pushing, issue updates — is automated. This keeps the flow fast while maintaining control over what goes into the commit log.

- **Graceful degradation.** If `gh` is not available, skip the issue update step. If the branch has no issue, skip it. If the issue body can't be parsed, skip it. The core job (commit + push) always completes.
