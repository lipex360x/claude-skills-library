# Issue Template

Use this structure when composing the GitHub issue body. Adapt sections to the project — not every project needs a reference files table or an architecture diagram.

## Template

```markdown
## Overview

[One paragraph: what this project/phase does and why. Include architecture if relevant — a simple ASCII diagram or bullet list of components and how they connect.]

## Part A — [Theme Name]

### Step 1: [Concise title]
- [ ] [Concrete task — include file path if known, e.g., `Create src/db/schema.ts with users table`]
- [ ] [Another task]
- [ ] [Verification: how to confirm this step works]

### Step 2: [Concise title]
- [ ] [Task]
- [ ] [Task]

## Part B — [Theme Name]

### Step 3: [Concise title]
- [ ] [Task]
- [ ] [Task]

### Step 4: [Concise title]
- [ ] [Task]

## Part C — [Theme Name]

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

## Parallel execution plan (Agent Teams)

> Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Remove this section if not using Agent Teams.

After Step [N] ([last sequential step]), spawn teammates:
- `[teammate-name]`: Steps [X-Y] — [what this teammate owns]
- `[teammate-name]`: Steps [W-Z] — [what this teammate owns]
- `[teammate-name]`: Steps [A-B] — blocked until `[dependency-teammate]` completes
```

## Section notes

### Overview
- Lead with the goal, not implementation details
- Architecture diagrams help when there are 3+ components interacting
- Mention key decisions (e.g., "SQLite for local-first, no cloud dependency")

### Parts
- Group by theme, not chronological order (though themes often map to phases)
- Good themes: "Database & Models", "API Routes", "Frontend Components", "Testing & CI", "Deployment"
- Each part should be a coherent unit of work

### Steps
- Each step = a work session (30 min to 2 hours of focused work)
- Start with a verb: "Create", "Add", "Configure", "Implement", "Set up"
- Include a verification checkbox as the last item when the step has observable output
- For projects with databases or file I/O, include a test environment setup step early (Part A). Create a `docker-compose.test.yml` (or `test` profile) to orchestrate the test stack — database, cloud service emulators, and any other dependencies. Configure `.env.test` pointing at local containers. This must exist before any test checkbox can run
- For web projects, include a CDP setup step early (Part A) — create `.claude/start-chrome.sh` and `.claude/project-settings.json` from skill templates. Configure `baseUrl`, `tabs` (what opens on launch), and `pages` (route map for navigation). This must exist before any visual verification checkbox can run
- When a step creates seed data with test credentials (users, API keys), include a checkbox to create/update a gitignored `TEST_USERS.md` at the project root with all credentials in a readable table. This is a living document — update it whenever seed data changes

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
- For web projects, include CDP-based visual verification: "Navigate to [page] via CDP and take screenshot — verify [expected state]". This catches layout issues, missing elements, and visual regressions that unit tests miss
- Cover the happy path first, then edge cases

### Parallel execution plan
- Only include when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is active
- Identify the sequential prefix (steps that must complete before parallelism starts)
- Group independent steps by layer/module — each group becomes a teammate
- Mark dependencies between teammates explicitly
- Teammates inherit the user's model by default — suggest Sonnet only if optimizing for speed/cost
- Keep to 2-4 teammates max
