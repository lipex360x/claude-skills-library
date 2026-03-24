# list-backlog

> List open backlog issues with table summary and size sorting.

Read-only board query that fetches all issues in the "Backlog" column, enriches each with labels, size, priority, and live dependency verification, then renders a markdown table with clickable issue links. Supports `asc`/`desc` size sorting to prioritize small wins or tackle big blockers first. Every blocker reference is verified against live issue state to prevent false positives.

## Usage

```text
/list-backlog [sort-order]
```

> [!TIP]
> Also activates when you say "list backlog", "show backlog", "backlog list", "what's in the backlog", or want to see pending backlog items.

### Examples

```text
/list-backlog          # default sort by issue number
/list-backlog asc      # sort by size ascending (XS first)
/list-backlog desc     # sort by size descending (XL first)
```

## How it works

1. **Detect repo URL** — Identify the current repository via `gh repo view`
2. **Discover project board** — Find the linked project board via GraphQL
3. **Fetch backlog items from board** — Query board items in the Backlog column
4. **Fetch full issue details** — Enrich each item with labels, size, priority, and live dependency detection (verifies referenced issues are actually open)
5. **Present results as table** — Render a markdown table with clickable `[#N](url)` links, size, priority, and blocker status
6. **Report** — Summary with item count, sort order, and any dependency warnings

[↑ Back to top](#list-backlog)

## Directory structure

```text
list-backlog/
├── SKILL.md              # Core skill instructions (6 steps, 0 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── project-board-operations.md  # Board GraphQL query patterns and column definitions
```

[↑ Back to top](#list-backlog)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-backlog
```
