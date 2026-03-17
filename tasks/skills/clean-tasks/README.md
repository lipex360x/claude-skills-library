# clean-tasks

> Remove completed tasks from the task visibility board, keeping pending and in-progress items.

Tidies up the task list by deleting all completed tasks while leaving pending and in-progress items untouched.

## Usage

```text
/clean-tasks
```

> [!TIP]
> Also activates when saying "remove done tasks", "clear completed", "tv clean", or wanting to tidy up the task list.

## How it works

1. **List** — reads all tasks from the task board
2. **Filter** — identifies tasks with completed status
3. **Delete** — removes each completed task using `TaskUpdate` with status `deleted`
4. **Confirm** — reports how many tasks were removed

## Directory structure

```text
clean-tasks/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill clean-tasks
```
