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

1. **Delete** — removes all tasks from the task list using `TaskUpdate` with status `deleted`
2. **Disable** — sets `task-visibility.always-open` to `false` in `~/.brain/config/behavior.config.json`
3. **Confirm** — reports that the board is closed

## Directory structure

```text
close-tasks/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill close-tasks
```
