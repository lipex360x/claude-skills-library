---
name: start-issue
description: >-
  Pull an issue and start implementation — reads the issue, expands acceptance
  criteria into a detailed step-by-step plan with checkboxes, rewrites the issue,
  creates branch and tasks. Use this skill when the user says "start issue",
  "work on issue #N", "pull from backlog", "start #N", or wants to begin
  implementing an issue — even if they don't explicitly say "issue."
model: opus
effort: high
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - EnterPlanMode
  - ExitPlanMode
  - TaskCreate
  - TaskUpdate
  - WebSearch
  - WebFetch
---

# Start Issue

Turn an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then set up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Pre-flight

<pre_flight>

Inputs: `issue-number` from $ARGUMENTS (optional, positive integer, accepts `#N` or `N`). If absent, AUQ with Backlog/Todo issues from the project board.

Reads: `.docs/architecture.md`, `.docs/project.md`, `.docs/quality.md`, `.claude/project-setup.json`, `.claude/scripts/validate-issue.config.json`, `templates/step-template.md`.

Writes: `.docs/issues/<N>.md` (local issue body), GitHub issue body, project board card, git branch, TaskCreate entries.

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. Working tree is clean → if dirty: warn user about uncommitted changes, suggest stashing.
5. **Read .docs/architecture.md** → if exists, read and store. Primary codebase context (~2k tokens). Do NOT spawn an Explore agent or scan the codebase if it provides sufficient context. Only explore when: (a) it doesn't exist (create it), or (b) the issue touches areas not covered by it. Saves ~50k tokens per invocation.
6. **Read .docs/project.md** → if exists, read and store. Domain context — terms, users, business rules, boundaries. Ensures plan uses correct domain language and respects project constraints.
7. **Read .docs/quality.md** → if exists, read and store. Non-negotiable code quality standards (DOs, DON'Ts, DDD patterns, branching rules). Every checkbox in the plan must comply. If absent, skip.
8. **Check infrastructure gaps** → read `.claude/project-setup.json` for the `dismiss` array. Items in the array have been explicitly declined — skip them. Items NOT in the array are applied by default (no AUQ needed for defaults).
   - **Logging:** scan .docs/architecture.md for `## Observability` section. If absent and `"logging"` is not in `dismiss` → AUQ: suggest adding structured logging. If accepted → include logging setup Step. If declined → add `"logging"` to `dismiss`.
9. **Read validator config** → if `.claude/scripts/validate-issue.config.json` exists, read and store. Key rules to internalize BEFORE writing the plan: `tag_order`, `green_no_consecutive`, `max_checkboxes`, `recommended_checkboxes`, `max_checkbox_chars`. Prevents validation failures after the issue body is written.

</pre_flight>

## Steps

### 1. Select issue

Parse `$ARGUMENTS` for an issue number. Accept both `2` and `#2`.

If no argument, query the project board for issues in **Backlog** and **Todo** columns:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[0].number')
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog" or .status == "Todo")
  | {number: .content.number, title: .content.title, status: .status}
  | "#\(.number) — \(.title) [\(.status)]"
]'
```

Present the list with `AskUserQuestion`. If no board exists, offer to create one via `references/project-board-setup.md`. If the board has no items in Backlog or Todo, inform and stop.

### 2. Analyze the issue

Fetch the issue body:

```bash
gh issue view <number> --json body,title,labels -q '{title: .title, labels: [.labels[].name], body: .body}'
```

Extract: **Title** (branch slug), **What/Why** (context), **Acceptance criteria** (checkboxes to expand).

**Read issue comments for context:**

```bash
gh issue view <number> --json comments --jq '.comments[] | {author: .author.login, body: .body}'
```

Scan comments for: file paths, scope transfers from `/open-pr` or `/close-pr`, partial completion notes, blocker resolutions, implementation hints. Store as **comment insights** to narrow exploration scope.

**Surface actionable items from comments.** Classify each into bug reports, feature requests, infrastructure asks. If actionable items exist, present as AUQ checklist: "Which ones should be included in the plan?" with "None — only the original acceptance criteria" option.

**Codebase context — .docs/architecture.md is the gate.** Pre-flight already loaded it. Do NOT spawn an Explore agent unless: (a) it was missing, (b) the issue touches areas not described in it, (c) comments point to specific files not in it. If it exists and covers the issue scope: **zero exploration needed**.

**Playwright detection (web projects).** Check for `playwright.config.ts`. If found, store project names and baseURL. Check for frontend framework signals (react, vue, svelte, next, etc.).

**Enforce development standards before planning.** Read `references/guidelines.md` for the full set of standards. Key rules to internalize for plan generation:

1. **TDD is mandatory.** Enforce test-first checkboxes in every behavioral Step. Read `references/tdd-methodology.md`.
2. **No workarounds.** Plan must solve problems at root. Hardcoded values, temporary flags, monkey-patches signal the Step is incomplete.
3. **Test isolation for database/stateful projects.** Scan for database signals (docker-compose, ORM configs, migrations/, BaaS references). When true and no existing test isolation exists, plan MUST include a test environment Step.
4. **Linter ignore audit in final Step.** Every plan's last Step must include: `- [ ] [INFRA] Audit linter ignore rules — review knip.json ignores, eslint-disable, noqa; remove if unneeded, justify if required`.
5. **Dev startup/teardown scripts for multi-service projects.** Check for `scripts/dev-start.sh` and `scripts/dev-stop.sh`. When missing and project has infrastructure signals, include a Step to create them.

### 3. Propose the detailed plan

Read `templates/step-template.md` for the expected format.

Transform acceptance criteria into Steps with checkboxes. Each criterion typically expands into 1-3 Steps with 2-8 concrete checkboxes.

**Sizing limits.** 2-8 Steps recommended, 10 warn, 12 hard. 1-8 checkboxes per Step (recommended), 10 hard. Each checkbox max 300 chars — if longer, break into multiple. **Mandatory split:** if plan exceeds 12 steps, split into multiple issues in Backlog.

**Apply Playwright detection from Step 2:**
- **Already configured**: reference existing config for E2E tests. Include `[E2E]` checkboxes for new routes.
- **Web project without Playwright**: include early Step — Configure Playwright. Read `references/playwright-practices.md`.
- **Not a web project**: skip Playwright entirely.

**Apply test isolation detection from Step 2:**
- **`has_database` true, no test setup**: include early Step — Configure test environment (docker-compose.test.yml, .env.test, runtime safety guard, Husky hooks).
- **`has_database` true, setup exists**: verify coverage, include update checkbox if needed.
- **No database**: skip.

**Checkbox tags (mandatory).** Every checkbox MUST have a tag prefix: `` `[TAG]` ``.

| Tag | Purpose | Semantic rule |
|-----|---------|---------------|
| `[RED]` | Write a failing test | Must mention "test" or "spec". No consecutive RED without GREEN |
| `[GREEN]` | Implement to pass the test | Requires RED earlier in the step. No consecutive GREEN without RED |
| `[INFRA]` | Infrastructure/config/tooling | Non-test work |
| `[WIRE]` | Connect layers (frontend ↔ backend) | Must mention integration/connection |
| `[E2E]` | Write Playwright E2E test | Must mention test/spec. Must appear after RED/GREEN pairs |

**Tag ordering:** RED → GREEN → INFRA → WIRE → E2E. RED and GREEN may alternate (vertical TDD: RED→GREEN→RED→GREEN is valid).

**Dependency ordering audit.** Before presenting, review step ordering for inverted dependencies. For each Step: "Can this be fully implemented AND tested using only what previous Steps produced?" Red flags: auth guards to uncreated pages, WIRE to later endpoints, E2E for routes not yet built. Fix by reordering — never paper over with workarounds.

**Present the plan via Plan mode.** Use `EnterPlanMode` and compose the full proposed issue body — **What**, **Why**, **Acceptance criteria** (original), **Steps** (detailed breakdown), **Post-development phases** (standard section). Include a task preview listing Step titles as bullet points.

Use `ExitPlanMode` to submit for user approval. This is the **single and only** approval gate.

- **User approves** — proceed to Step 4 immediately.
- **User requests changes** — adjust, re-enter Plan mode, re-present, repeat until approved.

### 4. Update the issue

Write the approved body to `.docs/issues/<N>.md` first (create `.docs/issues/` if needed). Then publish to GitHub:

```bash
gh issue edit <number> --body "$(cat .docs/issues/<N>.md)" --add-assignee @me
```

**Safety rule:** NEVER use sed/regex on the GitHub issue body. Always edit `.docs/issues/<N>.md` locally and publish the entire file. Git history is the backup — `git restore` or `git show HEAD~1:.docs/issues/<N>.md` recovers any prior state.

If split rule triggered, create additional issues and add to Backlog. Add cross-references and preserve labels.

**Issue structure validation.** If `.claude/scripts/validate-issue.sh` exists, run `bash .claude/scripts/validate-issue.sh <number>`. Fix errors and re-edit until validation passes.

### 5. Create branch linked to issue

```bash
git checkout main && git pull
gh issue develop <number> --name feat/<number>-<slug> --checkout
git push -u origin feat/<number>-<slug>
```

Derive `<slug>` from issue title (kebab-case, max 40 chars).

### 5b. Board transitions and blocker check

Read `references/project-board-operations.md` for the full command reference.

Find the project board. If none exists, offer to create via `references/project-board-setup.md`.

**Validate board structure.** Query Status field options and compare against expected 7 columns (Backlog, Todo, Ready, In Progress, In review, Done, Cancelled). If columns are missing, run the `updateProjectV2Field` mutation from `references/project-board-setup.md` § 2. After updating, re-assign items with null/empty status to "Backlog".

**Check for blockers.** Scan issue body for `> **Blocked by** #N` (bold markdown format). If blocking issue is still open, flag with AUQ.

