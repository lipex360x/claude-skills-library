# /open-pr

Create a pull request from the current branch, linking it to the open issue. Handles scope transfers for incomplete tasks and moves the card to "Ready to PR" on the project board.

## Triggers

- `/open-pr [title]`
- "open pr", "make a pull request", "submit for review"

## How it works

1. **Validate branch** — ensures you're not on `main`, pushes unpushed commits
2. **Link to issue** — extracts issue number from branch name (e.g., `42-add-feature` → #42)
3. **Build PR content** — derives title from arguments, issue, or commits; builds body with summary, test plan, and `Closes #N`
4. **Readiness check** — verifies all issue checkboxes are complete. If unchecked items exist, offers to transfer them to other issues with bidirectional scope transfer comments. Scans for `.fixme`, `.skip`, `.todo`, and `only` markers in test files
5. **Move card** — moves the issue card to "In review" on the project board
6. **Create and report** — creates the PR with `gh pr create` and reports the URL

## Directory structure

```text
open-pr/
├── SKILL.md
├── README.md
└── references/
    └── project-board-operations.md    # Commands for moving cards on the board
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill open-pr
```
