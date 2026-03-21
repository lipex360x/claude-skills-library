---
name: list-backlog
description: List open backlog issues with table summary and size sorting. Use this skill when the user says "list backlog", "show backlog", "backlog list", "what's in the backlog", or wants to see pending backlog items — even if they don't explicitly say "backlog."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash
---

List all issues in the "Backlog" column of the project board for the current repo.

Read `references/project-board-operations.md` for board query patterns and column definitions.

## Arguments

`/list-backlog [asc|desc]`

- `asc` — sort by size ascending (XS → S → M → L → XL)
- `desc` — sort by size descending (XL → L → M → S → XS)
- No argument — default sort by issue number ascending

## 1. Detect repo URL

Run: `gh repo view --json url -q '.url'`

Store the result as `REPO_URL` for building issue links.

## 2. Discover project board

Find the project board for the current repo:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[] | select(.title | test("<repo-name>"; "i")) | .number')
```

If no board is found, say "No project board found for this repo." and stop.

## 3. Fetch backlog items from board

Query the board for items in the "Backlog" column:

```bash
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog")
  | {number: .content.number, title: .content.title}
]'
```

If no items are in Backlog, say so and stop.

## 4. Fetch full issue details

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

### Dependency detection

Scan the body for patterns like "Depends on #N", "After #N", "Blocked by #N", or "Related issues: #N" — these are the canonical formats used by `/add-backlog` and `/close-pr`, so matching them covers real dependencies reliably.

For each referenced issue, verify it is actually open before flagging: `gh issue view #N --json state -q '.state'`. Only flag direct, explicit dependencies — not loose topical overlap. If any dependency is open, set status to `**Blocked** by #N, #M` (listing all open blockers). Otherwise leave status empty.

**Accuracy is critical here.** A false-positive blocker misleads the user into thinking work is stuck when it isn't. A stale "Blocked" status (referencing an already-closed issue) is equally misleading. Always verify state at query time.

**Sorting** — size-based sorting exists because it helps the user prioritize by effort (tackle small wins first with `asc`, or clear big blockers first with `desc`):
- If user passed `asc`: sort by size ascending using order: XS < S < M < L < XL (issues without size go last)
- If user passed `desc`: sort by size descending using order: XL > L > M > S > XS (issues without size go last)
- If no argument: sort by issue number ascending (natural order)

## 5. Present results as table

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

## Error handling

- **`gh` CLI failure** — if any `gh` command fails (network error, auth expired, API rate limit), display the error message and stop gracefully. Do not attempt retries or fallback queries.
- **Malformed issue body** — if an issue body cannot be parsed for size, priority, or dependency patterns, skip the unparseable fields with a `—` placeholder rather than failing the entire listing. Note which issues had parse issues in a footer line.
- **Board query returns unexpected shape** — if the board JSON lacks expected fields (`.items`, `.status`), report "Board data format unexpected — run `gh project item-list` manually to verify." and stop.

## Anti-patterns

- **False-positive blockers** — topical overlap between issues is not a dependency. "Both touch auth" does not mean one blocks the other. Only explicit "Blocked by #N" / "Depends on #N" annotations count.
- **Stale board data shown as current** — board queries reflect a point in time. Do not cache results across invocations or present old data as fresh.
- **Showing closed issues as blockers** — always verify referenced issue state before flagging. A closed issue is not a blocker.
- **Truncating long titles** — display the full issue title. Truncation hides context the user needs to identify the issue at a glance.
