---
name: cancel-issue
description: Cancel an issue — closes it on GitHub with a reason, moves the card to "Cancelled" on the project board, unblocks dependent issues, and cleans up branches/PRs. Use this skill when the user says "cancel issue", "drop issue", "cancel #N", "won't do", "close as not planned", or wants to cancel an issue — even if they don't explicitly say "cancel."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

**Input:** Issue number as `$ARGUMENTS` (e.g., `28` or `#28`), or no argument to detect from the current branch name. If the argument is not a valid number, inform the user and stop.

## 1. Validate and select issue

Verify `gh` is available (`which gh`). If missing, inform the user: "GitHub CLI (`gh`) is required but not found. Install it: https://cli.github.com/" — then stop.

Parse `$ARGUMENTS` for an issue number. Accept both direct numbers (`2`) and index references (`#2`).

If no argument provided, detect from the current branch name:

1. **Number in branch name** — `feat/14-chat-backend` → issue #14
2. **Fallback** — list open issues via `gh issue list --state open --json number,title --limit 20` and present with `AskUserQuestion` for the user to pick one.

Fetch the issue details:

```bash
gh issue view <number> --json body,title,state,labels -q '{title: .title, state: .state, body: .body}'
```

If the command fails (issue not found), inform the user: "Issue #<number> not found." — then stop.

If the issue is already closed, inform the user: "Issue #<number> is already closed." — then stop.

## 2. Ask cancellation reason and close

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

Post the comment using this format:

```bash
gh issue comment <number> --body "$(cat <<'EOF'
## Cancelled

**Reason:** <reason selected or explained by user>

Cancelled on <YYYY-MM-DD>.
EOF
)"
```

If `gh issue close` fails, surface the error message and stop — do not proceed with board operations on an issue that wasn't successfully closed.

## 3. Move card to "Cancelled"

Read `references/project-board-operations.md` for the full command reference.

Find the project board (`gh project list --owner "@me"`). If no board exists, skip board operations and inform the user: "No project board found — skipping card move."

Move the issue card to the **"Cancelled"** column:

1. Fetch all project items once (batch approach — never re-fetch per item, because each `item-list` call consumes GraphQL rate limit points)
2. Find the item ID for this issue from the fetched list
3. Get the Status field ID and the "Cancelled" option ID
4. Update with `gh project item-edit`

If the issue is not found on the board, inform the user and continue — the issue was still closed successfully.

## 4. Unblock dependent issues

Scan the **cancelled issue's body** for `> **Blocks** #N` annotations. Also run a reverse scan — fetch open issues and check for dependency patterns referencing the cancelled issue:

```bash
gh issue list --state open --json number,title,body --limit 100
```

Look for patterns: `Depends on #N`, `Blocked by #N`, `After #N` where N is the cancelled issue number.

For each blocked issue that is still open:

1. **Post a comment** on the blocked issue:

   ```bash
   gh issue comment <blocked-number> --body "$(cat <<'EOF'
   ## Blocker cancelled

   #<cancelled-number> (<cancelled title>) has been cancelled: <reason>. This dependency no longer applies.

   Review whether this issue can proceed independently or needs replanning.
   EOF
   )"
   ```

2. **Clean the dependency reference** — remove or strikethrough the line referencing the cancelled issue in the blocked issue's body. Fetch the body, update it, then `gh issue edit <blocked-number> --body "<updated>"`.

3. **Move the card to "Ready"** on the project board if the issue has no other open blockers. Reuse the project items already fetched in Step 3 — do not re-fetch.

If no blocked issues are found in either scan, skip this step.

## 5. Clean up branch and PR

Check if the cancelled issue has associated branches or PRs:

```bash
# Check for branches matching the issue number
git branch -a | grep "<number>-"

# Check for open PRs referencing the issue
gh pr list --state open --json number,title,headRefName --limit 20
```

Filter results that match the cancelled issue number.

**If an open PR exists**, use `AskUserQuestion`:
- "Yes, close the PR"
- "No, keep it open"

If closing: `gh pr close <pr-number>`

**If a remote branch exists**, use `AskUserQuestion`:
- "Yes, delete the branch"
- "No, keep it"

If deleting:
- If the user is currently on the branch being deleted, switch to main first: `git checkout main && git pull`
- Then: `git push origin --delete <branch-name>`

## 6. Summary

Present using this format:

```
## Cancelled

- **Issue:** #<number> — <title>
- **Reason:** <reason>
- **Board:** card moved to "Cancelled" | no board found
- **Unblocked:** #X, #Y moved to Ready | none
- **Cleanup:** PR #Z closed, branch `feat/N-slug` deleted | none
```

## Anti-patterns

- **Cancelling without a reason.** Every cancellation must have a recorded reason — it's the paper trail for future decisions. Never close silently.
- **Leaving blocked issues stranded.** If the cancelled issue blocks others, those must be notified — because a cancelled blocker without notification leaves dependent issues stuck forever with no one knowing why.
- **Force-deleting branches without asking.** The branch may have uncommitted work or be referenced by other PRs — always prompt before deletion because irreversible data loss is worse than an extra confirmation step.
- **Skipping the reverse scan.** Forward scan (`> **Blocks** #N`) only catches explicitly declared dependencies. Reverse scan catches issues that declare `Depends on` the cancelled issue — both are needed because dependency declarations are often one-directional.
- **Re-fetching project items per operation.** Each `item-list` call consumes GraphQL rate limit points. Fetch once in Step 3, reuse in Step 4 — because the 5,000 points/hour limit is shared across all `gh project` commands.

## Guidelines

- **Cancellation is not deletion.** The issue stays in GitHub history with its full context. The "Cancelled" column and the comment preserve the decision trail — this matters because future issues may reference the cancelled one for context.

- **Unblock notifications are mandatory when dependencies exist.** The comment on blocked issues explains what happened and prompts replanning — because without it, dependent issues stay in limbo, technically unblocked but nobody knows.

- **English for all issue content.** Comments are always in English. Communication with the user follows their language preference.

- **No local paths in comments.** Use project-relative paths only.

- **Batch API calls.** When operating on multiple board items, fetch the item list once and parse locally — never re-fetch per item.
