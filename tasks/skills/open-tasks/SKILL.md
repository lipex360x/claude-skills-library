---
name: open-tasks
description: Reopen the task visibility board and resume task tracking. Use this skill when the user says "open tasks", "show tasks", "tv open", "start tracking", or wants to enable the task board — even if they don't explicitly say "open."
user-invocable: true
disable-model-invocation: false
---

Reopen the task visibility board.

1. Read `~/.brain/config/behavior.config.json`. If the file is missing, create it with `{ "task-visibility": { "always-open": true } }`. If `task-visibility.always-open` is already `true`, confirm the board is already open and skip remaining steps.
2. Set `task-visibility.always-open` to `true`.
3. Read the config again to verify the change took effect. If the value is not `true`, report the failure.
4. Resume creating and tracking tasks as normal.
5. Confirm briefly that the board is open.

## Anti-patterns

- Don't recreate previously deleted tasks — only enable tracking for new work.
