---
name: start-issue
description: >-
  Pull an issue and start implementation — reads the issue, expands acceptance
  criteria into a detailed step-by-step plan with checkboxes, rewrites the issue,
  creates branch and tasks. Use this skill when the user says "start issue",
  "work on issue #N", "pull from backlog", "start #N", or wants to begin
  implementing an issue — even if they don't explicitly say "issue."
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
  - TeamCreate
  - WebSearch
  - WebFetch
---

# Start Issue

Turn an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then set up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `issue-number` | $ARGUMENTS | no | Positive integer (accepts `#N` or `N`) | AUQ with Backlog/Todo issues from project board |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Rewritten issue body | GitHub API | yes | Markdown with Steps + checkboxes |
| Feature branch | git | yes | `feat/<number>-<slug>` |
| Board card update | GitHub Projects | yes | Status → In Progress |
| Task list | TaskCreate | no | One task per Step |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GitHub issue | `gh issue view` | R/W | Markdown body |
| Project board | GitHub Projects API | R/W | GraphQL |
| ARCHITECTURE.md | project root | R/W | Markdown |
| quality.md | project root | R | Markdown |
| Step template | `templates/step-template.md` | R | Markdown |
| Board operations | `references/project-board-operations.md` | R | Markdown |
| Board setup | `references/project-board-setup.md` | R | Markdown |
| Playwright practices | `references/playwright-practices.md` | R | Markdown |
| Dev guidelines | `references/development-guidelines.md` | R | Markdown |
| TDD methodology | `references/tdd-methodology.md` | R | Markdown |
| Execution strategy | `references/execution-strategy.md` | R | Markdown |
| Project setup | `.claude/project-setup.json` | R/W | JSON — `dismiss` section for declined suggestions |
| Validator config | `.claude/scripts/validate-issue.config.json` | R | JSON — tag rules, checkbox limits, UI patterns |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. Working tree is clean → if dirty: warn user about uncommitted changes, suggest stashing.
5. **Read ARCHITECTURE.md** → if `./ARCHITECTURE.md` exists, read it NOW and store the content. This is the primary codebase context (~2k tokens). Do NOT spawn an Explore agent or scan the codebase if ARCHITECTURE.md provides sufficient context. Only explore when: (a) ARCHITECTURE.md doesn't exist (create it), or (b) the issue touches areas not covered by it. This check saves ~50k tokens per invocation.
6. **Read quality.md** → if `./quality.md` exists, read it NOW and store the content. This file contains non-negotiable code quality standards (DOs, DON'Ts, DDD patterns, branching rules). Every checkbox in the plan must comply with these standards. If quality.md doesn't exist, skip — but if it does, it is mandatory context for planning.
7. **Check infrastructure gaps** → read `.claude/project-setup.json` for the `dismiss` array. Items in the array have been explicitly declined — skip them. Items NOT in the array are applied by default (no AUQ needed for defaults).
   - **Logging:** scan ARCHITECTURE.md for `## Observability` section. If absent and `"logging"` is not in `dismiss` → `AskUserQuestion`: suggest adding structured logging (explain: silent failures, errors only visible in browser DevTools). If accepted → include logging setup Step in the plan. If declined → add `"logging"` to the `dismiss` array in `project-setup.json`.
   - **Tags are mandatory.** Tags are always applied when rewriting the issue body (Step 3). No AUQ needed — the step template requires tags on every checkbox. The `[LOG]` process gate verifies error logging coverage in every step.
   - **Delegation:** check `project-setup.json` for `delegate-mechanical`. If absent → `AskUserQuestion`: "Usar delegação para sub-agentes? (RED/GREEN mecânicos delegados, manager faz review + quality gates)". If accepted → set `"delegate-mechanical": true` in `project-setup.json`. If declined → set `"delegate-mechanical": false`. When `true`, Step 3 (plan writing) adds `[SPAWN]` to qualifying steps (2+ RED/GREEN cycles or 3+ mechanical checkboxes).
8. **Read validator config** → if `.claude/scripts/validate-issue.config.json` exists, read it NOW and store the rules. This file contains tag chain rules, checkbox limits, UI pattern detection, and TDD ordering constraints. Knowing these rules BEFORE writing the plan (Step 3) prevents validation failures after the issue body is written. Key rules to internalize: `tag_order`, `green_no_consecutive` (no consecutive GREEN without RED), `ui_chain` patterns (words containing "ui" as substring trigger E2E/PW/HUMAN requirement), `max_checkboxes`, `recommended_checkboxes`, and `count_excluded_tags`. If the file doesn't exist, skip — not all projects use the validator.
9. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Select issue

Parse `$ARGUMENTS` for an issue number. Accept both direct numbers (`2`) and index references (`#2`).

If no argument provided, query the project board for issues in the **Backlog** and **Todo** columns:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[0].number')
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog" or .status == "Todo")
  | {number: .content.number, title: .content.title, status: .status}
  | "#\(.number) — \(.title) [\(.status)]"
]'
```

Present the list with `AskUserQuestion` for the user to pick one.

If no board exists, prompt the user with `AskUserQuestion` offering `["Yes, create a board", "No, cancel"]`. If they choose to create one, read `references/project-board-setup.md` and set up the full board (7 status columns, Priority and Size fields). If they cancel, stop — board tracking is required for all workflow skills.

If the board has no items in Backlog or Todo, inform the user and stop.

### 2. Analyze the issue

Fetch the issue body:

```bash
gh issue view <number> --json body,title,labels -q '{title: .title, labels: [.labels[].name], body: .body}'
```

Extract: **Title** (branch slug), **What/Why** (context), **Acceptance criteria** (checkboxes to expand).

**Read issue comments for context.** Fetch comments before analyzing the codebase:

```bash
gh issue view <number> --json comments --jq '.comments[] | {author: .author.login, body: .body}'
```

Scan comments for: file paths, scope transfers from `/open-pr` or `/close-pr`, partial completion notes, blocker resolutions, implementation hints. Store as **comment insights** to narrow exploration scope.

**Surface actionable items from comments.** After reading all comments, classify each into:
- **Bug reports** — issues found during previous phases (e.g., hydration errors, broken layouts)
- **Feature requests** — new functionality suggested for this phase (e.g., UX improvements, new tools)
- **Infrastructure asks** — logging, monitoring, tooling requests

If actionable items exist, present them as an `AskUserQuestion` checklist: "These items were mentioned in the issue comments. Which ones should be included in the plan?" with options listing each item and a "None — only the original acceptance criteria" option. Only items the user selects get added to the plan. This prevents both silently ignoring comments and silently adding scope.

**Codebase context — ARCHITECTURE.md is the gate.** Pre-flight already loaded ARCHITECTURE.md. Use it as the primary source. Do NOT spawn an Explore agent unless:
- ARCHITECTURE.md was missing (create it after exploring)
- The issue touches areas not described in ARCHITECTURE.md (explore only those areas, not the full codebase)
- Comments point to specific files not in ARCHITECTURE.md (read those files directly, not via Explore)

If ARCHITECTURE.md exists and covers the issue scope: **zero exploration needed**. Read specific files mentioned in comments or ARCHITECTURE.md directly with the Read tool. An Explore agent costs ~50k tokens — never spawn one when a few targeted reads suffice.

**Playwright detection (for web projects).** Check:
1. **Playwright already configured?** Look for `playwright.config.ts` at the project root. If found, store the project names and baseURL for verification checkboxes.
2. **Web project with frontend?** Check for frontend framework signals (react, vue, svelte, next, etc.). Store the result for Step 3.

### 2b. Determine execution strategy

Run `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to check if Agent Teams is enabled (value `1`). If not enabled, strategy is always **Sequential** — skip the rest of this step.

