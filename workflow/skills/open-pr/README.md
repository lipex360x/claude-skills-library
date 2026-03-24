# open-pr

> Create a pull request from the current branch, linking it to the open issue.

Seven-step PR creation with built-in readiness checks: resolves every unchecked issue checkbox before opening (move to another issue, create backlog issue, mark as done, or skip with justification), scans test files for `.skip`/`.only`/`.fixme`/`.todo` markers, generates a structured PR body with summary and test plan, moves the board card to "In review", and offers immediate merge via `/close-pr`. Bidirectional scope transfer comments ensure no work item is silently dropped.

## Usage

```text
/open-pr [title]
```

> [!TIP]
> Also activates when you say "create pr", "open pr", "pr create", "make a pull request", "submit for review", or want to open a PR for the current branch.

### Examples

```text
/open-pr                               # derive title from issue or first commit
/open-pr "Add billing dashboard"       # use explicit title
```

## How it works

1. **Link to issue** — Extract the issue number from the branch name (`feat/42-slug` or `42-slug`)
2. **Build PR content** — Derive title from arguments, issue title, or first commit; build body with summary, test plan, and `Closes #N`
3. **PR readiness check** — Verify all issue checkboxes complete; for each unchecked item, offer move/create/skip/mark-done options with bidirectional scope transfer comments; scan test files for `.skip`/`.only`/`.fixme`/`.todo` markers
4. **Move card to "In review"** — Update the board card status via GraphQL
5. **Create PR** — Create the pull request via `gh pr create`
6. **Suggest merge** — Offer to run `/close-pr` immediately or wait for review
7. **Report** — Summary with PR URL, linked issue, scope transfers, and board status

[↑ Back to top](#open-pr)

## Directory structure

```text
open-pr/
├── SKILL.md              # Core skill instructions (7 steps, 2 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── project-board-operations.md  # Board GraphQL mutation patterns and field IDs
```

[↑ Back to top](#open-pr)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill open-pr
```
