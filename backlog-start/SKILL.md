---
name: backlog-start
description: Pull a backlog issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks. Use this skill when the user says "backlog start", "start issue", "pull from backlog", "work on issue #N", or wants to begin implementing a backlog item — even if they don't explicitly say "backlog."
user-invocable: true
---

# Backlog Start

Turn a backlog issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then set up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

## Steps

### 1. Select issue

Parse `$ARGUMENTS` for an issue number. Accept both direct numbers (`2`) and index references (`#2`).

If no argument provided, list open issues in the "Backlog" milestone:

```bash
gh issue list --milestone "Backlog" --state open --json number,title -q '.[] | "#\(.number) — \(.title)"'
```

Present the list with `AskUserQuestion` for the user to pick one.

If the milestone doesn't exist or has no issues, inform the user and stop.

### 2. Analyze the issue

Fetch the issue body:

```bash
gh issue view <number> --json body,title,labels -q '{title: .title, labels: [.labels[].name], body: .body}'
```

Extract:
- **Title** — will become the branch slug
- **What/Why** — context for planning
- **Acceptance criteria** — the high-level checkboxes to expand into detailed steps

Also analyze the **current codebase** to inform the plan. Read relevant files, understand existing patterns, identify where changes will land. This context is essential for writing concrete checkboxes with file paths.

**CDP detection (for web projects).** Check two things:

1. **CDP already configured?** Look for `.claude/project-settings.json`. If it exists and has a `chrome.cdp` field, CDP is ready — store the `pages` map for use in verification checkboxes.

2. **Web project with frontend?** If CDP is not configured, determine if this is a web project with a frontend layer. Check for signals: `package.json` with frontend frameworks (react, vue, svelte, next, nuxt, remix, astro, angular, solid), HTML template files, a `pages/` or `app/` directory with UI components, or a dev server config (vite, webpack, next.config). Store the result — you **MUST** use it in Step 3 to decide whether to include CDP setup.

### 2b. Check Agent Teams capability

Run `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to determine if Agent Teams is enabled (value `1`). Store the result — you **MUST** use it in Step 3 to decide whether to include the parallel execution plan. This check is not optional.

### 3. Propose the detailed plan

Read `templates/step-template.md` for the expected format.

Transform the high-level acceptance criteria into a detailed plan with **Steps** and checkboxes. Each acceptance criterion typically expands into 1-3 Steps, each with 2-6 concrete checkboxes.

**Apply CDP detection result from Step 2:**

- **CDP already configured** (`.claude/project-settings.json` exists): use the `pages` map to write verification checkboxes with the pattern "Navigate to [page] via CDP and take screenshot to verify [expected state]". No setup Step needed — but if this issue introduces new routes, include a checkbox to update the `pages` map in `project-settings.json`.
- **Web project without CDP**: include a **Step 1 — Configure CDP for visual verification** before all other Steps. Checkboxes:
  - `Create .claude/start-chrome.sh` from the start-new-project skill template (cross-platform Chrome launcher with `--remote-debugging-port=9222`)
  - `Create .claude/project-settings.json` with `baseUrl` pointing to the dev server, `tabs` with the app URL, and `pages` mapping all known routes. This file is a living document — whenever a Step creates new routes or pages, include a checkbox to update the `pages` map
  - `Verify CDP connection — run .claude/start-chrome.sh and confirm Playwright can connect via connectOverCDP`
  - Subsequent Steps should use CDP verification checkboxes for any UI-facing changes.
- **Not a web project**: skip CDP entirely.

Present the full proposed issue body in a fenced code block. The structure:

- **What** — keep the original description (or improve it slightly)
- **Why** — keep the original motivation
- **Acceptance criteria** — keep original checkboxes as-is (these are the success criteria)
- **Steps** — the new detailed breakdown:
  - Numbered Steps with concise titles
  - Each Step has checkboxes with specific, verifiable actions
  - Include file paths when the codebase structure is known
  - Include verification checkboxes where steps have observable output

Sizing guidelines:
- 2-8 Steps total (depending on issue complexity)
- 2-6 checkboxes per Step (TDD steps naturally have more checkboxes — test + implementation pairs)
- Each checkbox = one focused action completable in a single work session

If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled (value `1`), also analyze the Steps for parallelism and append a **Parallel execution plan** section to the proposed issue body:

```markdown
## Parallel execution plan (Agent Teams)

> Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

After Step N (last sequential dependency), spawn teammates:
- `teammate-name`: Steps X-Y — description
- `teammate-name`: Steps W-Z — description
- `teammate-name`: Steps A-B — blocked until teammate-name completes
```

Rules for the parallel plan:
- **Identify the sequential prefix** — Steps that must run first because everything depends on them (e.g., template definition, shared types). These stay with the lead.
- **Group independent Steps by layer** — each group becomes a teammate.
- **Mark blocked teammates** — if a teammate depends on another's output, note it explicitly.
- **Keep it practical** — 2-4 teammates max.

If Agent Teams is not enabled, skip this section entirely.

**Before presenting the plan, confirm:** if Agent Teams is enabled (Step 2b), does the plan include a "Parallel execution plan" section? If not, add it now — this is mandatory when Agent Teams is active.

**Wait for the user's approval before proceeding.** This is the only approval gate. The user may request changes — iterate until they approve.

### 4. Update the issue

After approval, rewrite the issue body with the detailed plan:

```bash
gh issue edit <number> --body "<approved body>"
```

Preserve the original title and labels. The issue stays in the Backlog milestone — it will be moved to an active milestone if the project uses them.

### 5. Create branch

```bash
git checkout main && git pull
git checkout -b feat/<number>-<slug>
git push -u origin feat/<number>-<slug>
```

Derive `<slug>` from the issue title (kebab-case, max 40 chars).

### 6. Create tasks

Parse the Steps from the approved plan. Create a `TaskCreate` for each **Step** (not each checkbox — Steps are the right granularity for tasks).

Each task:
- **subject** — the Step title (e.g., "Step 1: Define README template")
- **description** — the checkboxes within that Step, so the agent knows what to accomplish
- **activeForm** — present continuous form for the spinner

Set up `addBlockedBy` dependencies between tasks when Steps have sequential dependencies.

### 7. Spawn teammates (if parallel plan approved)

If the approved issue body contains a "Parallel execution plan" section, offer to execute it:

- Present the plan with `AskUserQuestion` options `["Sim, rodar com teammates", "Não, vou fazer sequencial"]`.
- If approved, spawn teammates using `TeamCreate` following the plan from the issue. Teammates inherit the user's model by default — suggest Sonnet only if the user wants to optimize for speed or cost.
- The lead completes the sequential prefix, then teammates work in parallel on their assigned Steps.

If the issue has no parallel plan (Agent Teams not enabled), skip this step.

### 8. Summary

Present concisely:
- Branch name
- Issue URL (linked)
- Task count and first task suggestion
- Total Steps and checkboxes count
- Remind: use `closes #N` in PR descriptions

