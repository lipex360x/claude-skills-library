---
name: list-issues
description: List all open issues grouped by milestone with priority sorting and next-issue suggestion. Use this skill when the user says "list issues", "show issues", "what issues are open", "issues list", or wants an overview of all open work — even if they don't explicitly say "issues."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

List all open issues for the current repo, grouped by milestone and sorted by priority.

## 1. Detect repo URL

Run: `gh repo view --json url -q '.url'`

Store the result as `REPO_URL` for building issue links.

## 2. Fetch issues

Run: `gh issue list --state open --json number,title,labels,milestone,body --limit 100`

If there are no open issues, say so and stop.

## 3. Process issues

For each issue extract:
- **number** — issue number
- **title** — issue title
- **priority** — extracted from `priority:*` or `P0`–`P3` labels. If none, treat as `—`
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If none, treat as `—`
- **milestone** — milestone name or "No milestone"
- **status** — determined by dependency detection (see below)

### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N". Check if referenced issues are still open. If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

## 4. Group and sort

- **Grouping:** Group issues by milestone name. Order groups: named milestones first (alphabetically), then "No milestone" last.
- **Priority sorting:** Within each group, sort by priority label: P0 > P1 > P2 > P3 > unlabeled.

## 5. Present results as table

For each milestone group, use this format:

```
### Milestone Name (N issues)

| # | Title | Size | Priority | Status |
|---|-------|------|----------|--------|
| [#10](REPO_URL/issues/10) | Title here | L | P2 | |
| [#31](REPO_URL/issues/31) | Title here | — | — | **Blocked** by #30 |
...
```

- The `#` column must be a markdown link: `[#<number>](REPO_URL/issues/<number>)`
- Status is empty when free, or `**Blocked** by #N, #M` listing open blockers

## 6. Suggest next issue

Find the highest-priority non-blocked issue across all milestones. After all tables, add:

`Suggested next: [#N](REPO_URL/issues/N) — Title here`
