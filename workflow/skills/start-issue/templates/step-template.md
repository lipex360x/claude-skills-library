# Step Template

Use this structure when rewriting the issue body with a detailed plan. Adapt to the issue — not every issue needs all sections.

## Template

```markdown
## Execution strategy

> **[Agent pattern / Teammate pattern]** — [1-line rationale from decision matrix].

[Choose ONE of the templates below based on Step 2b decision. Remove this section entirely if Sequential or Agent Teams is not enabled.]

### If Agent pattern:

> **Agent pattern** — steps are independent and follow the same template. Workers run in background and return results. Lead validates and marks checkboxes.

After completing Step [N] (last sequential step), spawn background agents:
- Agent 1: Step [X] — [scope] ([count] items)
- Agent 2: Step [Y] — [scope] ([count] items)

**Agent prompt pattern:** "[Context + golden example]. For each item in your batch: [read input], [produce output]. Report completion when done."

### If Teammate pattern:

> **Teammate pattern** — steps have dependencies or shared state requiring coordination.

After completing Step [N] (last sequential step):
- `[teammate-name]`: Steps [X-Y] — [what this teammate owns]
- `[teammate-name]`: Steps [W-Z] — [what this teammate owns]

**Teammate prompt pattern:** "Read issue #<number> Step X via `gh issue view`. Create one internal task per sub-section in your Step. Execute each unit, mark internal tasks as completed. Do NOT edit the issue body — lead verifies and marks checkboxes."

**Teammate task pattern:** Create one task per sub-section in your assigned Step. Task names must match sub-section headers for lead monitoring.

## What

[Keep or slightly improve the original description]

## Why

[Keep or slightly improve the original motivation]

## Acceptance criteria

- [ ] [Original criterion 1]
- [ ] [Original criterion 2]
- [ ] [Original criterion 3]

## Step 1 — [Concise title]

- [ ] `[INFRA]` [Concrete task — include file path, e.g., `Create src/templates/readme.md with standard sections`]
- [ ] `[INFRA]` [Another task — specific and verifiable]
- [ ] `[AUDIT]` Audit all Step 1 code against `quality.md` — review every file against every DON'T/DO rule

## Step 2 — [Concise title]

- [ ] `[RED]` [Write failing test with file path and expected behavior]
- [ ] `[GREEN]` [Implement to make test pass with file path]
- [ ] `[AUDIT]` Audit all Step 2 code against `quality.md` — review every file against every DON'T/DO rule

## Step 3 — [Concise title]

- [ ] `[RED]` [Test]
- [ ] `[GREEN]` [Implementation]
- [ ] `[E2E]` [Playwright test with file path]
- [ ] `[PW]` [Run tests, read screenshots, fix visual issues]
- [ ] `[HUMAN]` Present screenshots to user and wait for visual approval
- [ ] `[AUDIT]` Audit all Step 3 code against `quality.md` — review every file against every DON'T/DO rule

```

## Section notes

### What / Why
- Preserve the original author's intent — don't rewrite substantially
- Improve clarity only if the original is ambiguous

### Acceptance criteria
- Copy the original checkboxes exactly
- These are the "definition of done" — they stay at the top
- Steps below are the HOW, acceptance criteria are the WHAT

### Steps
- Each Step = a focused work session (30 min to 2 hours)
- Start title with a verb: "Define", "Add", "Update", "Configure", "Implement"
- Number Steps sequentially across the entire issue (Step 1, 2, 3... not per-section)
- Include a verification checkbox as the last item when the Step has observable output
- For changes involving databases or file I/O, include test environment setup early — create or verify `docker-compose.test.yml` (or `test` profile) to orchestrate the test stack. Configure `.env.test` pointing at local containers. Configure Husky with `pre-commit` (lint + type-check via lint-staged) and `pre-push` (tests + build). This must exist before any test checkbox can run
- For web projects with UI changes, include Playwright setup as an early Step if `playwright.config.ts` doesn't exist yet. If it does, add E2E tests with screenshots for new pages — and always include both the test-writing and the verification cycle checkboxes (see Playwright verification below)

### Checkbox tags

Every checkbox MUST have a tag prefix: `` `[TAG]` ``. Tags classify the work and enable automated validation via `validate-issue.sh`.

**Valid tags:** `[RED]`, `[GREEN]`, `[INFRA]`, `[WIRE]`, `[E2E]`, `[PW]`, `[HUMAN]`, `[DOCS]`, `[AUDIT]`

**Tag ordering within each step:** RED → GREEN → INFRA → WIRE → E2E → PW → HUMAN → DOCS → AUDIT

