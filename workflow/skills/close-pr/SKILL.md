---
name: close-pr
description: Merge the open pull request for the current branch, write a detailed implementation summary on the issue, and move the card to Done. Use this skill when the user says "close pr", "merge pr", "merge pull request", "merge this", "land the pr", or wants to finalize and merge the current branch's PR — even if they don't explicitly say "merge."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, Read
---

## 1. Find the PR

Find the open PR for the current branch:

```bash
gh pr view --json number,state,baseRefName,title,body,url
```

If no open PR exists, inform the user and stop.

## 2. Determine target branch

Check `.claude/project-settings.json` for the `pr-merge-to` field. If it exists, use its value as the target branch. If the file doesn't exist or the field is missing, default to `main`.

Verify the PR's `baseRefName` matches the expected target. If it doesn't, warn the user:

```
⚠️ PR targets '<baseRefName>' but project-settings.json says '<pr-merge-to>'. Continue?
```

## 3. Write implementation summary on the issue

Extract the issue number from the PR body (`Closes #N` pattern) or from the branch name.

If an issue is found, generate a detailed implementation summary and post it as a **comment on the issue**. This comment serves as the single source of truth — anyone visiting the issue can understand what was built without navigating commits, branches, or PRs.

**Gather context:**

```bash
# All commits in this branch
git log main..HEAD --oneline

# Full diff stats
git diff main...HEAD --stat

# Detailed diff for the summary (read key files if diff is too large)
git diff main...HEAD

# Issue body for context on what was planned
gh issue view <number> --json body,title -q '{title: .title, body: .body}'
```

**Write the comment** using this format:

```markdown
## Implementation summary

### What was built
<2-5 bullet points describing the key changes — what the user would care about, not internal details>

### Key decisions
<1-3 bullet points on architectural or technical decisions made during implementation — things that aren't obvious from the code>

### Files changed
<Grouped by concern — e.g., "Backend", "Tests", "Config". List significant files, not every single change>

### Test coverage
<What tests were added/modified, what they verify>

### How to verify
<1-3 steps to manually verify the implementation works — e.g., "Run `npm test`, navigate to /dashboard, check the new widget renders">

---
PR: #<pr-number> | Branch: `<branch-name>`
```

Post with:

```bash
gh issue comment <number> --body "<summary>"
```

The summary should be **specific and concrete** — file paths, test names, route URLs. Generic summaries ("improved the auth system") are useless. Someone reading this comment six months from now should understand exactly what changed and why.

## 4. Update ARCHITECTURE.md

Check if `ARCHITECTURE.md` exists at the project root. If it does, analyze the diff (`git diff main...HEAD`) for changes that affect the architecture document:

- **New routes or pages** — add to the Routes section
- **New patterns** — add to the Patterns section with a canonical example reference
- **Schema changes** — update the Schema summary
- **New dependencies** — add to Stack & dependencies
- **New layers or modules** — update the Layers section
- **Auth changes** — update the Auth model section

Read the current `ARCHITECTURE.md`, then update it with the relevant additions. Be surgical — only add what this branch introduced, don't rewrite existing content. Each addition should name the specific change (e.g., "add `/billing` route", "add `recharts` to dependencies").

If `ARCHITECTURE.md` doesn't exist and the project has sufficient complexity (3+ routes, multiple layers, or a database), generate it from the current codebase state — this branch's merge is the trigger. Use the same structure as `start-new-project` (stack, layers, patterns, schema, auth, routes).

**Commit the ARCHITECTURE.md update** as part of the merge preparation — it should be on the branch before merging so the base branch receives the updated file:

```bash
git add ARCHITECTURE.md
git commit -m "docs: update ARCHITECTURE.md with implementation changes"
```

If no architectural changes were introduced (e.g., pure bugfix, config-only change), skip this step.

## 5. Merge the PR

```bash
gh pr merge --merge --delete-branch
```

## 6. Move card to "Done"

If a project board exists for the repo (`gh project list --owner "@me"`), move the issue card from **"In review"** → **"Done"**:

1. Find the project and get the project node ID
2. Find the item ID for this issue
3. Get the Status field ID and the "Done" option ID
4. Update with `gh project item-edit`

Read `references/project-board-operations.md` for the full command reference.

If no project board exists, skip this step and Step 7.

## 7. Notify unblocked issues

Detect all issues that were blocked by the closed issue, using two complementary scans:

### 7a. Forward scan — closed issue declares what it blocks

Scan the **closed issue's body** for `> **Blocks** #N` annotations. Collect all referenced issue numbers.

### 7b. Reverse scan — other issues declare dependency on this one

Fetch all open issues and scan their bodies for patterns referencing the closed issue number:
- `Depends on #N`
- `Blocked by #N`
- `After #N`
- `Related issues: #N` (where N is the closed issue number)

```bash
gh issue list --state open --json number,title,body --limit 100
```

Filter issues whose body contains a dependency pattern matching the closed issue number. Collect these issue numbers.

### 7c. Process unblocked issues

Merge results from 7a and 7b (deduplicate). For each referenced issue that is still open:

1. **Add a comment** on the unblocked issue:
   ```markdown
   ## Blocker resolved

   #<source> (<source title>) has been merged. This issue is now unblocked.
   ```

2. **Clean the dependency reference** from the unblocked issue's body — remove or strike through the line referencing the closed issue (e.g., `Depends on #N` → `~Depends on #N~` or remove entirely). This prevents `/list-issues` and `/list-backlog` from still showing the issue as blocked.

   ```bash
   # Fetch current body, update it, then edit
   gh issue view <unblocked-number> --json body -q '.body'
   # Remove/strikethrough the dependency line referencing the closed issue
   gh issue edit <unblocked-number> --body "<updated body>"
   ```

3. **Move the card to "Ready"** on the project board — signaling that the issue is now actionable. Use the same project board operations (get item ID, get "Ready" option ID, update with `gh project item-edit`).

If no blocked issues are found in either scan, skip this step.

## 8. Switch to base branch

After merge, switch to the target branch and pull:

```bash
git checkout <target-branch> && git pull
```

## 9. Report

Present concisely:
- PR number and merge status
- Issue summary posted (with issue URL)
- ARCHITECTURE.md updated (or "no architectural changes")
- Board status (card moved to Done)
- Unblocked issues (if any — list issue numbers and their new status)
- Current branch after switch

## Guidelines

- **Implementation summaries are the issue's memory.** Six months from now, the issue is the first place someone looks to understand what was done. If the summary is vague, they'll have to dig through commits and diffs — that's a failure. Be specific: file paths, function names, test coverage, verification steps.

- **Key decisions matter most.** The "what" is visible in the diff. The "why" lives only in the summary. Document trade-offs, alternatives considered, and constraints that shaped the implementation.

- **Unblock notifications close the loop.** When a blocker is resolved, the blocked issue needs to know. The comment + card move to "Ready" makes this visible to anyone watching the board — no manual triage needed.

- **English for all issue content.** Comments and summaries are always in English because they're public and portable. Communication with the user follows their language preference.

- **No local paths in comments.** Use project-relative paths only.

- **ARCHITECTURE.md is the project's living memory.** This file carries context across issues — what `/start-backlog` reads to understand the codebase, and what `/close-pr` updates to keep it current. Updating it after each merge is not optional documentation work; it's feeding the next development cycle. A stale ARCHITECTURE.md causes the next `/start-backlog` to make decisions based on outdated information, which cascades into wrong file paths, missed patterns, and duplicated exploration.

- **Respect the target branch.** The `pr-merge-to` setting exists because not every project merges to `main` — some use `develop`, `staging`, or release branches. Always check before merging.
