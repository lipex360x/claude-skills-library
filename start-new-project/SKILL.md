---
name: start-new-project
description: Plan and scaffold a new project from a prompt. Asks clarifying questions, proposes a phased GitHub issue structure with checkboxes, creates the issue and feature branch. Use when the user says "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", or provides a project idea wanting structured planning — even if they don't explicitly say "new project."
user-invocable: true
---

# Start New Project

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates ensure the user stays in control: once after clarifying questions, once after the proposed structure.

## Steps

### 1. Parse the prompt

Extract from the user's input:
- **Project name / slug** — if not obvious, derive from the description (kebab-case)
- **Tech stack hints** — languages, frameworks, libraries mentioned
- **Scope indicators** — "MVP", "production", "prototype", "just a quick..."
- **Domain** — web app, CLI, library, API, monorepo, mobile, etc.

If no argument was provided (bare `/start-new-project`), ask the user what they want to build before continuing.

### 2. Ask clarifying questions

Generate 3-5 targeted questions to fill gaps. Present as a numbered list. Common gaps:

1. **Platform** — web, CLI, library, API, mobile?
2. **Tech stack** — language, framework, database?
3. **Scope** — MVP or production-ready? What's the first milestone?
4. **Key features** — what are the 3 most important things it should do?
5. **Deployment** — where will it run? Docker, Vercel, npm, local-only?
6. **Existing code** — new repo or adding to an existing codebase?

Skip questions the prompt already answers. Adapt to the project type — a CLI tool needs different questions than a web app.

**Wait for the user's answers before proceeding.** This is the first approval gate.

### 3. Propose the phase structure

Read `templates/issue-template.md` for the expected format. Read `references/phase-planning-guide.md` for decomposition heuristics by project type.

Decompose the project into **Phases** (numbered, grouped by theme) and **Steps** (concrete milestones). Each step contains checkboxes with specific, verifiable actions — include file paths when the project structure is known.

Present the full issue body in a fenced code block. The structure should include:
- **Overview** with architecture description
- **Phases** numbered sequentially (Phase 1, 2, 3...)
- **Numbered Steps** with concrete checkboxes
- **Reference files table** (if working in an existing codebase)
- **Verification section** — how to confirm the project works end-to-end

Sizing guidelines:
- 2-4 phases per issue
- 3-8 steps per phase
- 2-6 checkboxes per step (TDD steps naturally have more checkboxes — test + implementation pairs)

**Mandatory split rule.** After drafting the full plan, count the total steps. If the plan has **more than 8 steps**, it **MUST** be split into multiple issues — one issue per Phase (or per logical group of Phases if some are small enough to merge). This is not a suggestion. A single issue with 10+ steps buries progress, makes milestone tracking useless, and overwhelms the developer. Each issue should have 3-8 steps, be independently completable, and have its own verification section. The Overview section is shared (copy it into each issue with a note: "This issue is Phase N of M"). Steps are renumbered starting from 1 within each issue. The Parallel execution plan (if applicable) goes in the first issue and references the other issues by number.

If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled (value `1`), add an **Execution mode** section **at the top of the issue body** (before Overview). This section must be the first thing the agent reads — placing it at the bottom causes the agent to default to isolated worktree agents instead of using `TeamCreate`.

```markdown
## Execution mode

> **MUST use Agent Teams (`TeamCreate`).** Do NOT fall back to isolated worktree agents.

After completing Step N (last sequential dependency):
- `teammate-name`: Steps X-Y — description
- `teammate-name`: Steps W-Z — description
- `teammate-name`: Steps A-B — blocked until `teammate-name` completes

_Remove this section entirely if Agent Teams is not enabled._
```

Also add an inline reminder in the first parallelizable step: `⚠️ This step runs in parallel via Agent Teams — see Execution mode above`.

