---
description: Create a PR from the current branch, linking it to the open issue.
argument-hint: [título]
disable-model-invocation: true
allowed-tools: Bash, Read, Grep
---

Determine the current branch name. If on `main`, stop and inform the user.

Check if there are unpushed commits. If yes, push with `git push -u origin HEAD`.

Extract the issue number from the branch name (pattern: `<number>-slug`, e.g., `42-add-feature` → issue #42). Use `gh issue view <number> --json title,body,state` to fetch the issue. If no issue is found, proceed without linking.

Build the PR:
- **Title:** Use `$ARGUMENTS` if provided. Otherwise, derive from the issue title or the first commit message since diverging from main.
- **Body:** Use a concise summary format:
  ```
  ## Summary
  <2-3 bullet points describing the changes>

  ## Test plan
  <bulleted checklist>

  Closes #<issue-number>
  ```
- Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat` to understand the full scope of changes for the summary.

Before creating the PR, run PR readiness check:
1. If there is a linked issue, verify all checkbox items are complete. Flag any open tasks to the user — do not proceed until confirmed.
2. Grep test files for `.fixme`, `.skip`, `.todo`, and `only` markers. If any are found, flag them to the user — do not proceed until resolved or explicitly approved.

Create the PR with `gh pr create --title "<title>" --body "<body>"`. Use a HEREDOC for the body.

Report the PR URL to the user.
