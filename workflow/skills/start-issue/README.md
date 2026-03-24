# start-issue

> Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks.

Turns an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then sets up the branch and tasks. Reads ARCHITECTURE.md and issue comments for context, enforces TDD order in every behavioral step, detects CDP configuration for web projects, and auto-selects an execution strategy (Agent, Teammate, or Sequential) when Agent Teams is enabled. One approval gate: the proposed plan. Everything else is automated.

## Usage

```text
/start-issue [issue-number]
```

> [!TIP]
> Also activates when you say "start issue", "work on issue #N", "pull from backlog", "start #N", or want to begin implementing an issue.

### Examples

```text
/start-issue           # pick from Backlog/Todo issues interactively
/start-issue 42        # start working on issue #42 directly
/start-issue #42       # same — accepts both formats
```

> [!NOTE]
> Requires GitHub CLI (`gh`) authenticated and an initialized git repository with a clean working tree. Run `gh auth login` if not set up. A project board is required — the skill will offer to create one if none exists.

## How it works

1. **Select issue** — Pick from Backlog/Todo issues by number or present a list
2. **Analyze the issue** — Fetch details, read comments for context, explore the codebase (ARCHITECTURE.md first, exploration agent only if needed), detect CDP configuration for web projects
3. **Determine execution strategy** — If Agent Teams is enabled, classify steps as sequential or parallelizable, choose Agent/Teammate/Sequential strategy
4. **Enforce development standards** — Verify TDD is present, reject workarounds, remove unnecessary code comments
5. **Propose the detailed plan** — Expand acceptance criteria into Steps with checkboxes, file paths, and TDD order (2-8 steps, 2-6 checkboxes each; splits into multiple issues if 8+ steps)
6. **Update the issue** — Rewrite the issue body with the approved plan and assign
7. **Create branch linked to issue** — Create `feat/<number>-<slug>` from main, move board card to "In Progress"
8. **Create tasks** — One task per Step with dependency tracking
9. **Spawn workers (automatic when Execution strategy is present)** — Launch parallel agents or teammates based on strategy, with progressive auditing as each worker completes
10. **Report** — Summary with branch name, step count, task list, and execution strategy

[↑ Back to top](#start-issue)

## Directory structure

```text
start-issue/
├── SKILL.md              # Core skill instructions (8 steps, 1 approval gate)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
├── references/
│   ├── anti-patterns.md              # 13 common mistakes to avoid during planning
│   ├── cdp-best-practices.md         # Chrome DevTools Protocol setup and verification
│   ├── development-guidelines.md     # General development standards (TDD, no workarounds)
│   ├── execution-strategy.md         # Agent vs Teammate vs Sequential decision matrix
│   ├── guidelines.md                 # 22 skill-specific guidelines and verification matrix
│   ├── project-board-operations.md   # Board GraphQL mutation patterns and field IDs
│   ├── project-board-setup.md        # Board column definitions (7 columns) and custom fields
│   └── tdd-methodology.md            # Test-driven development methodology and examples
└── templates/
    └── step-template.md              # Step checkbox format template with naming conventions
```

[↑ Back to top](#start-issue)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-issue
```