If enabled, read `references/execution-strategy.md` for the full decision matrix. After building the plan in Step 3 (but before presenting), classify each step as sequential or parallelizable, then evaluate:

1. **Are parallelizable steps present?** → if no: **Sequential**
2. **Is the work templated?** (same pattern repeated on independent targets, no shared state, no feedback needed) → if yes: **Agent**
3. **Do parallel steps share state or need coordination?** (same files, exchanging data, iterative feedback) → if yes: **Teammate**
4. **Default** for parallelizable steps without clear signals → **Agent** (simpler, cheaper)

Store the chosen strategy — it determines the "Execution strategy" section in Step 3 and the spawn behavior in Step 7.

### 2c. Enforce development standards

Before proposing any plan, verify non-negotiable standards. If any are missing, the plan must compensate:

1. **TDD is mandatory.** Scan for TDD references. If absent, enforce test-first checkboxes in every behavioral Step. Read `references/tdd-methodology.md`.
2. **No workarounds.** The plan must solve problems at root. Hardcoded values, temporary flags, monkey-patches signal the Step is incomplete.
3. **No unnecessary code comments.** Only allowed for genuinely non-obvious logic. Never include "add comments" checkboxes.
4. **Test isolation is mandatory for database/stateful projects.** Scan the codebase for database signals: `docker-compose*`, `.env*`, `prisma/`, `drizzle/`, `migrations/`, ORM config files (knex, sequelize, typeorm), BaaS references (supabase, firebase, neon, planetscale). Also check ARCHITECTURE.md for database mentions. Store the result as `has_database` flag. When true and no existing test isolation setup is found (`docker-compose.test.yml`, `.env.test`), the plan MUST include a test environment configuration Step as a prerequisite. Read `references/development-guidelines.md` § 1 for the full isolation requirements (env separation, runtime safety guard, high ports, teardown).
5. **Linter ignore audit is mandatory in the final Step.** Every plan's last verification/consolidation Step must include a checkbox: `- [ ] Audit linter ignore rules — review knip.json ignores, eslint-disable, noqa; remove if no longer needed, add justification comment if still required`. Suppression rules added during development tend to accumulate and become permanent workarounds. This checkpoint forces a cleanup pass before release.
6. **Dev startup/teardown scripts are mandatory for multi-service projects.** Check if `scripts/dev-start.sh` and `scripts/dev-stop.sh` exist. When the project has infrastructure signals (docker-compose, multiple services, database) but these scripts are missing, the plan MUST include a Step to create them. Analyze the project's infrastructure to determine what the scripts need to orchestrate — this is project-specific, not templated. The startup script must: (1) validate prerequisites, (2) clean ports, (3) bring up infrastructure, (4) run migrations, (5) seed data, (6) create test user, (7) start services, (8) **validate everything works** — port checks, health endpoints, DB reachability, seed data presence, test user login. The validation must also be runnable standalone via `--check` flag. The teardown script kills services and stops infrastructure, with `--keep-db` flag. After creation, add `## Scripts` section to ARCHITECTURE.md. Works for monorepo and multi-repo — adapt to the project's actual structure (Docker, Supabase CLI, virtualenvs, npm workspaces, etc.).

