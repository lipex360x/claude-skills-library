---
name: continue-issue
description: >-
  Resume work on an in-progress issue from where it left off. Reads the issue
  body, identifies completed steps via checkboxes, recreates the task board
  matching issue state, and starts working on the next pending step. Use this
  skill when the user says "continue issue", "resume issue", "continue #N",
  "where was I", "pick up where I left off", "continue working", or wants to
  resume an issue started with /start-issue — even if they don't explicitly
  say "continue."
user-invocable: true
argument-hint: "[issue-number]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - WebSearch
  - WebFetch
---

# Continue Issue

Resume work on an in-progress issue by reconstructing session state from the issue checkboxes. Tasks are session-scoped and disappear between conversations — this skill rebuilds them so progress tracking stays accurate.

**IMPORTANT:** Read the entire Pre-flight section before taking any action.

## Pre-flight

<pre_flight>

**Inputs:** `$ARGUMENTS` → issue number (positive integer, accepts `#N` or `N`). If absent, auto-detect from branch name (`feat/<N>-*` or `feature/<N>-*`).

**Reads:** `.docs/issues/<N>.md` (local issue body), `.docs/architecture.md`, `.docs/project.md`, `.docs/quality.md`, CLAUDE.md, `.claude/project-setup.json`.

**Checks:**

1. `which gh` → if missing: "GitHub CLI required." — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. **Read `.docs/architecture.md`** → if exists, read and store. Primary codebase context.
5. **Read `.docs/project.md`** → if exists, read and store. Domain context (terms, business rules, boundaries).
6. **Read `.docs/quality.md`** → if exists, read and store. Code quality standards for this project.
7. **Read `.claude/scripts/validate-issue.config.json`** → if exists, internalize tag rules (`tag_order`, `max_checkboxes`, etc.) so you can fix validation errors efficiently in Step 2b.
8. **Working tree clean?** `git status --porcelain` → if not clean: warn "Uncommitted changes detected — consider committing or stashing before continuing." Continue (warning, not a block).
9. **Read development references.** Before starting implementation, read `references/guidelines.md` for development standards (TDD, Playwright, DDD). Read `references/tdd-methodology.md` when executing `[RED]`/`[GREEN]` steps.

</pre_flight>

## Steps

### 1. Identify the issue

Parse `$ARGUMENTS` for an issue number. Accept `#N` or `N`.

If no argument provided, detect from the current branch name:

```bash
git branch --show-current | grep -oE '[0-9]+' | head -1
```

Branches follow `feat/<number>-<slug>` or `feature/<number>-<slug>`. Extract the number.

If detection fails, query the project board for issues in "In Progress":

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[0].number')
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "In Progress")
  | "#\(.content.number) — \(.content.title)"
]'
```

Present the list with `AskUserQuestion` if multiple. If only one, use it automatically.

If no issue found, stop: "No in-progress issue found. Use `/start-issue` to begin one."

### 2. Read the issue and parse progress

Read the local issue body first. If `.docs/issues/<N>.md` exists, use it as the source of truth. Fall back to GitHub API only if the local file is missing:

```bash
gh issue view <number> --json body,title,labels -q '{title: .title, labels: [.labels[].name], body: .body}'
```

Parse the issue body to extract:

1. **Steps** — each `## Step N — Title` section
2. **Checkbox states** — for each step, count checked `- [x]` vs unchecked `- [ ]` checkboxes
3. **Step status** — derive from checkboxes:
   - All checkboxes checked → `completed`
   - At least one checked, others unchecked → `in_progress`
   - No checkboxes checked → `pending`
4. **Next step** — first step that is `pending` or `in_progress`

Present a status table:

```
| Step | Title                  | Progress | Status      |
|------|------------------------|----------|-------------|
| 1    | Scaffold frontend      | 4/4      | completed   |
| 2    | Scaffold backend       | 6/6      | completed   |
| 3    | Test isolation          | 3/6      | in_progress |
| 4    | Configure Playwright   | 0/5      | pending     |
| ...  | ...                    | ...      | ...         |
```

