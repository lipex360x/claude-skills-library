# Start Issue — Guidelines

## TDD is mandatory, not optional

Every Step that introduces new behavior MUST include a test checkbox **before** the implementation checkbox — no exceptions. This is the single most important quality rule in this skill. The TDD-ordered checkboxes in the plan ARE the enforcement mechanism — when the agent executes the steps, the test-first order ensures red-green-refactor discipline naturally. No separate skill invocation is needed. Read `references/tdd-methodology.md` for the full methodology. Key principles: vertical slices (one test → one implementation → repeat, never write all tests first), test behavior through public interfaces (not implementation details), mock only at system boundaries (external APIs, not your own modules). When proposing the detailed plan, verify every step follows TDD order: test checkbox first, implementation checkbox second. If a step has no test checkbox before its implementation, it's wrong — fix it before presenting. This applies to all change types — new routes, new commands, new components, new utilities.

## Test isolation via docker-compose

Tests must never touch production data. When the codebase contains database signals (docker-compose, ORM configs, migrations/, .env with DB URLs, BaaS references like supabase/firebase), the plan MUST include test isolation as a prerequisite Step — never assume the existing test setup covers new changes. Include checkboxes for: `docker-compose.test.yml` (isolated DB on high port), `.env.test` (local container URLs), runtime safety guard (abort if not localhost), test runner config (auto-load `.env.test`), `beforeAll`/`afterAll` (migrate/teardown), and Husky git hooks (`pre-commit` for lint + type-check, `pre-push` for tests + build). If the project already has a test setup, include a checkbox to verify it covers the new changes. Read `references/development-guidelines.md` § 1 for env file separation, runtime safety guards, high ports, and full teardown requirements.

## E2E state changes go through the UI

When E2E tests need to change application state, always go through the UI (forms, buttons, navigation) — never manipulate the database directly and expect the app to see the change. Fullstack frameworks cache server-side data; direct DB writes don't trigger cache invalidation. Direct DB is valid only for setup/teardown (seed data) and assertions (verifying persistence after UI actions).

## "Full test" means unit + lint + E2E

When generating verification checkboxes that say "run full test suite", expand to all three layers: unit tests + lint + E2E (with server and database). Unit tests with mocks can pass while the schema is broken. CDP screenshots catch UI issues but don't verify persistence. Only E2E with real DB writes confirms the full stack. List the actual commands in the checkbox, not just "run tests".

## Seed data quick-reference file

When a Step creates or modifies seed data with test credentials (users, API keys, tokens), include a checkbox to create or update a gitignored `TEST_USERS.md` (or `TEST_CREDENTIALS.md`) at the project root. Format credentials as a readable table (email, password, role, relevant attributes). If the file already exists, check if the changes affect it and include an update checkbox. Without this, developers waste time digging through SQL files to find login credentials for manual testing. This file is especially important when the project has no signup flow — it's the only way to know how to log in.

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

Issue content is public and portable. Never reference local paths like `~/.brain/`, `~/.claude/`, or absolute user paths. Use paths relative to the project root (e.g., `create-skill/SKILL.md`, not `~/.brain/skills/skill-creator/SKILL.md`). This applies to checkboxes, descriptions, and any text written to the issue body.

## Visual verification via CDP (mandatory for web projects)

When the issue touches UI, verification checkboxes must use CDP: "Navigate to [page] via CDP and take screenshot to verify [expected state]". Read `references/development-guidelines.md` § 2 for setup steps, key CDP rules, and persistent test script requirements. Also see `references/cdp-best-practices.md` for the full rule set.

## ARCHITECTURE.md maintenance

Every Step that introduces a new pattern, route, table, or dependency must include a checkbox: "Update `ARCHITECTURE.md` with [specific addition]" — naming exactly what changed (e.g., "add billing query hook to Patterns section", "add `/billing` route to Routes section", "add `recharts` to Stack & dependencies"). This keeps the codebase knowledge cache current without a bulk "update everything" step at the end. If ARCHITECTURE.md doesn't exist and the project is a web app or has sufficient complexity, include a checkbox in Step 1 to generate it using the patterns discovered during codebase analysis.

## No workarounds

Every step must solve problems at their root. If a step would require a workaround (hardcoded values to bypass a bug, temporary flags, monkey-patches, `any` casts to silence type errors, skipped validations), it's a signal that the step is wrong or incomplete. Rewrite it to address the underlying issue. Workarounds create invisible tech debt that compounds across issues — what starts as "just for now" becomes permanent the moment the next issue lands on top of it.

## No unnecessary code comments

Code comments are allowed only when the logic is genuinely non-obvious — complex algorithms, unintuitive business rules, or regulatory constraints that aren't self-evident from the code. Self-documenting code (clear names, small functions, explicit types) replaces comments. Never include "add comments" or "document the code" as checkboxes — if the code needs a comment to be understood, the code needs to be rewritten.

## Web research is authorized

When the agent is blocked on a problem — unfamiliar framework behavior, unclear best practices, or an error with no obvious solution — it is authorized to search the web for best practices and solutions. This is not a last resort; it's a standard tool. Better to spend 30 seconds searching than 10 minutes guessing.

## Verification is part of the plan, not an afterthought

When the plan uses Agent Teams, the verification step checkboxes must name specific checks (not "verify everything works"). Each check maps to a row in the verification matrix the lead presents after teammates complete. This prevents improvised verification and ensures every parallel execution has consistent, comparable quality evidence. Document false positive precedents (e.g., "runtime paths in SKILL.md are legitimate, not a local-path violation") so future sessions don't re-analyze the same edge cases.

## Checkbox ownership with Agent Teams

When teammates run in parallel, they must NEVER edit the issue body directly. Progress tracking uses internal tasks (`TaskCreate`/`TaskUpdate`) — one task per unit of work within their assigned Step, with task names matching the sub-section headers from the issue. The lead monitors progress via `TaskList` and marks issue checkboxes only after verifying each teammate's output in the verification step. This prevents race conditions (GitHub's issue API has no merge — last write wins) and ensures checkboxes reflect verified completion.

## Execution strategy is a first-class decision

The choice between Agent, Teammate, and Sequential is not cosmetic — it determines cost, complexity, and correctness. Read `references/execution-strategy.md` for the full decision matrix. Default to Agent for independent work and Teammate only when coordination is genuinely needed. Sequential is always valid — parallelism is an optimization, not a requirement. The strategy must be chosen in Step 2b and reflected in the "Execution strategy" section of the issue body before the plan is presented to the user.

## Agent strategy: issue checkboxes are the sole tracker

When using Agent strategy, do NOT create internal tasks (`TaskCreate`) to mirror issue checkboxes. Agents run in background, return results, and die. The lead validates each agent's output and marks issue checkboxes directly. This avoids the dual-tracking problem where internal tasks and issue checkboxes diverge. The GitHub issue is the single source of truth.

## Progressive audit: don't wait, stream

When workers run in parallel (Agent or Teammate), audit each worker's output as soon as it completes — do NOT wait for all workers to finish before starting audits. Spawn a background audit agent immediately when a completion notification arrives, even while other workers are still running. This overlaps audit I/O with remaining worker execution, reducing total wall-clock time by the duration of the audits that run in parallel. The consolidation step at the end collects results — by then, most audits are already done and the step becomes a quick summary rather than a bottleneck.
