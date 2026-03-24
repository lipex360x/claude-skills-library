---
name: list-issues
description: >-
  List all open issues grouped by board column with priority sorting and
  next-issue suggestion. Use this skill when the user says "list issues",
  "show issues", "what issues are open", "issues list", or wants an overview
  of all open work — even if they don't explicitly say "issues."
user-invocable: true
allowed-tools:
  - Bash
---

# List Issues

List all open issues for the current repo, grouped by project board status column and sorted by priority, with dependency detection and next-issue suggestion.

## Input contract

> _Skipped: "No input — lists all open issues for the current repo."_

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Grouped issue tables | stdout | no | Markdown tables |
| Next-issue suggestion | stdout | no | Markdown line |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Project board | GitHub Projects API | R | GraphQL / JSON |
| Open issues | `gh issue list` | R | JSON |
| Board operations guide | `references/project-board-operations.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
3. `gh auth status` succeeds → if not: "Run `gh auth login` first." — stop.

</pre_flight>

## Steps

Read `references/project-board-operations.md` for board query patterns and column definitions.

### 1. Detect repo URL

Run: `gh repo view --json url -q '.url'`

Store the result as `REPO_URL` for building issue links.

### 2. Discover project board

Find the project board for the current repo:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[] | select(.title | test("<repo-name>"; "i")) | .number')
```

If no board is found, say "No project board found for this repo." and stop. If `gh` fails (auth, network), show the raw error and stop — don't guess.

### 3. Fetch board items

Query all items from the board:

```bash
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json
```

Extract each item's `.content.number`, `.content.title`, and `.status` (column name).

### 4. Fetch open issues and cross-reference

Fetch all open issues:

```bash
gh issue list --state open --json number,title,labels,body --limit 100
```

If the result contains exactly 100 issues, warn the user: "Showing first 100 open issues — there may be more." If there are zero open issues, say "No open issues found." and stop.

Cross-reference the two lists:
- Issues on the board: use the board's `.status` as their column group
- Issues NOT on the board: place them in a "Not on board" group

For each issue extract:
- **number** — issue number
- **title** — issue title
- **priority** — extracted from `priority:*` or `P0`–`P3` labels. If none, treat as `—`
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If none, treat as `—`
- **status** — determined by dependency detection (see below)

#### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N". Check if referenced issues are still open. If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

### 5. Group and sort

- **Grouping:** Group issues by board status column in workflow order: Backlog → Todo → Ready → In Progress → In Review. Omit empty groups. Show "Not on board" last (only if there are untracked issues). This order follows the natural issue lifecycle — left-to-right mirrors how work moves through the board, so the user sees what's waiting before what's active.
- **Priority sorting:** Within each group, sort by priority label: P0 > P1 > P2 > P3 > unlabeled. Critical issues surface first because they're what the user should act on next.

### 6. Present results as table

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

### 7. Suggest next issue

Find the highest-priority non-blocked issue from the "Ready" column first, then "Todo", then "Backlog". Never suggest a blocked issue — if all candidates are blocked, say "All remaining issues are blocked" instead of picking one. After all tables, add:

`Suggested next: [#N](REPO_URL/issues/N) — Title here`

### 8. Report

Present concisely:
- **What was done** — total open issues listed, groups displayed, sort applied
- **Suggested next** — the recommended next issue (or "all blocked")
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

Run `/start-issue <number>` to begin working on the suggested issue.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, git repo confirmed
2. **Steps completed?** — board discovered, issues fetched, tables presented, next issue suggested
3. **Output exists?** — markdown tables rendered with correct link format
4. **Anti-patterns clean?** — no Done/Cancelled issues shown, no blocked issue suggested, no silent truncation
5. **Cross-reference complete?** — untracked issues placed in "Not on board" group

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (read-only display)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` CLI failure | Display error message and stop — no retries or fallback queries |
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| No project board found | Report "No project board found for this repo." → stop |
| 100-issue limit reached | Warn user: "Showing first 100 open issues — there may be more." |
| Zero open issues | Report "No open issues found." → stop |

## Anti-patterns

- **Showing Done/Cancelled issues as open.** Only list issues in active columns (Backlog through In Review) and "Not on board" — because this skill answers "what's open", not "what exists."
- **Suggesting a blocked issue as next.** Always check blockers before suggesting — because a blocked issue wastes the user's time.
- **Truncating output silently.** If `--limit 100` caps results, warn explicitly — because the user needs to know they're seeing a partial view.
- **False-positive blocker detection.** Only treat `Blocked by #N`, `Depends on #N`, `After #N` as blockers — because not every `#N` reference means a dependency.

## Guidelines

- **Read-only operation.** This skill only reads and displays data — it never modifies issues, labels, or board state. Modifications are other skills' responsibility.
- **Workflow order grouping.** Groups follow Backlog → Todo → Ready → In Progress → In Review — because this mirrors the natural issue lifecycle and helps the user see the full pipeline at a glance.
- **Priority-first sorting.** Within each group, P0 surfaces before P3 — because the user should act on critical issues first.
- **Honest about limits.** When the 100-issue cap is hit, say so explicitly — because partial data presented as complete is worse than no data.
