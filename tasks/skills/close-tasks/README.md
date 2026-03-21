# close-tasks

> Close the task visibility board and stop task tracking for the session.

Shuts down the task board by deleting all tasks and disabling the always-open setting, effectively stopping task tracking until reopened.

## Usage

```text
/close-tasks
```

> [!TIP]
> Also activates when saying "stop tracking", "tv close", "hide tasks", or wanting to disable the task board.

## How it works

1. **Pre-check** — reads config to verify the board isn't already closed
2. **Safety check** — warns before closing if any tasks are still in-progress
3. **Delete** — removes all tasks from the task list using `TaskUpdate` with status `deleted`
4. **Disable** — sets `task-visibility.always-open` to `false` in config
5. **Verify** — reads config again to confirm the change persisted
6. **Confirm** — reports the board is closed and how many tasks were removed

## Directory structure

```text
close-tasks/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill close-tasks
```
