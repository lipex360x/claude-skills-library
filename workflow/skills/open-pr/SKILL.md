---
name: open-pr
description: Create a pull request from the current branch, linking it to the open issue. Use this skill when the user says "create pr", "open pr", "pr create", "make a pull request", "submit for review", or wants to open a PR for the current branch — even if they don't explicitly say "pull request."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, Read, Grep, AskUserQuestion
argument-hint: [title]
---

## 1. Validate branch

Determine the current branch name. If on `main`, stop and inform the user.

Check for unpushed commits. If any exist, push with `git push -u origin HEAD`.

## 2. Link to issue

Extract the issue number from the branch name (pattern: `<number>-slug`, e.g., `42-add-feature` → issue #42). Also try `feat/<number>-slug` pattern. Fetch the issue with `gh issue view <number> --json title,body,state,labels`.

If no issue is found, proceed without linking.

## 3. Build PR content

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

## 4. PR readiness check

Before creating, verify:

### 4a. Check for incomplete tasks

Parse all checkboxes in the linked issue body (`- [ ]` unchecked, `- [x]` checked). If all are checked, proceed to Step 4b.

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

     <Brief technical context explaining why — e.g., "The fix requires migrating the repository to SQL, which is exactly Step 1 of this issue.">
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

     **Reason:** <justification — e.g., "Behavior is already covered by query-level tests in tests/db/queries.test.ts. A dedicated component test would only mock the same function call, adding no meaningful coverage.">
     ```

   **If "Mark as done":**
   - Mark the checkbox as checked (`- [ ]` → `- [x]`)
   - No comment needed — the work was done, the checkbox was just missed

5. After all decisions, update the source issue body with `gh issue edit`.

### 4b. Check test markers

Grep test files for `.fixme`, `.skip`, `.todo`, and `only` markers. Flag any found — do not proceed until resolved or explicitly approved.

## 5. Move card to "In review"

If a project board exists for the repo (`gh project list --owner "@me"`), move the issue card to **"In review"** — the PR is now open and being reviewed:

1. Find the project and get the project node ID
2. Find the item ID for this issue
3. Get the Status field ID and the "In review" option ID
4. Update with `gh project item-edit`

Read `references/project-board-operations.md` for the full command reference.

If no project board exists, skip this step.

## 6. Create and report

Create the PR with `gh pr create --title "<title>" --body "<body>"`. Use a HEREDOC for the body.

Report:
- PR URL
- Issue linked (if any)
- Scope transfers performed (if any)
- Board status (card moved to "In review", or skipped)

## 7. Suggest merge

After reporting, use `AskUserQuestion` with options `["Yes, merge now", "No, wait for review"]`.

- **"Yes, merge now"** → invoke `/close-pr`
- **"No, wait for review"** → end normally

## Guidelines

- **All comments in English.** Scope transfer comments, PR body, and all issue content must be in English because they're public and portable. Communication with the user follows their language preference.

- **Scope transfers preserve traceability.** The bidirectional comments (source → target and target → source) ensure anyone reading either issue understands the full history. Never move a task silently — always leave a paper trail.

- **Don't force transfers.** The user decides what happens to each unchecked item. Present suggestions with context, but respect their choice. "Skip with justification" is always a valid option.

- **Every skip leaves a trace.** The "Skip with justification" option exists specifically to prevent silent drops. When an item is skipped, the comment on the issue ensures future readers (including future sessions) understand the rationale. Draft the justification from conversation context when possible — don't make the user write it from scratch.

- **Technical context in transfer comments.** Don't just say "moved to #10" — explain WHY the item belongs there. This helps future readers understand the decision (e.g., "The fix requires migrating the repository to SQL, which is exactly Step 1 of this issue").

- **No local paths in comments.** Use project-relative paths only. Never reference `~/.brain/`, `/Users/...`, or any absolute paths.
