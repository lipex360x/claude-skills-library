---
name: list-backlog
description: >-
  List open backlog issues with table summary and size sorting. Use this skill
  when the user says "list backlog", "show backlog", "backlog list", "what's in
  the backlog", or wants to see pending backlog items — even if they don't
  explicitly say "backlog."
user-invocable: true
allowed-tools:
  - Bash
---

# List Backlog

List all issues in the "Backlog" column of the project board for the current repo, with dependency detection and optional size sorting.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `sort-order` | $ARGUMENTS | no | `asc`, `desc`, or empty | Default to issue number ascending |

- `asc` — sort by size ascending (XS → S → M → L → XL)
- `desc` — sort by size descending (XL → L → M → S → XS)
- No argument — default sort by issue number ascending

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Backlog table | stdout | no | Markdown table |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Project board | GitHub Projects API | R | GraphQL / JSON |
| Open issues | `gh issue view` | R | JSON |
| Board operations guide | `references/project-board-operations.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
3. `gh auth status` succeeds → if not: "Run `gh auth login` first." — stop.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

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

If no board is found, say "No project board found for this repo." and stop.

### 3. Fetch backlog items from board

Query the board for items in the "Backlog" column:

```bash
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog")
  | {number: .content.number, title: .content.title}
]'
```

If no items are in Backlog, say so and stop.

### 4. Fetch full issue details

The board query returns limited data. For each issue number from step 3, fetch full details:

```bash
gh issue view <number> --json number,title,labels,body
```

Parse each issue and extract:
- **number** — issue number
- **title** — issue title
- **labels** — all labels except size and priority labels
- **size** — extracted from `size:*` label (XS, S, M, L, XL). If none, treat as `—`
- **priority** — extracted from `priority:*` or `P0`–`P3` labels. If none, treat as `—`
- **status** — determined by dependency detection (see below)

#### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N" — these are the canonical formats used by `/add-backlog` and `/close-pr`, so matching them covers real dependencies reliably.

For each referenced issue, verify it is actually open before flagging: `gh issue view #N --json state -q '.state'`. Only flag direct, explicit dependencies — not loose topical overlap. If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

**Accuracy is critical here.** A false-positive blocker misleads the user into thinking work is stuck when it isn't. A stale "Blocked" status (referencing an already-closed issue) is equally misleading. Always verify state at query time.

#### Sorting

Size-based sorting exists because it helps the user prioritize by effort (tackle small wins first with `asc`, or clear big blockers first with `desc`):
- If user passed `asc`: sort by size ascending using order: XS < S < M < L < XL (issues without size go last)
- If user passed `desc`: sort by size descending using order: XL > L > M > S > XS (issues without size go last)
- If no argument: sort by issue number ascending (natural order)

### 5. Present results as table

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

After the table, add: `Pick an issue number to start working on it.`

### 6. Report

Present concisely:
- **What was done** — number of backlog issues listed, sort order used
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

Run `/start-issue <number>` to begin working on a backlog issue.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, git repo confirmed
2. **Steps completed?** — board discovered, items fetched, table presented
3. **Output exists?** — markdown table rendered with correct link format
4. **Anti-patterns clean?** — no false-positive blockers, no stale data, no truncated titles
5. **Dependency verification?** — all referenced issues checked for open/closed state

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (read-only display)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` CLI failure | Display error message and stop — no retries or fallback queries |
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| No project board found | Report "No project board found for this repo." → stop |
| Malformed issue body | Skip unparseable fields with `—` placeholder, note in footer |
| Board query unexpected shape | Report "Board data format unexpected — run `gh project item-list` manually to verify." → stop |

## Anti-patterns

- **False-positive blockers.** Topical overlap between issues is not a dependency — because "both touch auth" does not mean one blocks the other. Only explicit "Blocked by #N" / "Depends on #N" annotations count.
- **Stale board data shown as current.** Board queries reflect a point in time — because caching results across invocations or presenting old data as fresh misleads the user.
- **Showing closed issues as blockers.** Always verify referenced issue state before flagging — because a closed issue is not a blocker.
- **Truncating long titles.** Display the full issue title — because truncation hides context the user needs to identify the issue at a glance.

## Guidelines

- **Read-only operation.** This skill only reads and displays data — it never modifies issues, labels, or board state. Modifications are other skills' responsibility.
- **Accuracy over speed.** Verify every dependency reference against live issue state — because a false blocker is worse than a slightly slower query.
- **Consistent table format.** Always use the exact markdown table format specified — because downstream skills and users rely on predictable output structure.