Rules for the execution plan:
- **Identify the sequential prefix** — steps that must run first because everything depends on them (e.g., scaffolding, schema). These stay with the lead.
- **Group independent steps by layer** — backend, frontend, infra, tests. Each group becomes a teammate.
- **Mark blocked teammates** — if a teammate depends on another's output, note it explicitly (e.g., "blocked until backend completes").
- **Teammates inherit the user's model by default.** Optionally suggest Sonnet for teammates if the user wants to optimize for speed or cost. Don't default to a cheaper model — let the user decide.
- **Keep it practical** — 2-4 teammates max. More creates coordination overhead that outweighs the parallelism benefit.

If Agent Teams is not enabled, skip the Execution mode section entirely — do not include it with a "not enabled" note.

Before presenting, review the plan with a critical eye: tighten vague checkboxes, remove redundancy, ensure TDD order, verify file paths are concrete. The question is "how can I make this plan more precise?" — not "what else can I add?"

**Wait for the user's approval before proceeding.** This is the second (and final) approval gate. The user may request changes — iterate until they approve.

### 4. Repo scaffolding (labels + milestone)

Before creating issues, ensure the repo has basic organizational primitives.

**Labels** — check with `gh label list`. If priority labels don't exist, offer to create them:
- `P0` (critical), `P1` (high), `P2` (medium), `P3` (low)
- Type labels (`feature`, `bug`, `chore`, `docs`) — only if missing

Don't force labels on repos that already have a custom scheme. Adapt to what's there.

**Milestone** — if the project generates 2+ issues, create a milestone to group them:

```bash
gh api repos/{owner}/{repo}/milestones -f title="<milestone name>" -f description="<one-line goal>" [-f due_on="<YYYY-MM-DDT00:00:00Z>"]
```

Good milestone names: the project name itself ("Project X MVP"), a version ("v1.0"), or a phase ("Phase 1: Core").

For single-issue projects, a project milestone is optional.

**Backlog milestone** — always create a "Backlog" milestone (no due date) for every new project. This is a permanent bucket for future ideas, improvements, and low-priority items. It stays open indefinitely and gives the user a place to park ideas without losing them. When an item gets prioritized, move it from Backlog to an active milestone.

### 5. Create the GitHub issues

After approval, create the issues. If the plan was split into multiple issues (mandatory split rule), create them sequentially — the first issue may reference later ones by number.

```bash
gh issue create --title "<concise title>" --body "<approved body>"
```

Apply labels if the repo uses them. Common: `enhancement`, `feature`, plus a priority label. For multi-issue projects, include the phase number in the issue title (e.g., "Phase 1: Scaffolding & Data Layer").

Assign all issues to the milestone:

```bash
gh issue edit <number> --milestone "<milestone name>"
```

For multi-issue projects, the milestone provides automatic progress tracking — each closed issue moves the percentage forward, giving clear visibility into how much of the project is done.

### 6. Project board (for large projects)

If the project generates **3+ issues**, offer to create a GitHub Project board for visual tracking:

```bash
# Create the project
gh project create --title "<project name>" --owner "@me"

# Add issues to the project
gh project item-add <project-number> --owner "@me" --url <issue-url>
```

GitHub Projects V2 creates "Todo", "In Progress", and "Done" columns by default — no extra setup needed.

**This step is optional and user-controlled.** Ask: "This project has N issues — want me to create a project board to track them visually?" If the user declines, skip silently.

For projects with 1-2 issues, skip this step entirely — milestones already provide enough tracking.

### 7. Create the feature branch

```bash
git checkout main
git pull origin main
git checkout -b feature/<slug>
git push -u origin feature/<slug>
```

The slug comes from step 1. If the issue number is known, optionally prefix: `feature/<number>-<slug>`.

### 8. Summary

Present:
- Issue URL(s) (linked)
- Milestone (if created) with link
- Project board (if created) with link
- Branch name
- Total steps and checkboxes count
- Remind: use `closes #N` in PR descriptions to auto-close issues on merge
- Suggest starting with Step 1

