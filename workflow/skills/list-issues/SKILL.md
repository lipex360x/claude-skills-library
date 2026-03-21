---
name: list-issues
description: List all open issues grouped by board column with priority sorting and next-issue suggestion. Use this skill when the user says "list issues", "show issues", "what issues are open", "issues list", or wants an overview of all open work — even if they don't explicitly say "issues."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

List all open issues for the current repo, grouped by project board status column and sorted by priority.

**Input:** No arguments. Lists all open issues for the current repo.

Read `references/project-board-operations.md` for board query patterns and column definitions.

## 1. Detect repo URL

Run: `gh repo view --json url -q '.url'`

Store the result as `REPO_URL` for building issue links.

## 2. Discover project board

Find the project board for the current repo:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[] | select(.title | test("<repo-name>"; "i")) | .number')
```

If no board is found, say "No project board found for this repo." and stop. If `gh` fails (auth, network), show the raw error and stop — don't guess.

## 3. Fetch board items

Query all items from the board:

```bash
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json
```

Extract each item's `.content.number`, `.content.title`, and `.status` (column name).

## 4. Fetch open issues and cross-reference

Fetch all open issues:

```bash
gh issue list --state open --json number,title,labels,body --limit 100
```

If the result contains exactly 100 issues, warn the user: "⚠️ Showing first 100 open issues — there may be more." If there are zero open issues, say "No open issues found." and stop.

Cross-reference the two lists:
- Issues on the board: use the board's `.status` as their column group
- Issues NOT on the board: place them in a "Not on board" group

For each issue extract:
- **number** — issue number
- **title** — issue title
- **priority** — extracted from `priority:*` or `P0`–`P3` labels. If none, treat as `—`
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If none, treat as `—`
- **status** — determined by dependency detection (see below)

### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N". Check if referenced issues are still open. If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

## 5. Group and sort

- **Grouping:** Group issues by board status column in workflow order: Backlog → Todo → Ready → In Progress → In Review. Omit empty groups. Show "Not on board" last (only if there are untracked issues). This order follows the natural issue lifecycle — left-to-right mirrors how work moves through the board, so the user sees what's waiting before what's active.
- **Priority sorting:** Within each group, sort by priority label: P0 > P1 > P2 > P3 > unlabeled. Critical issues surface first because they're what the user should act on next.

## 6. Present results as table

For each status group, use this format:

```
### Status Column Name (N issues)

| # | Title | Size | Priority | Status |
|---|-------|------|----------|--------|
| [#10](REPO_URL/issues/10) | Title here | L | P2 | |
| [#31](REPO_URL/issues/31) | Title here | — | — | **Blocked** by #30 |
...
```

- The `#` column must be a markdown link: `[#<number>](REPO_URL/issues/<number>)`
- Status is empty when free, or `**Blocked** by #N, #M` listing open blockers

## 7. Suggest next issue

Find the highest-priority non-blocked issue from the "Ready" column first, then "Todo", then "Backlog". Never suggest a blocked issue — if all candidates are blocked, say "All remaining issues are blocked" instead of picking one. After all tables, add:

`Suggested next: [#N](REPO_URL/issues/N) — Title here`

## Anti-patterns

- **Showing Done/Cancelled issues as open.** Only list issues in active columns (Backlog through In Review) and "Not on board". Done/Cancelled are excluded because this skill answers "what's open", not "what exists."
- **Suggesting a blocked issue as next.** Always check blockers before suggesting — a blocked issue wastes the user's time.
- **Truncating output silently.** If `--limit 100` caps results, warn explicitly. The user needs to know they're seeing a partial view.
- **False-positive blocker detection.** Only treat `Blocked by #N`, `Depends on #N`, `After #N` as blockers — not every `#N` reference means a dependency.