## Guidelines

- **TDD by default.** Every Step that introduces new behavior must include a test checkbox **before** the implementation checkbox. Write the test first, watch it fail, then implement. This applies to all change types — new routes, new commands, new components, new utilities. TDD catches design issues early and produces code that is testable by construction, not by afterthought. When proposing the detailed plan, ensure test checkboxes precede their corresponding implementation checkboxes within each Step.

- **Test isolation via docker-compose.** Tests must never touch production data. When the issue involves database changes or file I/O, include a checkbox to configure the test environment using `docker-compose.test.yml` (or a `test` profile in the main compose file) — this orchestrates the full test stack so any developer can spin it up with a single command. For cloud services (Supabase, Firebase, PlanetScale, Neon, etc.), include their local emulators as compose services. When tests produce files, use a temporary directory cleaned up after each run. If the project already has a docker-compose test setup, verify it covers the new changes. Tests that leak data into production are worse than no tests because they create false confidence. Two critical details:
  - **Env file separation.** Keep `.env.local` pointing at the remote/production service. Inject local container URLs **only** in the test context — via `.env.test`, test runner config (e.g., Playwright's `webServer.env`), or docker-compose environment variables. Never overwrite `.env.local` with test URLs.
  - **Runtime safety guard.** Include a global test setup (e.g., `global-setup.ts`) that verifies target URLs point to local services (`127.0.0.1`, `localhost`) before running. If the check fails, abort with a clear error — this is the last line of defense against accidentally testing against production.
  - **High ports.** Bind all test services to high ports (e.g., 54321, 54322, 9090) in docker-compose to avoid collisions with dev servers and system services. Define ports in `.env.test` so they're easy to change.
  - **Full teardown.** Include a `global-teardown.ts` (or equivalent) that stops all test containers and processes when the suite finishes — success or failure. Use `docker compose down` to remove containers, networks, and volumes. Orphaned containers cause port conflicts on the next run.

- **Codebase-aware plans.** The most valuable part of this skill is producing checkboxes with concrete file paths and references to existing patterns. Always read the codebase before planning — generic checkboxes like "implement the feature" are a failure mode.

- **Acceptance criteria are success criteria, not the plan.** Keep the original acceptance criteria as top-level checkboxes. Steps are the implementation plan to achieve those criteria. Mark an acceptance criterion as done when all its related Steps are complete.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English. Communication with the user follows their language preference.

- **Don't over-plan.** Later Steps can be less detailed than early ones. The first Step should have precise checkboxes; the last can be higher-level. The user will refine as they go.

- **Steps are work sessions.** Each Step should represent a focused work session — something you can complete, commit, and verify before moving on. Too large = lost focus. Too small = overhead.

- **No local environment paths in issues.** Issue content is public and portable. Never reference local paths like `~/.brain/`, `~/.claude/`, or absolute user paths. Use paths relative to the project root (e.g., `create-skill/SKILL.md`, not `~/.brain/skills/skill-creator/SKILL.md`). This applies to checkboxes, descriptions, and any text written to the issue body.

- **Visual verification via CDP (mandatory for web projects).** When the issue touches UI — new pages, component changes, layout fixes, styling — verification checkboxes must use CDP to confirm the result visually, not just functionally. The pattern: "Navigate to [page] via CDP and take screenshot to verify [expected state]". This catches layout breaks, missing elements, and visual regressions that unit tests and functional tests miss entirely. If CDP is not yet configured and the project is a web app with frontend, the first Step in the plan must set it up (`.claude/start-chrome.sh` + `.claude/project-settings.json`). If CDP is already configured, read the `pages` map from `project-settings.json` to reference routes by name in checkboxes. For non-web projects or backend-only issues, skip CDP entirely.

- **Avoid these anti-patterns:**
  - Checkboxes without TDD order — implementation before test, or tests missing entirely. Always: test checkbox first, then implementation checkbox
  - Generic checkboxes without file paths ("Add tests" → "Add test for login in `src/__tests__/auth.test.ts` — expect 200 with valid credentials")
  - Steps that mix concerns (backend + frontend in one Step)
  - Missing verification checkboxes (how do you know the Step works?)
  - Over-expanding simple issues into 10+ Steps when 3 would suffice
  - Checkboxes that duplicate the acceptance criteria verbatim instead of expanding them
  - Local/absolute paths in issue content (`~/.brain/`, `/Users/...`) — always use project-relative paths
  - Proposing a plan without checking `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` first — if enabled, the parallel execution plan section is **mandatory**, not optional. Skipping it means the user loses the ability to parallelize work
