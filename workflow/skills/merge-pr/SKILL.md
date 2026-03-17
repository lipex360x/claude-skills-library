---
name: merge-pr
description: Merge the open pull request for the current branch and switch back to main. Use this skill when the user says "merge pr", "merge pull request", "merge this", "land the pr", or wants to finalize and merge the current branch's PR — even if they don't explicitly say "merge."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash
---

## 1. Find the PR

Find the open PR for the current branch using `gh pr view --json number,state,baseRefName`.

If no open PR exists, inform the user and stop.

## 2. Merge

Merge the PR using `gh pr merge --merge --delete-branch`.

## 3. Switch to base branch

After merge, switch to the base branch: `git checkout <baseRefName> && git pull`.

## 4. Report

Report: PR number, merge status, and current branch.
