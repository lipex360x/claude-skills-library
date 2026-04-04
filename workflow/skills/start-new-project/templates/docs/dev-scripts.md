# Dev Scripts — Startup & Teardown Reference

Every project with backend services, databases, or multi-process orchestration needs a pair of scripts: `dev-start.sh` (bring everything up) and `dev-stop.sh` (tear everything down). These scripts live in `scripts/` at the project root and must be referenced in ARCHITECTURE.md.

## Why

Without these scripts, every new session starts with "how do I run this?" — the developer (or agent) must mentally reconstruct the startup sequence. With them, it's always one command: `scripts/dev-start.sh`.

## What goes in each script

### `scripts/dev-start.sh` — Startup

The script brings the full local environment up in the correct order. Adapt to the project's stack:

| Phase | What it does | Examples |
|-------|-------------|----------|
| **Pre-flight** | Validate required tools exist | `docker`, `bun`/`npm`/`python`, `supabase` CLI |
| **Port cleanup** | Kill anything on the project's ports | `lsof -i :3000 -t \| xargs kill` |
| **Infrastructure** | Start databases, queues, caches | `docker compose -f docker-compose.test.yml up -d --wait`, `supabase start` |
| **Migrations** | Apply schema changes | `drizzle-kit migrate`, `supabase db push`, `alembic upgrade head` |
| **Seed** | Populate test data | Run seed script, import fixtures |
| **Test user** | Create a manual login user | API signup call or direct DB insert |
| **Services** | Start backend + frontend | API on one port, frontend on another |
| **Health check** | Verify everything is running | `curl` retry loops on `/health` and frontend URL |
| **Validation** | Verify everything is actually working | Health check, port test, seed verification, login test |
| **Summary** | Print URLs and credentials | Ports, login email/password, stop command |

Every phase that starts something must validate it succeeded before proceeding. The validation phase at the end runs a comprehensive audit:

| Check | How | Fail action |
|-------|-----|-------------|
| **Ports open** | `curl -s -o /dev/null -w "%{http_code}" http://localhost:PORT` | Error with which service failed |
| **Health endpoint** | `curl -s http://localhost:PORT/health` returns 200 | Error: "API not healthy" |
| **DB reachable** | Test connection (psql, supabase status, prisma db execute) | Error: "DB not reachable on port X" |
| **Seed data exists** | Query a known table for minimum row count | Warning: "Seed data missing — run without --skip-seed" |
| **Test user works** | Attempt login via API with test credentials | Warning: "Test user signup may have failed" |
| **Frontend serves** | `curl -s http://localhost:PORT` returns HTML | Error: "Frontend not responding" |

The script must exit with a non-zero code if any critical check (ports, health, DB) fails. Warnings (seed, test user) are logged but don't block.

**Flags:**
- `--skip-seed` — skip seed step when DB already has data (faster restart)
- `--check` — run only the validation phase (no startup, just audit current state)
- `--help` — print usage

### `scripts/dev-stop.sh` — Teardown

The script kills everything the startup created:

| Phase | What it does |
|-------|-------------|
| **Kill services** | Terminate processes on project ports |
| **Stop infrastructure** | `docker compose down`, `supabase stop` |
| **Summary** | Confirm ports freed |

**Flags:**
- `--keep-db` — stop services but keep database running (preserves data for faster restart)
- `--help` — print usage

## Script skeleton

Both scripts follow the same structure:

