---
name: tdd
description: Execute Test-Driven Development with strict red-green-refactor discipline. Guides the agent through vertical slices — one test, one implementation, repeat. Use when the user says "tdd", "test first", "red green refactor", "write tests", "test driven", "let's TDD this", or wants to implement a feature with test discipline — even if they don't explicitly say "TDD."
user-invocable: true
---

# Test-Driven Development

Execute the red-green-refactor loop with strict vertical slice discipline. One test at a time, one implementation at a time — never write all tests first.

## Steps

### 1. Understand what to build

Parse `$ARGUMENTS` for the feature or behavior to implement. If no argument, ask the user what they want to build.

Read the codebase to understand:
- **Existing test patterns** — framework (Jest, Vitest, Pytest, Go test, etc.), file locations, naming conventions
- **Public interfaces** — where the new behavior will be exposed
- **Related tests** — existing tests that cover adjacent functionality

If `ARCHITECTURE.md` exists, read it first for orientation.

### 2. Plan behaviors to test

List the behaviors the feature needs — not implementation steps, but observable outcomes from the caller's perspective.

```markdown
Behaviors to test:
1. User can create an order with valid items
2. Order rejects empty cart
3. Order calculates total with tax
4. Order applies discount codes
```

Present the list and ask: **"Which behaviors matter most? Any to skip or add?"**

This is the only approval gate. After this, the loop runs autonomously.

**You can't test everything.** Focus on critical paths and complex logic. Simple getters, pass-through functions, and framework boilerplate don't need dedicated tests.

### 3. Design interface for testability

Before writing any test, consider the interface:

- **Accept dependencies, don't create them** — use dependency injection for external services
- **Return results, don't produce side effects** — pure functions are trivially testable
- **Small surface area** — fewer methods = fewer tests needed, fewer params = simpler setup

Read `references/tdd-methodology.md` for deep modules, mocking rules, and interface design patterns.

If the interface needs to change from what exists, confirm with the user before proceeding.

### 4. Execute the loop

For each behavior from Step 2, run one cycle:

**RED — Write the test first.**

```bash
# Run the test — it MUST fail
npm test -- --testPathPattern="<test-file>" 2>&1
```

The test describes behavior through the public interface. It reads like a specification: "user can checkout with valid cart" — not "checkout calls paymentService.process".

If the test passes immediately, it's testing nothing useful — either the behavior already exists or the test is wrong. Investigate before proceeding.

**GREEN — Write minimal code to pass.**

Implement just enough to make the test pass. No speculative features, no "while I'm here" additions. The test defines the scope.

```bash
# Run the test — it MUST pass now
npm test -- --testPathPattern="<test-file>" 2>&1
```

If it fails, fix the implementation — not the test. The test was written first and represents the desired behavior.

**REFACTOR — Clean up with confidence.**

After GREEN, look for refactor candidates:
- Duplication → extract function
- Long methods → break into private helpers (keep tests on public interface)
- Shallow modules → combine or deepen
- Feature envy → move logic to where data lives
- Primitive obsession → introduce value objects

**Never refactor while RED.** Get to GREEN first. Run tests after each refactor step to confirm nothing broke.

Move to the next behavior. Repeat until all behaviors are covered.

### 5. Verify

After all cycles complete:

```bash
# Run the full test suite — not just the new tests
npm test 2>&1
```

Report:
- Tests added (count and names)
- Code added/modified (files and line counts)
- Refactors performed
- Any behaviors skipped and why

## Guidelines

- **Vertical slices only.** One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Horizontal slicing (all tests first, then all code) produces tests that verify imagined behavior, not actual behavior — they become insensitive to real changes and break on harmless refactors.

- **Test behavior, not implementation.** Tests verify what the system does through public interfaces. They should survive internal refactors — if you rename a private function and tests break, those tests were testing implementation. Read `references/tdd-methodology.md` for good vs bad test examples.

- **Mock at system boundaries only.** Mock external APIs, databases (prefer test DB when possible), time/randomness. Never mock your own classes or internal collaborators — that couples tests to implementation. Use dependency injection to make boundary mocking easy.

- **One logical assertion per test.** A test that checks 5 things is really 5 tests crammed together. When it fails, you don't know which behavior broke. Split into focused tests with descriptive names.

- **Test names are specifications.** `"user can checkout with valid cart"` tells you what capability exists. `"test checkout"` tells you nothing. `"should call processPayment"` tests implementation, not behavior.

- **Adapt to the project's test stack.** Use whatever framework and conventions the project already has. Don't introduce a new test runner because you prefer it — match the existing patterns. If no patterns exist, suggest one and confirm with the user.

- **TDD applies to all layers.** Backend routes, CLI commands, library functions, UI components, database queries. The red-green-refactor loop is universal. Only skip for pure configuration files, static assets, and trivial boilerplate.

- **Avoid these anti-patterns:**
  - Writing all tests first (horizontal slicing) — each test must be written, run (RED), and satisfied (GREEN) before the next
  - Testing private methods or internal state — always go through the public interface
  - Mocking internal collaborators — mock only at system boundaries
  - Tests that verify HOW instead of WHAT — "calls service.process" vs "order is confirmed"
  - Verifying through external means (querying DB directly) instead of through the interface
  - Skipping the RED step — if the test passes before implementation, it's not testing new behavior
  - Refactoring while RED — get to GREEN first, then refactor with the safety net of passing tests
  - Adding speculative features during GREEN — implement only what the current test demands
