# list-issues

> List all open issues grouped by board column with priority sorting and next-issue suggestion.

Lists all open issues for the current repo, grouped by project board status column and sorted by priority, with dependency detection and a next-issue suggestion to help decide what to work on next.

## Usage

```text
/list-issues
```

> [!TIP]
> Also activates when you say "list issues", "show issues", "what issues are open", "issues list", or want an overview of all open work.

## How it works

1. **Detect repo URL** — Identify the current repository via `gh repo view`
2. **Discover project board** — Find the linked project board via GraphQL
3. **Fetch board items** — Query all board items with their status columns
4. **Fetch open issues and cross-reference** — Enrich with labels, size, and dependencies
5. **Group and sort** — Organize issues by column, sort by priority within each group
6. **Present results as table** — Render grouped markdown tables
7. **Suggest next issue** — Recommend the highest-priority unblocked issue to start
8. **Report** — Summary with issue counts per column and next-issue suggestion

## Directory structure

```text
list-issues/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── project-board-operations.md  # Board GraphQL patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-issues
```
