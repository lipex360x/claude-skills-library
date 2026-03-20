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

Run: `gh issue list --milestone "Backlog" --state open --json number,title,labels,body --limit 100`

If the milestone doesn't exist or has no issues, say so and stop.

## 3. Process and sort

Parse each issue and extract:
- **number** — issue number
- **title** — issue title
- **labels** — all labels except size and priority labels
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If none, treat as `—`
- **priority** — extracted from `priority:*` or `P0`–`P3` labels. If none, treat as `—`
- **status** — determined by dependency detection (see below)

### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N". Check if referenced issues are still open (use `gh issue view #N --json state -q '.state'` or cross-reference with the fetched list). If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

**Sorting:**
- If user passed `asc`: sort by size ascending using order: XS < S < M < L < XL (issues without size go last)
- If user passed `desc`: sort by size descending using order: XL > L > M > S > XS (issues without size go last)
- If no argument: sort by issue number ascending (natural order)

## 4. Present results as table

Use this exact format:

```
Backlog (N issues):

| # | Title | Size | Priority | Status |
|---|-------|------|----------|--------|
| [#28](REPO_URL/issues/28) | Title here | M | P2 | |
| [#31](REPO_URL/issues/31) | Title here | — | — | **Blocked** by #30 |
...
```

- The `#` column must be a markdown link: `[#<number>](REPO_URL/issues/<number>)`
- Status is empty when free, or `**Blocked** by #N, #M` listing open blockers

After the table, add: `Use /start-issue <issue-number> to start working on one.`
