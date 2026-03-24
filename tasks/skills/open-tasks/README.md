# open-tasks

> Reopen the task visibility board and resume task tracking.

Enables the task board by setting the always-open config flag to true, so tasks are created and tracked for non-trivial work throughout the session. Creates the config file automatically if it doesn't exist.

## Usage

```text
/open-tasks
```

> [!TIP]
> Also activates when you say "show tasks", "tv open", "start tracking", or want to enable the task board.

## How it works

1. **Update config** — sets `task-visibility.always-open` to `true` in the behavior config
2. **Verify config change** — re-reads the config file to confirm the value persisted
3. **Resume tracking** — task creation and tracking resumes for non-trivial work
4. **Report** — confirms the board is open and task tracking is enabled

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
