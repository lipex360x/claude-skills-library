# list-backlog

> List open backlog issues with table summary, clickable links, and size sorting.

Fetches all open issues in the Backlog milestone and presents them as a markdown table with clickable issue links, labels, and size. Supports sorting by size (ascending/descending).

## Usage

```text
/list-backlog          # default: sorted by issue number (asc)
/list-backlog asc      # sorted by size: XS → S → M → L → XL
/list-backlog desc     # sorted by size: XL → L → M → S → XS
```

> [!TIP]
> Also activates when the user says "show backlog", "what's in the backlog", or wants to see pending backlog items.

## How it works

1. **Detect repo URL** — gets the GitHub repo URL for building clickable issue links
2. **Fetch issues** — queries the Backlog milestone for open issues with labels
3. **Process and sort** — extracts size from labels, applies sorting (by size or issue number)
4. **Present results** — displays a table with linked issue numbers, titles, labels, and size; suggests `/start-issue` to begin working on one

## Directory structure

```text
list-backlog/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-backlog
```
