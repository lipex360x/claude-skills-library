// Template: CDP verification script | Adapt to project language (.ts or .mjs)
// Location: e2e/cdp/verify-<page>.ts
// Run: npx tsx e2e/cdp/verify-<page>.ts (TS) or node e2e/cdp/verify-<page>.mjs (JS)
// Requires: Chrome with --remote-debugging-port=9222, test server on dedicated port
//
// Rules (see references/cdp-best-practices.md):
// - ALWAYS browser.newContext() — never reuse existing context (cookie isolation)
// - ALWAYS context.close() in finally — removes tab even on error
// - Test server on dedicated port with local env — never hit dev server
// - waitUntil: "networkidle" on every goto — prevent interacting before hydration
// - log() with timestamps — identify where scripts hang
// - page.on("pageerror") — catch silent JS errors
// - Short timeouts (5-10s) — fail fast, don't hang
// - Generic login redirect — waitForURL(url => !url.pathname.includes("/login"))
// - Never run_in_background — run inline with Bash tool timeout (30-60s)
// - Screenshots go to test-results/cdp/screenshots/

import { chromium } from "playwright";

const CDP_ENDPOINT = process.env.CDP_ENDPOINT || "http://localhost:9222";
const BASE = process.env.BASE_URL || "http://localhost:3100"; // test port, never dev port

function log(msg: string) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

async function main() {
  log("Connecting to Chrome via CDP...");
  const browser = await chromium.connectOverCDP(CDP_ENDPOINT);

  // ALWAYS fresh context — never browser.contexts()[0]
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 }, // mobile-first
  });
  const page = await context.newPage();

  // Observability — always active
  page.on("pageerror", (err) => log(`[page error] ${err.message}`));

  try {
    // Login (if auth required)
    log("Navigating to login...");
    await page.goto(`${BASE}/login`, { waitUntil: "networkidle" });

    await page.fill('input[name="email"]', "test@user.com");
    await page.fill('input[name="password"]', "test1234");
    await page.click('button[type="submit"]');
    log("Login submitted, waiting for redirect...");

    // Generic redirect — works regardless of destination
    await page
      .waitForURL((url) => !url.pathname.includes("/login"), { timeout: 10000 })
      .catch(() => {
        throw new Error("Login redirect failed — check auth flow");
      });
    log("Login successful");

    // Verify target page — mobile
    log("Navigating to target page (mobile)...");
    await page.goto(`${BASE}/target-page`, { waitUntil: "networkidle" });
    await page.screenshot({
      path: "test-results/cdp/screenshots/target-mobile.png",
      fullPage: true,
    });
    log("Mobile screenshot saved");

    // Verify target page — desktop
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`${BASE}/target-page`, { waitUntil: "networkidle" });
    await page.screenshot({
      path: "test-results/cdp/screenshots/target-desktop.png",
      fullPage: true,
    });
    log("Desktop screenshot saved");

    log("All checks passed");
  } catch (err) {
    log(`FAILED: ${(err as Error).message}`);
    await page.screenshot({
      path: "test-results/cdp/screenshots/failure.png",
      fullPage: true,
    });
    log("Failure screenshot saved");
    process.exit(1);
  } finally {
    await context.close(); // close context, not page — removes the tab cleanly
  }
}

main().catch(console.error);
