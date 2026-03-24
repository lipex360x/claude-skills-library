# close-tasks

> Close the task visibility board and stop task tracking for the session.

Shuts down the task board by deleting all tasks and disabling the always-open config flag. Warns before closing if any tasks are still in-progress, ensuring no active work is accidentally lost.

## Usage

```text
/close-tasks
```

> [!TIP]
> Also activates when you say "stop tracking", "tv close", "hide tasks", or want to disable the task board.

## How it works

1. **Check for in-progress tasks** — warns the user if any tasks are still active before proceeding
2. **Delete all tasks** — removes every task from the board using `TaskUpdate` with status `deleted`
3. **Update config** — sets `task-visibility.always-open` to `false` in the behavior config
4. **Verify config change** — re-reads the config file to confirm the change persisted
5. **Report** — confirms the board is closed, how many tasks were removed, and any errors

## Directory structure

```text
close-tasks/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill close-tasks
```