### 3. Propose the detailed plan

Read `templates/step-template.md` for the expected format.

Transform acceptance criteria into Steps with checkboxes. Each criterion typically expands into 1-3 Steps with 2-6 concrete checkboxes.

**Apply Playwright detection result from Step 2:**
- **Playwright already configured**: reference existing config for E2E verification checkboxes. If new routes, include checkbox to add E2E tests with screenshots.
- **Web project without Playwright**: include an early Step — Configure Playwright. Read `references/playwright-practices.md` for setup (config, page objects, test helpers, global setup/teardown).
- **Not a web project**: skip Playwright entirely.

**Apply test isolation detection from Step 2c:**
- **`has_database` is true and no test setup exists**: include an early Step — "Configure test environment" with checkboxes for: (1) create `docker-compose.test.yml` with isolated DB on high port, (2) create `.env.test` with local container URLs, (3) add runtime safety guard in global test setup, (4) configure test runner to load `.env.test`, (5) add `beforeAll`/`afterAll` for migrate/teardown, (6) configure Husky with `pre-commit` hook running lint + type-check and `pre-push` hook running tests + build — ensures CI-breaking code never reaches remote.
- **`has_database` is true but test setup exists**: verify the existing setup covers new changes. Include a checkbox to update if needed.
- **No database signals**: skip test isolation entirely.

