# start-issue

> Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, creates branch and tasks.

Turns an issue with high-level acceptance criteria into a detailed implementation plan with TDD-ordered Steps and checkboxes, then sets up the branch and task board. One approval gate: the proposed plan.

## Usage

```text
/start-issue <issue-number>
```

> [!TIP]
> Also activates when the user says "start issue", "work on issue #N", "pull from backlog", "start #N", or wants to begin implementing an issue.

## How it works

1. **Select issue** — picks from Backlog milestone by number or presents a list for selection
2. **Analyze the issue** — fetches issue details and reads the codebase (ARCHITECTURE.md first, then exploration if needed); detects CDP config for web projects; checks Agent Teams availability
3. **Propose the detailed plan** — expands acceptance criteria into Steps with concrete checkboxes, file paths, and TDD order. Splits into multiple issues if 8+ steps. Adds Agent Teams execution mode if enabled
4. **Update the issue** — rewrites the issue body with the approved plan (creates additional issues if split)
5. **Create branch** — `feat/<number>-<slug>` from main
6. **Create tasks** — one task per Step with dependency tracking
7. **Spawn teammates** — if Agent Teams is enabled and the plan includes parallel steps, offers to launch teammates

## Directory structure

```text
start-issue/
├── SKILL.md              # Core instructions
├── references/           # CDP best practices
└── templates/            # Step template format
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-issue
```