**Move card to "In Progress"** (plan is already approved at this point — skip "Ready" intermediate state).

Check if Priority and Size are set. If missing, infer from plan (P0/P1/P2 and S/M/L/XL based on step count). Set with `gh project item-edit`.

### 6. Create tasks

Parse Steps from the approved plan. Create a `TaskCreate` for each Step (not each checkbox). Set up `addBlockedBy` dependencies between sequential tasks.

### 7. Report

Present concisely:
- **What was done** — issue analyzed, plan approved, branch created, tasks set up
- **Errors** — issues encountered (or "none")
- **Next step** — "Start working on Step 1"

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report number and suggest `gh issue list` → stop |
| No board exists | Offer to create one via AUQ → proceed or stop |
| Board has no Backlog/Todo items | Inform user → stop |
| Branch already exists | Offer to checkout existing or create new → AUQ |
| `.docs/` directory missing | Create it with warning: "`.docs/` not found — creating it now" |

## Anti-patterns

Read `references/anti-patterns.md` for the full list. Key traps:

- **Generic checkboxes without file paths.** "Add tests" instead of specifying the test file and expected behavior — vague checkboxes produce vague implementations.
- **Spawning Explore when .docs/architecture.md exists.** Explore costs ~50k tokens. .docs/architecture.md has the same context in ~2k tokens. Read it first. Only explore areas it doesn't cover.
- **Horizontal TDD.** Writing all tests first, then all implementations — forbidden. Always vertical: RED→GREEN→RED→GREEN.
- **Workarounds in checkboxes.** Hardcoded values, temporary flags, `any` casts — if it needs a TODO, the step is incomplete.
- **Using sed/regex on GitHub issue body.** Last write wins, regex can corrupt markdown. Always write local `.docs/issues/<N>.md` and publish with `cat`.

## Next action

Begin working on Step 1 of the approved plan. After all steps are complete, run the post-development pipeline: `/review` → `/pw` → `/validate` → `/update-docs` → `/review --final` → `/open-pr`.
