---
name: close-tasks
description: Close the task visibility board and stop task tracking for the session. Use this skill when the user says "close tasks", "stop tracking", "tv close", "hide tasks", or wants to disable the task board — even if they don't explicitly say "close."
user-invocable: true
disable-model-invocation: false
---

Close the task visibility board.

1. Delete all tasks from the task list using TaskUpdate with status `deleted`.
2. Set `task-visibility.always-open` to `false` in `~/.brain/config/behavior.config.json`.
3. Confirm briefly that the board is closed.
