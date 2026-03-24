# list-backlog

> List open backlog issues with table summary and size sorting.

Lists all issues in the "Backlog" column of the project board for the current repo, with dependency detection and optional size sorting. Provides a quick overview of pending work items.

## Usage

```text
/list-backlog
```

> [!TIP]
> Also activates when you say "list backlog", "show backlog", "backlog list", "what's in the backlog", or want to see pending backlog items.

## How it works

1. **Detect repo URL** — Identify the current repository via `gh repo view`
2. **Discover project board** — Find the linked project board via GraphQL
3. **Fetch backlog items from board** — Query board items in the Backlog column
4. **Fetch full issue details** — Enrich each item with labels, size, and dependencies
5. **Present results as table** — Render a markdown table with sorting applied
6. **Report** — Summary with item count and any dependency warnings

## Directory structure

```text
list-backlog/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── project-board-operations.md  # Board GraphQL patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-backlog
```
