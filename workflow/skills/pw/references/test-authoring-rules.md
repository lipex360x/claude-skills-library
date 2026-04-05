# Test Authoring Rules — E2E & Visual Verification

Rules governing **when**, **what**, and **with what discipline** E2E tests are written and validated. For **how** to write them (Playwright patterns, selectors, fixtures), see `playwright-practices.md`.

---

## 1. E2E vs PW — the distinction

| Concept | What it means | Who does it |
|---------|--------------|-------------|
| **[E2E] tag** (in issue plan) | Write the Playwright test file | Developer, during implementation |
| **/pw skill** (pipeline phase) | Run tests, capture screenshots, diagnose, fix, re-run | Agent, after all steps complete |

Writing the test (`[E2E]`) and running the validation (`/pw`) are **separate activities**. The `[E2E]` step produces `.spec.ts` files. The `/pw` phase executes them, reads screenshots, and iterates on failures.

An `[E2E]` step **never** runs the tests — it only writes them. `/pw` primarily fixes **application code**, but can also touch test files in these cases:

| Situation | /pw action |
|-----------|-----------|
| Selector stale after UI change | Update the selector in the existing test |
| Timing/race condition in test | Adjust wait strategy in the existing test |
| Missing console capture fixture | Add to shared fixture or relevant test files |
| Visual bug with no test coverage | Fix the app bug, then add a minimal regression test |

What `/pw` must **never** do: write broad new test suites, expand test scope beyond the discovered bug, or loosen assertions to make a failing test pass.

---

## 2. TDD discipline for E2E steps

E2E tests follow the same RED → GREEN discipline as unit tests, but at a higher level:

### Tag ordering in issue plans

```
[RED] → [GREEN] → [INFRA] → [WIRE] → [E2E]
```

- `[E2E]` steps **must appear after** the RED/GREEN pairs for the feature they test
- You can't write an E2E test for a feature that hasn't been implemented yet
- `[E2E]` steps must mention `test`, `spec`, or `e2e` in the checkbox text

### What an [E2E] step looks like

```markdown
- [ ] `[E2E]` Write Playwright test for document upload flow — 
      happy path (PDF upload → processing → success), 
      error path (invalid file type → error message)
```

Each `[E2E]` checkbox should specify:
- **Which flow** is being tested
- **Which scenarios** (happy path, error paths, edge cases)
- Test file path when it's not obvious from the flow name

### What an [E2E] step does NOT include

- Running the tests (that's `/pw`)
- Screenshot capture or visual validation (that's `/pw`)
- Fixing test failures (that's `/pw` fix cycle)

---

## 3. Test writing quality criteria

These rules come from the issue plan validator and apply when writing `[E2E]` steps:

| Rule | Enforcement | Description |
|------|-------------|-------------|
| `e2e_mentions_test` | Error | `[E2E]` checkboxes must mention test/spec/e2e |
| `e2e_after_implementation` | Error | `[E2E]` steps appear after RED/GREEN pairs |
| One flow per test file | Convention | Don't bundle unrelated flows in one spec |
| Scenarios explicit in checkbox | Convention | List happy + error paths in the step text |

---

## 4. Pipeline position

```
Development → /review → /pw → /validate → /update-docs → /open-pr
```

### When /pw runs
- **After /review passes** — all static, semantic, and runtime checks are green
- **Only for web projects with UI changes** — skip if backend-only or no visual impact
- **Scoped to changed pages** — pre-flight identifies affected UI via `git diff`

### When /pw re-runs
- **After /validate feedback** — user tested the live app and requested changes
- The re-run cycle is: `/validate` → user feedback → developer fix → REVIEW-LITE → `/pw` re-run (modified pages only) → `/validate` re-present
- Re-runs are scoped to **modified pages only**, not the full suite

### When /pw is skipped
- No Playwright config in the project
- No UI changes in the diff (backend-only, config, docs)
- User explicitly skips (`--skip-pw` or verbal confirmation)

---

## 5. The fix cycle

When `/pw` finds failures, it enters a fix-and-rerun loop:

```
Run tests → failures? → fix app code → re-run failing tests → repeat
                                          ↑                       |
                                          +--- still failing? ----+
```

### Rules
1. **Default: fix the app, not the test** — a failing test usually means the app is wrong. Only fix the test when the app behavior is confirmed correct (stale selector, timing issue).
2. **Uncovered bugs get minimal regression tests** — if screenshots reveal a bug with no test coverage, fix the app first, then add a focused test for that specific regression. Don't expand scope.
3. **Re-run only failing tests** — don't re-run the full suite after each fix.
4. **Read screenshots after every re-run** — visual confirmation is mandatory, not optional.
5. **Check browser console even when screenshots look clean** — hydration mismatches, runtime errors, and failed network requests are bugs.
6. **Max 5 cycles** — if issues persist after 5 iterations, stop and escalate to the user.

---

## 6. What "clean" means

A `/pw` run is clean when ALL of these are true:

| Check | Criteria |
|-------|----------|
| Tests pass | All executed specs green |
| Screenshots clean | No layout breakage, overflow, misalignment, rendering artifacts |
| Console clean | No `pageerror`, no `console.error`, no failed network requests |
| Scoped correctly | Only relevant tests ran (not the entire suite for a 1-file change) |

---

## 7. Test scope decisions

| Change type | Test scope |
|-------------|-----------|
| Single component change | Tests that exercise that component's page |
| Route/page change | Tests for that route + navigation tests that traverse it |
| Layout/theme change | All visual tests (broad impact) |
| API change with UI consumer | Tests for the UI that calls that API |
| Auth flow change | All tests (auth affects every authenticated page) |

---

## 8. Cross-reference

- **Technical patterns** (selectors, page objects, fixtures, navigation helpers): `playwright-practices.md`
- **Human navigation rule** (no `page.goto` except entry point): `playwright-practices.md` § 3
- **Browser console capture fixture**: `playwright-practices.md` § 8
- **Screenshot strategies** (light/dark, desktop/mobile): `playwright-practices.md` § 7
- **Framework-agnostic config**: `playwright-practices.md` § 1, 2