**Sizing and validator rules.** 2-8 Steps total. 2-6 checkboxes per Step (recommended), max 8 (hard limit). Each checkbox = one focused action, max 200 chars — if longer, break into multiple checkboxes (never shorten to lose context).

**Checkbox tags (mandatory).** Every checkbox MUST have a tag prefix in backtick format: `` `[TAG]` ``. Valid tags and their rules:

| Tag | Purpose | Semantic rule |
|-----|---------|---------------|
| `[SPAWN]` | Delegate mechanical work to sub-agent — scope description + non-derivable hints (max 400 chars) | Non-countable. Must be first tag in step. Requires REVIEW in same step. Only add when step has 2+ RED/GREEN cycles or 3+ mechanical checkboxes |
| `[RED]` | Write a failing test | Must mention "test" or "spec". No consecutive RED without GREEN between them |
| `[GREEN]` | Implement to pass the test | Requires RED earlier in the step. Must not mention writing tests |
| `[INFRA]` | Infrastructure/config/tooling | Must not mention writing tests |
| `[WIRE]` | Connect layers (frontend↔backend) | Must mention integration/connection |
| `[E2E]` | Write Playwright E2E test | Must mention test/spec. Requires PW in same step |
| `[REVIEW]` | Manager reviews sub-agent output — validates code quality, fixes issues, updates issue checkboxes for completed mechanical work | Non-countable process gate. Recommended when step has GREEN or WIRE. Position: after mechanical work, before PW |
| `[PW]` | Run E2E **as the user would** (full flow via UI, no programmatic auth shortcuts). Read `.claude/project-setup.json` for flags: `headed`, `project`. **Also capture browser console** — listen for `console.error` and `page.on('pageerror')` during test runs. Report any browser-only errors (hydration mismatches, runtime exceptions, unhandled rejections) that don't appear in application logs. Fix before proceeding | Must mention screenshots/verification. Requires HUMAN in same step |
| `[HUMAN]` | User validates the running app visually — agent provides testing guide and waits | Must mention iterate/feedback. Requires PW in same step. Agent gives step-by-step guide (URLs, credentials, actions); user runs the app and reports feedback. If changes: fix → PW re-verify → HUMAN again until approved |
| `[DOCS]` | Update ARCHITECTURE.md | **Mandatory** when step has GREEN or WIRE. Non-countable process gate |
| `[LOG]` | Verify error logging coverage — check that error paths in code written this step emit structured logs (backend: logger calls in catch/Err branches; frontend: error boundaries, API error handlers). If `has_logging` is false (no Observability section in ARCHITECTURE.md), flag as a gap and recommend adding logging infrastructure | Non-countable process gate. Position: after DOCS, before AUDIT |
| `[AUDIT]` | Audit against quality.md | Mandatory in every step, must be the last checkbox |

Process gates (SPAWN, REVIEW, PW, HUMAN, DOCS, LOG, AUDIT) are non-countable — they don't count toward the step's checkbox limit.

**Tag ordering:** SPAWN → RED → GREEN → INFRA → WIRE → E2E → REVIEW → PW → HUMAN → DOCS → LOG → AUDIT. Tags must appear in this sequence within each step. RED and GREEN may alternate (vertical TDD: RED→GREEN→RED→GREEN is valid).

**Delegation via [SPAWN].** Check `.claude/project-setup.json` for `delegate-mechanical`. When `true`, add `[SPAWN]` to steps that qualify: 2+ RED/GREEN cycles or 3+ mechanical checkboxes. SPAWN text (max 400 chars) describes what to delegate and includes hints the manager can't derive from ARCHITECTURE.md or quality.md (e.g., "mock HTTP — TEI not running in tests", "use httpx async client"). Steps without SPAWN are executed directly by the manager. Every SPAWN requires a matching REVIEW gate.

