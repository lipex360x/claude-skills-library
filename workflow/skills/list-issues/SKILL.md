---
name: list-issues
description: List all open issues grouped by milestone with priority sorting and next-issue suggestion. Use this skill when the user says "list issues", "show issues", "what issues are open", "issues list", or wants an overview of all open work — even if they don't explicitly say "issues."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash
---

List all open issues for the current repo, grouped by milestone and sorted by priority.

## 1. Fetch issues

Run: `gh issue list --state open --json number,title,labels,milestone,body --limit 100`

If there are no open issues, say so and stop.

## 2. Group and sort

- **Grouping:** Group issues by milestone name. Order groups: named milestones first (alphabetically), then "No milestone" last.
- **Priority sorting:** Within each group, sort by priority label: P0 > P1 > P2 > P3 > unlabeled.

## 3. Dependency detection

For each issue, scan the body for patterns like "Depends on #N", "After #N", or "Related issues: #N". Check if referenced issues are closed. An issue is "blocked" if any dependency is still open.

## 4. Suggest next issue

Find the highest-priority non-blocked issue across all milestones. Mark it in the output as the suggested next issue.