### 2b. Validate the next step

After identifying the next step (first `pending` or `in_progress`), validate its structure before starting work. If `.claude/scripts/validate-issue.sh` exists in the project, run:

```bash
bash .claude/scripts/validate-issue.sh <number> --step <next-step-number>
```

- **Errors** → fix the issue body (add missing tags, split oversized steps) and re-validate until it passes. Do NOT start work on a step with validation errors.
- **Warnings** → report to user in the status table, but proceed. Warnings are advisory.
- **Script not found** → skip validation silently (not all projects have the validator).

### 3. Recreate the task board

Create one `TaskCreate` per Step, matching the parsed status:

- **Completed steps** → create task then immediately `TaskUpdate` to `completed`
- **In-progress step** → create task then `TaskUpdate` to `in_progress`
- **Pending steps** → create task (stays `pending`)

Task subjects follow the pattern: `Step N — Title` (matching the issue exactly).

### 4. Load codebase context

Pre-flight already loaded `.docs/architecture.md` and `.docs/quality.md`. Additionally:

- **Read issue comments** for recent context:
  ```bash
  gh issue view <number> --json comments --jq '.comments[-3:] | .[] | {author: .author.login, body: .body}'
  ```
  Last 3 comments may contain scope changes, blocker resolutions, or implementation hints from previous sessions.

- **Check git log** for recent work on this branch:
  ```bash
  git log main..HEAD --oneline --no-decorate | head -10
  ```
  Recent commits reveal what was already implemented.

### 5. Report and begin

Present concisely:
- **Issue** — #N title
- **Progress** — X/Y steps completed
- **Next step** — Step N title with its unchecked checkboxes listed
- **Recent commits** — last 3 commits on branch (if any)
- **Context loaded** — `.docs/architecture.md`, `.docs/quality.md`, last comments

Then **immediately begin working on the next pending step**. Read the step's checkboxes from the issue body and execute them in order. Each checkbox has a tag that determines execution behavior:

| Tag | Action |
|-----|--------|
| `[RED]` | Write the failing test as described in the checkbox |
| `[GREEN]` | Implement code to pass the test |
| `[INFRA]` | Execute infrastructure/config task |
| `[WIRE]` | Connect layers as described |
| `[E2E]` | Write the Playwright E2E test |

Execute tags in order. The RED→GREEN cycle is vertical TDD (one test, one implementation). After completing each checkbox, check it off in `.docs/issues/<N>.md`.

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report number and suggest `gh issue list` → stop |
| No in-progress issues | Inform user, suggest `/start-issue` → stop |
| Branch doesn't match issue | Warn user, offer to checkout correct branch via AUQ |
| Issue has no Steps | "This issue wasn't created with `/start-issue`. Use `/start-issue` to restructure it." → stop |
| `.docs/issues/<N>.md` missing | Fall back to GitHub API, warn user |

## Anti-patterns

- **Recreating tasks without reading the issue.** Tasks must match issue checkbox state exactly — because stale tasks mislead about actual progress and cause duplicate work.
- **Modifying the GitHub issue body directly.** Edit `.docs/issues/<N>.md` locally. Only `/push` syncs checkboxes back to GitHub — because concurrent edits cause last-write-wins data loss.
- **Skipping context loading.** Starting work without reading `.docs/architecture.md`, `.docs/quality.md`, and recent comments — because the agent in a new session has zero context and will produce code that doesn't follow project patterns.
- **Re-doing completed work.** Always check git log for recent commits before starting — because the previous session may have committed work that the issue checkboxes don't yet reflect.

## Next action

When all dev steps are complete (all checkboxes checked):

```
-> Next: run `/review` to start the quality review phase
```

When individual steps are complete:

```
-> Next: continue with Step N+1, or run `/push` to commit progress
```
