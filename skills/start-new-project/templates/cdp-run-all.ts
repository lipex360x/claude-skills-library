// Template: CDP runner — auto-discovers and runs all verify-*.ts scripts
// Location: e2e/cdp/run-all.ts
// Run: npx tsx e2e/cdp/run-all.ts (or via package.json: bun run test:cdp)
// Requires: test server running with env vars (start via `bun run test:cdp:server`)

import { readdirSync } from "fs";
import { execSync } from "child_process";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

function log(msg: string) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

const scripts = readdirSync(__dirname)
  .filter((f) => f.startsWith("verify-") && f.endsWith(".ts"))
  .sort();

if (scripts.length === 0) {
  log("No verify-*.ts scripts found in e2e/cdp/");
  process.exit(0);
}

log(`Found ${scripts.length} CDP verification script(s)`);

let passed = 0;
let failed = 0;
const failures: string[] = [];

for (const script of scripts) {
  const path = join(__dirname, script);
  log(`Running ${script}...`);
  try {
    execSync(`npx tsx ${path}`, { stdio: "inherit", timeout: 60000 });
    passed++;
    log(`${script} — PASSED`);
  } catch {
    failed++;
    failures.push(script);
    log(`${script} — FAILED`);
  }
}

log(`\nResults: ${passed} passed, ${failed} failed out of ${scripts.length}`);

if (failures.length > 0) {
  log(`Failed scripts: ${failures.join(", ")}`);
  process.exit(1);
}
