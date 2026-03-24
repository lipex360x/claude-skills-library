# clean-tasks

> Remove completed tasks from the task visibility board, keeping pending and in-progress items.

Tidies up the task list by identifying and deleting all completed tasks while preserving pending and in-progress items. Useful for keeping the task board focused on active work without manual cleanup.

## Usage

```text
/clean-tasks
```

> [!TIP]
> Also activates when you say "remove done tasks", "clear completed", "tv clean", or want to tidy up the task list.

## How it works

1. **Find completed tasks** — scans the task board for all tasks with completed status
2. **Delete completed tasks** — removes each completed task using `TaskUpdate` with status `deleted`
3. **Report** — confirms how many tasks were removed, how many remain, and any errors

## Directory structure

```text
clean-tasks/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill clean-tasks
```
