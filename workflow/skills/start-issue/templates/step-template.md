# Step Template

Use this structure when rewriting the issue body with a detailed plan. Adapt to the issue — not every issue needs all sections.

## Template

```markdown
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

## Step 2 — [Concise title]

- [ ] `[RED]` [Write failing test with file path and expected behavior]
- [ ] `[GREEN]` [Implement to make test pass with file path]
- [ ] `[RED]` [Next failing test]
- [ ] `[GREEN]` [Next implementation]

## Step 3 — [Concise title]

- [ ] `[RED]` [Test]
- [ ] `[GREEN]` [Implementation]
- [ ] `[WIRE]` [Connect frontend to backend — mention integration point]
- [ ] `[E2E]` [Write Playwright test for page in `tests/e2e/page.spec.ts` — verify expected state, screenshots]

## Post-development phases

After all steps are complete, run in order:

1. `/review` — Quality review (static + semantic + runtime)
2. Fix issues from review report, then re-run `/review` if needed
3. `/pw` — Playwright visual verification (web projects)
4. `/validate` — User tests live app, provides feedback (UI changes)
5. `/update-docs` — Update .docs/architecture.md + .docs/project.md
6. `/review --final` — Final quality gate (delta only)
7. `/open-pr` — Create pull request
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
- For changes involving databases or file I/O, include test environment setup early — create or verify `docker-compose.test.yml`, `.env.test`, runtime safety guard, Husky hooks
- For web projects with UI changes, include Playwright setup as an early Step if `playwright.config.ts` doesn't exist yet. If it does, add `[E2E]` checkboxes for new pages

### Checkbox tags

Every checkbox MUST have a tag prefix: `` `[TAG]` ``. Tags classify the work and enable automated validation via `validate-issue.sh`.

**Valid tags:** `[RED]`, `[GREEN]`, `[INFRA]`, `[WIRE]`, `[E2E]`

**Tag ordering within each step:** RED → GREEN → INFRA → WIRE → E2E

RED and GREEN may alternate within a step (vertical TDD: RED→GREEN→RED→GREEN is valid and encouraged).

**Tag chain rules:**
- `[GREEN]` requires `[RED]` earlier in the step (otherwise use `[INFRA]`)
- No consecutive `[GREEN]` without `[RED]` between them — each implementation needs its own failing test first
- No consecutive `[RED]` without `[GREEN]` between them — write the test, make it pass, then next test
- `[WIRE]` must mention integration/connection
- `[E2E]` must mention test/spec. Should appear after RED/GREEN pairs in the step

**Format:** `- [ ] \`[TAG]\` Description of the task`

**Max length:** 300 characters per checkbox text (after the tag). If longer, break into multiple checkboxes — never shorten to lose context.

### Checkboxes
- One action per checkbox — avoid "X and Y" (split into two)
- Include file paths: `Create src/templates/readme.md` not just `Create readme template`
- **Vertical TDD slices** — pair each test with its implementation, one by one:
  ```
  - [ ] `[RED]` Write test "transfer reduces sender balance" in `account.test.ts`
  - [ ] `[GREEN]` Implement `Account.transfer(amount, target)` for the debit side
  - [ ] `[RED]` Write test "transfer rejects insufficient funds"
  - [ ] `[GREEN]` Add balance guard to `Account.transfer()`
  ```
  NOT this (horizontal TDD — forbidden):
  ```
  - [ ] Write tests in `account.test.ts` — transfer, deposit, withdraw
  - [ ] Create Account entity, TransferService, repository
  ```
- **Rich domain entities, not anemic models** — when the issue involves domain logic, checkboxes must specify entity behavior:
  ```
  - [ ] `[GREEN]` Create `Account` entity in `domain/account.ts` — invariants (balance >= 0), `transfer()` with overdraft guard
  - [ ] `[GREEN]` Create `Money` value object — immutable, currency-aware, `add()`/`subtract()`, factory with validation
  ```
- For config tasks: `Configure Y in config-file.ext`

### Post-development phases
This section is **mandatory** at the bottom of every issue body. It tells the developer (and future agents) what to run after all steps are complete. Copy the template exactly — do not customize per issue.

### Sizing
- 2-8 Steps per issue recommended, 10 warn, 12 hard limit
- 1-8 checkboxes per Step recommended, 10 hard limit
- Max 300 chars per checkbox text — if longer, break into multiple checkboxes (never shorten)
- If you need 13+ Steps, the issue MUST be split into multiple issues
- `validate-issue.sh` enforces all sizing and structural rules — run it after editing
