---
description: List open backlog issues with numbered summary for selection.
disable-model-invocation: true
allowed-tools: Bash
---

List all open issues in the "Backlog" milestone for the current repo.

Run: `gh issue list --milestone "Backlog" --state open --json number,title,labels --jq '.[] | {number, title, labels: [.labels[].name]}'`

If the milestone doesn't exist or has no issues, say so and stop.

Present results as a **numbered list** (1-based index) in this format:

```
Backlog (N issues):

  1. #<number> — <title>  [label1, label2]
  2. #<number> — <title>
  ...
```

After the list, add: `Use /backlog-start <issue-number> to start working on one.`

Keep it compact — no extra commentary.
