---
name: open-pr
description: >-
  Create a pull request from the current branch, linking it to the open issue.
  Use this skill when the user says "create pr", "open pr", "pr create",
  "make a pull request", "submit for review", or wants to open a PR for the
  current branch — even if they don't explicitly say "pull request."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Grep
  - AskUserQuestion
argument-hint: [title]
---

# Open PR

Create a pull request from the current branch, link it to the related issue, resolve incomplete checkboxes, and move the project board card to "In review."

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `title` | $ARGUMENTS | no | Non-empty string | Derive from issue title or first commit message |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Pull request | GitHub API | yes | PR with title, body, linked issue |
| Board card update | GitHub Projects | yes | Status field → "In review" |
| Scope transfer comments | GitHub Issues | yes | Markdown comments |
| Report | stdout | no | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Git repository | local `.git/` | R | Git |
| GitHub Issues | `gh issue view` | R/W | Markdown |
| GitHub PRs | `gh pr create` | W | API |
| Project board | GitHub Projects API | R/W | GraphQL |
| Open issues list | `gh issue list` | R | JSON |

</external_state>

## Pre-flight

<pre_flight>

1. Current branch is not `main` → if on main: "Cannot create PR from main." — stop.
2. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
3. Unpushed commits exist → if any: push with `git push -u origin HEAD` before proceeding.

</pre_flight>

## Steps

### 1. Link to issue

