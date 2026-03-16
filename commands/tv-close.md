---
description: Close the task visibility board and stop task tracking for the rest of the session.
disable-model-invocation: true
---

Close the task visibility board. Delete all tasks from the task list using TaskUpdate with status "deleted". Set `task-visibility.always-open` to `false` in `~/.brain/config/behavior.config.json` so no new tasks are created for the remainder of this session. Confirm briefly that the board is closed.
