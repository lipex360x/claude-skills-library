# clean-tasks

> Remove completed tasks from the task visibility board, keeping pending and in-progress items.

One-command cleanup that scans the board for all completed tasks and batch-deletes them. Keeps the board focused on active work without manual per-task removal. Runs without confirmation gates since only already-completed items are affected.

## Usage

```text
/clean-tasks
```

> [!TIP]
> Also activates when you say "remove done tasks", "clear completed", "tv clean", or want to tidy up the task list.

### Examples

```text
/clean-tasks               # remove all completed tasks from the board
```

Also triggered by natural language:

```text
"remove done tasks"        # same effect via model invocation
"clear completed"          # same effect via model invocation
```

> [!WARNING]
> This skill permanently deletes completed tasks from the board. There is no undo — deleted tasks cannot be recovered.

## How it works

1. **Find completed tasks** — Scans the task board for all tasks with completed status
2. **Delete completed tasks** — Removes each completed task using `TaskUpdate` with status `deleted`
3. **Report** — Confirms how many tasks were removed, how many remain, and any errors

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
