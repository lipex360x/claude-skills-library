# continue-issue

Resume work on an in-progress issue from where it left off.

## What it does

Reads the GitHub issue body, identifies completed steps via checkboxes, recreates the task board matching issue state (completed steps get green ticks, current step shows spinner, pending steps stay empty), and immediately starts working on the next pending step.

## When to use

- Opening a new Claude Code conversation to continue an issue started with `/start-issue`
- After a session timeout or context window reset
- When you want to see progress status and resume working

## Usage

```
/continue-issue         # Auto-detects issue from current branch
/continue-issue 1       # Explicitly specify issue #1
/continue-issue #1      # Also accepts #N format
```

## How it works

1. **Detect issue** — from argument, branch name (`feat/<N>-*`), or "In Progress" board items
2. **Parse progress** — reads issue body, counts checked vs unchecked checkboxes per step
3. **Validate next step** — runs `validate-issue.sh --step N` (if the project has the validator) to catch structural problems before work begins. Errors must be fixed before proceeding; warnings are advisory.
4. **Rebuild task board** — creates tasks matching issue state (completed/in_progress/pending)
5. **Load context** — reads ARCHITECTURE.md, quality.md, recent comments, git log
6. **Resume work** — starts executing the next pending step immediately

### Validation details

The step validator (`validate-issue.sh`) enforces issue structure rules:

- **Process gate exclusion** — tags `[PW]`, `[HUMAN]`, `[DOCS]`, and `[AUDIT]` are process gates, not work scope. They are excluded from checkbox counting when evaluating step size limits, so a step with 6 work checkboxes + 4 process gates is counted as 6, not 10.
- **Vertical TDD enforcement** — the `green_no_consecutive` rule flags consecutive `[GREEN]` checkboxes without an intervening `[RED]`. RED/GREEN may alternate freely (vertical TDD: RED→GREEN→RED→GREEN is valid via `repeatable_groups`).
- **DOCS mandatory** — `[DOCS]` is required (error) in steps with `[GREEN]` or `[WIRE]`. Positioned after HUMAN and before AUDIT.
- **PW runs as user would** — E2E tests simulate the full user flow via UI (no programmatic auth shortcuts). Reads `.claude/project-setup.json` for `headed`, `project`, and `workers` flags.
- **HUMAN is user-driven** — agent provides a step-by-step testing guide (URLs, credentials, actions); the user validates the running app themselves.
- Validation errors block work; warnings are reported but don't block.

## Install

```bash
npx @anthropic-ai/claude-code skills add workflow:continue-issue
```

## Requirements

- GitHub CLI (`gh`) authenticated
- Issue created with `/start-issue` (must have `## Step N — Title` format)
- Git repository with remote origin
