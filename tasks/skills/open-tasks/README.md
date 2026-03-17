# open-tasks

> Reopen the task visibility board and resume task tracking.

Enables the task board by setting the always-open flag, so tasks are created and tracked for the rest of the session.

## Usage

```text
/open-tasks
```

> [!TIP]
> Also activates when saying "show tasks", "tv open", "start tracking", or wanting to enable the task board.

## How it works

1. **Enable** — sets `task-visibility.always-open` to `true` in `~/.brain/config/behavior.config.json`
2. **Resume** — task creation and tracking resumes as normal
3. **Confirm** — reports that the board is open

## Directory structure

```text
open-tasks/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill open-tasks
```
