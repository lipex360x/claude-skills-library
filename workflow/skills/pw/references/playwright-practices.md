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

## 3. Human navigation rule (CRITICAL)

**E2E tests must navigate like a human.** No `page.goto('/dashboard')`. Navigate via UI: clicks, sidebar, menus, links. A human expert does not type URLs into the address bar — tests should not either.

**The only valid `page.goto()` is for the initial entry point** — the login page or the app's home page. Every subsequent page transition must happen through UI interactions: clicking navigation links, sidebar items, menu options, buttons, or following redirects.

### Why this matters

- `page.goto()` bypasses auth guards, middleware, redirects, and loading states that real users encounter
- Navigation bugs (broken links, wrong hrefs, missing routes) are invisible when tests teleport via URL
- Framework-specific behaviors (client-side routing, prefetching, hydration) only trigger through real navigation
- If a test needs `page.goto()` to reach a page, the UI probably has a navigation gap

### Pattern: navigate through UI

```ts
// BAD — teleporting to pages
await page.goto('/dashboard');
await page.goto('/settings/profile');
await page.goto('/projects/123');

// GOOD — navigating like a human
await page.goto('/'); // Initial entry — only valid page.goto
await page.getByRole('link', { name: /login/i }).click();
await authPage.login(email, password);
// Now on dashboard after login redirect

await page.getByRole('navigation').getByRole('link', { name: /settings/i }).click();
await page.getByRole('link', { name: /profile/i }).click();
// Now on settings/profile via sidebar navigation

await page.getByRole('navigation').getByRole('link', { name: /projects/i }).click();
await page.getByRole('link', { name: /my project/i }).click();
// Now on project detail page via project list
```

### Pattern: shared navigation helpers

```ts
// tests/e2e/helpers/navigation.ts
export class AppNavigation {
  constructor(private page: Page) {}

  async goToDashboard() {
    await this.page.getByRole('navigation').getByRole('link', { name: /dashboard/i }).click();
    await this.page.waitForURL('**/dashboard');
  }

  async goToSettings() {
    await this.page.getByRole('navigation').getByRole('link', { name: /settings/i }).click();
    await this.page.waitForURL('**/settings');
  }

  async goToProfile() {
    await this.goToSettings();
    await this.page.getByRole('link', { name: /profile/i }).click();
    await this.page.waitForURL('**/settings/profile');
  }
}
```

## 4. Page objects for reusable interactions

Abstract framework-specific interactions into page objects:

```ts
// tests/e2e/pages/auth.page.ts
export class AuthPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto('/login'); // Entry point — valid page.goto
    await this.page.fill('[name=email]', email);
    await this.page.fill('[name=password]', password);
    await this.page.click('button[type=submit]');
    await this.page.waitForURL(url => !url.pathname.includes('/login'), { timeout: 10000 });
  }
}
```

Note: `page.goto('/login')` is acceptable here because login is an entry point — the user types the app URL to start. After login, all navigation is via UI.

## 5. Test user helpers

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

## 6. Global setup and teardown

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

## 7. Screenshot-based visual validation

Take screenshots during tests for visual validation — light/dark mode, desktop/mobile:

```ts
test('dashboard renders correctly', async ({ page }) => {
  // Navigate to dashboard via UI (not page.goto)
  await page.getByRole('navigation').getByRole('link', { name: /dashboard/i }).click();
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'test-results/dashboard-desktop-light.png', fullPage: true });

  // Toggle dark mode via UI
  await page.getByRole('button', { name: /switch to/i }).click();
  await page.screenshot({ path: 'test-results/dashboard-desktop-dark.png', fullPage: true });
});
```

## 8. Browser console capture

Capture browser errors during test runs to detect issues that don't appear in screenshots:

```ts
// tests/e2e/fixtures/console-capture.ts
import { test as base } from '@playwright/test';

export const test = base.extend<{ consoleErrors: string[] }>({
  consoleErrors: async ({ page }, use) => {
    const errors: string[] = [];

    page.on('pageerror', (error) => {
      errors.push(`[PAGE ERROR] ${error.message}`);
    });

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(`[CONSOLE ERROR] ${msg.text()}`);
      }
    });

    await use(errors);
  },
});

// Usage in tests:
test('no console errors on dashboard', async ({ page, consoleErrors }) => {
  // ... navigate and interact ...
  expect(consoleErrors).toEqual([]);
});
```

Common browser-only errors to watch for:
- **Hydration mismatches** — server/client HTML divergence (framework-specific messages)
- **Runtime TypeError/ReferenceError** — accessing undefined properties
- **Unhandled promise rejections** — async operations without catch
- **Failed fetch requests** — 4xx/5xx responses from API calls

## 9. Rules

| # | Rule | Why |
|---|------|-----|
| 1 | **Navigate like a human** — no `page.goto()` except initial entry | Catches navigation bugs, tests real user flows, validates routing |
| 2 | Headless by default | No window stealing; same rendering; zero disruption |
| 3 | `webServer` config for test server lifecycle | Automatic startup/shutdown; no orphan processes |
| 4 | `.env.test` for test env vars | Single source of truth for test configuration |
| 5 | `reuseExistingServer: !process.env.CI` | Dev reuses; CI starts fresh |
| 6 | Short timeouts (5-10s) with descriptive errors | Fail fast with context |
| 7 | `trace: 'on-first-retry'` in config | Post-mortem debugging without overhead |
| 8 | Page objects for reusable interactions | Framework-agnostic, boilerplate-ready |
| 9 | State changes through UI, not direct DB | Framework caching invalidates only through mutation paths |
| 10 | Test data isolation by prefix (`e2e-*`) | Parallel tests don't collide |
| 11 | Manual test user preserved across runs | Developer can always log in after tests finish |
| 12 | Teardown kills servers and frees ports | No port conflicts between test and manual runs |
| 13 | Screenshots for visual validation (light/dark, desktop/mobile) | Agent validates visually before presenting as done |
| 14 | Capture browser console errors | Catches hydration, runtime, and network errors invisible in screenshots |
| 15 | "Full test" = unit + lint + E2E | Each layer catches different classes of bugs |

## Framework-agnostic design

| Concern | Framework-specific | Abstraction |
|---------|-------------------|-------------|
| Dev server command | `next dev`, `vite dev`, `bun run dev` | `TEST_SERVER_COMMAND` env var |
| Test port | Varies | `TEST_BASE_URL` env var (default `http://localhost:3000`) |
| Auth flow | Login form varies | Page object `AuthPage.login(email, pwd)` |
| Env loading | Format varies | `dotenv-cli` or framework-native env loading |
| Server readiness | Health check varies | `webServer.url` in config (Playwright polls automatically) |