```bash
#!/usr/bin/env bash
# dev-start — Start all [project] services for local development
#
# Usage:
#   scripts/dev-start.sh              Start everything
#   scripts/dev-start.sh --skip-seed  Skip seed step
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"

# --- Flag parsing ---
SKIP_SEED=false
CHECK_ONLY=false
for arg in "$@"; do
  case "$arg" in
    --skip-seed) SKIP_SEED=true ;;
    --check) CHECK_ONLY=true ;;
    --help|-h)
      sed -n '/^# Usage:/,/^set/{ /^set/d; s/^# \{0,1\}//; p; }' "$0"
      exit 0
      ;;
    *) printf "\033[0;31m[error]\033[0m Unknown flag: %s (try --help)\n" "$arg"; exit 1 ;;
  esac
done

# --- Output helpers ---
info()  { printf "\033[0;34m[info]\033[0m  %s\n" "$1"; }
ok()    { printf "\033[0;32m[ok]\033[0m    %s\n" "$1"; }
error() { printf "\033[0;31m[error]\033[0m %s\n" "$1"; }

cd "$PROJECT_ROOT"

# --- Pre-flight ---
# Check for required tools (docker, runtime, etc.)

# --- Port cleanup ---
for port in 3000 8000; do
  pids=$(lsof -i :"$port" -t 2>/dev/null || true)
  if [ -n "$pids" ]; then
    echo "$pids" | xargs kill 2>/dev/null || true
    info "Killed existing process(es) on port $port"
    sleep 1
  fi
done

# --- Infrastructure (DB, etc.) ---
# docker compose -f docker-compose.test.yml up -d --wait
# supabase start

# --- Migrations ---
# alembic upgrade head / drizzle-kit migrate / supabase db push

# --- Seed ---
if ! $SKIP_SEED; then
  info "Seeding database..."
  # Run seed script
  ok "Database seeded"
fi

# --- Test user ---
# Create manual test user via API or direct insert

# --- Start services ---
# Start backend and frontend with retry loops for readiness

# --- Validation (runs always, including --check mode) ---
validate() {
  local failures=0

  # Port checks
  for port in 3000 8000; do
    if curl -s -o /dev/null -w "" "http://localhost:$port" 2>/dev/null; then
      ok "Port $port responding"
    else
      error "Port $port not responding"
      failures=$((failures + 1))
    fi
  done

  # Health endpoint (adapt URL to project)
  if curl -s http://localhost:8000/health 2>/dev/null | grep -q "ok"; then
    ok "Backend health check passed"
  else
    error "Backend health check failed"
    failures=$((failures + 1))
  fi

  # DB reachable (adapt to project — psql, supabase status, etc.)
  # if supabase status 2>/dev/null | grep -q "running"; then
  #   ok "Database running"
  # else
  #   error "Database not reachable"
  #   failures=$((failures + 1))
  # fi

  # Seed data (adapt query to project — check a known table)
  # ROW_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT count(*) FROM some_table" 2>/dev/null || echo "0")
  # if [ "$ROW_COUNT" -gt 0 ]; then
  #   ok "Seed data present ($ROW_COUNT rows)"
  # else
  #   info "Warning: seed data missing — run without --skip-seed"
  # fi

  # Test user login (adapt to project's auth endpoint)
  # LOGIN_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/api/auth/login \
  #   -H "Content-Type: application/json" \
  #   -d '{"email":"test@project.dev","password":"Test1234"}')
  # if [ "$LOGIN_CODE" = "200" ]; then
  #   ok "Test user login works"
  # else
  #   info "Warning: test user login returned $LOGIN_CODE"
  # fi

  return $failures
}

if $CHECK_ONLY; then
  info "Running validation only (--check)..."
  validate
  exit $?
fi

# Run validation after startup
validate || {
  error "Some checks failed — review output above"
  exit 1
}

echo ""
printf "\033[0;32m✓ All services running.\033[0m\n"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  Login:    test@project.dev / Test1234"
echo ""
echo "  Stop with: scripts/dev-stop.sh"
echo "  Check:     scripts/dev-start.sh --check"
```

## ARCHITECTURE.md reference

The scripts must appear in the `## Scripts` section of ARCHITECTURE.md:

```markdown
## Scripts

- `scripts/dev-start.sh` — Start DB, migrations, seed, test user, backend + frontend
- `scripts/dev-stop.sh` — Kill all services and free ports
```

Gitignored files (`.env.test`, `node_modules/`, build artifacts) do NOT appear in ARCHITECTURE.md.

## Detection rules for /start-issue

When `/start-issue` runs and finds:
1. ARCHITECTURE.md exists
2. `scripts/dev-start.sh` does NOT exist
3. The project has infrastructure signals (docker-compose, .env files, database config, multiple services)

→ Add a Step to the plan: "Create dev startup and teardown scripts". Checkboxes:
- Identify what needs to start (from docker-compose, ARCHITECTURE.md, package.json scripts)
- Identify ports used by each service
- Create `scripts/dev-start.sh` with project-specific startup sequence
- Create `scripts/dev-stop.sh` with matching teardown
- Add `## Scripts` section to ARCHITECTURE.md
- Verify: `scripts/dev-start.sh` brings up all services, `scripts/dev-stop.sh` tears them down
