---
name: create-pr
description: Create a pull request from the current branch, linking it to the open issue. Use this skill when the user says "create pr", "open pr", "pr create", "make a pull request", "submit for review", or wants to open a PR for the current branch — even if they don't explicitly say "pull request."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash, Read, Grep
argument-hint: [title]
---

## 1. Validate branch

Determine the current branch name. If on `main`, stop and inform the user.

Check for unpushed commits. If any exist, push with `git push -u origin HEAD`.

## 2. Link to issue

Extract the issue number from the branch name (pattern: `<number>-slug`, e.g., `42-add-feature` → issue #42). Fetch the issue with `gh issue view <number> --json title,body,state`.

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

1. If there is a linked issue, check all checkbox items are complete. Flag any open tasks to the user — do not proceed until confirmed.
2. Grep test files for `.fixme`, `.skip`, `.todo`, and `only` markers. Flag any found — do not proceed until resolved or explicitly approved.

## 5. Create and report

Create the PR with `gh pr create --title "<title>" --body "<body>"`. Use a HEREDOC for the body.

Report the PR URL to the user.