**UI chain:** Any step with frontend UI work (components, layouts, pages) MUST include the full chain: E2E → PW → HUMAN.

**ARCHITECTURE.md maintenance via [DOCS].** Steps with GREEN or WIRE must include a `[DOCS]` checkbox to update ARCHITECTURE.md with any new directories, files, patterns, or infrastructure introduced in that Step. Position it after HUMAN (if present) and before AUDIT. This keeps the architecture doc current as the project grows and prevents future sessions from wasting tokens on codebase exploration.

**Human visual validation.** For any Step that includes a PW verify checkbox (Playwright visual verification), add a subsequent checkbox: `- [ ] Human validation — user tests the running app and provides feedback`. The agent provides a step-by-step testing guide (URLs, credentials, actions); the user validates by interacting with the live app.

**Mandatory quality.md audit.** Every Step must include a `quality.md` audit as its final action before `/push`. The agent must review all code written in the step against every rule in `quality.md`, fix violations, then commit. This audit cannot be skipped.

**Mandatory split rule.** If plan has **more than 8 steps**, split into multiple smaller issues — all added to Backlog. Each issue independently completable with 3-8 steps.

If Agent Teams is enabled, add an **Execution strategy** section at the top of the issue body (before What/Why) based on the strategy chosen in Step 2b. Read `references/execution-strategy.md` for the strategy templates (Agent, Teammate, Sequential). Also add inline reminders in parallelizable steps. Read `references/guidelines.md` § "Verification is part of the plan" and § "Checkbox ownership with Agent Teams" for the verification matrix and ownership rules.

### 3b. Dependency ordering audit

Before presenting the plan, review the step ordering for **inverted dependencies** — cases where Step N requires something only produced by Step M (M > N). This is an LLM reasoning step, not a static check.

**For each Step, answer:** "Can this Step be fully implemented AND tested end-to-end without workarounds, using only what previous Steps produced?"

**Red flags that signal inverted dependencies:**
- A Step has an auth guard or redirect to a page that hasn't been created yet
- A Step connects frontend to a backend endpoint (`[WIRE]`) that's defined in a later Step
- A Step writes E2E tests (`[E2E]`) that navigate to routes built in a later Step
- A Step references components, hooks, or utilities created in a later Step
- **The workaround test:** if testing a Step would require injecting state programmatically (mock auth, seed data for entities not yet created, stub API responses for endpoints not yet built), the dependency is inverted. Real users go through the UI — tests should follow the same path

**If violations are found:**
1. Reorder the steps to resolve the dependency (move the producer before the consumer)
2. If reordering breaks other dependencies, flag the conflict and present options to the user
3. Never paper over a dependency with a workaround (programmatic auth injection, mock stubs for real pages) — fix the ordering instead

**Example:** If Step 7 builds a chat page with an auth guard that redirects to `/login`, but Step 6 creates the login page — this works. If the order were reversed (chat before login), E2E tests for chat would need programmatic auth injection — that's the red flag. Reorder so login comes first.

**Present the plan via Plan mode.** Use `EnterPlanMode` and compose the full proposed issue body as the plan content — with **What**, **Why**, **Acceptance criteria** (original), **Steps** (new detailed breakdown). Include a task preview listing Step titles as bullet points at the end. Plan mode keeps the plan out of the main context window and provides a structured approval UI.

Use `ExitPlanMode` to submit the plan for user approval. This is the **single and only** approval gate.

- **User approves** — proceed immediately to Step 4. No additional confirmation.
- **User requests changes** — apply adjustments, re-enter Plan mode, re-present, repeat until approved.

### 4. Update the issue

After approval, **snapshot the current body before overwriting** — if `.claude/scripts/issue-backup.sh` exists, run `bash .claude/scripts/issue-backup.sh snapshot <number>` first. This is a safety net: the hook should catch `gh issue edit` automatically, but an explicit snapshot before a full body rewrite provides defense in depth.

Then rewrite the issue body and assign:

