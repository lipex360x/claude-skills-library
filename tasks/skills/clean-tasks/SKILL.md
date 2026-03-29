---
name: clean-tasks
model: sonnet
description: >-
  Remove completed tasks from the task visibility board, keeping pending and
  in-progress items. Use this skill when the user says "clean tasks", "remove
  done tasks", "clear completed", "tv clean", or wants to tidy up the task
  list — even if they don't explicitly say "clean."
user-invocable: true
allowed-tools:
  - TaskList
  - TaskUpdate
---

# Clean Tasks

Remove completed tasks from the task list. Keep pending and in-progress tasks untouched.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

> _Skipped: "No input — operates on current task list state."_

</input_contract>

## Output contract

<output_contract>

> _Skipped: "No persistent output — task deletions are immediate."_

</output_contract>

## External state

<external_state>

> _Skipped: "N/A — operates only on the internal task system."_

</external_state>

## Pre-flight

<pre_flight>

1. Task list has completed tasks → if none: "No completed tasks to clean." — stop.

</pre_flight>

## Steps

### 1. Find completed tasks

Use TaskList to identify all tasks with status `completed`.

### 2. Delete completed tasks

Use TaskUpdate with status `deleted` for each completed task.

### 3. Report

Present concisely:
- **Removed:** {count} completed tasks
- **Remaining:** {count} pending/in-progress tasks (list briefly)
- **Errors:** issues encountered (or "none")

## Next action

> _Skipped: "Session complete — no follow-up needed."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — completed tasks existed before deletion
2. **Steps completed?** — all completed tasks deleted
3. **Anti-patterns clean?** — no pending or in-progress tasks were touched

</self_audit>

## Content audit

<content_audit>

> _Skipped: "N/A — skill does not generate verifiable content (state management only)."_

</content_audit>

## Error handling

> _Skipped: "No external calls — no error surface."_

## Anti-patterns

- **Deleting pending or in-progress tasks.** Only completed tasks are cleaned — because active tasks represent work the user needs to track and deleting them loses context.
- **Skipping the report.** Always confirm how many tasks were removed — because silent deletion leaves the user unsure whether the skill ran correctly.

## Guidelines

- **Silent execution.** No user confirmation needed — cleaning completed tasks is a safe, reversible operation that should execute without gates.
- **Preserve active work.** The task list is the user's working memory. Only remove items explicitly marked as done — because partial or ambiguous statuses should never be touched.
