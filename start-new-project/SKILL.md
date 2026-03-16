---
name: start-new-project
description: Plan and scaffold a new project from a prompt. Asks clarifying questions, proposes a phased GitHub issue structure with checkboxes, creates the issue and feature branch. Use when the user says "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", or provides a project idea wanting structured planning — even if they don't explicitly say "new project."
user-invocable: true
---

# Start New Project

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates ensure the user stays in control: once after clarifying questions, once after the proposed structure.

## Steps

### 1. Parse the prompt

Extract from the user's input:
- **Project name / slug** — if not obvious, derive from the description (kebab-case)
- **Tech stack hints** — languages, frameworks, libraries mentioned
- **Scope indicators** — "MVP", "production", "prototype", "just a quick..."
- **Domain** — web app, CLI, library, API, monorepo, mobile, etc.

If no argument was provided (bare `/start-new-project`), ask the user what they want to build before continuing.

### 2. Ask clarifying questions

Generate 3-5 targeted questions to fill gaps. Present as a numbered list. Common gaps:

1. **Platform** — web, CLI, library, API, mobile?
2. **Tech stack** — language, framework, database?
3. **Scope** — MVP or production-ready? What's the first milestone?
4. **Key features** — what are the 3 most important things it should do?
5. **Deployment** — where will it run? Docker, Vercel, npm, local-only?
6. **Existing code** — new repo or adding to an existing codebase?

Skip questions the prompt already answers. Adapt to the project type — a CLI tool needs different questions than a web app.

**Wait for the user's answers before proceeding.** This is the first approval gate.

### 3. Propose the phase structure

Read `templates/issue-template.md` for the expected format. Read `references/phase-planning-guide.md` for decomposition heuristics by project type.

Decompose the project into **Parts** (grouped by theme) and **Steps** (concrete milestones). Each step contains checkboxes with specific, verifiable actions — include file paths when the project structure is known.

Present the full issue body in a fenced code block. The structure should include:
- **Overview** with architecture description
- **Parts** grouped by theme (Part A, B, C...)
- **Numbered Steps** with concrete checkboxes
- **Reference files table** (if working in an existing codebase)
- **Verification section** — how to confirm the project works end-to-end

Sizing guidelines:
- 1-3 issues per project (each issue = independent milestone)
- 2-4 parts per issue
- 3-8 steps per part
- 2-6 checkboxes per step (TDD steps naturally have more checkboxes — test + implementation pairs)

If `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled (value `1`), append a **Parallel execution plan** section to the issue body. Analyze step dependencies and group independent steps into teammate assignments:

```markdown
## Parallel execution plan (Agent Teams)

> Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

After Step N (last sequential dependency), spawn teammates:
- `teammate-name`: Steps X-Y (description)
- `teammate-name`: Steps W-Z (description)
- `teammate-name`: Steps A-B (blocked until teammate-name completes)
```

Rules for the parallel plan:
- **Identify the sequential prefix** — steps that must run first because everything depends on them (e.g., scaffolding, schema). These stay with the lead.
- **Group independent steps by layer** — backend, frontend, infra, tests. Each group becomes a teammate.
- **Mark blocked teammates** — if a teammate depends on another's output, note it explicitly (e.g., "blocked until backend completes").
- **Teammates inherit the user's model by default.** Optionally suggest Sonnet for teammates if the user wants to optimize for speed or cost. Don't default to a cheaper model — let the user decide.
- **Keep it practical** — 2-4 teammates max. More creates coordination overhead that outweighs the parallelism benefit.

If Agent Teams is not enabled, skip this section entirely.

**Wait for the user's approval before proceeding.** This is the second (and final) approval gate. The user may request changes — iterate until they approve.

### 4. Repo scaffolding (labels + milestone)

Before creating issues, ensure the repo has basic organizational primitives.

**Labels** — check with `gh label list`. If priority labels don't exist, offer to create them:
- `P0` (critical), `P1` (high), `P2` (medium), `P3` (low)
- Type labels (`feature`, `bug`, `chore`, `docs`) — only if missing

Don't force labels on repos that already have a custom scheme. Adapt to what's there.

**Milestone** — if the project generates 2+ issues, create a milestone to group them:

```bash
gh api repos/{owner}/{repo}/milestones -f title="<milestone name>" -f description="<one-line goal>" [-f due_on="<YYYY-MM-DDT00:00:00Z>"]
```

Good milestone names: the project name itself ("Project X MVP"), a version ("v1.0"), or a phase ("Phase 1: Core").

For single-issue projects, a project milestone is optional.

**Backlog milestone** — always create a "Backlog" milestone (no due date) for every new project. This is a permanent bucket for future ideas, improvements, and low-priority items. It stays open indefinitely and gives the user a place to park ideas without losing them. When an item gets prioritized, move it from Backlog to an active milestone.

### 5. Create the GitHub issue

After approval, create the issue:

```bash
gh issue create --title "<concise title>" --body "<approved body>"
```

Apply labels if the repo uses them. Common: `enhancement`, `feature`, `phase-N`, plus a priority label.

If a milestone was created in step 4, assign the issue to it:

```bash
gh issue edit <number> --milestone "<milestone name>"
```

### 6. Project board (for large projects)

If the project generates **3+ issues**, offer to create a GitHub Project board for visual tracking:

```bash
# Create the project
gh project create --title "<project name>" --owner "@me"