```bash
gh issue edit <number> --body "<approved body>" --add-assignee @me
```

If split rule triggered, create additional issues and add to Backlog. Add cross-references and preserve labels.

**Issue structure validation.** After writing the issue body, if `.claude/scripts/validate-issue.sh` exists in the project, run `bash .claude/scripts/validate-issue.sh <number>`. Fix any errors and re-edit the issue until validation passes. The plan must pass before work begins.

### 5. Create branch linked to issue

```bash
git checkout main && git pull
gh issue develop <number> --name feat/<number>-<slug> --checkout
git push -u origin feat/<number>-<slug>
```

Derive `<slug>` from issue title (kebab-case, max 40 chars).

### 5b. Board transitions and blocker check

Read `references/project-board-operations.md` for the full command reference.

Find the project board. If no board exists, offer to create one via `references/project-board-setup.md`.

**Validate board structure.** After finding the board, query the Status field options and compare against the expected 7 columns (Backlog, Todo, Ready, In Progress, In review, Done, Cancelled). If columns are missing (common when the board was created via GitHub UI with only 3 defaults), run the `updateProjectV2Field` mutation from `references/project-board-setup.md` § 2 to replace with the full 7. After updating, query items with null/empty status and re-assign them to "Backlog" — items in deleted columns lose their status silently.

**Check for blockers.** Scan issue body for `> Blocked by #N`. If blocking issue is still open, flag with AUQ.

**Move card to "Ready"** → then after plan approval, **move to "In Progress"**.

Check if Priority and Size are set. If missing, infer from plan (P0/P1/P2 and S/M/L/XL based on step count). Set with `gh project item-edit`.

### 6. Create tasks

Parse Steps from the approved plan. Create a `TaskCreate` for each Step (not each checkbox). Set up `addBlockedBy` dependencies between sequential tasks.

### 7. Spawn workers (automatic when Execution strategy is present)

If the approved issue body contains an "Execution strategy" section, spawn workers immediately — no second approval. The strategy determines the spawn mechanism:

**Agent strategy:**
- Use `Agent` tool with `run_in_background: true` for each batch
- Each agent receives full instructions in its prompt (golden example + target list)
- No `TeamCreate`, no internal tasks — agents return results and die
- Lead collects results via completion notifications, validates, marks issue checkboxes
- GitHub issue checkboxes are the **sole tracker** — no local task board duplication

