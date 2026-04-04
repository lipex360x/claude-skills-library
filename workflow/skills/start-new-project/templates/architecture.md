# Architecture

Codebase knowledge cache — avoids expensive exploration on every new conversation/phase. Read this first; explore only when something looks stale or missing.

## At a glance

- **Type:** [project type — e.g., web app, CLI, API, library, monorepo]
- **Framework:** [primary framework — e.g., Next.js 15, Hono, FastAPI]
- **Entry points:** [main entry files — e.g., `src/app/layout.tsx`, `src/index.ts`, `cmd/main.go`]

## Stack & dependencies

[Key deps with their purpose — not the full package.json, just the ones that inform architectural decisions]

## Layers

[Brief description of each layer with the canonical file path pattern]

- Domain: `src/domain/<entity>/` — types, pure services, value objects
- Application: `src/application/<entity>/` — use cases, orchestration
- Infrastructure: `src/infrastructure/` — database, auth, external APIs
- Presentation: `src/app/` — routes, server actions, UI components

## Key flows

[2-3 numbered sequences showing how data moves through layers — the "trace this" reference for debugging and onboarding.]

1. **[Flow name — e.g., Create entity]**
   Request → [Presentation layer entry] → [Validation] → [Domain/Application logic] → [Infrastructure persistence] → Response

2. **[Flow name — e.g., Authenticated action]**
   Request → [Auth check] → [Permission gate] → [Business logic] → [Side effects] → Response

3. **[Flow name — e.g., Background job]**
   Trigger → [Queue/scheduler] → [Worker] → [Domain logic] → [Notification/cleanup] → Done

## Patterns (by example)

[One concrete example of each recurring pattern — the "copy this" reference. Point to canonical files, don't paste code.]

### Server action

- Location: `src/app/(group)/<page>/actions.ts`
- Pattern: verify auth → validate input → call domain/application layer → return `{ error?, success?, data? }`
- Example: `src/app/(dashboard)/admin/billing/actions.ts`

### Query hook

- Location: `src/infrastructure/query/use-<entity>.ts`
- Pattern: call server action, invalidate related queries on mutation
- Example: `src/infrastructure/query/use-billing-mutations.ts`

### Unit test

- Location: `src/__tests__/<layer>/<entity>/<name>.test.ts`
- Pattern: (test framework) + (mocking strategy), test pure logic
- Example: `src/__tests__/domain/billing/distribution.test.ts`

### E2E test

- Location: `e2e/<feature>.spec.ts`
- Pattern: (E2E framework), serial mode for DB tests, login helper, cleanup before/after
- Example: `e2e/billing.spec.ts`

### CDP verification script

- Location: `e2e/cdp/verify-<page>.ts`
- Pattern: connectOverCDP, newContext with viewport, login, navigate, screenshot
- Example: `e2e/cdp/verify-admin-billing.ts`

## Schema summary

[Tables with key columns and relationships — not the full DDL, just enough to understand the data model]

## Auth model

[How auth works: roles, permission checks, client vs server patterns]

## Observability

[Structured logging setup — libraries, log levels per environment, where request/error logging is configured]

| Concern | Tool | Config |
|---------|------|--------|
| Backend logging | [library — e.g., structlog, pino, slog] | [log level env var, middleware location] |
| Frontend logging | [library — e.g., loglevel, custom wrapper] | [error boundary, API error handler locations] |
| Tracing (optional) | [tool — e.g., LangSmith, OpenTelemetry] | [env vars, decorator/middleware location] |

Log levels: `silent` (test), `debug` (dev), `info` (prod). Debug/trace logs must never expose stack traces, SQL queries, or request bodies in production.

## Routes

[List of routes with purpose and access level — living document, update when routes change]

## Config

[Environment variables that affect runtime behavior — not secrets, just the knobs.]

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|

## Scripts

[Dev scripts and their purpose — quick reference for common operations.]

| Script | Purpose | When to use |
|--------|---------|-------------|

---

## What NOT to include

- File listings or directory trees — `ls` and Glob handle this
- Business logic or domain rules — that's in the code
- Configuration values — document the pattern, not the value
- Full code examples — point to a canonical file
- Git history or changelog — `git log` is authoritative

---

<!-- arch-hash: <hash> -->
<!-- last-updated: <date> -->
