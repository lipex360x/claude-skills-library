# list-issues

> List all open issues grouped by board column with priority sorting and next-issue suggestion.

Snapshot of every open issue on the project board, organized in workflow column order (Backlog → Todo → Ready → In Progress → In Review). Detects orphaned issues not linked to the board ("Not on board" group), enforces a 100-issue cap with explicit warnings, and recommends the next issue to pick up based on priority and blocker status.

## Usage

```text
/list-issues
```

> [!TIP]
> Also activates when you say "list issues", "show issues", "what issues are open", "issues list", or want an overview of all open work.

### Examples

```text
/list-issues             # show all open issues grouped by board column
"what issues are open"   # same effect via model invocation
"show the board"         # same effect via model invocation
```

## How it works

1. **Detect repo URL** — Identify the current repository via `gh repo view`
2. **Discover project board** — Find the linked project board via GraphQL
3. **Fetch board items** — Query all board items with their status columns
4. **Fetch open issues and cross-reference** — Enrich with labels, size, priority; detect untracked issues not on the board
5. **Group and sort** — Organize by column in workflow order (Backlog, Todo, Ready, In Progress, In Review), sort by priority (P0 first) within each group
6. **Present results as table** — Render grouped markdown tables with clickable links and blocker status
7. **Suggest next issue** — Recommend the highest-priority unblocked issue from Ready, then Todo, then Backlog
8. **Report** — Summary with issue counts per column and next-issue suggestion

[↑ Back to top](#list-issues)

## Directory structure

```text
list-issues/
├── SKILL.md              # Core skill instructions (8 steps, 0 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── project-board-operations.md  # Board GraphQL query patterns and column definitions
```

[↑ Back to top](#list-issues)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-issues
```
