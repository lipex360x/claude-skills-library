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
  - EnterPlanMode
  - ExitPlanMode
---

# Continue Issue

Resume work on an in-progress issue by reconstructing session state from the GitHub issue checkboxes. Tasks are session-scoped and disappear between conversations — this skill rebuilds them so progress tracking stays accurate.

**IMPORTANT:** Read the entire Pre-flight section before taking any action.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `issue-number` | $ARGUMENTS | no | Positive integer (accepts `#N` or `N`) | Auto-detect from current branch name (`feat/<number>-*` or `feature/<number>-*`) |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Task list | TaskCreate | no | One task per Step, status matches issue checkboxes |
| Status report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GitHub issue | `gh issue view` | R | Markdown body |
| ARCHITECTURE.md | project root | R | Markdown |
| quality.md | project root | R | Markdown |
| CLAUDE.md | project root | R | Markdown |
| Issue validator | `.claude/scripts/validate-issue.sh` | R (optional) | Bash script |
| Project setup | `.claude/project-setup.json` | R/W | JSON — `dismiss` section for declined suggestions |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required." — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. **Read ARCHITECTURE.md** → if exists, read and store. Primary codebase context.
5. **Read quality.md** → if exists, read and store. Code quality standards for this project.
6. **Check infrastructure gaps** → read `.claude/project-setup.json` for the `dismiss` array. Items in the array have been explicitly declined — skip them. Items NOT in the array are applied by default.
   - **Logging:** scan ARCHITECTURE.md for `## Observability` section. If absent and `"logging"` is not in `dismiss` → `AskUserQuestion`: suggest adding structured logging. If declined → add `"logging"` to the `dismiss` array in `project-setup.json`.
   - **Tags are mandatory.** Tags are always applied when rewriting the issue body. No AUQ needed — the step template requires tags on every checkbox.
7. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

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

Fetch the issue body:

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

Pre-flight already loaded ARCHITECTURE.md and quality.md. Additionally:

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
- **Context loaded** — ARCHITECTURE.md, quality.md, last comments

Then **immediately begin working on the next pending step**. Read the step's checkboxes from the issue body and execute them in order. Each checkbox has a tag that determines execution behavior:

| Tag | Execution behavior |
|-----|--------------------|
| `[RED]` | Write a failing test — run it, confirm it fails |
| `[GREEN]` | Implement code to make the RED test pass — run it, confirm green |
| `[INFRA]` | Infrastructure/config/tooling — no test cycle needed |
| `[WIRE]` | Connect layers (frontend↔backend) — integration work |
| `[E2E]` | Write Playwright E2E test with screenshots |
| `[PW]` | Run E2E tests **as the user would** (full flow via UI, no programmatic shortcuts). Read `.claude/project-setup.json` for Playwright flags: `headed` (true=`--headed`), `project` (`--project=<value>`), `workers` (`--workers=<value>`). **Also capture browser console** — listen for `console.error` and `page.on('pageerror')` during test runs. Report any browser-only errors (hydration mismatches, runtime exceptions, unhandled rejections). Fix before proceeding |
| `[HUMAN]` | User validates the running app visually. Agent provides a step-by-step testing guide (URLs, credentials, exact actions) and waits for feedback. If changes requested: fix → PW re-verify → HUMAN again until approved |
| `[DOCS]` | Update ARCHITECTURE.md with new directories, files, patterns from this step. **Mandatory** in steps with GREEN or WIRE — non-countable process gate |
| `[LOG]` | Verify error logging coverage — check that error paths in code written this step emit structured logs (backend: logger calls in catch/Err branches; frontend: error boundaries, API error handlers). If `has_logging` is false (no Observability section in ARCHITECTURE.md), flag as a gap. Non-countable process gate |
| `[AUDIT]` | Audit all code written in this step against every rule in quality.md — fix violations |

Process gates (PW, HUMAN, DOCS, LOG, AUDIT) are non-countable — they don't count toward the step's checkbox limit.