**Tag chain rules:**
- `[GREEN]` requires `[RED]` earlier in the step (otherwise use `[INFRA]`)
- `[E2E]` requires `[PW]` in the same step
- `[PW]` requires `[HUMAN]` in the same step (visual approval gate)
- `[AUDIT]` is mandatory in every step and must be the last checkbox
- `[DOCS]` is recommended when the step has `[GREEN]` or `[WIRE]`
- Frontend UI work (components, layouts, pages) requires the full chain: `[E2E]` → `[PW]` → `[HUMAN]`

**Format:** `- [ ] \`[TAG]\` Description of the task`

**Max length:** 200 characters per checkbox text (after the tag). If longer, break into multiple checkboxes with the same tag — never shorten to lose context.

### Checkboxes
- One action per checkbox — avoid "X and Y" (split into two)
- Include file paths: `Create src/templates/readme.md` not just `Create readme template`
- **Vertical TDD slices** — pair each test with its implementation, one by one. Never group all tests together then all implementations:
  ```
  - [ ] `[RED]` Write test "transfer reduces sender balance" in `account.test.ts`
  - [ ] `[GREEN]` Implement `Account.transfer(amount, target)` for the debit side
  - [ ] `[RED]` Write test "transfer rejects insufficient funds"
  - [ ] `[GREEN]` Add balance guard to `Account.transfer()`
  - [ ] `[AUDIT]` Audit all code against `quality.md`
  ```
  NOT this (horizontal TDD — forbidden):
  ```
  - [ ] Write tests in `account.test.ts` — transfer, deposit, withdraw
  - [ ] Create Account entity, TransferService, repository
  ```
- **Rich domain entities, not anemic models** — when the issue involves domain logic, checkboxes must specify entity behavior, not just types/interfaces:
  ```
  - [ ] `[GREEN]` Create `Account` entity in `domain/account.ts` — invariants (balance >= 0), `transfer()` with overdraft guard
  - [ ] `[GREEN]` Create `Money` value object — immutable, currency-aware, `add()`/`subtract()`, factory with validation
  ```
  NOT this (anemic model):
  ```
  - [ ] Create `Account` entity type, AccountRepository interface
  ```
- For config tasks: `Configure Y in config-file.ext`
- **Playwright visual verification cycle** — for every Step that creates or modifies UI, include three checkboxes:
  ```
  - [ ] `[E2E]` Write Playwright test for [page] in `tests/e2e/[page].spec.ts` — verify [expected state], screenshots
  - [ ] `[PW]` Run `npm run test:e2e -- [page].spec.ts`, read screenshots, fix visual issues until all pass
  - [ ] `[HUMAN]` Present screenshots to user and wait for visual approval before proceeding
  ```
  The first checkbox writes the test. The second is the feedback loop: **run → read screenshots → analyze visually → fix → re-run** until the UI matches expectations. Writing the test alone is NOT sufficient — the agent must actively view and analyze the screenshots before marking as done. See `references/development-guidelines.md` § 2 for the full cycle.

### Parallelizable Steps (Agent Teams)
When a Step will be assigned to a teammate, make it self-contained:
- Start with a **"Before starting"** block listing references to read (repo-relative paths)
- Use **sub-sections** (`### unit-name (path/)`) for each unit of work with individual checkboxes
- The teammate reads the issue step directly — no context duplication in the TeamCreate prompt

Example:
```markdown
## Step 2 — Migrate batch A

⚠️ This step runs in parallel via Agent Teams — see Execution mode above.

**Before starting:** Read these references:
- `path/to/reference-1.md` — what it provides
- `path/to/reference-2.md` — what it provides

### component-a (`src/components/a/`)
- [ ] Task 1
- [ ] Task 2
- [ ] Verify

### component-b (`src/components/b/`)
- [ ] Task 1
- [ ] Task 2
- [ ] Verify
```

### Consolidation Step (Agent Teams)
The final step consolidates progressive audit results — the actual auditing happens in background as teammates deliver (see Step 7 in SKILL.md):
- Each checkbox names a specific consolidation action
- The lead collects audit results and presents the verification matrix
- Flag failures for remediation, document false positives

Example:
```markdown
## Step 4 — Consolidate audit results and push

- [ ] Collect progressive audit results for all [units] — present consolidated verification matrix
- [ ] Flag any audit failures for remediation
- [ ] Document false positives with reasoning
- [ ] Push all changes
```

### Sizing
- 2-8 Steps per issue (simple issues: 2-3, complex: 5-8)
- 2-6 checkboxes per Step (recommended), max 8 (hard limit — validator errors above this)
- Max 200 chars per checkbox text — if longer, break into multiple checkboxes (never shorten)
- If you need 9+ Steps, the issue MUST be split into multiple issues
- `validate-issue.sh` enforces all sizing and structural rules — run it after editing
