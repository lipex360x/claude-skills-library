# Issue Template

Use this structure when composing the GitHub issue body. Adapt sections to the project — not every project needs a reference files table or an architecture diagram.

## Template

```markdown
## Execution mode

> **MUST use Agent Teams (`TeamCreate`).** Do NOT fall back to isolated worktree agents.

After completing Step [N] ([last sequential step]):
- `[teammate-name]`: Steps [X-Y] — [what this teammate owns]
- `[teammate-name]`: Steps [W-Z] — [what this teammate owns]
- `[teammate-name]`: Steps [A-B] — blocked until `[dependency-teammate]` completes

_Remove this section entirely if Agent Teams is not enabled._

## Overview

[One paragraph: what this project/phase does and why. Include architecture if relevant — a simple ASCII diagram or bullet list of components and how they connect.]

## Phase 1 — [Theme Name]

### Step 1: [Concise title]
- [ ] [Concrete task — include file path if known, e.g., `Create src/db/schema.ts with users table`]
- [ ] [Another task]
- [ ] [Verification: how to confirm this step works]

### Step 2: [Concise title]
- [ ] [Task]
- [ ] [Task]

## Phase 2 — [Theme Name]

### Step 3: [Concise title]
- [ ] [Task]
- [ ] [Task]

### Step 4: [Concise title]
- [ ] [Task]

## Phase 3 — [Theme Name]

### Step 5: [Concise title]
- [ ] [Task]

## Reference files (patterns to follow)

| Pattern | File |
|---------|------|
| [What this file demonstrates] | `path/to/file` |
| [Another pattern] | `path/to/other/file` |

## Verification

1. [End-to-end check: how to verify the whole phase works]
2. [Edge case or integration check]
3. [Performance or security check if applicable]

```

## Section notes

### Overview
- Lead with the goal, not implementation details
- Architecture diagrams help when there are 3+ components interacting
- Mention key decisions (e.g., "SQLite for local-first, no cloud dependency")

### Phases
- Number sequentially (Phase 1, 2, 3...) — not lettered (A, B, C)
- Group by theme, not chronological order (though themes often map to phases)
- Good themes: "Database & Models", "API Routes", "Frontend Components", "Testing & CI", "Deployment"
- Each phase should be a coherent unit of work

### Steps
- Each step = a work session (30 min to 2 hours of focused work)
- Start with a verb: "Create", "Add", "Configure", "Implement", "Set up"
- Include a verification checkbox as the last item when the step has observable output
- For projects with databases or file I/O, include a test environment setup step early (Phase 1). Create a `docker-compose.test.yml` (or `test` profile) to orchestrate the test stack — database, cloud service emulators, and any other dependencies. Configure `.env.test` pointing at local containers. Configure Husky with `pre-commit` (lint + type-check via lint-staged) and `pre-push` (tests + build). This must exist before any test checkbox can run
- For web projects, include a Playwright setup step early (Phase 1) — `playwright.config.ts` with `webServer`, page objects, test user helpers, global setup/teardown. Read `references/playwright-practices.md` for full setup. This must exist before any E2E verification checkbox can run
- When a step creates seed data with test credentials (users, API keys), include a checkbox to create/update a gitignored `TEST_USERS.md` at the project root with all credentials in a readable table. This is a living document — update it whenever seed data changes
- Include a checkbox in the last Step of Phase 1 to create `CLAUDE.md` (agent context) and `ARCHITECTURE.md` (codebase knowledge cache) at the project root. See `references/guidelines.md` for content requirements of each

### Checkboxes
- One action per checkbox — avoid "X and Y" (split into two)
- Include file paths: `Create src/routes/auth.ts` not just `Create auth routes`
- **TDD order:** for steps with new behavior, place test checkboxes before implementation checkboxes. Example:
  - `Add test for login endpoint in src/__tests__/auth.test.ts — expect 200 with valid credentials`
  - `Implement login endpoint in src/routes/auth.ts`
- For config tasks: `Configure Y in config-file.ext`

### Reference files
- Only include for existing codebases where patterns should be followed
- Point to concrete files, not directories
- Describe what pattern to extract, not just the file name

### Verification
- Describe how to confirm the entire phase works, not individual steps
- Include the actual commands or actions: "Run `bun test` — all pass", "Open http://localhost:3000 — dashboard loads"
- For web projects, include Playwright E2E verification: "Run `npm run test:e2e` — all passing". This catches layout issues, auth flows, and integration bugs that unit tests miss
- Cover the happy path first, then edge cases

### Execution mode
- Only include when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is active — remove entirely otherwise
- **Placed at the top** (before Overview) so the agent sees it first and doesn't default to isolated worktree agents
- Use directive language: "MUST use Agent Teams (`TeamCreate`)" — not descriptive "Parallel execution plan"
- Identify the sequential prefix (steps that must complete before parallelism starts)
- Group independent steps by layer/module — each group becomes a teammate
- Mark dependencies between teammates explicitly
- Teammates inherit the user's model by default — suggest Sonnet only if optimizing for speed/cost
- Keep to 2-4 teammates max
- Add inline reminders in the first parallelizable step: "⚠️ This step runs in parallel via Agent Teams — see Execution mode above"
