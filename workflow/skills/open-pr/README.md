# open-pr

> Create a pull request from the current branch, linking it to the open issue.

Creates a pull request from the current branch, links it to the related issue, resolves incomplete checkboxes with scope transfer options, and moves the project board card to "In review."

## Usage

```text
/open-pr [title]
```

> [!TIP]
> Also activates when you say "create pr", "open pr", "pr create", "make a pull request", "submit for review", or want to open a PR for the current branch.

## How it works

1. **Link to issue** — Extract the issue number from the branch name
2. **Build PR content** — Derive title and body with summary, test plan, and `Closes #N`
3. **PR readiness check** — Verify all issue checkboxes are complete, handle incomplete items with scope transfer options
4. **Move card to "In review"** — Update the board card status via GraphQL
5. **Create PR** — Create the pull request via `gh pr create`
6. **Suggest merge** — Offer to run `/close-pr` when ready
7. **Report** — Summary with PR URL and linked issue

## Directory structure

```text
open-pr/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── project-board-operations.md  # Board GraphQL patterns
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill open-pr
```
