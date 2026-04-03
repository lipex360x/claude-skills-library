---
name: cancel-issue
description: >-
  Cancel an issue — closes it on GitHub with a reason, moves the card to
  "Cancelled" on the project board, unblocks dependent issues, and cleans up
  branches/PRs. Use this skill when the user says "cancel issue", "drop issue",
  "cancel #N", "won't do", "close as not planned", or wants to cancel an
  issue — even if they don't explicitly say "cancel."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# Cancel Issue

Close a GitHub issue with a recorded reason, move its board card to "Cancelled", unblock dependent issues, and clean up associated branches and PRs. Preserves the full decision trail in GitHub history.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `issue-number` | $ARGUMENTS | no | Positive integer (accepts `#N` or `N`) | Detect from branch name, or AUQ with open issues list |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Closed issue | GitHub API | yes | State = closed (not planned) |
| Board card | GitHub Projects | yes | Status = Cancelled |
| Unblock comments | GitHub API | yes | Markdown comments on dependent issues |
| Cleanup | GitHub / git | yes | PR closed, branch deleted (if approved) |
| Report | stdout | no | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GitHub issues | `gh issue` CLI | R/W | JSON / Markdown |
| Project board | GitHub Projects API | R/W | GraphQL |
| Pull requests | `gh pr` CLI | R/W | JSON |
| Git branches | `git branch -a` | R/W | Text |
| Board operations reference | `references/project-board-operations.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI (`gh`) required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo with a GitHub remote → if not: "Must run inside a GitHub-linked repo." — stop.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Validate and select issue

Parse `$ARGUMENTS` for an issue number. Accept both direct numbers (`2`) and index references (`#2`).

If no argument provided, detect from the current branch name:

1. **Number in branch name** — `feat/14-chat-backend` → issue #14
2. **Fallback** — list open issues via `gh issue list --state open --json number,title --limit 20` and present with `AskUserQuestion` for the user to pick one.

Fetch the issue details:

```bash
gh issue view <number> --json body,title,state,labels -q '{title: .title, state: .state, body: .body}'
```

If the command fails (issue not found): "Issue #<number> not found." — stop.

If the issue is already closed: "Issue #<number> is already closed." — stop.

### 2. Ask cancellation reason and close

Use `AskUserQuestion` to ask why the issue is being cancelled:

- "No longer needed"
- "Superseded by another issue"
- "Out of scope"
- "Other (I'll explain)"

If the user selects "Other", ask for a free-text explanation via a follow-up `AskUserQuestion`.

Close the issue and post a cancellation comment:

```bash
gh issue close <number> --reason "not planned"
```

Post the comment:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Cancelled

**Reason:** <reason selected or explained by user>

Cancelled on <YYYY-MM-DD>.
EOF
)"
```

If `gh issue close` fails, surface the error message and stop — do not proceed with board operations on an issue that wasn't successfully closed.

### 3. Move card to "Cancelled"

Read `references/project-board-operations.md` for the full command reference.

Find the project board (`gh project list --owner "@me"`). If no board exists, skip board operations and inform the user: "No project board found — skipping card move."

Move the issue card to the **"Cancelled"** column:

1. Fetch all project items once (batch approach — never re-fetch per item, because each `item-list` call consumes GraphQL rate limit points)
2. Find the item ID for this issue from the fetched list
3. Get the Status field ID and the "Cancelled" option ID
4. Update with `gh project item-edit`

If the issue is not found on the board, inform the user and continue — the issue was still closed successfully.

### 4. Unblock dependent issues

Scan the **cancelled issue's body** for `> **Blocks** #N` annotations. Also run a reverse scan — fetch open issues and check for dependency patterns referencing the cancelled issue:

```bash
gh issue list --state open --json number,title,body --limit 100
```

Look for patterns: `Depends on #N`, `Blocked by #N`, `After #N` where N is the cancelled issue number.

For each blocked issue that is still open:

1. **Post a comment** on the blocked issue explaining the blocker was cancelled and the dependency no longer applies.

2. **Clean the dependency reference** — remove or strikethrough the line referencing the cancelled issue in the blocked issue's body. Fetch the body, update it, then `gh issue edit <blocked-number> --body "<updated>"`.

3. **Move the card to "Ready"** on the project board if the issue has no other open blockers. Reuse the project items already fetched in Step 3 — do not re-fetch.

If no blocked issues are found in either scan, skip this step.

### 5. Clean up branch and PR

Check if the cancelled issue has associated branches or PRs:

```bash
git branch -a | grep "<number>-"
gh pr list --state open --json number,title,headRefName --limit 20
```

Filter results that match the cancelled issue number.

**If an open PR exists**, use `AskUserQuestion`: "Yes, close the PR" / "No, keep it open". If closing: `gh pr close <pr-number>`.

**If a remote branch exists**, use `AskUserQuestion`: "Yes, delete the branch" / "No, keep it". If deleting:
- If the user is currently on the branch being deleted, switch to main first: `git checkout main && git pull`
- Then: `git push origin --delete <branch-name>`

### 6. Report

Present concisely:
- **What was done** — issue #N closed with reason, board card moved to "Cancelled"
- **Unblocked** — issues moved to Ready (list numbers), or "none"
- **Cleanup** — PR closed, branch deleted (if applicable), or "none"
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

> _Skipped: "Issue cancelled — no follow-up needed."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — `gh` authenticated, inside a GitHub-linked repo
2. **Steps completed?** — issue closed, board updated, dependents notified, cleanup offered
3. **Output exists?** — issue state is closed, board card in Cancelled column
4. **Anti-patterns clean?** — reason recorded, blocked issues notified, no force-deletions without approval
5. **Approval gates honored?** — user confirmed cancellation reason, PR close, and branch deletion

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (state management only)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report "Issue #N not found" → stop |
| Issue already closed | Report "Issue #N is already closed" → stop |
| `gh issue close` fails | Surface error message → stop (do not proceed with board ops) |
| Board not found | Skip board operations, inform user, continue with remaining steps |
| Network error | Report error with details → stop (no silent retry) |
| Branch deletion fails | Report error, suggest manual cleanup → continue |

## Anti-patterns

- **Cancelling without a reason.** Every cancellation must have a recorded reason — because it's the paper trail for future decisions. Never close silently.
- **Leaving blocked issues stranded.** If the cancelled issue blocks others, those must be notified — because a cancelled blocker without notification leaves dependent issues stuck forever with no one knowing why.
- **Force-deleting branches without asking.** The branch may have uncommitted work or be referenced by other PRs — because irreversible data loss is worse than an extra confirmation step.
- **Skipping the reverse scan.** Forward scan (`> **Blocks** #N`) only catches explicitly declared dependencies. Reverse scan catches issues that declare `Depends on` the cancelled issue — because dependency declarations are often one-directional.
- **Re-fetching project items per operation.** Each `item-list` call consumes GraphQL rate limit points — because the 5,000 points/hour limit is shared across all `gh project` commands. Fetch once in Step 3, reuse in Step 4.

## Guidelines

- **Cancellation is not deletion.** The issue stays in GitHub history with its full context. The "Cancelled" column and the comment preserve the decision trail — because future issues may reference the cancelled one for context.

- **Unblock notifications are mandatory when dependencies exist.** The comment on blocked issues explains what happened and prompts replanning — because without it, dependent issues stay in limbo, technically unblocked but nobody knows.

- **English for all issue content.** Comments are always in English. Communication with the user follows their language preference.

- **No local paths in comments.** Use project-relative paths only.

- **Batch API calls.** When operating on multiple board items, fetch the item list once and parse locally — never re-fetch per item.
