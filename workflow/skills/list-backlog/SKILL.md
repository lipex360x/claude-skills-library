---
name: list-backlog
description: List open backlog issues with table summary and size sorting. Use this skill when the user says "list backlog", "show backlog", "backlog list", "what's in the backlog", or wants to see pending backlog items — even if they don't explicitly say "backlog."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash
---

List all open issues in the "Backlog" milestone for the current repo.

## Arguments

`/list-backlog [asc|desc]`

- `asc` — sort by size ascending (XS → S → M → L → XL)
- `desc` — sort by size descending (XL → L → M → S → XS)
- No argument — default sort by issue number ascending

## 1. Detect repo URL

Run: `gh repo view --json url -q '.url'`

Store the result as `REPO_URL` for building issue links.

## 2. Fetch issues

Run: `gh issue list --milestone "Backlog" --state open --json number,title,labels --jq '.[] | {number, title, labels: [.labels[].name]}'`

If the milestone doesn't exist or has no issues, say so and stop.

## 3. Process and sort

Parse each issue and extract:
- **number** — issue number
- **title** — issue title
- **labels** — all labels except size labels
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If no size label, treat as `—`

**Sorting:**
- If user passed `asc`: sort by size ascending using order: XS < S < M < L < XL (issues without size go last)
- If user passed `desc`: sort by size descending using order: XL > L > M > S > XS (issues without size go last)
- If no argument: sort by issue number ascending (natural order)

## 4. Present results as table

Use this exact format:

```
Backlog (N issues):

| Issue | Title | Labels | Size |
|-------|-------|--------|------|
| [#28](REPO_URL/issues/28) | Title here | feature | M |
| [#27](REPO_URL/issues/27) | Title here | enhancement | XS |
...
```

- The `Issue` column must be a markdown link: `[#<number>](REPO_URL/issues/<number>)`
- The `Labels` column shows all labels EXCEPT the `size:*` label, comma-separated
- The `Size` column shows only the size letter (XS, S, M, L, XL) or `—` if none

After the table, add: `Use /start-issue <issue-number> to start working on one.`
