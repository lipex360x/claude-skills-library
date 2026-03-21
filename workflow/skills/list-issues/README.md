# list-issues

> List all open issues grouped by board column with priority sorting and next-issue suggestion.

Fetches all open issues, groups them by project board status column, sorts by priority labels (P0-P3), detects blocked issues via dependency references, and suggests the highest-priority unblocked issue to work on next.

## Usage

```text
/list-issues
```

> [!TIP]
> Also activates when the user says "show issues", "what issues are open", or wants an overview of all open work.

## How it works

1. **Detect repo and board** — finds the project board for the current repo
2. **Fetch and cross-reference** — retrieves all open issues and maps them to board columns (Backlog → Todo → Ready → In Progress → In Review)
3. **Dependency detection** — scans issue bodies for "Blocked by #N" / "Depends on #N" / "After #N" patterns, checks if referenced issues are still open
4. **Suggest next issue** — identifies the highest-priority non-blocked issue as the recommended next pick

## Directory structure

```text
list-issues/
├── SKILL.md                              # Core instructions
└── references/
    └── project-board-operations.md       # Board query patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-issues
```