Follow the tags in order. The RED→GREEN cycle is vertical TDD (one test, one implementation). The E2E→PW→HUMAN chain is the visual verification gate — where PW is the agent's own validation loop (run → screenshot → fix → re-run) and HUMAN is the user's own validation (agent provides a testing guide with URLs, credentials, and exact steps; user runs the app and reports feedback). After HUMAN approval, DOCS updates ARCHITECTURE.md with any new directories, files, or patterns. AUDIT is always last — no `/push` until the audit passes.

## Post-flight

<post_flight>

After presenting the Report, verify:

1. **Task count matches step count?** — TaskList count equals number of Steps in the issue.
2. **Task statuses match issue checkboxes?** — completed tasks correspond to fully-checked steps, in-progress to partially-checked.
3. **Correct branch checked out?** — `git branch --show-current` matches `feat/<N>-*` or `feature/<N>-*`.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all post-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</post_flight>

## Next action

Continue working through the current step's checkboxes. After completing a PW verify step (Playwright visual verification), provide the user a step-by-step testing guide (URLs, test credentials from `TEST_USERS.md` or seed data, exact click paths) and wait for their feedback. The user runs the app themselves — the agent does not present screenshots. If the user requests changes: fix → PW re-verify → provide updated guide → repeat until approved. Only after user approval, execute `[DOCS]` — update ARCHITECTURE.md with any new directories, files, patterns, or infrastructure added during this step. Then proceed to `[LOG]` — verify that error paths in this step's code emit structured logs. Then `[AUDIT]` — audit all code written in the step against `quality.md`, check every file against every DON'T and DO rule, fix violations before committing. The process gate chain is: HUMAN → DOCS → LOG → AUDIT → `/push`. This sequence is mandatory and cannot be skipped. Then use `/push` to commit, push, and update the issue checkboxes.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, repo valid
2. **Issue found?** — issue number resolved (from args, branch, or board)
3. **Steps parsed correctly?** — step count matches issue body
4. **Next step validated?** — `validate-issue.sh --step N` passed (no errors)
5. **Task board reconstructed?** — tasks created with correct statuses
6. **Context loaded?** — ARCHITECTURE.md, quality.md, recent comments, git log

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate content, it reconstructs session state."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report number and suggest `gh issue list` → stop |
| No in-progress issues | Inform user, suggest `/start-issue` → stop |
| Branch doesn't match issue | Warn user, offer to checkout correct branch via AUQ |
| Issue has no Steps | "This issue wasn't created with `/start-issue`. Use `/start-issue` to restructure it." → stop |

## Anti-patterns

- **Recreating tasks without reading the issue.** Tasks must match issue checkbox state exactly — because stale tasks mislead about actual progress and cause duplicate work.
- **Modifying the issue body.** This skill is read-only on the issue. Only `/push` and `/close-pr` update issue checkboxes — because concurrent edits cause last-write-wins data loss.
- **Skipping context loading.** Starting work without reading ARCHITECTURE.md, quality.md, and recent comments — because the agent in a new session has zero context and will produce code that doesn't follow project patterns.
- **Re-doing completed work.** Always check git log for recent commits before starting — because the previous session may have committed work that the issue checkboxes don't yet reflect.

## Guidelines

- **Session state lives in the issue, not in tasks.** Tasks are ephemeral (session-scoped). The issue body is the source of truth for progress. This skill bridges the gap by reconstructing tasks from the issue.
- **Automatic detection over manual input.** Branch name → issue number is the happy path. Only ask when detection fails — because the user ran this skill to resume quickly, not to answer questions.
- **Start working immediately.** After the status report, begin the next step. Don't wait for confirmation — because the user ran `/continue-issue` to work, not to review a status board.
- **Respect the plan.** Follow the issue's checkboxes in order. Don't skip ahead, reorder, or add unplanned work — because the plan was approved in `/start-issue` and changes require explicit scope negotiation.
