# CDP Visual Verification — Best Practices

Hard-won rules from production CDP testing. Each one exists because the alternative caused real debugging time.

## 1. Headless by default, CDP for manual debugging

Verification scripts have two modes:

- **Automated verification (default):** `chromium.launch({ headless: true })` — no window, no focus stealing, same rendering. Use for agent-driven screenshot checks.
- **Manual inspection:** `chromium.connectOverCDP('http://localhost:9222')` — connects to a visible Chrome the user launched via `start-chrome.sh`. Use only when the user wants to watch the browser in real-time.

**Default to headless** unless the user explicitly asks for visible browser or manual debugging. Headless gives identical screenshots with zero disruption — no windows opening, no focus stealing on macOS.

```ts
// DEFAULT — headless for automated verification
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 375, height: 812 },
});
const page = await context.newPage();

// MANUAL ONLY — when user wants to watch
const browser = await chromium.connectOverCDP("http://localhost:9222");
const context = await browser.newContext({ /* ... */ });
```

When using `connectOverCDP`, never reuse existing contexts (`browser.contexts()[0]`) — they carry cookies from user sessions. Always `browser.newContext()`.

**Always wrap in `try/finally`** — cleanup must run even on error:

```ts
try {
  // ... login, navigate, verify, screenshot ...
} finally {
  await context.close();
  await browser.close(); // headless — close browser entirely
  log("Done.");
}
```

## 2. Test server must point to local services

The dev server (e.g., port 3000) typically uses `.env.local` which points to remote/production services. Seed/test users only exist in the local Docker instance.

**CDP verification with test users requires a dedicated test server on a separate port** (e.g., 3100) with local environment variables. These should come from the Playwright `webServer.env` config, `.env.test`, or be passed explicitly when starting the server. Never overwrite `.env.local` — it serves the developer's normal workflow.

The `testPort` is declared in `.claude/project-settings.json` so both the skill and CDP scripts reference the same value.

## 3. Server startup and immediate cleanup

Never auto-start servers with `nohup` — it creates orphan processes that block ports and accumulate open shells.

**Before running any verification script, run the pre-flight checklist:**

```bash
# 1. Local DB/services running?
# (framework-specific: supabase status, docker compose ps, etc.)

# 2. Test server running on test port?
curl -s -o /dev/null -w "%{http_code}" localhost:<test-port>

# 3. Chrome CDP available? (only if using manual/visible mode)
curl -s localhost:9222/json/version | head -1
```

If the test server isn't running, **ask the user** rather than auto-starting. If the user confirms auto-start and the agent launches it with `run_in_background`, **note the returned task ID** and `TaskStop` it immediately after verification completes — never leave background servers running.

**Cleanup after every verification:**

```
# If agent started the server → TaskStop with the task ID
TaskStop(task_id)

# If server was already running before the agent → do NOT kill it
# The user manages their own servers
```

**Critical: only stop tasks the agent created.** Never blindly `lsof -ti:PORT | xargs kill` — the user may have their own servers running on that port. Always use `TaskStop` with the specific task ID returned by `run_in_background`.

Orphaned background tasks are invisible clutter — they occupy ports (blocking future runs), show as "N active shells" in the status bar, generate confusing task failure notifications (exit 137 = SIGKILL), and signal sloppy resource management. Clean up after yourself.

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

## 8. Framework-specific cleanup

After killing the test server (see section 3), also remove framework lock files if the server died dirty:

```bash
# Framework-specific lock files
rm -f .next/dev/lock    # Next.js
rm -f .nuxt/dev/lock    # Nuxt
```

## 9. Never `run_in_background` for CDP scripts

Run CDP scripts inline with the Bash tool using `timeout: 30000` (30s is enough for most verifications). Background execution via `run_in_background` orphans the process — `TaskOutput` with timeout consumes the output but does NOT kill the process. This causes "open bashes" accumulation, blocked ports, and stale lock files.

**`run_in_background` is valid for servers** (e.g., test server on port 3100) but requires disciplined cleanup — see section 3. The rule is: CDP scripts run inline, servers run in background with a mandatory `TaskStop` after use.

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

## 14. Every `run_in_background` must have a matching `TaskStop`

This is the general principle behind sections 3 and 9. When the agent launches any background task — test servers, build watchers, database containers — it must:

1. **Note the task ID** returned by `run_in_background`
2. **`TaskStop` the task** as soon as the work that needed it is done
3. **Self-check before responding** — if there are background tasks that are no longer needed, stop them before moving on to the next user interaction

There is no built-in "finally" block for background tasks — cleanup is the agent's responsibility. Without it, orphaned shells accumulate over a session: ports stay occupied, the status bar shows "N active shells", and eventually the system kills them with SIGKILL (exit 137), generating confusing notifications.

**The fix is trivial — just call `TaskStop` — but it needs to be a habit, not an afterthought.**

## Rules summary

| Rule | Why |
|---|---|
| Headless by default (`chromium.launch`) | No window stealing focus; same rendering; zero disruption |
| CDP (`connectOverCDP`) only for manual debugging | User explicitly wants to watch the browser |
| `browser.newContext()` when using CDP — never reuse | Cookies from personal browser pollute and break auth |
| `context.close()` + `browser.close()` in `finally` | Removes contexts and closes headless browser cleanly |
| Test server on dedicated port with local env | Dev server uses production env; test users only exist locally |
| `TaskStop` server after verification — never `lsof kill` | Only kill what the agent created; user may have own servers |
| `waitUntil: "networkidle"` on every `goto` | Prevents interacting before hydration |
| `log()` with timestamp on each step | Identifies where script hangs |
| `page.on("pageerror")` always active | Catches silent JS errors |
| Short timeouts (5-10s) with `.catch()` | Fail fast instead of hanging 30s |
| Generic login redirect (`!includes("/login")`) | Works regardless of redirect destination |
| Never `run_in_background` for verification | Orphans processes, blocks ports |
| Match project language extension | `.ts` for TS, `.mjs` for JS |
| Cleanup framework lock files after kill | `.next/dev/lock`, `.nuxt/dev/lock` prevent restart |
| State changes via UI, not direct DB | Framework caching invalidates only through mutation paths |
| Every `run_in_background` needs a matching `TaskStop` | Orphaned shells accumulate ports, status bar clutter, exit 137 |
| "Full test" = unit + lint + E2E | Each layer catches different classes of bugs |
