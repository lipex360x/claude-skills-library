---
name: validate
description: >-
  User acceptance testing — present a specific testing guide (URLs, click paths,
  expected results), collect feedback, fix issues, and loop until approved. Use
  when the user says "validate", "test it", "check the UI", "user test", "let me
  see it", "does it work", or wants to validate the running app — even if they
  don't explicitly say "validate."
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# /validate

Present a concrete testing guide for the running app, collect user feedback, and iterate fixes until the user approves. Runs after `/review` and `/pw`.

## Pre-flight

1. **Detect issue context.** Read `.claude/project-setup.json` for the current issue number. If missing, `AskUserQuestion` for the issue number.
2. **Check review-state.json.** Look for `.claude/review-state.json`. If missing, warn: "No review-state.json found -- `/review` may not have run yet. Proceeding, but quality issues may surface during validation." Continue (warning, not a block).
3. **Load issue body.** Fetch the issue via `gh issue view <number> --json body,title -q '{title: .title, body: .body}'`. Extract step descriptions and acceptance criteria for testing guide context.
4. **Detect app type.** Scan for signals: `playwright.config.*` (web), `package.json` scripts with `dev`/`start` (web/node), `docker-compose*` (containerized). Store for testing guide specificity.
5. **Check app is running.** If web project, verify dev server is reachable (e.g., `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`). If not running, warn the user and suggest starting it before proceeding.

## Steps

### 1. Build testing guide

Analyze the issue acceptance criteria, completed steps (checked checkboxes), and the git diff against main to understand what changed. Build a **specific** testing guide:

- **URLs to visit** (e.g., "Go to /checkout")
- **Actions to perform** (e.g., "Add item X to cart, click 'Pay', verify total shows R$ 42,00")
- **Expected results** (e.g., "Toast notification appears with 'Order confirmed'")
- **Edge cases to try** (e.g., "Submit the form empty -- validation errors should appear for name and email")
- **Credentials if needed** (e.g., "Login with test@example.com / password123")

Present the guide to the user via `AskUserQuestion` with the full testing guide text and options `["Starting tests now", "Guide needs adjustment"]`. If adjustment requested, refine and re-present.

### 2. Collect feedback

After the user finishes testing, collect their feedback via `AskUserQuestion`:
- Options: `["Everything works -- approved", "Found issues (I'll describe them)"]`
- If approved, skip to Step 5.
- If issues found, the user describes them in their response. Parse the feedback into actionable items.

### 3. Apply fixes

Fix each issue the user reported. Keep changes minimal and scoped to the feedback -- do not refactor unrelated code.

After applying fixes, run **REVIEW-LITE** inline:

#### REVIEW-LITE (internal quality check)

This is NOT a separate skill invocation. It is a lightweight, single-pass inline check scoped to changed files only (~10k tokens):

1. **Get changed files:** `git diff --name-only HEAD~1` (files changed by the fix commit).
2. **Static check:** Run linter and type-checker if configured (e.g., detect from `package.json` scripts). Report any errors.
3. **Semantic check:** Read each changed file. Verify against `.docs/quality.md` if it exists (DON'Ts list). Check for: hardcoded values, skipped error handling, commented-out code, debug leftovers.
4. **Fix issues found** by REVIEW-LITE before proceeding. Do not present REVIEW-LITE results to the user -- fix silently and move on.

### 4. Re-validate

After fixes + REVIEW-LITE pass:

1. If the project has Playwright, suggest the user run `/pw` to re-verify E2E tests on modified pages.
2. Re-present the testing guide (updated if the fix changed behavior) via `AskUserQuestion`.
3. Collect feedback again (same as Step 2).
4. If approved, proceed to Step 5. If more issues, return to Step 3.

There is **no hard limit** on iteration cycles. The loop runs until the user approves. Layout iteration is naturally convergent -- each cycle addresses fewer issues.

### 5. Finalize

Once approved:

1. Ensure all fix commits are pushed: `git status` and `git push` if needed.
2. Report: "User validation complete. All feedback addressed and approved."

## Error handling

| Failure | Strategy |
|---------|----------|
| App not running | Warn user with start command (e.g., `npm run dev`) -- do not start it automatically |
| Issue not found | `AskUserQuestion` for correct issue number |
| No review-state.json | Warn and continue (pre-flight step 2) |
| Linter/type-check not configured | Skip static check in REVIEW-LITE, run semantic only |
| `/pw` not available (no Playwright) | Skip E2E re-run suggestion in Step 4, rely on manual testing |

## Anti-patterns

- **Vague testing guides.** "Test the app" instead of "Go to /checkout, add item X, verify total shows Y" -- because vague guides produce vague feedback and waste cycles.
- **Fixing issues before presenting the testing guide.** The user needs to see the current state first -- because pre-emptive fixes hide the real user experience.
- **Silently re-running after user approves.** Approval means DONE -- because extra cycles after approval erode trust and waste time.
- **Starting a fix cycle without REVIEW-LITE afterward.** Every fix must pass the lightweight quality check -- because user-requested changes can introduce regressions.
- **Running full /review inside validate.** REVIEW-LITE is proportional to small feedback changes -- because spawning 3 sub-agents for a button color change wastes ~50k tokens.
- **Hardcoding cycle limits.** No "max 3 cycles" -- because artificial limits force premature approval of broken UIs.

## Next action

Run `/update-docs` to update `.docs/architecture.md` with any new patterns or routes introduced during validation fixes.
