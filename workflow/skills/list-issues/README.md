# list-issues

> List all open issues grouped by milestone with priority sorting and next-issue suggestion.

Fetches all open issues, groups them by milestone, sorts by priority labels (P0-P3), detects blocked issues via dependency references, and suggests the highest-priority unblocked issue to work on next.

## Usage

```text
/list-issues
```

> [!TIP]
> Also activates when the user says "show issues", "what issues are open", or wants an overview of all open work.

## How it works

1. **Fetch issues** — retrieves all open issues with labels, milestones, and bodies
2. **Group and sort** — groups by milestone (named first, then "No milestone"), sorts within each group by priority (P0 > P1 > P2 > P3 > unlabeled)
3. **Dependency detection** — scans issue bodies for "Depends on #N" / "After #N" patterns, checks if referenced issues are still open
4. **Suggest next issue** — identifies the highest-priority non-blocked issue as the recommended next pick

## Directory structure

```text
list-issues/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill list-issues
```
