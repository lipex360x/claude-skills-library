# Development Guidelines (Extended)

Guidelines extracted from SKILL.md for reference. Read this file when applying test isolation, CDP verification, or DDD principles in the plan.

## 1. Test isolation via docker-compose

Tests must never touch production data. When the issue involves database changes or file I/O, include a checkbox to configure the test environment using `docker-compose.test.yml` (or a `test` profile in the main compose file) — this orchestrates the full test stack so any developer can spin it up with a single command. For cloud services (Supabase, Firebase, PlanetScale, Neon, etc.), include their local emulators as compose services. When tests produce files, use a temporary directory cleaned up after each run. If the project already has a docker-compose test setup, verify it covers the new changes. Tests that leak data into production are worse than no tests because they create false confidence. Critical details:

- **Env file separation.** Keep `.env.local` pointing at the remote/production service. Inject local container URLs **only** in the test context — via `.env.test`, test runner config (e.g., Playwright's `webServer.env`), or docker-compose environment variables. Never overwrite `.env.local` with test URLs.
- **Runtime safety guard.** Include a global test setup (e.g., `global-setup.ts`) that verifies target URLs point to local services (`127.0.0.1`, `localhost`) before running. If the check fails, abort with a clear error — this is the last line of defense against accidentally testing against production.
- **High ports.** Bind all test services to high ports (e.g., 54321, 54322, 9090) in docker-compose to avoid collisions with dev servers and system services. Define ports in `.env.test` so they're easy to change.
- **Full teardown.** Include a `global-teardown.ts` (or equivalent) that stops all test containers and processes when the suite finishes — success or failure. Use `docker compose down` to remove containers, networks, and volumes. Orphaned containers cause port conflicts on the next run.
- **Husky git hooks.** Configure Husky as part of the test environment setup. `pre-commit` runs lint + type-check (via `lint-staged` to scope to changed files only). `pre-push` runs the full test suite + build. This catches CI-breaking code before it reaches the remote. Setup: `npx husky init`, then create `.husky/pre-commit` and `.husky/pre-push` with the appropriate commands. If the project uses a monorepo, scope hooks to the relevant workspace.

## 2. Visual verification via CDP (mandatory for web projects)

When the issue touches UI — new pages, component changes, layout fixes, styling — verification checkboxes must use CDP to confirm the result visually, not just functionally. The pattern: "Navigate to [page] via CDP and take screenshot to verify [expected state]". This catches layout breaks, missing elements, and visual regressions that unit tests and functional tests miss entirely.

**Setup (when CDP is not yet configured and the project is a web app with frontend):** the first Step in the plan must set it up:
- `.claude/start-chrome.sh` + `.claude/project-settings.json` + `e2e/cdp/run-all.ts` runner + `test:cdp` and `test:cdp:server` scripts in `package.json`

**When CDP is already configured:** read the `pages` map from `project-settings.json` to reference routes by name in checkboxes.

**For non-web projects or backend-only issues:** skip CDP entirely.

Key CDP rules (see `references/cdp-best-practices.md` for the full set):
- **Fresh context:** always `browser.newContext()` — never `browser.contexts()[0]`. Always `context.close()` in a `finally` block.
- **Dedicated test port:** hit the test server (declared as `testPort` in `project-settings.json`), never the dev server. Test/seed users only exist locally.
- **Test server needs env vars:** start via `test:cdp:server` (loads `.env.test` with service URLs, API keys). Without env vars, CDP scripts timeout on auth — the server starts but can't authenticate.
- **No `run_in_background`:** run CDP scripts inline with Bash tool `timeout: 30000`. Background execution orphans processes.
- **Server is user's responsibility:** pre-flight check before running. Never auto-start with `nohup`.
- **Generic login redirect:** `waitForURL(url => !url.pathname.includes("/login"))` — never hardcode destination.
- **Cleanup after CDP sessions:** `TaskStop` the server task (never `lsof kill` — user may have own servers), remove framework lock files.
- **CDP is not E2E:** when instructing teammates (Agent Teams), be explicit — "do NOT run Playwright E2E tests" but "DO create CDP verification scripts in `e2e/cdp/`". Teammates conflate the two.
- **Persistent CDP test scripts:** every visual verification must be saved in `e2e/cdp/verify-<page>.ts` (match project language — `.ts` for TypeScript, `.mjs` for plain JS). Screenshots go to `test-results/cdp/screenshots/` (gitignored). Before writing a new script, check `e2e/cdp/` for an existing one — run it first, only create new if needed. When a Step modifies existing UI, update the corresponding script. Include checkboxes: "Save CDP test script to `e2e/cdp/verify-[page].ts`".

## 3. Domain-Driven Design by default

When proposing Steps, follow DDD principles: rich domain entities with behavior and validations built in (not anemic models with logic scattered across services), value objects for concepts without identity, clear separation of layers (domain, application, infrastructure) with dependencies pointing inward. When the issue involves new business logic, the Step should place it in the domain layer — not in controllers, routes, or database queries. When the issue touches an existing codebase, read the current architecture first: if it already follows DDD, respect the patterns; if it doesn't, don't force a rewrite — but new code should follow DDD within its scope. Skip for issues that are purely infrastructure, config, or UI-only with no business rules.
