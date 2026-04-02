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
| **Summary** | Print URLs and credentials | Ports, login email/password, stop command |

**Flags:**
- `--skip-seed` — skip seed step when DB already has data (faster restart)
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
for arg in "$@"; do
  case "$arg" in
    --skip-seed) SKIP_SEED=true ;;
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
# Start backend and frontend with health check loops

echo ""
printf "\033[0;32m✓ All services running.\033[0m\n"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:3000"
echo "  Login:    test@project.dev / Test1234"
echo ""
echo "  Stop with: scripts/dev-stop.sh"
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
