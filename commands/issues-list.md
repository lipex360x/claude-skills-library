---
description: List all open issues grouped by milestone with priority sorting and next-issue suggestion.
disable-model-invocation: true
allowed-tools: Bash
---

List all open issues for the current repo, grouped by milestone and sorted by priority.

Run: `gh issue list --state open --json number,title,labels,milestone,body --limit 100`

If there are no open issues, say so and stop.

**Grouping:** Group issues by milestone name. Order groups: named milestones first (alphabetically), then "No milestone" last. Within each group, sort by priority label: P0 > P1 > P2 > P3 > unlabeled.

**Dependency detection:** For each issue, scan the body for patterns like "Depends on #N", "After #N", or "Related issues: #N". Check if referenced issues are closed. An issue is "blocked" if any dependency is still open.

**Suggested next:** Find the highest-priority non-blocked issue across all milestones. Mark it in the output.

**Output format:**

```
Open issues (N total):

## Milestone Name (M issues)
  1. #<number> — <title>  [label1, label2]
  2. #<number> — <title>  [label1, label2]  << suggested next
  3. #<number> — <title>  [label1]  (blocked by #N)

## No milestone (K issues)
  4. #<number> — <title>

Use /backlog-start <issue-number> to start working on one.
```

Keep it compact — no extra commentary.
