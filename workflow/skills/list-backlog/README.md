# list-backlog

> List open backlog issues with numbered summary for selection.

Fetches all open issues in the Backlog milestone and presents them as a numbered list with labels, ready for selection.

## Usage

```text
/list-backlog
```

> [!TIP]
> Also activates when the user says "show backlog", "what's in the backlog", or wants to see pending backlog items.

## How it works

1. **Fetch issues** — queries the Backlog milestone for open issues with labels
2. **Present results** — displays a numbered list with issue numbers, titles, and labels; suggests `/start-backlog` to begin working on one

## Directory structure

```text
list-backlog/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-backlog
```
