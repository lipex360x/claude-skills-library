# Start Issue — Guidelines

## TDD is mandatory, not optional

Every Step that introduces new behavior MUST include a test checkbox **before** the implementation checkbox — no exceptions. This is the single most important quality rule in this skill. The TDD-ordered checkboxes in the plan ARE the enforcement mechanism — when the agent executes the steps, the test-first order ensures red-green-refactor discipline naturally. Read `references/tdd-methodology.md` for the full methodology. Key principles: vertical slices (one test → one implementation → repeat, never write all tests first), test behavior through public interfaces (not implementation details), mock only at system boundaries (external APIs, not your own modules). When proposing the detailed plan, verify every step follows TDD order: test checkbox first, implementation checkbox second. If a step has no test checkbox before its implementation, it's wrong — fix it before presenting. This applies to all change types — new routes, new commands, new components, new utilities.

## Test isolation via docker-compose

Tests must never touch production data. When the codebase contains database signals (docker-compose, ORM configs, migrations/, .env with DB URLs, BaaS references like supabase/firebase), the plan MUST include test isolation as a prerequisite Step — never assume the existing test setup covers new changes. Include checkboxes for: `docker-compose.test.yml` (isolated DB on high port), `.env.test` (local container URLs), runtime safety guard (abort if not localhost), test runner config (auto-load `.env.test`), `beforeAll`/`afterAll` (migrate/teardown), and Husky git hooks (`pre-commit` for lint + type-check, `pre-push` for tests + build). If the project already has a test setup, include a checkbox to verify it covers the new changes. Read `references/development-guidelines.md` § 1 for env file separation, runtime safety guards, high ports, and full teardown requirements.

## E2E state changes go through the UI

When E2E tests need to change application state, always go through the UI (forms, buttons, navigation) — never manipulate the database directly and expect the app to see the change. Fullstack frameworks cache server-side data; direct DB writes don't trigger cache invalidation. Direct DB is valid only for setup/teardown (seed data) and assertions (verifying persistence after UI actions).

## "Full test" means unit + lint + E2E

When generating verification checkboxes that say "run full test suite", expand to all three layers: unit tests + lint + E2E (with server and database). Unit tests with mocks can pass while the schema is broken. CDP screenshots catch UI issues but don't verify persistence. Only E2E with real DB writes confirms the full stack. List the actual commands in the checkbox, not just "run tests".

## Seed data quick-reference file

When a Step creates or modifies seed data with test credentials (users, API keys, tokens), include a checkbox to create or update a gitignored `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root. Format credentials as a readable table (email, password, role, relevant attributes). Without this, developers waste time digging through SQL files to find login credentials for manual testing.

## Domain-Driven Design by default

Rich domain entities with behavior, value objects, and clear layer separation (domain → application → infrastructure). Place new business logic in the domain layer. Read `references/development-guidelines.md` § 3 for full DDD principles and when to skip.

## Codebase-aware plans

The most valuable part of this skill is producing checkboxes with concrete file paths and references to existing patterns. Always read the codebase before planning — generic checkboxes like "implement the feature" are a failure mode.

## Acceptance criteria are success criteria, not the plan

Keep the original acceptance criteria as top-level checkboxes. Steps are the implementation plan to achieve those criteria. Mark an acceptance criterion as done when all its related Steps are complete.

## English for all issue content

Issues, checkboxes, and branch names are always in English because issue content is public, portable, and often read by collaborators or tools that expect English. Communication with the user follows their language preference.

## Don't over-plan

Later Steps can be less detailed than early ones because over-specifying Step 5 when Step 1 hasn't started wastes planning effort on assumptions that will change once early work is done. The first Step should have precise checkboxes; the last can be higher-level — the user will refine as they go.

## Steps are work sessions

Each Step should represent a focused work session — something you can complete, commit, and verify before moving on. Too large = lost focus. Too small = overhead.

## Backlog issues are standalone — no Phases

Unlike project issues created by `start-new-project` (which use "Phase 1: Theme", "Phase 2: Theme"), backlog issues are self-contained items. They use Steps directly, never Phases. If a backlog item grows too large (8+ steps), split it into multiple independent backlog issues — each with a descriptive title, 3-8 steps, and its own verification. All split issues are added to the board's Backlog column and reference each other.

## No local environment paths in issues

Issue content is public and portable. Never reference local paths like `~/.brain/`, `~/.claude/`, or absolute user paths. Use paths relative to the project root (e.g., `src/domain/account.ts`, not `/Users/dev/project/src/domain/account.ts`). This applies to checkboxes, descriptions, and any text written to the issue body.

## Visual verification via Playwright (mandatory for web projects)

When the issue touches UI, include `[E2E]` checkboxes to write Playwright tests: "Write Playwright test for [page] in `tests/e2e/[page].spec.ts` — verify [expected state], screenshots". Read `references/playwright-practices.md` for setup (config, page objects, test helpers, global setup/teardown). The actual running/verification of these tests is handled by the `/pw` phase after development.

## .docs/architecture.md maintenance

Every Step that introduces a new pattern, route, table, or dependency should be documented. The `.docs/architecture.md` update happens via the `/update-docs` phase after development — not inline during steps. However, the plan should reference what will change (e.g., "new `/billing` route", "new `recharts` dependency") so the docs update is informed.

## No workarounds

Every step must solve problems at their root. If a step would require a workaround (hardcoded values to bypass a bug, temporary flags, monkey-patches, `any` casts to silence type errors, skipped validations), it's a signal that the step is wrong or incomplete. Rewrite it to address the underlying issue.

## No unnecessary code comments

Code comments are allowed only when the logic is genuinely non-obvious — complex algorithms, unintuitive business rules, or regulatory constraints that aren't self-evident from the code. Self-documenting code (clear names, small functions, explicit types) replaces comments. Never include "add comments" or "document the code" as checkboxes.

## Web research is authorized

When the agent is blocked on a problem — unfamiliar framework behavior, unclear best practices, or an error with no obvious solution — it is authorized to search the web. Better to spend 30 seconds searching than 10 minutes guessing.
