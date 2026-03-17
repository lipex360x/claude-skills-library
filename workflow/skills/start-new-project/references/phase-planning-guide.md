# Phase Planning Guide

Heuristics for decomposing projects into phases and steps. These are starting points — adapt based on the specific project's needs, constraints, and the user's preferences.

## Table of contents

- [By project type](#by-project-type) — web apps, CLIs, libraries, monorepos, data pipelines, infra
- [Sizing heuristics](#sizing-heuristics) — steps per phase, checkboxes per step, issues per project
- [Common anti-patterns](#common-anti-patterns) — monolithic issues, mixed concerns, missing verification
- [GitHub hierarchy](#github-hierarchy) — milestones, labels, project boards
- [Phase ordering principles](#phase-ordering-principles) — dependencies, risk, TDD, test isolation
- [Agent Teams parallelism](#agent-teams-parallelism) — patterns, sizing, anti-patterns

## By project type

### Web applications

Typical phase progression:

1. **Scaffolding & CDP setup** — project structure, dependencies, `.claude/start-chrome.sh` + `.claude/project-settings.json` for browser automation. CDP must be ready before any frontend step so Claude can navigate and screenshot to verify UI. Use the skill templates as source files, adapting `baseUrl`, `tabs`, and `pages` to the project
2. **Data layer** — database schema, models, migrations, seed data. When seed includes test credentials, create a gitignored `TEST_USERS.md` with all seeded emails/passwords/roles in a table for quick reference
3. **Backend / API** — routes, controllers, middleware, auth
4. **Frontend** — pages, components, state management, forms. Verification checkboxes should use CDP: "Navigate to [page] via CDP and screenshot to verify"
5. **Integration** — connect frontend to API, error handling, loading states
6. **Polish & Deploy** — responsive design, performance, CI/CD, hosting

Variations:
- **Fullstack frameworks** (Next.js, Remix, SvelteKit): combine backend + frontend phases since they're co-located. CDP setup still goes in scaffolding
- **API-only**: skip frontend and CDP phases, add documentation and SDK/client generation
- **Existing frontend**: start from integration, not data layer. CDP setup goes in the first step to enable visual verification of existing UI

### CLI tools

1. **Core logic** — the main algorithm or transformation, independent of I/O
2. **Commands & args** — CLI parser, subcommands, flags, validation
3. **Output & UX** — formatting, colors, progress bars, error messages
4. **Distribution** — packaging, npm publish / binary builds, man pages

### Libraries / packages

1. **Core API** — the main exports, function signatures, behavior
2. **Types** — TypeScript types, generics, inference, JSDoc
3. **Edge cases** — error handling, validation, boundary conditions
4. **Testing** — unit tests, integration tests, property-based tests
5. **Documentation & publishing** — README, API docs, examples, npm/crates/PyPI

### Monorepos

1. **Shared packages** — types, utilities, configuration
2. **Individual apps** — each app gets its own phase or issue
3. **Build & CI** — workspace tooling, shared scripts, CI pipelines
4. **Integration** — cross-package testing, version management

### Data pipelines

1. **Ingestion** — data sources, connectors, raw data storage
2. **Transformation** — cleaning, normalization, enrichment
3. **Output** — storage, API, visualization, exports
4. **Orchestration** — scheduling, monitoring, error recovery

### Infrastructure / DevOps

1. **Foundation** — networking, IAM, base configuration
2. **Services** — containers, functions, databases, caches
3. **Observability** — logging, metrics, alerting, dashboards
4. **Automation** — CI/CD, IaC, deployment scripts

## Sizing heuristics

### Steps per phase
- **Too few** (1-2): the phase is either too granular or the steps are too large. Split steps or merge the phase into another.
- **Sweet spot** (3-8): each step is a focused work session.
- **Too many** (9+): the phase covers too much ground. Split into two phases.

### Checkboxes per step
- **Too few** (1): likely not a real step — merge into an adjacent step or expand.
- **Sweet spot** (2-6): each checkbox is a single, verifiable action.
- **Too many** (7+): the step is trying to do too much. Split into two steps.

### Total steps per issue
- **Sweet spot** (3-8): manageable scope, clear progress per issue.
- **Too many** (9+): **mandatory split** — one issue per Phase. A 15-step issue buries progress and makes the milestone bar useless. Each Phase becomes its own issue with steps renumbered from 1.

### Issues per project
- **Simple project** (1 issue): 8 steps or fewer — a weekend project, a single feature, a small tool.
- **Medium project** (2-3 issues): distinct phases with clear handoff points — "backend" then "frontend", or "core" then "extensions". Each issue 3-8 steps.
- **Large project** (4+ issues): each issue maps to a Phase. Keep the first issue self-contained — it should deliver value on its own. Milestone shows real progress (25%/50%/75%/100%).

## Common anti-patterns

### Monolithic issue
Dumping 15 steps into one issue because "it's all one project." The milestone shows 0% until the entire thing is done — zero visibility. Split into one issue per Phase. A project with 4 Phases = 4 issues = milestone shows 25% per issue closed. Each issue is a checkpoint.

### Steps too large
"Implement the entire authentication system" — this is a phase, not a step. Break it into: schema, routes, middleware, tests, frontend integration.

### Steps too small
"Create the `src/` directory" — this isn't meaningful on its own. Merge into the step that creates the first file inside it.

### Mixed concerns
"Add user model and login page" — these touch different layers. Split into a backend step (model) and a frontend step (page).

### Missing verification
Steps without a way to confirm they work lead to integration surprises later. Add "Run X — expect Y" checkboxes or a verification section.

### Front-loading all detail
The first phase should be detailed (you know what to build). Later phases can be higher-level — they'll get refined when the user reaches them. Over-specifying Phase 3 when Phase 1 hasn't started yet wastes planning effort on assumptions.

### Ignoring existing patterns
In an existing codebase, the first step should be "study existing patterns" — read reference files, understand conventions, then follow them. Greenfield freedom doesn't apply when adding to an established project.

## GitHub hierarchy

When structuring a project, the full GitHub hierarchy (from broadest to narrowest) is:

```
Project (board)         ← visual overview of all work (optional for solo dev)
  └── Milestone         ← goal with optional deadline (e.g., "MVP", "v1.0")
        └── Issue       ← unit of work (feature, bug, chore)
              └── Tasks (checkboxes / sub-issues)
                    └── Branch → PR → Merge
```

### When to use milestones

- **Multi-issue projects (2+ issues):** always create a milestone. It provides automatic % progress and groups related issues.
- **Single-issue projects:** optional. Skip unless the user wants to track future phases.
- **Backlog milestone:** create one (no due date) when the user mentions scope beyond the current plan. This is the bucket for "later" items.

### Milestone naming

- Use the project name or version: "Project X MVP", "v1.0", "Phase 1: Core"
- Avoid generic names like "Sprint 1" unless the user follows sprint methodology

### When to use project boards

- **3+ issues:** offer a project board. Multiple issues benefit from a visual kanban view (Todo / In Progress / Done) to track overall progress between sessions.
- **1-2 issues:** skip. Milestones already provide enough tracking.
- **Always optional:** ask the user, never force. Solo devs may prefer the simplicity of just milestones + issues.

### Labels as metadata

Labels answer "what type?" and "what priority?" — they complement milestones, not replace them.

Minimum useful set for a new project:
- **Priority:** P0 (critical), P1 (high), P2 (medium), P3 (low)
- **Type:** feature, bug, chore, docs

Don't create labels the repo already has. Adapt to existing schemes.

## Phase ordering principles

1. **Dependencies first** — if B needs A, A goes first. Obvious but often violated.
2. **Highest risk first** — uncertain or technically challenging work early. If it fails, you want to know before building everything else.
3. **Value early** — deliver something usable as soon as possible. Even if it's incomplete, seeing results maintains motivation and surfaces design issues.
4. **TDD — tests first, not alongside.** Write the test before the implementation in every step that introduces new behavior. This is not optional. TDD surfaces design flaws early, prevents untestable code, and guarantees coverage by construction. Structure each step as: define the expected behavior in a test, watch it fail, then implement until it passes.
5. **Test isolation via docker-compose.** Orchestrate the test environment with `docker-compose.test.yml` (or a `test` profile). For cloud services, include local emulators as compose services. Keep `.env.local` pointing at remote services; inject local URLs only in test context (`.env.test`, test runner config, compose env vars). Bind test services to high ports (54321+) to avoid collisions with dev servers. Add a runtime safety guard (`global-setup.ts`) that verifies URLs point to `127.0.0.1`/`localhost` — abort if not. Include a `global-teardown.ts` that runs `docker compose down` to remove all containers, networks, and volumes after the suite finishes. Tests that leak into production or leave orphaned containers are a liability.

## Agent Teams parallelism

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is active, steps can be distributed across teammates for parallel execution. The key is identifying the **dependency graph** between steps.

### Parallelism patterns by project type

**Web apps:**
```
Lead: scaffolding + schema (sequential)
  ├─ Teammate "backend-auth": auth routes, middleware
  ├─ Teammate "backend-api": CRUD routes, business logic
  └─ Teammate "frontend": pages, components (blocked until API exists)
       └─ Teammate "polish": error handling, responsive, docs
```

**CLI tools:**
```
Lead: core logic (sequential)
  ├─ Teammate "commands": CLI parser, subcommands, flags
  └─ Teammate "output": formatting, colors, progress bars
       └─ Teammate "dist": packaging, publishing
```

**Libraries:**
```
Lead: core API + types (sequential)
  ├─ Teammate "edge-cases": validation, error handling
  ├─ Teammate "tests": unit + integration tests
  └─ Teammate "docs": README, API docs, examples
```

**Monorepos:**
```
Lead: shared packages (sequential)
  ├─ Teammate "app-1": first app
  ├─ Teammate "app-2": second app
  └─ Teammate "ci": build scripts, CI pipelines
```

### Sizing teammates

- **2-4 teammates** is the sweet spot. More creates coordination overhead.
- **5-6 steps per teammate** keeps them productive without context switching.
- **Teammates inherit the user's model by default.** Suggest Sonnet only if the user wants to optimize for speed or cost.
- **Avoid same-file edits** — two teammates editing the same file causes conflicts. Split by layer/module, not by feature.

### Anti-patterns

- **Too many teammates**: 5+ teammates = high token cost + coordination overhead > parallelism benefit.
- **Same-file conflicts**: two teammates editing `schema.prisma` simultaneously = merge hell.
- **Premature parallelism**: spawning teammates before the sequential prefix is done = wasted work on wrong assumptions.
- **No dependency tracking**: teammates that block each other without explicit ordering = race conditions.
