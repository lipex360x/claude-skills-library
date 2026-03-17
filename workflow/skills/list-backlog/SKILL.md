---
name: list-backlog
description: List open backlog issues with numbered summary for selection. Use this skill when the user says "list backlog", "show backlog", "backlog list", "what's in the backlog", or wants to see pending backlog items — even if they don't explicitly say "backlog."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash
---

List all open issues in the "Backlog" milestone for the current repo.

## 1. Fetch issues

Run: `gh issue list --milestone "Backlog" --state open --json number,title,labels --jq '.[] | {number, title, labels: [.labels[].name]}'`

If the milestone doesn't exist or has no issues, say so and stop.

## 2. Present results

Present results as a **numbered list** (1-based index):

```
Backlog (N issues):

  1. #<number> — <title>  [label1, label2]
  2. #<number> — <title>
  ...
```

After the list, add: `Use /workflow:start-backlog <issue-number> to start working on one.`
