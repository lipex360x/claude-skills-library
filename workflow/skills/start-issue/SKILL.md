---
name: start-issue
description: Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks. Use this skill when the user says "start issue", "work on issue #N", "pull from backlog", "start #N", or wants to begin implementing an issue — even if they don't explicitly say "issue."
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
  - TaskCreate
  - TaskUpdate
  - TeamCreate
  - WebSearch
  - WebFetch
---

# Start Issue

Turn an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then set up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

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

Extract:
- **Title** — will become the branch slug
- **What/Why** — context for planning
- **Acceptance criteria** — the high-level checkboxes to expand into detailed steps

Also analyze the **current codebase** to inform the plan. **Start by checking for `ARCHITECTURE.md` at the project root.** If it exists, read it first — it contains stack, layers, patterns, schema, auth model, and routes, eliminating the need for expensive exploration (~2k tokens vs ~53k). Only spawn an exploration agent if ARCHITECTURE.md is missing, incomplete, or appears stale (e.g., routes in the file don't match `src/app/` directory).

**If ARCHITECTURE.md doesn't exist, create it.** This is the first issue being worked on — the codebase has no knowledge cache yet. Explore the codebase (read package.json, directory structure, key config files, existing routes/schema), then generate `ARCHITECTURE.md` at the project root using the same structure as `start-new-project` (stack, layers, patterns by canonical example, schema summary, auth model, routes). This file is the **living context document** — `/close-pr` will update it after each merge, and every subsequent `/start-backlog` will read it first. Creating it now pays for itself immediately: the plan you're about to write will be more concrete, and every future session starts with context instead of re-exploration.

If ARCHITECTURE.md already exists but is stale, update it with what you discover during exploration — don't leave known-incorrect information in the file.

This context is essential for writing concrete checkboxes with file paths.

**CDP detection (for web projects).** Check two things:

1. **CDP already configured?** Look for `.claude/project-settings.json`. If it exists and has a `chrome.cdp` field, CDP is ready — store the `pages` map for use in verification checkboxes.

2. **Web project with frontend?** If CDP is not configured, determine if this is a web project with a frontend layer. Check for signals: `package.json` with frontend frameworks (react, vue, svelte, next, nuxt, remix, astro, angular, solid), HTML template files, a `pages/` or `app/` directory with UI components, or a dev server config (vite, webpack, next.config). Store the result — you **MUST** use it in Step 3 to decide whether to include CDP setup.

### 2b. Check Agent Teams capability

Run `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to determine if Agent Teams is enabled (value `1`). Store the result — you **MUST** use it in Step 3 to decide whether to include the parallel execution plan. This check is not optional.

### 2c. Enforce development standards

Before proposing any plan, verify that the issue and project setup enforce these non-negotiable standards. If any are missing or weak, the plan **must** compensate by making them explicit in every relevant Step:

1. **TDD is mandatory.** Scan the issue body for TDD references (test-first checkboxes, red-green-refactor mentions, references to `tdd-methodology.md`). If TDD is not explicitly enforced — either because `/start-new-project` didn't make it clear or because this is a standalone backlog item — **you must enforce it yourself**. Every Step that introduces behavior gets test-first checkboxes. This is not a suggestion to consider; it's a structural requirement of the plan. Read `references/tdd-methodology.md` for the full methodology.

2. **No workarounds.** The plan must solve problems at their root. If a Step would require a workaround (hardcoded values to bypass a bug, temporary flags, monkey-patches, `any` casts to silence type errors, skipped validations), it's a signal that the Step is wrong or incomplete. Rewrite it to address the underlying issue. Workarounds create invisible tech debt that compounds across issues — what starts as "just for now" becomes permanent the moment the next issue lands on top of it.

3. **No unnecessary code comments.** Code comments are allowed only when the logic is genuinely non-obvious — complex algorithms, unintuitive business rules, or regulatory constraints that aren't self-evident from the code. Self-documenting code (clear names, small functions, explicit types) replaces comments. Never add comments that restate what the code does ("// increment counter"), explain obvious patterns ("// check if user exists"), or serve as section dividers. When proposing checkboxes, never include "add comments" or "document the code" — if the code needs a comment to be understood, the code needs to be rewritten.

If any of these standards conflict with the original issue's approach, flag it to the user and propose the correction. Don't silently ignore a weak issue setup.

### 3. Propose the detailed plan

Read `templates/step-template.md` for the expected format.

Transform the high-level acceptance criteria into a detailed plan with **Steps** and checkboxes. Each acceptance criterion typically expands into 1-3 Steps, each with 2-6 concrete checkboxes.

**Apply CDP detection result from Step 2:**

- **CDP already configured** (`.claude/project-settings.json` exists): use the `pages` map to write verification checkboxes with the pattern "Navigate to [page] via CDP and take screenshot to verify [expected state]". No setup Step needed — but if this issue introduces new routes, include a checkbox to update the `pages` map in `project-settings.json`.
- **Web project without CDP**: include a **Step 1 — Configure CDP for visual verification** before all other steps. Checkboxes:
  - `Create .claude/start-chrome.sh` from the start-new-project skill template (cross-platform Chrome launcher with `--remote-debugging-port=9222`)
  - `Create .claude/project-settings.json` with `baseUrl` pointing to the dev server, `testPort` for the dedicated test server port, `tabs` with the app URL, and `pages` mapping all known routes. This file is a living document — whenever a Step creates new routes or pages, include a checkbox to update the `pages` map
  - `Verify CDP connection — run .claude/start-chrome.sh and confirm Playwright can connect via connectOverCDP`
  - Subsequent Steps should use CDP verification checkboxes for any UI-facing changes.
- **Not a web project**: skip CDP entirely.

Present the full proposed issue body in a fenced code block. The structure:

- **What** — keep the original description (or improve it slightly)
- **Why** — keep the original motivation
- **Acceptance criteria** — keep original checkboxes as-is (these are the success criteria)
- **Steps** — the new detailed breakdown:
  - Numbered Steps with concise titles
  - Each Step has checkboxes with specific, verifiable actions
  - Include file paths when the codebase structure is known
  - Include verification checkboxes where steps have observable output

Sizing guidelines:
- 2-8 Steps total (depending on issue complexity)
- 2-6 checkboxes per Step (TDD steps naturally have more checkboxes — test + implementation pairs)
- Each checkbox = one focused action completable in a single work session

**Mandatory split rule for backlog issues.** After drafting the plan, count the total steps. If the plan has **more than 8 steps**, it **MUST** be split into multiple smaller issues — all added to the project board in the "Backlog" column. Backlog issues don't use Phases (they're standalone items, not parts of a larger project plan). Instead, split by logical grouping: each resulting issue should be independently completable with 3-8 steps and its own verification. Title each issue descriptively (no "Phase N" prefix). Create them sequentially, referencing related issues in the body (e.g., "Related: #12, #13"). The original issue becomes the first chunk (rewritten with its subset of steps), and new issues are created for the rest.

If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled (value `1`), also analyze the Steps for parallelism and add an **Execution mode** section **at the top of the proposed issue body** (before What/Why). This section must be the first thing the agent reads — placing it at the bottom causes the agent to default to isolated worktree agents instead of using `TeamCreate`.

```markdown
## Execution mode

> **MUST use Agent Teams (`TeamCreate`).** Do NOT fall back to isolated worktree agents.

After completing Step N (last sequential dependency):
- `teammate-name`: Steps X-Y — description
- `teammate-name`: Steps W-Z — description

_Remove this section entirely if Agent Teams is not enabled._
```

Also add an inline reminder in the first parallelizable step: `⚠️ This step runs in parallel via Agent Teams — see Execution mode above`.

Rules for the execution plan:
- **Identify the sequential prefix** — Steps that must run first because everything depends on them (e.g., template definition, shared types). These stay with the lead.
- **Group independent Steps by layer** — each group becomes a teammate.
- **Mark blocked teammates** — if a teammate depends on another's output, note it explicitly.
- **Keep it practical** — 2-4 teammates max.

If Agent Teams is not enabled, skip the Execution mode section entirely — do not include it with a "not enabled" note.

**Before presenting the plan, confirm:** if Agent Teams is enabled (Step 2b), does the plan include an "Execution mode" section at the top? If not, add it now — this is mandatory when Agent Teams is active.

Before presenting, review the plan with a critical eye: tighten vague checkboxes, remove redundancy, ensure TDD order, verify file paths are concrete. The question is "how can I make this plan more precise?" — not "what else can I add?"

**Include a task preview.** After the fenced code block with the plan, add a "Tasks that will be created" section listing the Step titles as bullet points. This lets the user see both the plan and the resulting tasks before approving — no separate task confirmation step.

Present the plan and use `AskUserQuestion` with options `["Approved", "I want to adjust"]`. This is the **single and only** approval gate in the entire skill flow.

- **"Approved"** — proceed immediately to Step 4. Do NOT ask for any additional confirmation, acknowledgment, or "aprovado" text. Execution starts now.
- **"I want to adjust"** — ask the user what to change (free text follow-up), apply the requested changes to the plan, then present the updated plan and the same `AskUserQuestion` again. Repeat until the user selects "Approved".

### 4. Update the issue (or create additional issues)

After approval, rewrite the issue body with the detailed plan and assign it to the user:

```bash
gh issue edit <number> --body "<approved body>" --add-assignee @me
```

If the mandatory split rule triggered (8+ steps), create the additional issues:

```bash
gh issue create --title "<descriptive title>" --body "<body with steps subset>"
```

Add each new issue to the project board's **Backlog** column using the same board operations from Step 7 of `/add-backlog`.

Add cross-references between related issues in each body (e.g., "Related: #12, #13"). Apply the same labels as the original issue.

Preserve the original title and labels.

### 5. Create branch linked to issue

Use `gh issue develop` to create the branch and automatically link it to the issue on GitHub. This makes the branch visible in the issue sidebar.

```bash
git checkout main && git pull
gh issue develop <number> --name feat/<number>-<slug> --checkout
git push -u origin feat/<number>-<slug>
```

Derive `<slug>` from the issue title (kebab-case, max 40 chars). The `gh issue develop` command creates the branch and links it — the subsequent `git push -u` ensures the remote tracking is set up.

### 5b. Board transitions and blocker check

Read `references/project-board-operations.md` for the full command reference.

Find the project board for the repo (`gh project list --owner "@me"`).

**If no board exists**, ask the user with `AskUserQuestion` offering `["Yes, create a board", "No, cancel"]`. If they choose to create one, read `references/project-board-setup.md` and set up the full board (7 status columns, Priority and Size fields). Add the current issue to the board after creation. If they cancel, stop — board tracking is required for all workflow skills.

**Check for blockers.** Before moving the card, scan the issue body for `> Blocked by #N` annotations. If any blocking issue is still open, flag it to the user:

```
⚠️ This issue is blocked by #N (<title>) which is still open. Continue anyway?
```

Use `AskUserQuestion` with options `["Yes, start anyway", "No, pick another issue"]`.

**Move card to "Ready".** After the blocker check passes, move the issue card to **"Ready"** — this signals the issue is picked up and the plan is about to be proposed:

1. Get the project node ID and the item ID for this issue
2. Get the Status field ID and the "Ready" option ID
3. Update the item status with `gh project item-edit`

Also check if **Priority** and **Size** are set on the card. If either is missing, infer from the plan:
- **Priority** — P0 for blocking/foundational, P1 for core features, P2 for nice-to-haves
- **Size** — based on step count: 1-2 = S, 3-4 = M, 5-6 = L, 7+ = XL

Set them with `gh project item-edit`. If unsure about priority, ask the user with `AskUserQuestion` offering `["P0 (Critical)", "P1 (High)", "P2 (Medium)"]`.

**Move card to "In Progress".** After the plan is approved (Step 3 approval gate), move the card from **Ready → In Progress** before creating the branch. This signals active development has started.

### 6. Create tasks

Tasks were already previewed to the user in Step 3. Create them silently — no user interaction needed.

Parse the Steps from the approved plan. Create a `TaskCreate` for each **Step** (not each checkbox — Steps are the right granularity for tasks).

Each task:
- **subject** — the Step title (e.g., "Step 1: Define README template")
- **description** — the checkboxes within that Step, so the agent knows what to accomplish
- **activeForm** — present continuous form for the spinner

Set up `addBlockedBy` dependencies between tasks when Steps have sequential dependencies.

### 7. Spawn teammates (automatic when Execution mode is present)

If the approved issue body contains an "Execution mode" section, spawn teammates immediately — **no second approval**. The user already approved the full plan (including the Execution mode section) in Step 3. Asking again violates the single-gate principle.

- Spawn teammates using `TeamCreate` following the plan from the issue. Each teammate must have explicit tool access: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Agent`, `TaskUpdate` at minimum — add `WebSearch` and `WebFetch` if the Step involves research or unfamiliar APIs. Teammates inherit the user's model by default — suggest Sonnet only if the user wants to optimize for speed or cost.
- The lead completes the sequential prefix, then teammates work in parallel on their assigned Steps.

If the issue has no Execution mode section (Agent Teams not enabled), skip this step.

## Guidelines

- **TDD is mandatory, not optional.** Every Step that introduces new behavior MUST include a test checkbox **before** the implementation checkbox — no exceptions. This is the single most important quality rule in this skill. The TDD-ordered checkboxes in the plan ARE the enforcement mechanism — when the agent executes the steps, the test-first order ensures red-green-refactor discipline naturally. No separate skill invocation is needed. Read `references/tdd-methodology.md` for the full methodology. Key principles: vertical slices (one test → one implementation → repeat, never write all tests first), test behavior through public interfaces (not implementation details), mock only at system boundaries (external APIs, not your own modules). When proposing the detailed plan, verify every step follows TDD order: test checkbox first, implementation checkbox second. If a step has no test checkbox before its implementation, it's wrong — fix it before presenting. This applies to all change types — new routes, new commands, new components, new utilities.

- **Test isolation via docker-compose.** Tests must never touch production data. When the issue involves database changes or file I/O, include a checkbox to configure the test environment. Read `references/development-guidelines.md` § 1 for env file separation, runtime safety guards, high ports, and full teardown requirements.

- **E2E state changes go through the UI.** When E2E tests need to change application state, always go through the UI (forms, buttons, navigation) — never manipulate the database directly and expect the app to see the change. Fullstack frameworks cache server-side data; direct DB writes don't trigger cache invalidation. Direct DB is valid only for setup/teardown (seed data) and assertions (verifying persistence after UI actions).

- **"Full test" means unit + lint + E2E.** When generating verification checkboxes that say "run full test suite", expand to all three layers: unit tests + lint + E2E (with server and database). Unit tests with mocks can pass while the schema is broken. CDP screenshots catch UI issues but don't verify persistence. Only E2E with real DB writes confirms the full stack. List the actual commands in the checkbox, not just "run tests".

- **Seed data quick-reference file.** When a Step creates or modifies seed data with test credentials (users, API keys, tokens), include a checkbox to create or update a gitignored `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root. Format credentials as a readable table (email, password, role, relevant attributes). If the file already exists, check if the changes affect it and include an update checkbox. Without this, developers waste time digging through SQL files to find login credentials for manual testing. This file is especially important when the project has no signup flow — it's the only way to know how to log in.

- **Domain-Driven Design by default.** Rich domain entities with behavior, value objects, and clear layer separation (domain → application → infrastructure). Place new business logic in the domain layer. Read `references/development-guidelines.md` § 3 for full DDD principles and when to skip.

- **Codebase-aware plans.** The most valuable part of this skill is producing checkboxes with concrete file paths and references to existing patterns. Always read the codebase before planning — generic checkboxes like "implement the feature" are a failure mode.

- **Acceptance criteria are success criteria, not the plan.** Keep the original acceptance criteria as top-level checkboxes. Steps are the implementation plan to achieve those criteria. Mark an acceptance criterion as done when all its related Steps are complete.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English because issue content is public, portable, and often read by collaborators or tools that expect English. Communication with the user follows their language preference.

- **Don't over-plan.** Later Steps can be less detailed than early ones because over-specifying Step 5 when Step 1 hasn't started wastes planning effort on assumptions that will change once early work is done. The first Step should have precise checkboxes; the last can be higher-level — the user will refine as they go.

- **Steps are work sessions.** Each Step should represent a focused work session — something you can complete, commit, and verify before moving on. Too large = lost focus. Too small = overhead.

- **Backlog issues are standalone — no Phases.** Unlike project issues created by `start-new-project` (which use "Phase 1: Theme", "Phase 2: Theme"), backlog issues are self-contained items. They use Steps directly, never Phases. If a backlog item grows too large (8+ steps), split it into multiple independent backlog issues — each with a descriptive title, 3-8 steps, and its own verification. All split issues are added to the board's Backlog column and reference each other.

- **No local environment paths in issues.** Issue content is public and portable. Never reference local paths like `~/.brain/`, `~/.claude/`, or absolute user paths. Use paths relative to the project root (e.g., `create-skill/SKILL.md`, not `~/.brain/skills/skill-creator/SKILL.md`). This applies to checkboxes, descriptions, and any text written to the issue body.

- **Visual verification via CDP (mandatory for web projects).** When the issue touches UI, verification checkboxes must use CDP: "Navigate to [page] via CDP and take screenshot to verify [expected state]". Read `references/development-guidelines.md` § 2 for setup steps, key CDP rules, and persistent test script requirements. Also see `references/cdp-best-practices.md` for the full rule set.

- **ARCHITECTURE.md maintenance.** Every Step that introduces a new pattern, route, table, or dependency must include a checkbox: "Update `ARCHITECTURE.md` with [specific addition]" — naming exactly what changed (e.g., "add billing query hook to Patterns section", "add `/billing` route to Routes section", "add `recharts` to Stack & dependencies"). This keeps the codebase knowledge cache current without a bulk "update everything" step at the end. If ARCHITECTURE.md doesn't exist and the project is a web app or has sufficient complexity, include a checkbox in Step 1 to generate it using the patterns discovered during codebase analysis.

- **No workarounds.** Every step must solve problems at their root. If a step would require a workaround (hardcoded values to bypass a bug, temporary flags, monkey-patches, `any` casts to silence type errors, skipped validations), it's a signal that the step is wrong or incomplete. Rewrite it to address the underlying issue. Workarounds create invisible tech debt that compounds across issues — what starts as "just for now" becomes permanent the moment the next issue lands on top of it.

- **No unnecessary code comments.** Code comments are allowed only when the logic is genuinely non-obvious — complex algorithms, unintuitive business rules, or regulatory constraints that aren't self-evident from the code. Self-documenting code (clear names, small functions, explicit types) replaces comments. Never include "add comments" or "document the code" as checkboxes — if the code needs a comment to be understood, the code needs to be rewritten.

- **Web research is authorized.** When the agent is blocked on a problem — unfamiliar framework behavior, unclear best practices, or an error with no obvious solution — it is authorized to search the web for best practices and solutions. This is not a last resort; it's a standard tool. Better to spend 30 seconds searching than 10 minutes guessing.

- **Avoid these anti-patterns:**
  - Checkboxes without TDD order — implementation before test, or tests missing entirely. Always: test checkbox first, then implementation checkbox
  - Generic checkboxes without file paths ("Add tests" → "Add test for login in `src/__tests__/auth.test.ts` — expect 200 with valid credentials")
  - Steps that mix concerns (backend + frontend in one Step)
  - Missing verification checkboxes (how do you know the Step works?)
  - Over-expanding simple issues into 10+ Steps when 3 would suffice
  - Checkboxes that duplicate the acceptance criteria verbatim instead of expanding them
  - Local/absolute paths in issue content (`~/.brain/`, `/Users/...`) — always use project-relative paths
  - Workarounds or hacks instead of proper solutions — if it needs a TODO comment, the step is incomplete
  - Comments that restate what the code does — self-documenting code replaces narration
  - Proposing a plan without checking `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` first — if enabled, the Execution mode section at the top is **mandatory**, not optional. Skipping it means the user loses the ability to parallelize work
  - Placing the Agent Teams section at the bottom of the issue — the agent reads top-down and will default to isolated worktree agents if it doesn't see the execution mode first
