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

If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled (value `1`), append a **Parallel execution plan** section to the issue body. Analyze step dependencies and group independent steps into teammate assignments:

```markdown
## Parallel execution plan (Agent Teams)

> Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

After Step N (last sequential dependency), spawn teammates:
- `teammate-name`: Steps X-Y (description)
- `teammate-name`: Steps W-Z (description)
- `teammate-name`: Steps A-B (blocked until teammate-name completes)
```

Rules for the parallel plan:
- **Identify the sequential prefix** — steps that must run first because everything depends on them (e.g., scaffolding, schema). These stay with the lead.
- **Group independent steps by layer** — backend, frontend, infra, tests. Each group becomes a teammate.
- **Mark blocked teammates** — if a teammate depends on another's output, note it explicitly (e.g., "blocked until backend completes").
- **Teammates inherit the user's model by default.** Optionally suggest Sonnet for teammates if the user wants to optimize for speed or cost. Don't default to a cheaper model — let the user decide.
- **Keep it practical** — 2-4 teammates max. More creates coordination overhead that outweighs the parallelism benefit.

If Agent Teams is not enabled, skip this section entirely.

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

- **Seed data quick-reference file.** When a project includes seed data with test credentials (users, API keys, tokens), include a checkbox to create a `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root with all seeded credentials in a readable format (table with email, password, role, relevant attributes). Add this file to `.gitignore` — it contains local test data that shouldn't be committed. This file is a living document: whenever seed data changes (new users, updated roles, new test accounts), update it. Without this, developers waste time digging through SQL files to find login credentials. The checkbox should go in the same Step that creates the seed file (e.g., `seed.sql`).

- **Domain-Driven Design by default.** Structure the codebase following DDD principles. Rich domain entities with behavior (not anemic data bags with external services doing all the work), value objects for domain concepts that have no identity, clear bounded contexts when the project has distinct domains. Separate layers with explicit responsibilities: domain (entities, value objects, domain services, repository interfaces), application (use cases/services orchestrating domain logic), infrastructure (database implementations, external APIs, framework adapters). Dependencies always point inward — infrastructure depends on domain, never the reverse. When proposing the phase structure, the data layer step should define domain entities with their business rules and validations built in, not just database schemas. This applies to projects with business logic (web apps, APIs, CLIs with domain rules) — skip for simple scripts, static sites, or pure infrastructure projects.

- **Project-agnostic.** This skill works for any kind of project — web apps, CLIs, libraries, APIs, mobile, data pipelines, infrastructure. The questions and structure adapt to the domain.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English. Communication with the user follows their language preference.

- **Checkboxes are verifiable actions.** Each checkbox should be completable in a single work session. "Implement the API" is too vague. "Create `src/routes/auth.ts` with login/logout endpoints" is concrete. For steps with new behavior, follow the TDD order: test checkbox first (`Add test for X in src/__tests__/x.test.ts — expect Y`), then implementation checkbox (`Implement X in src/x.ts`).

- **File paths when structure is known.** If the project builds on an existing codebase, include file paths in checkboxes. For greenfield projects, include paths once the structure is defined in early steps.

- **Don't over-plan.** Later phases can be less detailed than early ones. The first part should have precise checkboxes; the last part can be higher-level. The user will refine as they go.

- **Split large projects into multiple issues.** A single monolithic issue with 10+ steps buries progress and makes the milestone useless. When the mandatory split rule triggers (8+ steps), each Phase becomes its own issue, titled "Phase N: Theme Name". Each issue is independently completable, has its own verification section, and contributes to milestone progress (e.g., 4 issues = each closure moves the milestone 25%). This gives clear visibility into project progress — both for the developer and for anyone watching the repo.

- **Milestones for multi-issue projects.** When a project spans 2+ issues, always group them under a GitHub milestone. This gives automatic progress tracking (% complete) and a clear finish line. For single-issue projects, milestones are optional.

- **`closes #N` in PRs.** Always remind the user to include `closes #N` in PR descriptions. This auto-closes the linked issue on merge and updates milestone progress automatically.

- **Visual verification via CDP (mandatory for web projects).** For every web application project (web apps, fullstack frameworks, frontends), include Chrome DevTools Protocol setup as a step in Phase 1 — before any frontend implementation. CDP enables Claude to connect to the user's browser, navigate as a user (visible in real-time), and take screenshots to evaluate the UI. The setup consists of two files created from skill templates:
  - `.claude/start-chrome.sh` — launches Chrome with `--remote-debugging-port=9222`, detects the Chrome binary cross-platform, reads tabs from `project-settings.json`. Use `templates/start-chrome.sh` as the source.
  - `.claude/project-settings.json` — declarative CDP configuration. Use `templates/project-settings.json` as the source, adapting `baseUrl`, `tabs`, and `pages` to the project's routes.
  - **`baseUrl`** — the app's root URL (e.g., `http://localhost:3000`). Resolves relative page paths.
  - **`tabs`** — URLs to open when Chrome launches. Typically just the app's main URL.
  - **`pages`** — a route map declaring every page Claude can navigate to. Claude uses this to browse the app, take screenshots, and validate flows without hardcoded procedural steps. Adapt to the project's actual routes. **This is a living document** — every step that creates a new route or page must include a checkbox to add it to `pages` in `project-settings.json`. An outdated `pages` map means Claude can't verify new UI.
  - Playwright connects via `playwright.chromium.connectOverCDP('http://localhost:9222')` — the user sees everything happening in their browser in real-time.
  - **Fresh context rule.** CDP tests must always create a fresh `browser.newContext()` — never reuse `browser.contexts()[0]`. The existing browser context carries cookies from the user's browsing session, which pollutes auth state and causes flaky tests. Create one page per context, navigate within it, and `context.close()` when done — this removes the tab cleanly. See `templates/cdp-test-example.mjs` for the correct pattern.
  - **Dedicated test port.** CDP tests must hit a test server running on a dedicated port (e.g., 3100) with local environment variables — never the dev server on port 3000 which points to production. Test/seed users only exist in the local Docker instance. The manifest includes `testPort` and `devPort` to make this explicit.
  - **Read `references/cdp-best-practices.md`** for the full set of rules: context isolation, test server setup, observability (timestamps + page errors), hydration checks (`networkidle`), pre-flight checklist, and short timeouts. Every CDP test script must follow these rules.
  - Verification checkboxes in later steps should use the pattern: "Navigate to [page] via CDP and take screenshot to verify [expected state]".
  - **Persistent CDP test scripts.** Every visual verification performed via CDP must be saved as a reusable `.mjs` script in `.claude/cdp-tests/`. Each script connects via `connectOverCDP`, creates a fresh context, performs assertions or takes screenshots, and can be re-run independently. Maintain a `.claude/cdp-tests/manifest.json` registry with `cdpPort`, `testPort`, `baseUrl`, pre-flight commands, and a `tests` array mapping each script to its purpose, target page, what it verifies, and whether it requires auth. See `templates/cdp-manifest.json` for the structure. This makes future visual test rounds faster — Claude reads the manifest, finds the relevant script, and runs it instead of writing a new one from scratch. When a step creates a new visual verification, include a checkbox to save the script and update the manifest. The manifest is a living document, just like `project-settings.json`.
  - This is not optional for web projects. Without CDP, visual bugs go undetected until manual review. The cost of setup (two files, one step) is negligible compared to the cost of shipping broken UI.
