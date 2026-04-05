# Development Guidelines (Extended)

Guidelines extracted from SKILL.md for reference. Read this file when applying test isolation, Playwright visual verification, or DDD principles in the plan.

## 1. Test isolation via docker-compose

Tests must never touch production data. When the issue involves database changes or file I/O, include a checkbox to configure the test environment using `docker-compose.test.yml` (or a `test` profile in the main compose file) — this orchestrates the full test stack so any developer can spin it up with a single command. For cloud services (Supabase, Firebase, PlanetScale, Neon, etc.), include their local emulators as compose services. When tests produce files, use a temporary directory cleaned up after each run. If the project already has a docker-compose test setup, verify it covers the new changes. Tests that leak data into production are worse than no tests because they create false confidence. Critical details:

- **Env file separation.** Keep `.env.local` pointing at the remote/production service. Inject local container URLs **only** in the test context — via `.env.test`, test runner config (e.g., Playwright's `webServer.env`), or docker-compose environment variables. Never overwrite `.env.local` with test URLs.
- **Runtime safety guard.** Include a global test setup (e.g., `global-setup.ts`) that verifies target URLs point to local services (`127.0.0.1`, `localhost`) before running. If the check fails, abort with a clear error — this is the last line of defense against accidentally testing against production.
- **High ports.** Bind all test services to high ports (e.g., 54321, 54322, 9090) in docker-compose to avoid collisions with dev servers and system services. Define ports in `.env.test` so they're easy to change.
- **Full teardown.** Include a `global-teardown.ts` (or equivalent) that stops all test containers and processes when the suite finishes — success or failure. Use `docker compose down` to remove containers, networks, and volumes. Orphaned containers cause port conflicts on the next run.
- **Husky git hooks.** Configure Husky as part of the test environment setup. `pre-commit` runs lint + type-check (via `lint-staged` to scope to changed files only). `pre-push` runs the full test suite + build. This catches CI-breaking code before it reaches the remote. Setup: `npx husky init`, then create `.husky/pre-commit` and `.husky/pre-push` with the appropriate commands. If the project uses a monorepo, scope hooks to the relevant workspace.

## 2. Visual verification via Playwright (mandatory for web projects)

When the issue touches UI — new pages, component changes, layout fixes, styling — verification checkboxes must use Playwright to confirm the result visually, not just functionally. This catches layout breaks, missing elements, and visual regressions that unit tests and functional tests miss entirely.

**"Rodar o PW" is a feedback loop, not just a test run.** Every UI step must include a verification cycle:

1. **Run** — execute the Playwright E2E test for the page/component
2. **Read screenshots** — visually analyze the captured screenshots (light/dark, desktop/mobile)
3. **Fix** — correct any visual issues, broken layouts, missing elements found in screenshots
4. **Re-run** — repeat until screenshots match expected state
5. **Only then** mark the checkbox as done

This cycle is mandatory. Writing the test is not enough — the agent must run it, read the screenshot output, and confirm the UI is correct before presenting work as complete.

**Checkbox pattern for UI steps:**
```
- [ ] E2E: Write Playwright test for [page] in `tests/e2e/[page].spec.ts` — verify [expected state], screenshot light/dark + desktop/mobile
- [ ] PW verify: Run `npm run test:e2e -- [page].spec.ts`, read screenshots, fix visual issues until all pass
```

The first checkbox writes the test. The second checkbox is the verification cycle — it's a separate action because the agent must actively read and analyze screenshots, not just check exit code 0.

**Setup (when Playwright is not yet configured):** include a dedicated Step early in the plan. See `references/playwright-practices.md` for the full setup (config, page objects, test helpers, global setup/teardown).

**When Playwright is already configured:** reference existing config for E2E verification checkboxes. If new routes are added, include both the test-writing checkbox and the PW verify checkbox.

**For non-web projects or backend-only issues:** skip Playwright entirely.

Key Playwright rules (see `references/playwright-practices.md` for details):
- **Headless by default.** No window stealing; consistent rendering.
- **`webServer` config** for automatic server lifecycle — no manual `nohup` or orphan processes.
- **`.env.test`** for test environment — single source of truth.
- **Page objects** for reusable interactions (`tests/e2e/pages/`).
- **Test data isolation** by prefix (`e2e-*`) — parallel tests don't collide.
- **Screenshots for visual validation** — light/dark mode, desktop/mobile viewports.
- **`trace: 'on-first-retry'`** — post-mortem debugging without overhead.
- **Generic login redirect:** `waitForURL(url => !url.pathname.includes("/login"))` — never hardcode destination.
- **Persistent E2E tests:** every visual verification saved in `tests/e2e/[page].spec.ts`. Screenshots go to `test-results/` (gitignored). Before writing a new test, check for an existing one — update it if the Step modifies existing UI.

## 3. Domain-Driven Design by default

When proposing Steps, follow DDD principles. Skip for issues that are purely infrastructure, config, or UI-only with no business rules. When the issue touches an existing codebase, read the current architecture first: if it already follows DDD, respect the patterns; if it doesn't, don't force a rewrite — but new code should follow DDD within its scope.

- **Rich entities with behavior.** Entities are classes, not interfaces/types. Business logic lives in the entity, not in services. Example: `Order.cancel()` enforces cancellation rules internally — the use case calls the method, not reimplements the logic.
- **Value objects for constrained concepts.** Concepts without identity that have validation rules: `Email` (format validation), `Money` (immutable, currency-aware, arithmetic methods), `DateRange` (start < end invariant). Factory methods with validation, not raw constructors.
- **Domain invariants in constructors.** If a field has constraints (e.g., balance >= 0, quantity > 0), the entity constructor enforces them — throwing on invalid input. The use case never checks what the entity should guarantee.
- **Factory methods over raw construction.** `Order.createDraft(customerId, items)` instead of `new Order({ status: 'draft', ... })` — because factory methods encode creation rules and make invalid states impossible.
- **Checkboxes must specify behavior.** "Create `Order` entity class with `cancel()`, `addItem()`, `calculateTotal()` methods and invariants" — not "Create Order type and OrderRepository interface".
