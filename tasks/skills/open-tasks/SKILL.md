---
name: open-tasks
description: >-
  Reopen the task visibility board and resume task tracking. Use this skill
  when the user says "open tasks", "show tasks", "tv open", "start tracking",
  or wants to enable the task board — even if they don't explicitly say "open."
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - TaskCreate
  - TaskList
---

# Open Tasks

Reopen the task visibility board and resume task tracking for the session.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

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

1. Read `~/.brain/config/behavior.config.json` → if file missing: create it with `{ "task-visibility": { "always-open": true } }` and skip to Step 3.
2. Check `task-visibility.always-open` → if already `true`: "Board is already open." — stop.

</pre_flight>

## Steps

### 1. Update config

Set `task-visibility.always-open` to `true` in `~/.brain/config/behavior.config.json`.

### 2. Verify config change

Read the config file again to verify the change took effect. If the value is not `true`, report the failure.

### 3. Resume tracking

Resume creating and tracking tasks as normal for non-trivial work.

### 4. Report

Present concisely:
- **Board opened:** task tracking enabled
- **Status:** tasks will be created for non-trivial work
- **Errors:** issues encountered (or "none")

## Next action

> _Skipped: "Session complete — no follow-up needed."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — board was closed or config was missing before opening
2. **Steps completed?** — config updated and verified
3. **Config verified?** — `task-visibility.always-open` is `true` after write

</self_audit>

## Content audit

<content_audit>

> _Skipped: "N/A — skill does not generate verifiable content (state management only)."_

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Config file missing | Create with default structure, continue |
| Config write didn't persist | Re-read and report discrepancy → stop |

## Anti-patterns

- **Recreating previously deleted tasks.** Only enable tracking for new work — because old tasks were intentionally removed and restoring them creates confusion about what is current.
- **Skipping verification.** Always re-read the config after writing — because silent write failures leave the board in an inconsistent state.

## Guidelines

- **Idempotent activation.** If the board is already open, report it and stop — because redundant config writes add noise without value.
- **Forward-looking only.** Opening the board means tracking new work from this point forward. Never attempt to reconstruct or restore previous task state.