## Guidelines

- **TDD by default.** Every step that introduces new behavior must include a test checkbox **before** the implementation checkbox. Write the test first, watch it fail, then implement. This applies to all project types — backend routes, CLI commands, library functions, UI components. TDD catches design issues early and produces code that is testable by construction, not by afterthought. When proposing the phase structure, ensure test checkboxes precede their corresponding implementation checkboxes within each step.

- **Test isolation via docker-compose.** Tests must never touch production data. Orchestrate the test environment with a `docker-compose.test.yml` (or a `test` profile in the main `docker-compose.yml`) so that any developer can spin up the full test stack with a single command. This guarantees portability — the same setup works on any machine and in CI. When the project uses a cloud service (Supabase, Firebase, PlanetScale, Neon, etc.), include its local emulator as a docker-compose service (`supabase start`, `firebase emulators:start`). When tests produce files, use a temporary directory that is cleaned up after each run. Include the docker-compose test setup as an early checkbox in Phase 1 — before any test can run, the isolation boundary must exist. Tests that leak data into production are worse than no tests because they create false confidence. Two critical details:
  - **Env file separation.** Keep `.env.local` pointing at the remote/production service for normal development. Inject local container URLs **only** in the test context — via `.env.test`, test runner config (e.g., Playwright's `webServer.env`), or docker-compose environment variables. Never overwrite `.env.local` with test URLs because it creates a risk of forgetting to revert before deploying.
  - **Runtime safety guard.** Include a global test setup file (e.g., `global-setup.ts`) that verifies the target URLs point to local services (`127.0.0.1`, `localhost`) before any test runs. If the check fails, abort the test suite with a clear error. This is the last line of defense against accidentally running tests against production.
  - **High ports.** Bind all test services to high ports (e.g., 54321, 54322, 9090) in docker-compose to avoid collisions with dev servers and system services running on standard ports. Define these ports in `.env.test` so they're easy to change if a port is already taken.
  - **Full teardown.** Include a `global-teardown.ts` (or equivalent) that stops all test containers and processes when the suite finishes — success or failure. Use `docker compose down` to remove containers, networks, and volumes created during the run. Tests that leave orphaned containers waste resources and cause port conflicts on the next run.

- **E2E state changes go through the UI.** When E2E tests need to change application state (toggle a feature, update a setting), always change it through the UI — navigate to the page, interact with the form, submit. Never manipulate the database directly and expect the app to see the change. Fullstack frameworks cache server-side data aggressively — direct DB writes don't trigger cache invalidation, causing false test failures. Direct DB access is valid only for setup/teardown (seed data) and assertions (verifying persistence after UI actions).

- **"Full test" means unit + lint + E2E.** When generating verification checkboxes that say "run full test suite", always expand to all three layers: unit tests + lint + E2E (with server and database). Unit tests with mocks can pass while the database schema is broken. CDP screenshots catch UI issues but don't verify data persistence. Only E2E tests with real database writes confirm the entire stack works. Verification checkboxes should list the actual commands, not just "run tests".

- **Seed data quick-reference file.** When a project includes seed data with test credentials (users, API keys, tokens), include a checkbox to create a `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root with all seeded credentials in a readable format (table with email, password, role, relevant attributes). Add this file to `.gitignore` — it contains local test data that shouldn't be committed. This file is a living document: whenever seed data changes (new users, updated roles, new test accounts), update it. Without this, developers waste time digging through SQL files to find login credentials. The checkbox should go in the same Step that creates the seed file (e.g., `seed.sql`).

- **Domain-Driven Design by default.** Structure the codebase following DDD principles. Rich domain entities with behavior (not anemic data bags with external services doing all the work), value objects for domain concepts that have no identity, clear bounded contexts when the project has distinct domains. Separate layers with explicit responsibilities: domain (entities, value objects, domain services, repository interfaces), application (use cases/services orchestrating domain logic), infrastructure (database implementations, external APIs, framework adapters). Dependencies always point inward — infrastructure depends on domain, never the reverse. When proposing the phase structure, the data layer step should define domain entities with their business rules and validations built in, not just database schemas. This applies to projects with business logic (web apps, APIs, CLIs with domain rules) — skip for simple scripts, static sites, or pure infrastructure projects.

- **Project-agnostic.** This skill works for any kind of project — web apps, CLIs, libraries, APIs, mobile, data pipelines, infrastructure. The questions and structure adapt to the domain.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English because issue content is public, portable, and often read by collaborators or tools that expect English. Communication with the user follows their language preference.

- **Checkboxes are verifiable actions.** Each checkbox should be completable in a single work session. "Implement the API" is too vague. "Create `src/routes/auth.ts` with login/logout endpoints" is concrete. For steps with new behavior, follow the TDD order: test checkbox first (`Add test for X in src/__tests__/x.test.ts — expect Y`), then implementation checkbox (`Implement X in src/x.ts`).

- **File paths when structure is known.** If the project builds on an existing codebase, include file paths in checkboxes. For greenfield projects, include paths once the structure is defined in early steps.

- **Don't over-plan.** Later phases can be less detailed than early ones because over-specifying Phase 3 when Phase 1 hasn't started wastes planning effort on assumptions that will change once early work is done. The first phase should have precise checkboxes; later phases can be higher-level — the user will refine as they go.

- **Split large projects into multiple issues.** A single monolithic issue with 10+ steps buries progress and makes the milestone useless. When the mandatory split rule triggers (8+ steps), each Phase becomes its own issue, titled "Phase N: Theme Name". Each issue is independently completable, has its own verification section, and contributes to milestone progress (e.g., 4 issues = each closure moves the milestone 25%). This gives clear visibility into project progress — both for the developer and for anyone watching the repo.

- **Milestones for multi-issue projects.** When a project spans 2+ issues, always group them under a GitHub milestone. This gives automatic progress tracking (% complete) and a clear finish line. For single-issue projects, milestones are optional.

- **`closes #N` in PRs.** Always remind the user to include `closes #N` in PR descriptions. This auto-closes the linked issue on merge and updates milestone progress automatically.

- **Visual verification via CDP (mandatory for web projects).** For every web application project (web apps, fullstack frameworks, frontends), include Chrome DevTools Protocol setup as a step in Phase 1 — before any frontend implementation. CDP enables Claude to connect to the user's browser, navigate as a user (visible in real-time), and take screenshots to evaluate the UI. The setup consists of two files created from skill templates:
  - `.claude/start-chrome.sh` — launches Chrome with `--remote-debugging-port=9222`, detects the Chrome binary cross-platform, reads tabs from `project-settings.json`. Use `templates/start-chrome.sh` as the source.
  - `.claude/project-settings.json` — declarative CDP configuration (the single living document for all CDP settings). Use `templates/project-settings.json` as the source, adapting `baseUrl`, `testPort`, `tabs`, and `pages` to the project's routes.
  - **`baseUrl`** — the app's root URL (e.g., `http://localhost:3000`). Resolves relative page paths.
  - **`testPort`** — dedicated port for the test server (e.g., 3100). CDP scripts hit this port, never the dev server.
  - **`tabs`** — URLs to open when Chrome launches. Typically just the app's main URL.
  - **`pages`** — a route map declaring every page Claude can navigate to. **This is a living document** — every step that creates a new route or page must include a checkbox to add it to `pages` in `project-settings.json`.
  - **CDP runner and `test:cdp` script.** Include in the CDP setup step: create `e2e/cdp/run-all.ts` from `templates/cdp-run-all.ts` (auto-discovers all `verify-*.ts` files), and add `"test:cdp": "npx tsx e2e/cdp/run-all.ts"` plus `"test:cdp:server": "dotenv -e .env.test -- npx next start -p 3100"` (adapt framework) to `package.json`. The server script ensures env vars (Supabase URLs, API keys) are loaded — without them, CDP scripts timeout on auth.
  - **CDP is not E2E.** When instructing teammates (Agent Teams), be explicit: "do NOT run Playwright E2E tests" but "DO create CDP verification scripts in `e2e/cdp/`". Teammates conflate the two and skip CDP when told to skip E2E.
  - Playwright connects via `playwright.chromium.connectOverCDP('http://localhost:9222')` — the user sees everything happening in their browser in real-time.
  - **Read `references/cdp-best-practices.md`** for all CDP rules. Key rules enforced in every CDP script:
    - **Fresh context:** always `browser.newContext()` — never `browser.contexts()[0]`. Always `context.close()` in a `finally` block.
    - **Dedicated test port:** hit the test server (e.g., 3100), never the dev server (3000). Test/seed users only exist locally.
    - **No `run_in_background`:** run CDP scripts inline with Bash tool `timeout: 30000`. Background execution orphans processes.
    - **Server is user's responsibility:** pre-flight check before running. Never auto-start with `nohup`.
    - **Generic login redirect:** `waitForURL(url => !url.pathname.includes("/login"))` — never hardcode destination.
    - **Cleanup after CDP sessions:** `TaskStop` the server task (never `lsof kill` — user may have own servers), remove framework lock files.
  - Verification checkboxes in later steps should use the pattern: "Navigate to [page] via CDP and take screenshot to verify [expected state]".
  - **Persistent CDP test scripts.** Every visual verification performed via CDP must be saved as a reusable script in `e2e/cdp/verify-<page>.ts` (match project language — `.ts` for TypeScript, `.mjs` for plain JS). Screenshots go to `test-results/cdp/screenshots/` (gitignored via Playwright's default config). See `templates/cdp-test-example.ts` for the pattern. Before writing a new script, check `e2e/cdp/` for an existing one that covers the same page — run it first, only create a new one if the verification is different. When a step modifies existing UI, update the corresponding script. Include checkboxes: "Save CDP test script to `e2e/cdp/verify-[page].ts`".
  - This is not optional for web projects. Without CDP, visual bugs go undetected until manual review. The cost of setup (two files, one step) is negligible compared to the cost of shipping broken UI.

- **ARCHITECTURE.md — codebase knowledge cache.** Include a checkbox in Phase 1 (Step 1 or the scaffolding step) to generate an initial `ARCHITECTURE.md` at the project root using `templates/architecture.md` as the structure. This file captures stack, layers, patterns (by canonical example), schema summary, auth model, and routes — the information an exploration agent would discover by reading 15+ files. Future conversations read this file instead of re-exploring from scratch (~2k tokens vs ~53k tokens). Every subsequent Step that introduces a new pattern, route, table, or dependency must include a checkbox: "Update `ARCHITECTURE.md` with [specific addition]" — naming exactly what changed (e.g., "add reserves query hook pattern", "add `/reserves` route", "add `recharts` to Stack & dependencies"). This is not a generic "update docs" checkbox — it must be tied to the specific change. The file is a living document; an outdated one is worse than none because it creates false confidence.

- **Avoid these anti-patterns:**
  - Checkboxes without TDD order — implementation before test, or tests missing entirely. Always: test checkbox first, then implementation checkbox
  - Generic checkboxes without file paths ("Add tests" → "Add test for login in `src/__tests__/auth.test.ts` — expect 200 with valid credentials")
  - Steps that mix concerns (backend + frontend in one Step)
  - Missing verification checkboxes (how do you know the Step works?)
  - Monolithic issues with 10+ steps when the mandatory split rule should have triggered
  - Front-loading detail on later phases — Phase 1 should be precise, later phases can be higher-level
  - Local/absolute paths in issue content (`~/.brain/`, `/Users/...`) — always use project-relative paths
