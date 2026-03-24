# add-backlog

> Create a GitHub issue and add it to the project board's Backlog column.

Full-lifecycle issue creation with 10 steps: scope analysis detects multi-concern requests and proposes splits, skill detection auto-references relevant `/commands` in implementation notes, and blocker detection cross-references existing open issues for dependency annotations. Every issue lands on the board with Size, labels, and verified acceptance criteria — never orphaned from tracking.

## Usage

```text
/add-backlog <description>
```

> [!TIP]
> Also activates when you say "add to backlog", "create backlog issue", "backlog add", "new issue for backlog", or want to register a task for later.

### Examples

```text
/add-backlog add dark mode toggle to settings page   # create issue from inline description
/add-backlog                                          # interactive — prompts for description
```

## How it works

1. **Analyze scope** — Detect multiple concerns and propose splitting into separate issues
2. **Structure the issue** — Build body with What, Why, and acceptance criteria checkboxes
3. **Detect relevant skills** — Scan available skills for implementation notes (agent-friendly format for repetitive work)
4. **Labels and Size** — Apply priority, type labels, and size estimate (XS through XL)
5. **Detect blocker impact** — Cross-reference open issues for blocking/blocked relationships
6. **Review draft** — Verify acceptance criteria are concrete and verifiable before creation
7. **Create issue** — Create the GitHub issue via `gh issue create`
8. **Update blocked issues** — Add `Depends on #N` annotations and comments to dependent issues
9. **Add to project board** — Place the card in the Backlog column with Size field set via GraphQL
10. **Report** — Summary with issue link, labels, size, blockers, and audit results

[↑ Back to top](#add-backlog)

## Directory structure

```text
add-backlog/
├── SKILL.md              # Core skill instructions (10 steps, 3 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    ├── project-board-operations.md  # Board GraphQL mutation patterns and field IDs
    └── project-board-setup.md       # Board column definitions (7 columns) and custom fields
```

[↑ Back to top](#add-backlog)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill add-backlog
```
