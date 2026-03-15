# Phase Planning Guide

Heuristics for decomposing projects into parts and steps. These are starting points — adapt based on the specific project's needs, constraints, and the user's preferences.

## By project type

### Web applications

Typical part progression:

1. **Data layer** — database schema, models, migrations, seed data
2. **Backend / API** — routes, controllers, middleware, auth
3. **Frontend** — pages, components, state management, forms
4. **Integration** — connect frontend to API, error handling, loading states
5. **Polish & Deploy** — responsive design, performance, CI/CD, hosting

Variations:
- **Fullstack frameworks** (Next.js, Remix, SvelteKit): combine backend + frontend parts since they're co-located
- **API-only**: skip frontend parts, add documentation and SDK/client generation
- **Existing frontend**: start from integration, not data layer

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
2. **Individual apps** — each app gets its own part or issue
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

### Steps per part
- **Too few** (1-2): the part is either too granular or the steps are too large. Split steps or merge the part into another.
- **Sweet spot** (3-8): each step is a focused work session.
- **Too many** (9+): the part covers too much ground. Split into two parts.

### Checkboxes per step
- **Too few** (1): likely not a real step — merge into an adjacent step or expand.
- **Sweet spot** (2-6): each checkbox is a single, verifiable action.
- **Too many** (7+): the step is trying to do too much. Split into two steps.

### Issues per project
- **Simple project** (1 issue): everything fits in one milestone — a weekend project, a single feature, a small tool.
- **Medium project** (2-3 issues): distinct phases with clear handoff points — "backend" then "frontend", or "core" then "extensions".
- **Large project** (3+ issues): each issue maps to a major milestone. Keep the first issue self-contained — it should deliver value on its own.

## Common anti-patterns

### Steps too large
"Implement the entire authentication system" — this is a part, not a step. Break it into: schema, routes, middleware, tests, frontend integration.

### Steps too small
"Create the `src/` directory" — this isn't meaningful on its own. Merge into the step that creates the first file inside it.

### Mixed concerns
"Add user model and login page" — these touch different layers. Split into a backend step (model) and a frontend step (page).

### Missing verification
Steps without a way to confirm they work lead to integration surprises later. Add "Run X — expect Y" checkboxes or a verification section.

### Front-loading all detail
The first part should be detailed (you know what to build). Later parts can be higher-level — they'll get refined when the user reaches them. Over-specifying part C when part A hasn't started yet wastes planning effort on assumptions.

### Ignoring existing patterns
In an existing codebase, the first step should be "study existing patterns" — read reference files, understand conventions, then follow them. Greenfield freedom doesn't apply when adding to an established project.

## Phase ordering principles

1. **Dependencies first** — if B needs A, A goes first. Obvious but often violated.
2. **Highest risk first** — uncertain or technically challenging work early. If it fails, you want to know before building everything else.
3. **Value early** — deliver something usable as soon as possible. Even if it's incomplete, seeing results maintains motivation and surfaces design issues.
4. **Tests alongside** — don't defer all testing to the end. Each step should include its own tests.
