# add-backlog

> Create a GitHub issue in the project's Backlog milestone.

Parses a description, analyzes scope for potential splitting, structures the issue with What/Why/Acceptance criteria, and creates it in the Backlog milestone with labels.

## Usage

```text
/add-backlog <description>
```

> [!TIP]
> Also activates when the user says "add to backlog", "create backlog issue", "new issue for backlog", or wants to register a task for later.

## How it works

1. **Analyze scope** — detects multiple independent concerns and proposes splitting into separate issues
2. **Structure the issue** — builds a body with What, Why, and Acceptance criteria (2-4 checkboxes)
3. **Labels** — asks which labels to apply from the repo's available labels
4. **Create** — creates the issue with `gh issue create` under the Backlog milestone

## Directory structure

```text
add-backlog/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill add-backlog
```
