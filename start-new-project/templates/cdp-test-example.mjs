// Template: CDP test script (ESM) | Version: 2.0 | Created: 2026-03-16
// Usage: node .claude/cdp-tests/verify-login.mjs
// Requires: Chrome with --remote-debugging-port=9222, test server on port 3100
//
// Rules (see references/cdp-best-practices.md for details):
// - ALWAYS browser.newContext() — never reuse existing context (cookie isolation)
// - Test server on dedicated port (3100) with local env — never hit dev server (3000)
// - waitUntil: "networkidle" on every goto — prevent interacting before hydration
// - log() with timestamps — identify where scripts hang
// - page.on("pageerror") — catch silent JS errors
// - Short timeouts (5-10s) — fail fast, don't hang
// - One page per context, context.close() when done — clean tab lifecycle

import { chromium } from 'playwright';

const CDP_ENDPOINT = process.env.CDP_ENDPOINT || 'http://localhost:9222';
const BASE = process.env.BASE_URL || 'http://localhost:3100'; // test port, never 3000

function log(msg) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

async function main() {
  log('Connecting to Chrome via CDP...');
  const browser = await chromium.connectOverCDP(CDP_ENDPOINT);

  // ALWAYS fresh context — never browser.contexts()[0]
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 }, // mobile-first
  });
  const page = await context.newPage();

  // Observability
  page.on('pageerror', (err) => log(`[page error] ${err.message}`));

  try {
    // Login (if auth required)
    log('Navigating to login...');
    await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });

    await page.fill('input[name="email"]', 'test@user.com');
    await page.fill('input[name="password"]', 'test1234');
    await page.click('button[type="submit"]');
    log('Login submitted, waiting for redirect...');

    await page.waitForURL(`${BASE}/`, { timeout: 10000 })
      .catch(() => { throw new Error('Login redirect failed — check auth flow'); });
    log('Login successful');

    // Verify target page — mobile
    log('Navigating to target page (mobile)...');
    await page.goto(`${BASE}/target-page`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: '.claude/cdp-tests/screenshots/target-mobile.png', fullPage: true });
    log('Mobile screenshot saved');

    // Verify target page — desktop
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`${BASE}/target-page`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: '.claude/cdp-tests/screenshots/target-desktop.png', fullPage: true });
    log('Desktop screenshot saved');

    log('All checks passed');
  } catch (err) {
    log(`FAILED: ${err.message}`);
    await page.screenshot({ path: '.claude/cdp-tests/screenshots/failure.png', fullPage: true });
    log('Failure screenshot saved');
    process.exit(1);
  } finally {
    await context.close(); // close context, not page — removes the tab cleanly
  }
}

main().catch(console.error);
