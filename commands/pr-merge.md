---
description: Merge the open PR for the current branch and switch to main.
disable-model-invocation: true
allowed-tools: Bash
---

Find the open PR for the current branch using `gh pr view --json number,state,baseRefName`.

If no open PR exists, inform the user and stop.

Merge the PR using `gh pr merge --merge --delete-branch`.

After merge, switch to the base branch: `git checkout <baseRefName> && git pull`.

Report: PR number, merge status, and current branch.
