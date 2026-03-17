# create-pr

> Create a pull request from the current branch, linking it to the open issue.

Validates the branch, pushes unpushed commits, extracts the issue number from the branch name, builds a PR with summary and test plan, and runs readiness checks before creating.

## Usage

```text
/create-pr [title]
```

> [!TIP]
> Also activates when the user says "open pr", "make a pull request", "submit for review", or wants to open a PR for the current branch.

## How it works

1. **Validate branch** — ensures you're not on `main`, pushes unpushed commits
2. **Link to issue** — extracts issue number from branch name (e.g., `42-add-feature` -> #42)
3. **Build PR content** — derives title from arguments, issue, or commits; builds body with summary, test plan, and `Closes #N`
4. **Readiness check** — verifies all issue checkboxes are complete, scans for `.fixme`, `.skip`, `.todo`, and `only` markers in test files
5. **Create and report** — creates the PR with `gh pr create` and reports the URL

## Directory structure

```text
create-pr/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-pr
```
