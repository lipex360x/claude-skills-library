# /add-backlog

Create a GitHub issue in the project's Backlog milestone and add it to the project board with Size.

## Triggers

- `/add-backlog <description>`
- "add to backlog", "create backlog issue", "new issue for backlog"

## How it works

1. **Analyze scope** — detects multiple independent concerns and proposes splitting into separate issues
2. **Structure the issue** — builds a body with What, Why, and Acceptance criteria (2-4 checkboxes)
3. **Labels and Size** — asks which labels to apply and the estimated Size (XS/S/M/L/XL)
4. **Create** — creates the issue with `gh issue create` under the Backlog milestone
5. **Add to board** — adds the issue to the project board with status "Backlog" and the chosen Size

## Directory structure

```text
add-backlog/
├── SKILL.md
├── README.md
└── references/
    └── project-board-operations.md    # Commands for board operations
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill add-backlog
```