# Add issues to the project
gh project item-add <project-number> --owner "@me" --url <issue-url>
```

GitHub Projects V2 creates "Todo", "In Progress", and "Done" columns by default — no extra setup needed.

**This step is optional and user-controlled.** Ask: "This project has N issues — want me to create a project board to track them visually?" If the user declines, skip silently.

For projects with 1-2 issues, skip this step entirely — milestones already provide enough tracking.

### 7. Create the feature branch

```bash
git checkout main
git pull origin main
git checkout -b feature/<slug>
git push -u origin feature/<slug>
```

The slug comes from step 1. If the issue number is known, optionally prefix: `feature/<number>-<slug>`.

### 8. Summary

Present:
- Issue URL(s) (linked)
- Milestone (if created) with link
- Project board (if created) with link
- Branch name
- Total steps and checkboxes count
- Remind: use `closes #N` in PR descriptions to auto-close issues on merge
- Suggest starting with Step 1

## Guidelines

- **TDD by default.** Every step that introduces new behavior must include a test checkbox **before** the implementation checkbox. Write the test first, watch it fail, then implement. This applies to all project types — backend routes, CLI commands, library functions, UI components. TDD catches design issues early and produces code that is testable by construction, not by afterthought. When proposing the phase structure, ensure test checkboxes precede their corresponding implementation checkboxes within each step.

- **Test isolation via docker-compose.** Tests must never touch production data. Orchestrate the test environment with a `docker-compose.test.yml` (or a `test` profile in the main `docker-compose.yml`) so that any developer can spin up the full test stack with a single command. This guarantees portability — the same setup works on any machine and in CI. When the project uses a cloud service (Supabase, Firebase, PlanetScale, Neon, etc.), include its local emulator as a docker-compose service (`supabase start`, `firebase emulators:start`). Point tests at the local containers via `.env.test` with service-specific URLs. When tests produce files, use a temporary directory that is cleaned up after each run. Include the docker-compose test setup as an early checkbox in the first Part — before any test can run, the isolation boundary must exist. Tests that leak data into production are worse than no tests because they create false confidence.

- **Project-agnostic.** This skill works for any kind of project — web apps, CLIs, libraries, APIs, mobile, data pipelines, infrastructure. The questions and structure adapt to the domain.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English. Communication with the user follows their language preference.

- **Checkboxes are verifiable actions.** Each checkbox should be completable in a single work session. "Implement the API" is too vague. "Create `src/routes/auth.ts` with login/logout endpoints" is concrete. For steps with new behavior, follow the TDD order: test checkbox first (`Add test for X in src/__tests__/x.test.ts — expect Y`), then implementation checkbox (`Implement X in src/x.ts`).

- **File paths when structure is known.** If the project builds on an existing codebase, include file paths in checkboxes. For greenfield projects, include paths once the structure is defined in early steps.

- **Don't over-plan.** Later phases can be less detailed than early ones. The first part should have precise checkboxes; the last part can be higher-level. The user will refine as they go.

- **One issue per milestone.** If the project has distinct milestones (e.g., "backend API" then "frontend"), create separate issues. Each issue should be independently completable and verifiable.

- **Milestones for multi-issue projects.** When a project spans 2+ issues, group them under a GitHub milestone. This gives automatic progress tracking (% complete) and a clear finish line. For single-issue projects, milestones are optional.

- **`closes #N` in PRs.** Always remind the user to include `closes #N` in PR descriptions. This auto-closes the linked issue on merge and updates milestone progress automatically.
