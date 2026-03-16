# CDP Visual Verification — Best Practices

Hard-won rules from production CDP testing. Each one exists because the alternative caused real debugging time.

## 1. Context isolation (critical)

`browser.contexts()[0]` reuses the existing Chrome context, which carries cookies from all user sessions. Auth cookies get lost or conflict.

**Always create a fresh context:**

```ts
// WRONG — reuses dirty browser context with leftover cookies
const context = browser.contexts()[0] ?? await browser.newContext();

// RIGHT — isolated context, no previous cookies, controlled viewport
const context = await browser.newContext({
  viewport: { width: 375, height: 812 },
});
const page = await context.newPage();
```

Use one page per context, navigate within it, then close the context (not the page). This keeps the browser clean — one tab per test run, automatically removed on `context.close()`.

**Always wrap in `try/finally`** — `context.close()` must run even on error:

```ts
try {
  // ... login, navigate, verify, screenshot ...
} finally {
  await context.close();
  log("Done.");
}
```

## 2. Test server must point to local services

The dev server (e.g., port 3000) typically uses `.env.local` which points to remote/production services. Seed/test users only exist in the local Docker instance.

**CDP verification with test users requires a dedicated test server on a separate port** (e.g., 3100) with local environment variables. These should come from the Playwright `webServer.env` config, `.env.test`, or be passed explicitly when starting the server. Never overwrite `.env.local` — it serves the developer's normal workflow.

The `testPort` is declared in `.claude/project-settings.json` so both the skill and CDP scripts reference the same value.

## 3. Server startup is the user's responsibility

Never auto-start servers with `nohup` or `run_in_background` — both create orphan processes that block ports and accumulate open shells.

**Before running any CDP script, run the pre-flight checklist:**

```bash
# 1. Chrome CDP available?
curl -s localhost:9222/json/version | head -1

# 2. Local DB/services running?
# (framework-specific: supabase status, docker compose ps, etc.)

# 3. Test server running on test port?
curl -s -o /dev/null -w "%{http_code}" localhost:<test-port>
```

If the test server isn't running, **ask the user** rather than auto-starting. If the user confirms auto-start, document that cleanup is manual afterward (see section 8).

## 4. Observability over blind timeouts

Scripts that hang 30-45s waiting for selectors with zero feedback waste time and hide the root cause.

**Always add observability:**

```ts
function log(msg: string) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

// JS errors on the page — catches silent hydration/render failures
page.on("pageerror", (err) => log(`[page error] ${err.message}`));
```

## 5. Verify hydration before interacting

Clicking submit on an unhydrated page does nothing. The HTML is visible but JS event handlers aren't attached yet.

**Use `waitUntil: "networkidle"` on every `goto`:**

```ts
await page.goto(`${BASE}/login`, { waitUntil: "networkidle" });
```

## 6. Short timeouts with fast failure

Default Playwright timeouts (30s) cause scripts to hang silently when something is wrong.

**Use 5-10s timeouts with `.catch()`:**

```ts
await page.waitForURL(`${BASE}/dashboard`, { timeout: 10000 })
  .catch(() => { throw new Error("Login redirect failed — check auth flow"); });
```

## 7. Login redirect is project-specific

Never hardcode the expected redirect destination after login. Different projects redirect to different pages.

```ts
// WRONG — will timeout if redirect goes elsewhere
await page.waitForURL("**/dashboard**");

// RIGHT — generic: wait for any non-login URL
await page.waitForURL(
  (url) => !url.pathname.includes("/login"),
  { timeout: 10000 }
);
```

## 8. Process cleanup after CDP sessions

After running CDP verifications, always clean up potential orphans:

```bash
# Kill anything on the test port
lsof -i :<test-port> -t | xargs kill 2>/dev/null

# Remove framework-specific lock files if server died dirty
# (e.g., .next/dev/lock for Next.js, .nuxt/dev/lock for Nuxt)
```

## 9. Never `run_in_background` for CDP scripts

Run CDP scripts inline with the Bash tool using `timeout: 30000` (30s is enough for most verifications). Background execution via `run_in_background` orphans the process — `TaskOutput` with timeout consumes the output but does NOT kill the process. This causes "open bashes" accumulation, blocked ports, and stale lock files.

## 10. Match project language extension

CDP scripts must match the project's language:
- **TypeScript projects** → `.ts` (run with `npx tsx`)
- **Plain JS projects** → `.mjs` (run with `node`)

Never generate `.mjs` in a TypeScript codebase — it creates inconsistency with the rest of the project.

## 11. E2E state changes go through the UI

When an E2E test needs to change application state (toggle a feature, update a setting), **always change it through the UI** — navigate to the page, interact with the form, submit. Never manipulate the database directly and expect the application to see the change.

**Why:** Fullstack frameworks cache server-side data aggressively. A server action may return a cached value even after a direct DB write. The application only sees changes that flow through its own mutation paths (server actions, API routes, form submissions), which trigger cache invalidation.

**Direct DB access is valid for:**
- **Setup/teardown** — inserting seed data before tests, cleaning up after
- **Assertions** — verifying that a UI action actually persisted to the database
- **Never for state the app needs to read during the test flow**

## 12. Serial E2E and shared database state

When writing multiple E2E test groups that share database tables, design each group to be self-contained with its own setup/teardown. Serial execution within a single test group does not prevent parallel execution across groups — different test files may run simultaneously and interfere with shared tables. Use unique identifiers per test (different months, names, IDs) to minimize collisions.

## 13. "Full test" means unit + lint + E2E

When generating verification checkboxes that say "run full test suite", always expand to include all three layers:

```
- [ ] Run full test suite: unit tests + lint + E2E — all passing
```

Unit tests with mocks can pass while the database schema is broken. CDP screenshots catch UI issues but don't verify data persistence. Only E2E tests with real database writes confirm the entire stack works. Skipping E2E gives false confidence.

## Rules summary

| Rule | Why |
|---|---|
| `browser.newContext()` always — never reuse existing context | Cookies from personal browser pollute and break auth |
| `context.close()` in `finally` block — always | Removes tab even on error, prevents orphan contexts |
| Test server on dedicated port with local env | Dev server uses production env; test users only exist locally |
| `waitUntil: "networkidle"` on every `goto` | Prevents interacting before hydration |
| `log()` with timestamp on each step | Identifies where script hangs |
| `page.on("pageerror")` always active | Catches silent JS errors |
| Short timeouts (5-10s) with `.catch()` | Fail fast instead of hanging 30s |
| Generic login redirect (`!includes("/login")`) | Works regardless of redirect destination |
| Never `run_in_background` for CDP | Orphans processes, blocks ports |
| Match project language extension | `.ts` for TS, `.mjs` for JS |
| Server startup = user's responsibility | `nohup` creates orphans; ask or pre-flight check |
| Cleanup after CDP sessions | Kill port orphans, remove lock files |
| State changes via UI, not direct DB | Framework caching invalidates only through mutation paths |
| "Full test" = unit + lint + E2E | Each layer catches different classes of bugs |
