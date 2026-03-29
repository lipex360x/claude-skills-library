---
name: tdd
description: >-
  Execute Test-Driven Development with strict red-green-refactor discipline.
  Guides the agent through vertical slices — one test, one implementation,
  repeat. Use when the user says "tdd", "test first", "red green refactor",
  "write tests", "test driven", "let's TDD this", or wants to implement a
  feature with test discipline — even if they don't explicitly say "TDD."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Test-Driven Development

Execute the red-green-refactor loop with strict vertical slice discipline. One test at a time, one implementation at a time — never write all tests first.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `feature` | $ARGUMENTS | yes | Non-empty description of behavior to implement | AUQ: "What feature or behavior do you want to build?" |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Test files | Project test directory (follows existing conventions) | yes | Test framework format |
| Implementation files | Project source directory | yes | Source code |
| Report | stdout | no | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Project source code | Project directory | R/W | Source files |
| Test suite | Project test directory | R/W | Test files |
| ARCHITECTURE.md | Project root (if exists) | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Project has a test framework configured → if not: AUQ suggesting common frameworks for the detected language — stop.
2. Test runner executes successfully (even with 0 tests) → if not: "Test runner is broken — fix before TDD." — stop.
3. `$ARGUMENTS` contains a feature description → if not: AUQ: "What feature or behavior do you want to build?" — stop.

</pre_flight>

## Steps

### 1. Understand what to build

Parse `$ARGUMENTS` for the feature or behavior to implement.

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

If any existing tests broke, fix them — regressions from new code are implementation bugs, not test problems.

### 6. Report

Present concisely:
- **What was done** — behaviors implemented, test count, files created/modified
- **Tests added** — count and names
- **Code added/modified** — files and line counts
- **Refactors performed** — what was cleaned up during refactor phases
- **Behaviors skipped** — any from the plan that were skipped and why
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered (or "none")

## Next action

Run the full test suite to confirm everything passes, then `/push` to commit the changes.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — test framework detected and working
2. **Steps completed?** — all planned behaviors have RED → GREEN → REFACTOR cycles
3. **Output exists?** — test files and implementation files created as declared
4. **Anti-patterns clean?** — no horizontal slicing, no implementation-coupled tests, no mocking of internal collaborators
5. **Approval gate honored?** — user confirmed behavior list before loop started

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (produces code and tests, not prose)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| Test framework not found | AUQ suggesting frameworks for the detected language → stop |
| Test runner broken | Report error details → stop (user must fix environment first) |
| Test passes immediately (RED phase) | Investigate: either behavior exists or test is wrong — report finding, adjust |
| Implementation breaks existing tests | Fix implementation, not tests — regressions are implementation bugs |
| Partial completion (some behaviors done) | Report what succeeded, list remaining behaviors for next session |

## Anti-patterns

- **Horizontal slicing.** Writing all tests first, then all implementations — because each test must respond to what you learned from the previous cycle; batch-writing produces tests that verify imagined behavior.
- **Testing private methods.** Accessing internal state or private functions directly — because tests coupled to internals break on harmless refactors and don't verify actual behavior.
- **Mocking internal collaborators.** Mocking your own classes instead of only system boundaries — because this couples tests to implementation details and makes refactoring painful.
- **Implementation-coupled assertions.** Verifying HOW instead of WHAT (e.g., "calls service.process" vs "order is confirmed") — because these tests break on any internal change.
- **Skipping the RED step.** Not running the test before implementation — because if the test passes before implementation, it's testing nothing new.
- **Refactoring while RED.** Cleaning up code when a test is failing — because you have no safety net to catch regressions; get to GREEN first.
- **Speculative features during GREEN.** Adding more than the current test demands — because untested code is unverified code.
- **Verifying through external means.** Querying the DB directly instead of through the interface — because this bypasses the contract and tests infrastructure, not behavior.

## Guidelines

- **Vertical slices only.** One test → one implementation → repeat. Each test responds to what you learned from the previous cycle — because horizontal slicing produces tests that verify imagined behavior, not actual behavior.

- **Test behavior, not implementation.** Tests verify what the system does through public interfaces. They should survive internal refactors — if you rename a private function and tests break, those tests were testing implementation. Read `references/tdd-methodology.md` for good vs bad test examples.

- **Mock at system boundaries only.** Mock external APIs, databases (prefer test DB when possible), time/randomness. Never mock your own classes or internal collaborators — because that couples tests to implementation.

- **One logical assertion per test.** A test that checks 5 things is really 5 tests crammed together — because when it fails, you don't know which behavior broke.

- **Test names are specifications.** `"user can checkout with valid cart"` tells you what capability exists — because `"test checkout"` tells you nothing and `"should call processPayment"` tests implementation.

- **Adapt to the project's test stack.** Use whatever framework and conventions the project already has — because introducing a new test runner creates unnecessary churn.

- **TDD applies to all layers.** Backend routes, CLI commands, library functions, UI components, database queries — because the red-green-refactor loop is universal. Only skip for pure configuration files, static assets, and trivial boilerplate.
