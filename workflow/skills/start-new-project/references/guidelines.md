# Start New Project — Guidelines

## TDD is mandatory, not optional

Every step that introduces new behavior MUST include a test checkbox **before** the implementation checkbox — no exceptions. This is the single most important quality rule in this skill. The TDD-ordered checkboxes in the plan ARE the enforcement mechanism — when the agent executes the steps, the test-first order ensures red-green-refactor discipline naturally. No separate skill invocation is needed. Read `references/tdd-methodology.md` for the full methodology. Key principles: vertical slices (one test → one implementation → repeat, never write all tests first), test behavior through public interfaces (not implementation details), mock only at system boundaries (external APIs, not your own modules). When proposing the phase structure, verify every step follows TDD order: test checkbox first, implementation checkbox second. If a step has no test checkbox before its implementation, it's wrong — fix it before presenting. This applies to all project types — backend routes, CLI commands, library functions, UI components.

## Test isolation via docker-compose

Tests must never touch production data. When the project tech stack includes any database, ORM, or BaaS (postgres, mysql, sqlite, supabase, firebase, mongo, prisma, drizzle, typeorm, sequelize), the plan MUST include test isolation as an early Phase 1 step — this is automatic, not optional. Orchestrate the test environment with a `docker-compose.test.yml` (or a `test` profile in the main `docker-compose.yml`) so that any developer can spin up the full test stack with a single command. This guarantees portability — the same setup works on any machine and in CI. When the project uses a cloud service (Supabase, Firebase, PlanetScale, Neon, etc.), include its local emulator as a docker-compose service (`supabase start`, `firebase emulators:start`). When tests produce files, use a temporary directory that is cleaned up after each run. Include the docker-compose test setup as an early checkbox in Phase 1 — before any test can run, the isolation boundary must exist. Tests that leak data into production are worse than no tests because they create false confidence. Two critical details:
- **Env file separation.** Keep `.env.local` pointing at the remote/production service for normal development. Inject local container URLs **only** in the test context — via `.env.test`, test runner config (e.g., Playwright's `webServer.env`), or docker-compose environment variables. Never overwrite `.env.local` with test URLs because it creates a risk of forgetting to revert before deploying.
- **Runtime safety guard.** Include a global test setup file (e.g., `global-setup.ts`) that verifies the target URLs point to local services (`127.0.0.1`, `localhost`) before any test runs. If the check fails, abort the test suite with a clear error. This is the last line of defense against accidentally running tests against production.
- **High ports.** Bind all test services to high ports (e.g., 54321, 54322, 9090) in docker-compose to avoid collisions with dev servers and system services running on standard ports. Define these ports in `.env.test` so they're easy to change if a port is already taken.
- **Full teardown.** Include a `global-teardown.ts` (or equivalent) that stops all test containers and processes when the suite finishes — success or failure. Use `docker compose down` to remove containers, networks, and volumes created during the run. Tests that leave orphaned containers waste resources and cause port conflicts on the next run.
- **Husky git hooks.** Configure Husky as part of the test environment setup — `pre-commit` runs lint + type-check, `pre-push` runs tests + build. This ensures CI-breaking code never reaches the remote. Use `npx husky init` to scaffold, then add the hook scripts. Pair with `lint-staged` for pre-commit to only lint changed files.

## E2E state changes go through the UI

When E2E tests need to change application state (toggle a feature, update a setting), always change it through the UI — navigate to the page, interact with the form, submit. Never manipulate the database directly and expect the app to see the change. Fullstack frameworks cache server-side data aggressively — direct DB writes don't trigger cache invalidation, causing false test failures. Direct DB access is valid only for setup/teardown (seed data) and assertions (verifying persistence after UI actions).

## "Full test" means unit + lint + E2E

When generating verification checkboxes that say "run full test suite", always expand to all three layers: unit tests + lint + E2E (with server and database). Unit tests with mocks can pass while the database schema is broken. Playwright screenshots catch UI issues but don't verify data persistence. Only E2E tests with real database writes confirm the entire stack works. Verification checkboxes should list the actual commands, not just "run tests".

## Seed data quick-reference file

When a project includes seed data with test credentials (users, API keys, tokens), include a checkbox to create a `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root with all seeded credentials in a readable format (table with email, password, role, relevant attributes). Add this file to `.gitignore` — it contains local test data that shouldn't be committed. This file is a living document: whenever seed data changes (new users, updated roles, new test accounts), update it. Without this, developers waste time digging through SQL files to find login credentials. The checkbox should go in the same Step that creates the seed file (e.g., `seed.sql`).

## Domain-Driven Design by default

Structure the codebase following DDD principles. Rich domain entities with behavior (not anemic data bags with external services doing all the work), value objects for domain concepts that have no identity, clear bounded contexts when the project has distinct domains. Separate layers with explicit responsibilities: domain (entities, value objects, domain services, repository interfaces), application (use cases/services orchestrating domain logic), infrastructure (database implementations, external APIs, framework adapters). Dependencies always point inward — infrastructure depends on domain, never the reverse. When proposing the phase structure, the data layer step should define domain entities with their business rules and validations built in, not just database schemas. This applies to projects with business logic (web apps, APIs, CLIs with domain rules) — skip for simple scripts, static sites, or pure infrastructure projects.

## Project-agnostic

This skill works for any kind of project — web apps, CLIs, libraries, APIs, mobile, data pipelines, infrastructure. The questions and structure adapt to the domain.

## English for all issue content

Issues, checkboxes, and branch names are always in English because issue content is public, portable, and often read by collaborators or tools that expect English. Communication with the user follows their language preference.

## Checkboxes are verifiable actions

Each checkbox should be completable in a single work session. "Implement the API" is too vague. "Create `src/routes/auth.ts` with login/logout endpoints" is concrete. For steps with new behavior, follow the TDD order: test checkbox first (`Add test for X in src/__tests__/x.test.ts — expect Y`), then implementation checkbox (`Implement X in src/x.ts`).

## File paths when structure is known

If the project builds on an existing codebase, include file paths in checkboxes. For greenfield projects, include paths once the structure is defined in early steps.

## Don't over-plan

Later phases can be less detailed than early ones because over-specifying Phase 3 when Phase 1 hasn't started wastes planning effort on assumptions that will change once early work is done. The first phase should have precise checkboxes; later phases can be higher-level — the user will refine as they go.

## Split large projects into multiple issues

A single monolithic issue with 10+ steps buries progress and makes the milestone useless. When the mandatory split rule triggers (8+ steps), each Phase becomes its own issue, titled "Phase N: Theme Name". Each issue is independently completable, has its own verification section, and contributes to milestone progress (e.g., 4 issues = each closure moves the milestone 25%).

## Milestones are optional scope groupings

Milestones serve as version/release/sprint groupings — not as status indicators. Status is tracked on the project board via columns. Create milestones only when the user requests them or the project has a clear versioning structure.

## `closes #N` in PRs

Always remind the user to include `closes #N` in PR descriptions. This auto-closes the linked issue on merge and updates milestone progress automatically.

## Visual verification via Playwright (mandatory for web projects)

For every web application project, include Playwright setup as a step in Phase 1 — before any frontend implementation. Playwright provides headless browser testing, screenshots, and E2E verification with zero custom infrastructure. The setup consists of:
- `playwright.config.ts` — test directory, web server config, browser projects (chromium + mobile)
- `tests/e2e/pages/` — page objects for reusable interactions (`AuthPage.login()`, etc.)
- `tests/e2e/helpers/` — test user factories, env validation, API signup helpers
- `tests/e2e/global-setup.ts` — seed DB, create manual test user with known credentials
- `tests/e2e/global-teardown.ts` — cleanup e2e users, kill servers, free ports
- Read `references/playwright-practices.md` for the full setup, rules, and framework-agnostic design.

## ARCHITECTURE.md — codebase knowledge cache

Include a checkbox in Phase 1 to generate `ARCHITECTURE.md` at the project root using `templates/architecture.md`. This file captures stack, layers, patterns, schema, auth model, and routes. Every subsequent Step that introduces a new pattern, route, table, or dependency must include a checkbox to update it — naming exactly what changed.

## Issue body backup (mandatory)

Every project must include issue body protection from day 1. A single malformed `sed` or bad `gh issue edit` can silently wipe an entire issue body with no recovery. Include a Phase 1 checkbox to scaffold the backup infrastructure:

1. **Copy `templates/issue-backup.sh` → `.claude/scripts/issue-backup.sh`** — SQLite-based backup that snapshots issue bodies before write operations. Supports `snapshot`, `restore`, `list`, `cleanup` subcommands with retention of 10 snapshots per issue.
2. **Copy `templates/pre-issue-edit-hook.sh` → `.claude/hooks/pre-issue-edit.sh`** — PreToolUse hook that automatically intercepts `gh issue edit` commands and snapshots the body before the edit is applied.
3. **Register the hook in `.claude/settings.json`** — add `PreToolUse` entry with matcher `Bash` pointing to the hook script.
4. **Add `.claude/issues.db` to `.gitignore`** — the SQLite database is local state, not committed.
5. **Run `issue-backup.sh snapshot-all`** after creating the first issues — seeds the database with initial backups.

This setup costs nothing at runtime (hook only fires on `gh issue edit`) and prevents catastrophic data loss. The backup script also supports `restore` for quick recovery.

## CLAUDE.md — agent context for new sessions

Include a checkbox in Phase 1 (same Step as ARCHITECTURE.md) to create `CLAUDE.md` at the project root. This file gives Claude Code immediate context when starting a new session — without it, every new conversation starts cold and wastes tokens re-discovering the project. Contents:

- **Quick start** — commands to run services, tests, linting (copy-paste ready)
- **Key files** — pointers to ARCHITECTURE.md, any mapping/guide docs, test credentials
- **Conventions** — error handling pattern (Result/Either if used), project structure for each layer, testing strategy, LLM usage, linting tools
- **Current state** — which issue/phase is in progress (update as work advances)

Keep it under 80 lines. It's a bootstrap document, not documentation — point to files, don't duplicate content. Update the "Current state" section whenever a phase completes.

## No workarounds

Every step must solve problems at their root. If a step would require a workaround (hardcoded values, temporary flags, monkey-patches, `any` casts), the step is incomplete. Rewrite it.

## No unnecessary code comments

Code comments allowed only for genuinely non-obvious logic. Never include "add comments" checkboxes — if the code needs a comment to be understood, the code needs to be rewritten.

## Web research is authorized

When blocked — unfamiliar framework, unclear best practices, error with no obvious solution — search the web. Better to spend 30 seconds searching than 10 minutes guessing.
