# open-tasks

> Reopen the task visibility board and resume task tracking.

Enables the task board by flipping the `task-visibility.always-open` config flag to `true`. Idempotent — reports and stops if the board is already open. Auto-creates the config file with defaults if it does not exist. Forward-looking only: never attempts to restore previously deleted tasks.

## Usage

```text
/open-tasks
```

> [!TIP]
> Also activates when you say "show tasks", "tv open", "start tracking", or want to enable the task board.

### Examples

```text
/open-tasks                # enable the task board and start tracking
```

Also triggered by natural language:

```text
"show tasks"               # same effect via model invocation
"start tracking"           # same effect via model invocation
```

## How it works

1. **Update config** — Sets `task-visibility.always-open` to `true` in the behavior config
2. **Verify config change** — Re-reads the config file to confirm the value persisted
3. **Resume tracking** — Task creation and tracking resumes for non-trivial work
4. **Report** — Confirms the board is open and task tracking is enabled

## Directory structure

```text
open-tasks/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill open-tasks
```
