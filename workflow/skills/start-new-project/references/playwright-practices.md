# Playwright Practices — Visual Verification & E2E

Standard Playwright setup for web project verification. Replaces the custom CDP approach.

## 1. Standard setup

```ts
// playwright.config.ts (framework-agnostic template)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? 'github' : 'html',
  use: {
    baseURL: process.env.TEST_BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: process.env.TEST_SERVER_COMMAND || 'npm run dev',
    url: process.env.TEST_BASE_URL || 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } },
  ],
});
```

## 2. Test server lifecycle

Playwright's `webServer` config handles startup/shutdown automatically:
- In CI: starts fresh, waits for ready, kills after tests
- In dev: reuses existing server if already running (`reuseExistingServer: true`)

No manual `nohup`, no `TaskStop`, no orphan processes.

## 3. Page objects for reusable interactions

Abstract framework-specific interactions into page objects:

```ts
// tests/e2e/pages/auth.page.ts
export class AuthPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto('/login');
    await this.page.fill('[name=email]', email);
    await this.page.fill('[name=password]', password);
    await this.page.click('button[type=submit]');
    await this.page.waitForURL(url => !url.pathname.includes('/login'), { timeout: 10000 });
  }
}
```

## 4. Test user helpers

Provide helper functions for unique test users and API-based signup:

```ts
// tests/e2e/helpers/test-user.ts
export function uniqueTestUser(prefix: string) {
  return {
    email: `e2e-${prefix}-${Date.now()}@project.test`,
    password: 'TestPassword123!',
    name: `E2E ${prefix}`,
  };
}

export async function signUpViaApi(user: TestUser) {
  const response = await fetch(`${API_URL}/api/auth/sign-up/email`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
  if (!response.ok) throw new Error(`Sign-up failed (${response.status})`);
}
```

## 5. Global setup and teardown

Setup seeds the database and creates a manual test user. Teardown cleans e2e users and kills servers:

```ts
// tests/e2e/global-setup.ts
async function globalSetup() {
  // 1. Check API health
  // 2. Seed DB if not already seeded
  // 3. Create manual test user (e.g., test@project.dev / Test1234)
}

// tests/e2e/global-teardown.ts
async function globalTeardown() {
  // 1. Delete e2e-* users (preserve manual test user)
  // 2. Kill processes on web/api ports
}
```

Teardown killing servers ensures no port conflicts between test runs and manual testing.

## 6. Browser console error capture (mandatory)

All E2E tests must fail on browser console errors. Errors that only appear in browser DevTools (hydration mismatches, runtime exceptions, unhandled rejections) are invisible to the agent and ship silently. Add a shared fixture or global setup that captures these:

```ts
// tests/e2e/helpers/console-errors.ts
import { type Page } from '@playwright/test';

export function captureConsoleErrors(page: Page): string[] {
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(`[pageerror] ${error.message}`));
  page.on('console', (msg) => {
    if (msg.type() === 'error') errors.push(`[console.error] ${msg.text()}`);
  });
  return errors;
}
```

Usage in tests:

```ts
import { captureConsoleErrors } from './helpers/console-errors';

test('page renders without errors', async ({ page }) => {
  const errors = captureConsoleErrors(page);
  await page.goto('/dashboard');
  // ... test logic ...
  expect(errors).toEqual([]);
});
```

This catches: React hydration mismatches (`<button>` inside `<button>`), unhandled promise rejections, runtime type errors, missing resources, and any error that surfaces only in browser console. Without it, the `[PW]` step can pass visually while the console is full of errors.

Include this helper in the Playwright scaffold step (same step as page objects and test user helpers). Every E2E test file should import and assert on it.

## 7. Screenshot-based visual validation

Take screenshots during tests for visual validation — light/dark mode, desktop/mobile:

```ts
test('dashboard renders correctly', async ({ page }) => {
  // ... navigate and wait for data
  await page.screenshot({ path: 'test-results/dashboard-desktop-light.png', fullPage: true });

  // Toggle dark mode
  await page.getByRole('button', { name: /switch to/i }).click();
  await page.screenshot({ path: 'test-results/dashboard-desktop-dark.png', fullPage: true });
});
```

## 8. Rules

| # | Rule | Why |
|---|------|-----|
| 1 | Headless by default | No window stealing; same rendering; zero disruption |
| 2 | `webServer` config for test server lifecycle | Automatic startup/shutdown; no orphan processes |
| 3 | `.env.test` for test env vars | Single source of truth for test configuration |
| 4 | `reuseExistingServer: !process.env.CI` | Dev reuses; CI starts fresh |
| 5 | Short timeouts (5-10s) with descriptive errors | Fail fast with context |
| 6 | `trace: 'on-first-retry'` in config | Post-mortem debugging without overhead |
| 7 | Page objects for reusable interactions | Framework-agnostic, boilerplate-ready |
| 8 | State changes through UI, not direct DB | Framework caching invalidates only through mutation paths |
| 9 | Test data isolation by prefix (`e2e-*`) | Parallel tests don't collide |
| 10 | Manual test user preserved across runs | Developer can always log in after tests finish |
| 11 | Teardown kills servers and frees ports | No port conflicts between test and manual runs |
| 12 | Screenshots for visual validation (light/dark, desktop/mobile) | Agent validates visually before presenting as done |
| 13 | "Full test" = unit + lint + E2E | Each layer catches different classes of bugs |
| 14 | Browser console errors fail the test | Hydration mismatches, runtime exceptions only visible in DevTools |

## Framework-agnostic design

| Concern | Framework-specific | Abstraction |
|---------|-------------------|-------------|
| Dev server command | `next dev`, `vite dev`, `bun run dev` | `TEST_SERVER_COMMAND` env var |
| Test port | Varies | `TEST_BASE_URL` env var (default `http://localhost:3000`) |
| Auth flow | Login form varies | Page object `AuthPage.login(email, pwd)` |
| Env loading | Format varies | `dotenv-cli` or framework-native env loading |
| Server readiness | Health check varies | `webServer.url` in config (Playwright polls automatically) |
