---
name: clean-tasks
description: Remove completed tasks from the task visibility board, keeping pending and in-progress items. Use this skill when the user says "clean tasks", "remove done tasks", "clear completed", "tv clean", or wants to tidy up the task list — even if they don't explicitly say "clean."
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - TaskList
  - TaskUpdate
---

Remove all completed tasks from the task list. Keep pending and in-progress tasks untouched.

1. Use TaskList to find completed tasks.
2. If no completed tasks are found, confirm with "No completed tasks to clean" and stop.
3. Use TaskUpdate with status `deleted` for each completed task.
4. Confirm how many tasks were removed and briefly list remaining tasks (pending/in-progress).

**Don't** delete pending or in-progress tasks — only completed ones.
