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

## 2. Test server must point to local services

`bun run dev` (or `npm run dev`) uses `.env.local` which points to remote/production services. Seed/test users only exist in the local Docker instance.

**CDP verification with test users requires a dedicated test server:**

```bash
# 1. Ensure seed is applied
supabase db reset

# 2. Build with local env
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321 \
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key_local> \
bun run build

# 3. Start on test port (3100) — never use 3000
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321 \
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key_local> \
bun next start --port 3100
```

The env vars and test port should be defined in `.env.test` and `playwright.config.ts`. Extract from there — don't hardcode.

## 3. Observability over blind timeouts

Scripts that hang 30-45s waiting for selectors with zero feedback waste time and hide the root cause.

**Always add observability:**

```ts
function log(msg: string) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

// JS errors on the page — catches silent hydration/render failures
page.on('pageerror', (err) => log(`[page error] ${err.message}`));

// Network monitoring (enable when debugging)
page.on('response', async (res) => {
  if (res.url().includes('localhost')) {
    log(`${res.request().method()} ${res.status()} ${res.url()}`);
  }
});
```

## 4. Verify hydration before interacting

Clicking submit on an unhydrated page does nothing. The HTML is visible but JS event handlers aren't attached yet.

**Use `waitUntil: "networkidle"` on every `goto`:**

```ts
await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
```

## 5. Pre-flight checklist

Before running any CDP script, verify all dependencies are up:

```bash
# 1. Chrome with CDP running?
curl -s http://localhost:9222/json/version | head -1

# 2. Local services running? (e.g., Supabase)
supabase status

# 3. Seed applied?
supabase db reset  # if needed

# 4. Test server (port 3100) running with local env?
curl -s http://localhost:3100 -o /dev/null -w "%{http_code}"
# If not: build + start with local env (see section 2)
```

## 6. Short timeouts with fast failure

Default Playwright timeouts (30s) cause scripts to hang silently when something is wrong.

**Use 5-10s timeouts with `.catch()`:**

```ts
await page.waitForURL(`${BASE}/dashboard`, { timeout: 10000 })
  .catch(() => { throw new Error('Login redirect failed — check auth flow'); });
```

## 7. Rules summary

| Rule | Why |
|---|---|
| `browser.newContext()` always — never reuse existing context | Cookies from personal browser pollute and break auth |
| Test server on dedicated port (e.g., 3100) with local env | Dev server uses production env; test users only exist in Docker |
| `supabase db reset` before first verification | Ensures up-to-date seed data |
| `waitUntil: "networkidle"` on every `goto` | Prevents interacting before hydration |
| `log()` with timestamp on each step | Identifies where script hangs |
| `page.on("pageerror")` always active | Catches silent JS errors |
| Short timeouts (5-10s) with `.catch()` | Fail fast instead of hanging 30s |
| One page per context, close context when done | Clean tab lifecycle, no orphans |
