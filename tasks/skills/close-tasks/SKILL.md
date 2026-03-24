---
name: close-tasks
description: >-
  Close the task visibility board and stop task tracking for the session. Use
  this skill when the user says "close tasks", "stop tracking", "tv close",
  "hide tasks", or wants to disable the task board — even if they don't
  explicitly say "close."
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - TaskGet
  - TaskUpdate
  - AskUserQuestion
---

# Close Tasks

Close the task visibility board, delete all tasks, and disable task tracking for the session.

## Input contract

<input_contract>

> _Skipped: "No input — operates on current board state."_

</input_contract>

## Output contract

<output_contract>

> _Skipped: "No persistent output beyond config file update."_

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Behavior config | `~/.brain/config/behavior.config.json` | R/W | JSON |

</external_state>

## Pre-flight

<pre_flight>

1. Read `~/.brain/config/behavior.config.json` and check `task-visibility.always-open` → if already `false`: "Board is already closed." — stop.

</pre_flight>

## Steps

### 1. Check for in-progress tasks

List all tasks with TaskGet. If any task has status `in_progress`, warn the user with AskUserQuestion offering `["Close anyway", "Cancel"]` — because deleting in-progress tasks loses context the user may need. If cancelled, stop.

### 2. Delete all tasks

Delete all tasks from the task list using TaskUpdate with status `deleted`.

### 3. Update config

Set `task-visibility.always-open` to `false` in `~/.brain/config/behavior.config.json`.

### 4. Verify config change

Read the config file again to verify the change took effect. If it didn't persist, report the error.

### 5. Report

Present concisely:
- **Board closed:** task tracking disabled
- **Tasks removed:** {count} tasks deleted
- **Errors:** issues encountered (or "none")

## Next action

> _Skipped: "Session complete — no follow-up needed."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — board was open before closing
2. **Steps completed?** — all tasks deleted and config updated
3. **Config verified?** — `task-visibility.always-open` is `false` after write
4. **Approval gates honored?** — user confirmed if in-progress tasks existed

</self_audit>

## Content audit

<content_audit>

> _Skipped: "N/A — skill does not generate verifiable content (state management only)."_

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Config file missing | Report path error → stop |
| Config write didn't persist | Re-read and report discrepancy → stop |

## Anti-patterns

- **Silently deleting in-progress tasks.** Always check and confirm with the user first — because in-progress tasks represent active work the user may need to revisit.
- **Skipping verification.** Always re-read the config after writing — because the config write can fail silently if the file path is wrong or permissions are restricted.
- **Closing without reporting.** Always confirm the board is closed and how many tasks were removed — because silent state changes leave the user uncertain about what happened.

## Guidelines

- **Confirm before destructive actions.** In-progress tasks are the user's working context. Deleting them without warning breaks trust — always ask first.
- **Verify state changes.** Config file writes are the skill's primary side effect. Re-reading after write is cheap insurance against silent failures.
