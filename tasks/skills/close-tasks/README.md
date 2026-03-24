# close-tasks

> Close the task visibility board and stop task tracking for the session.

Full board shutdown: deletes every task (completed, pending, and in-progress) and flips the `task-visibility.always-open` config flag to `false`. Includes a safety gate — warns and asks for confirmation if any in-progress tasks exist before proceeding. Verifies the config write persisted by re-reading the file after update.

## Usage

```text
/close-tasks
```

> [!TIP]
> Also activates when you say "stop tracking", "tv close", "hide tasks", or want to disable the task board.

### Examples

```text
/close-tasks               # delete all tasks and disable tracking
```

Also triggered by natural language:

```text
"stop tracking"            # same effect via model invocation
"hide tasks"               # same effect via model invocation
```

> [!WARNING]
> This skill deletes ALL tasks from the board (including pending and in-progress) and disables task tracking for the session. There is no undo — deleted tasks cannot be recovered. You will be prompted to confirm if any in-progress tasks exist.

## How it works

1. **Check for in-progress tasks** — Warns the user if any tasks are still active before proceeding
2. **Delete all tasks** — Removes every task from the board using `TaskUpdate` with status `deleted`
3. **Update config** — Sets `task-visibility.always-open` to `false` in the behavior config
4. **Verify config change** — Re-reads the config file to confirm the change persisted
5. **Report** — Confirms the board is closed, how many tasks were removed, and any errors

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
