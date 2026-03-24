# start-issue

> Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks.

Turns an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then sets up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

## Usage

```text
/start-issue [issue-number]
```

> [!TIP]
> Also activates when you say "start issue", "work on issue #N", "pull from backlog", "start #N", or want to begin implementing an issue.

## How it works

1. **Select issue** — Pick from Backlog/Todo issues by number or present a list
2. **Analyze the issue** — Fetch details, read comments for context, explore the codebase
3. **Propose the detailed plan** — Expand acceptance criteria into Steps with checkboxes, file paths, and TDD order
4. **Update the issue** — Rewrite the issue body with the approved plan
5. **Create branch linked to issue** — Create `feat/<number>-<slug>` from main
6. **Create tasks** — One task per Step with dependency tracking
7. **Spawn teammates (automatic when Execution mode is present)** — Launch parallel teammates if Agent Teams is enabled
8. **Report** — Summary with branch name, step count, and task list

## Directory structure

```text
start-issue/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── anti-patterns.md              # Common mistakes to avoid
│   ├── cdp-best-practices.md         # Chrome DevTools Protocol practices
│   ├── development-guidelines.md     # General development guidelines
│   ├── guidelines.md                 # Skill-specific guidelines
│   ├── project-board-operations.md   # Board GraphQL patterns
│   ├── project-board-setup.md        # Board column definitions
│   └── tdd-methodology.md            # Test-driven development methodology
└── templates/
    └── step-template.md              # Step checkbox format template
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-issue
```