Extract the issue number from the branch name (pattern: `<number>-slug`, e.g., `42-add-feature` → issue #42). Also try `feat/<number>-slug` pattern. Fetch the issue with `gh issue view <number> --json title,body,state,labels`.

If no issue is found, proceed without linking.

### 2. Build PR content

- **Title:** Use `$ARGUMENTS` if provided. Otherwise, derive from the issue title or the first commit message since diverging from main.
- **Body:** Use this format:
  ```
  ## Summary
  <2-3 bullet points describing the changes>

  ## Test plan
  <bulleted checklist>

  Closes #<issue-number>
  ```
- Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat` to understand the full scope of changes for the summary.

### 3. PR readiness check

Before creating, verify:

#### 3a. Check for incomplete tasks

Parse all checkboxes in the linked issue body (`- [ ]` unchecked, `- [x]` checked). If all are checked, proceed to Step 3b.

**If unchecked items exist**, determine what to do with each:

1. **List the unchecked items** to the user with their Step context
2. **Fetch open issues** in the same repo to find potential transfer targets:
   ```bash
   gh issue list --state open --json number,title,body --limit 20
   ```
3. For each unchecked item, use `AskUserQuestion` with options:
   - **"Move to #N (<title>)"** — suggest the most relevant open issue based on topic overlap (compare the unchecked item's content against open issue titles and bodies)
   - **"Create new backlog issue"** — if no existing issue fits
   - **"Mark as done (already completed)"** — if the work was actually done but the checkbox wasn't ticked
   - **"Skip with justification"** — drop it from the PR scope with a recorded reason

4. **Execute the decisions.** Handle each based on the user's choice:

   **If "Move to #N":**

   On the source issue (current):
   - Mark the checkbox as checked (`- [ ]` → `- [x]`)
   - Add a comment explaining the transfer:
     ```markdown
     ## Scope transfer

     The following item was moved to #<target> (<target title>) because it fits better in that scope:

     - <checkbox text>

     Marking as complete here — resolution tracked in #<target>.
     ```

   On the target issue:
   - Add the unchecked item as a new checkbox in the appropriate Step (or create a new Step if none fits)
   - Add a comment connecting the two issues:
     ```markdown
     ## Scope transfer from #<source>

     During #<source> (<source title>), the following item was identified as belonging to this issue's scope:

     - <checkbox text>

     <Brief technical context explaining why>
     ```

   **If "Create new backlog issue":**
   - Create a new issue with the unchecked items, add to the project board in the "Backlog" column
   - Add the scope transfer comment on the source issue pointing to the new issue

   **If "Skip with justification":**
   - Ask the user for the reason (or draft one based on conversation context)
   - Mark the checkbox as checked (`- [ ]` → `- [x]`)
   - Add a comment on the source issue:
     ```markdown
     ## Scope skip

     The following item was skipped during PR readiness check for branch `<branch-name>`:

     - <checkbox text>

     **Reason:** <justification>
     ```

   **If "Mark as done":**
   - Mark the checkbox as checked (`- [ ]` → `- [x]`)
   - No comment needed — the work was done, the checkbox was just missed

5. After all decisions, update the source issue body with `gh issue edit`.

#### 3b. Check test markers

Grep test files (patterns: `**/*.test.{ts,js,tsx,jsx}`, `**/*.spec.{ts,js,tsx,jsx}`) for `.fixme`, `.skip`, `.todo`, and `only` markers. Flag any found — do not proceed until resolved or explicitly approved.

### 4. Move card to "In review"

If a project board exists for the repo (`gh project list --owner "@me"`), move the issue card to **"In review"** — the PR is now open and being reviewed:

1. Find the project and get the project node ID
2. Find the item ID for this issue
3. Get the Status field ID and the "In review" option ID
4. Update with `gh project item-edit`

Read `references/project-board-operations.md` for the full command reference.

If no project board exists, skip this step.

### 5. Create PR

Create the PR with `gh pr create --title "<title>" --body "<body>"`. Use a HEREDOC for the body.

### 6. Suggest merge

Use `AskUserQuestion` with options `["Yes, merge now", "No, wait for review"]`.

- **"Yes, merge now"** → invoke `/close-pr`. If `/close-pr` is unavailable, run `gh pr merge --merge --delete-branch` directly and move the issue card to "Done".
- **"No, wait for review"** → end normally.

### 7. Report

Present concisely:
- **What was done** — PR created, issue linked, scope transfers performed
- **PR URL** — the created PR link
- **Board status** — card moved to "In review", or skipped
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered (or "none")

## Next action

Run `/close-pr` when the PR is approved and ready to merge.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — not on main, gh available, commits pushed
2. **Steps completed?** — PR created, issue linked (if applicable), board updated
3. **Output exists?** — PR URL returned, scope transfer comments posted (if any)
4. **Anti-patterns clean?** — no unchecked items silently dropped, no test markers left, no force-push
5. **Approval gates honored?** — user decided on each unchecked item, merge suggestion presented

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **PR body accurate?** — summary reflects actual changes from `git diff main...HEAD`, not guesses
2. **Issue link correct?** — `Closes #N` references the right issue number
3. **Scope transfer comments complete?** — bidirectional comments posted on both source and target issues
4. **No local paths?** — PR body and comments contain no machine-specific absolute paths

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Push rejected (behind remote) | Explain, suggest `git pull --rebase`, ask user → stop |
| Issue not found | Proceed without linking — PR can exist without an issue |
| Project board not found | Skip board update, note in report |
| PR creation fails | Report error with full `gh` output → stop |

## Anti-patterns

- **Silently dropping unchecked items.** Every unchecked checkbox must be explicitly resolved (move, skip, mark done, or create backlog) — because silent drops lose work tracking and break traceability.
- **Creating PRs with test markers.** `.skip`, `.only`, `.fixme`, `.todo` in test files must be resolved — because these indicate incomplete or focused tests that shouldn't ship.
- **Force-pushing to resolve conflicts.** Resolve conflicts properly — because force-push rewrites shared history and causes data loss for others.
- **Generic PR summaries.** "Various fixes" or "Updates" are not acceptable — because reviewers need specific context to evaluate changes effectively.
- **Local paths in PR body.** Never reference `~/.brain/`, `/Users/...`, or machine-specific paths — because PR content is public and must be portable.

## Guidelines

- **All comments in English.** Scope transfer comments, PR body, and all issue content must be in English — because they're public and portable. Communication with the user follows their language preference.

- **Scope transfers preserve traceability.** The bidirectional comments (source → target and target → source) ensure anyone reading either issue understands the full history — because silent moves create orphaned context.

- **Don't force transfers.** The user decides what happens to each unchecked item. Present suggestions with context, but respect their choice — because "Skip with justification" is always a valid option.

- **Every skip leaves a trace.** The "Skip with justification" option exists specifically to prevent silent drops — because the comment on the issue ensures future readers understand the rationale.

- **Technical context in transfer comments.** Don't just say "moved to #10" — explain WHY the item belongs there — because this helps future readers understand the decision.

- **No local paths in comments.** Use project-relative paths only — because absolute paths break across environments.
