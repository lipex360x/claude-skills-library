# Architecture

Codebase knowledge cache — avoids expensive exploration on every new conversation/phase. Read this first; explore only when something looks stale or missing.

## Stack & dependencies

[Key deps with their purpose — not the full package.json, just the ones that inform architectural decisions]

## Layers

[Brief description of each layer with the canonical file path pattern]

- Domain: `src/domain/<entity>/` — types, pure services, value objects
- Application: `src/application/<entity>/` — use cases, orchestration
- Infrastructure: `src/infrastructure/` — database, auth, external APIs
- Presentation: `src/app/` — routes, server actions, UI components

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

## Routes

[List of routes with purpose and access level — living document, update when routes change]

---

## What NOT to include

- File listings or directory trees — `ls` and Glob handle this
- Business logic or domain rules — that's in the code
- Configuration values — document the pattern, not the value
- Full code examples — point to a canonical file
- Git history or changelog — `git log` is authoritative
