---
name: pw
description: >-
  Run Playwright E2E tests, capture screenshots and browser console errors,
  visually diagnose issues, fix, and re-run until clean. Use this skill when
  the user says "pw", "playwright", "run e2e", "visual check", "check
  screenshots", "verify the UI", or wants visual validation of web changes
  — even if they don't explicitly say "playwright."
model: opus
effort: medium
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

# /pw

Run Playwright E2E tests against the live app, capture screenshots + browser console errors, read and diagnose visual issues, fix the app code, and re-run until all tests pass clean.

## Pre-flight

1. **Playwright config exists?** Glob for `playwright.config.*` at project root. If missing: "No Playwright config found. Set up Playwright first or skip /pw." — stop.
2. **Read `.claude/project-setup.json`** for project-specific flags: `headed` (run with browser visible), `project` (Playwright project name to use, e.g. "chromium", "mobile"). Store for Step 2.
3. **Dev server running?** Check if the `baseURL` from the Playwright config is reachable (`curl -s -o /dev/null -w "%{http_code}"` the URL). If not reachable: warn user the dev server may be down — the `webServer` config may auto-start it, but if tests fail with connection errors, the server needs attention.
4. **Identify changed pages.** Detect the base branch (`main` or `master` — check which exists) and run `git diff <base-branch> --name-only`. Filter for files that affect UI (components, pages, routes, layouts, styles). Store as `changed_scope` — used to decide which tests to run.
5. **Locate test files.** Read the `testDir` from the Playwright config and list available test files. Match against `changed_scope` to determine which tests are relevant.

## Steps

### 1. Run E2E tests

Run Playwright tests scoped to the changed pages when possible:

```bash
npx playwright test <matched-test-files> --reporter=list
```

If no specific tests match the changed scope, run the full suite. Use flags from project-setup.json:
- If `headed: true` → add `--headed`
- If `project` is set → add `--project=<value>`

**Browser console capture.** Before running tests, verify that test files listen for browser errors. If the project uses a shared test setup (e.g., `beforeEach` in a base fixture), check there. The tests should capture:
- `page.on('pageerror')` — uncaught exceptions
- `page.on('console', msg => msg.type() === 'error')` — console.error calls

If no console capture exists in the test infrastructure, add it to a shared fixture or the relevant test files before running.

### 2. Analyze results

**If tests pass:** Check if tests generated screenshots (look in `test-results/` or the path configured in the Playwright config). If screenshots exist, read them using the Read tool and visually inspect each one for:
- Layout breakage (overlapping elements, broken grids, overflow)
- Missing or misaligned content
- Dark/light mode rendering issues
- Mobile vs desktop inconsistencies
- Hydration artifacts (flash of unstyled content, duplicate elements)

**If tests fail:** Read the failure output. Classify each failure:
- **App bug** — the application code is wrong. Proceed to Step 3.
- **Test infrastructure** — config, selector, or timing issue. Fix the test only if the app behavior is confirmed correct. Never mask an app bug by loosening a test.

**Browser console errors.** Review any captured `pageerror` or `console.error` output. Flag:
- Hydration mismatches
- Runtime exceptions (TypeError, ReferenceError)
- Unhandled promise rejections
- Failed network requests (4xx/5xx)

These are bugs even if the screenshot looks fine — fix before proceeding.

### 3. Fix and re-run

Classify the problem and fix accordingly:

- **App bug** (wrong behavior, broken layout, missing element) → fix the application code.
- **Stale test** (selector outdated after UI change, wrong expected text, timing issue) → fix the existing test. Never mask an app bug by loosening assertions — only fix the test when the app behavior is confirmed correct.
- **Missing test infrastructure** (no console capture fixture, no shared setup) → add to shared fixtures or relevant test files.
- **Uncovered bug** (visual issue found via screenshots that no test catches) → fix the app bug first, then add a focused test for the regression. Keep the new test minimal — cover the discovered bug, don't expand scope.

After each fix:

1. Re-run only the failing tests
2. Capture new screenshots
3. Read the new screenshots — confirm the fix visually
4. Check browser console is clean

**Repeat** Steps 2-3 until:
- All tests pass
- All screenshots look correct (visually confirmed by reading them)
- No browser console errors

**Max 5 cycles.** If issues persist after 5 fix-and-rerun cycles, stop and report what remains broken. Ask the user how to proceed.

### 4. Summary

Report:
- **Tests run** — count and which files
- **Screenshots reviewed** — list with visual status (clean / issues found and fixed)
- **Browser console** — clean or errors found and fixed
- **Cycles** — how many fix-and-rerun iterations were needed

**CRITICAL RULE: E2E tests must navigate like a human.** Tests must reach pages through UI interactions — clicking links, menus, sidebar items, buttons. A human does not type URLs into the address bar to navigate an app. The ONLY acceptable `page.goto()` is for the initial entry point (login page or home page). All subsequent navigation must happen through clicks. Read `references/playwright-practices.md` for the full rationale and patterns. Read `references/test-authoring-rules.md` for the distinction between [E2E] steps (writing tests) and /pw (running/validating), fix cycle discipline, and scope decisions.

## Error handling

| Failure | Strategy |
|---------|----------|
| No Playwright config | Stop — tell user to set up Playwright first |
| Dev server unreachable | Warn — Playwright `webServer` may auto-start it. If tests fail with ECONNREFUSED, ask user to start the server |
| All tests fail on first run | Check if this is a fresh setup (no prior passing state). If so, focus on getting one test green first — fix app code, not tests. Never loosen assertions even on fresh setup |
| Screenshot read fails | Verify file path from test output. Screenshots may be in `test-results/` or a custom path from config |
| Browser console errors but tests pass | These are still bugs. Fix before declaring clean |
| Persistent failures after 5 cycles | Stop, report remaining issues, ask user for direction |

## Anti-patterns

- **Running with default config without reading project-setup.json** — because the project may specify `headed` mode or a specific Playwright `project` that changes behavior.
- **Fixing test infrastructure instead of the actual app bug** — because a failing test usually means the app is wrong, not the test. Only fix tests when the app behavior is confirmed correct.
- **Running against stale build** — because the dev server must reflect the latest code. If using a build step, verify it ran after the latest changes.
- **Capturing screenshots but not reading them** — because screenshots ARE the validation. Taking them without visual analysis defeats the purpose of /pw.
- **Using `page.goto()` for navigation instead of clicking UI elements** — because E2E tests must simulate real user behavior. Humans click links and menus, not type URLs. The only valid `page.goto()` is the initial entry point.
- **Running all tests when only specific pages changed** — because scoped runs are faster and give clearer signal. Use `changed_scope` from pre-flight to target relevant tests.

## Next action

`/validate` — present a testing guide to the user for manual visual validation of the running app.
