# add-backlog

> Create a GitHub issue and add it to the project board's Backlog column.

Structures a new GitHub issue with acceptance criteria, scope analysis, and blocker detection, then places it in the project board's **Backlog** column. Ensures every issue is board-tracked and dependency-aware from the start.

## Usage

```text
/add-backlog <description>
```

> [!TIP]
> Also activates when you say "add to backlog", "create backlog issue", "backlog add", "new issue for backlog", or want to register a task for later.

## How it works

1. **Analyze scope** — Detect multiple concerns and propose splitting into separate issues
2. **Structure the issue** — Build body with What, Why, and acceptance criteria checkboxes
3. **Detect relevant skills** — Scan available skills for implementation notes
4. **Labels and Size** — Apply priority, type labels, and size estimate
5. **Detect blocker impact** — Identify blocking/blocked relationships with existing issues
6. **Review draft** — Present the issue draft for approval before creation
7. **Create issue** — Create the GitHub issue via `gh issue create`
8. **Update blocked issues** — Add blocker references to dependent issues
9. **Add to project board** — Place the card in the Backlog column via GraphQL
10. **Report** — Summary with issue link, labels, size, and blockers

## Directory structure

```text
add-backlog/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── project-board-operations.md  # Board GraphQL patterns
    └── project-board-setup.md       # Board column definitions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill add-backlog
```