**Teammate strategy:**
- Use `TeamCreate` + `Agent` with `team_name` for coordinated workers
- Each teammate receives the standardized prompt pattern pointing to the issue
- Teammates must have explicit tool access: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Agent`, `TaskCreate`, `TaskUpdate` at minimum
- **Checkbox ownership:** teammates track progress via internal tasks. Lead monitors via `TaskList`, verifies output, then marks issue checkboxes. This prevents race conditions
- **Shutdown protocol** required when teammates complete their batch

**Sequential strategy:** Skip this step — lead executes directly.

**Progressive audit (both strategies).** Do NOT wait for all workers to finish before auditing. As each worker reports completion, immediately spawn a background audit agent to verify that worker's output against the verification matrix. This overlaps audit work with remaining agent execution, significantly reducing total wall-clock time. The consolidation step (final Step) collects all audit results — by then, most or all audits are already done.

Example timeline with 4 agents:
1. Agent 3 finishes → spawn audit-agent-3 in background
2. Agent 1 finishes → spawn audit-agent-1 in background (audit-3 still running)
3. Audit-agent-3 completes → results stored
4. Agent 2 finishes → spawn audit-agent-2 in background
5. Audit-agent-1 completes → results stored
6. Agent 4 finishes → spawn audit-agent-4 in background
7. ... consolidation step: most audits already done, minimal wait

### 8. Report

Present concisely:
- **What was done** — issue analyzed, plan approved, branch created, tasks set up
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered (or "none")
- **Next step** — "Start working on Step 1" or teammate status if Agent Teams active

## Post-flight

<post_flight>

After presenting the Report, verify external state:

1. **Issue body matches approved plan?** — fetch `gh issue view <N> --json body` and verify the Steps/checkboxes match the approved text. Issue update can fail silently.
2. **Branch exists on remote?** — `git ls-remote origin feat/<N>-<slug>` must return a commit hash.
3. **Board card in "In Progress"?** — query `gh project item-list <PROJECT> --owner "@me" --format json | jq '.items[] | select(.content.number == <N>) | .status'` — must equal `"In Progress"`.
4. **Tasks match Step count?** — verify TaskList count matches the number of Steps in the approved plan.
5. **If Agent Teams spawned:** verify Agent output or TeamCreate exists in conversation. If issue body has "Execution strategy" but no agents ran, flag it.

If any check fails, report the specific failure and the fix command.
6. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all post-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</post_flight>

## Next action

Begin working on Step 1 of the approved plan. If Agent Teams is active, teammates are already executing.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, repo valid, working tree clean
2. **Steps completed?** — issue rewritten, branch created, board updated, tasks created
3. **Output exists?** — issue body updated on GitHub, branch pushed, card in "In Progress"
4. **Anti-patterns clean?** — no generic checkboxes, TDD order enforced, no local paths in issue
5. **Approval gate honored?** — user explicitly approved the plan before execution

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Checkboxes concrete?** — every checkbox has file paths or specific actions, no vague "implement X"
2. **TDD order correct?** — test checkbox before implementation in every behavioral Step, using `RED:` and `GREEN:` labels (see `templates/step-template.md` § Checkboxes)
3. **Plan structure matches template?** — What/Why/Acceptance criteria/Steps format
4. **Split rule respected?** — if 8+ steps, plan was split into multiple issues
5. **quality.md compliance?** — if quality.md was loaded in pre-flight, scan every proposed checkbox against its DON'Ts. Flag any checkbox that would produce code violating a DON'T (e.g., a checkbox suggesting raw primitives instead of value objects, horizontal TDD, nested if/else, magic numbers, workarounds). The plan must not instruct what quality.md forbids.
6. **Linter ignore audit present?** — the final verification Step includes a checkbox to audit linter suppression rules (knip ignores, eslint-disable, noqa). If missing, add it before presenting the plan.
7. **Dependency ordering valid?** — every Step is testable end-to-end using only what previous Steps produced. No Step requires workarounds (mock auth, stub APIs) to compensate for pages/routes/endpoints created in later Steps. If a Step needs programmatic state injection to be testable, the dependency is inverted — reorder before presenting.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report number and suggest `gh issue list` → stop |
| No board exists | Offer to create one via AUQ → proceed or stop |
| Board has no Backlog/Todo items | Inform user → stop |
| Branch already exists | Offer to checkout existing or create new → AUQ |
| Agent Teams check fails | Default to sequential execution (no Execution strategy section) |

## Anti-patterns

Read `references/anti-patterns.md` for the full list (13 items). Key traps:

- **Generic checkboxes without file paths.** "Add tests" instead of specifying the test file and expected behavior — because vague checkboxes produce vague implementations.
- **Spawning Explore when ARCHITECTURE.md exists.** An Explore agent costs ~50k tokens. ARCHITECTURE.md has the same context in ~2k tokens — because it's updated by `/close-pr` after every merge. Read it first. Only explore areas it doesn't cover.
- **Skipping Agent Teams check.** Proposing a plan without checking the env var first — because if enabled, the Execution mode section is mandatory.
- **Multiple agents editing the same issue body.** Last write wins, earlier edits silently lost — because GitHub's issue API has no merge.

## Guidelines

Read `references/guidelines.md` for the full list (20 items). Key principles:

- **TDD is mandatory, not optional.** Every Step with new behavior MUST include test checkbox before implementation — because the TDD-ordered checkboxes ARE the enforcement mechanism.
- **Codebase-aware plans.** Always read the codebase before planning — because generic checkboxes like "implement the feature" are a failure mode.
- **Steps are work sessions.** Each Step = focused work session you can complete, commit, and verify — because too large loses focus, too small adds overhead.
