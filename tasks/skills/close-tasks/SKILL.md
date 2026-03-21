---
name: close-tasks
description: Close the task visibility board and stop task tracking for the session. Use this skill when the user says "close tasks", "stop tracking", "tv close", "hide tasks", or wants to disable the task board — even if they don't explicitly say "close."
user-invocable: true
disable-model-invocation: false
---

Close the task visibility board.

1. Read `~/.brain/config/behavior.config.json` and check `task-visibility.always-open`. If already `false`, inform the user the board is already closed and stop.
2. List all tasks with TaskGet. If any task has status `in_progress`, warn the user with AskUserQuestion offering `["Close anyway", "Cancel"]`. If cancelled, stop.
3. Delete all tasks from the task list using TaskUpdate with status `deleted`.
4. Set `task-visibility.always-open` to `false` in `~/.brain/config/behavior.config.json`.
5. Read the config file again to verify the change took effect. If it didn't persist, report the error.
6. Confirm briefly that the board is closed and how many tasks were removed.

## Anti-patterns

- Don't silently delete in-progress tasks without warning the user — always check and confirm first.
- Don't skip verification — the config write can fail silently if the file path is wrong or permissions are restricted.
