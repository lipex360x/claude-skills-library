#!/usr/bin/env bash
# ==============================================================================
# issue-backup — SQLite backup for GitHub issue bodies before write operations
#
# Snapshots issue bodies into a local SQLite database so they can be restored
# if a write operation (gh issue edit) accidentally destroys content.
# Compatible with macOS default bash (3.x).
#
# Usage:
#   issue-backup snapshot <number>     Snapshot current body of issue #N
#   issue-backup snapshot-all          Snapshot all open issues
#   issue-backup restore <number>      Restore issue #N from latest snapshot
#   issue-backup list [number]         List snapshots (all or for issue #N)
#   issue-backup cleanup <number>      Delete all snapshots for issue #N
#   issue-backup --check               Report DB status without changes
#   issue-backup --verbose             Show detailed output
#   issue-backup --help                Show this help
# ==============================================================================

set -euo pipefail

# --- Constants ----------------------------------------------------------------

GIT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")"
DB_PATH="${GIT_ROOT}/.claude/issues.db"
MAX_SNAPSHOTS_PER_ISSUE=10

# --- Flags --------------------------------------------------------------------

CHECK_MODE=false
VERBOSE=false
SUBCOMMAND=""
ISSUE_NUMBER=""

for arg in "$@"; do
  case "$arg" in
    --check)   CHECK_MODE=true ;;
    --verbose) VERBOSE=true ;;
    --help|-h)
      sed -n '/^# Usage:/,/^# ===/{ /^# ===/d; s/^# \{0,1\}//; p; }' "$0"
      exit 0
      ;;
    snapshot|snapshot-all|restore|list|cleanup)
      SUBCOMMAND="$arg"
      ;;
    *)
      if printf '%s' "$arg" | grep -qE '^[0-9]+$'; then
        if [ -z "$ISSUE_NUMBER" ]; then
          ISSUE_NUMBER="$arg"
        else
          printf "\033[0;31m[error]\033[0m Multiple issue numbers provided (try --help)\n"
          exit 1
        fi
      else
        printf "\033[0;31m[error]\033[0m Unknown argument: %s (try --help)\n" "$arg"
        exit 1
      fi
      ;;
  esac
done

# --- Output helpers -----------------------------------------------------------

if [ -t 1 ]; then
  _blue="\033[0;34m" _green="\033[0;32m" _yellow="\033[0;33m"
  _red="\033[0;31m" _dim="\033[0;90m" _reset="\033[0m"
else
  _blue="" _green="" _yellow="" _red="" _dim="" _reset=""
fi

info()  { printf "${_blue}[info]${_reset}  %s\n" "$1"; }
ok()    { printf "${_green}[ok]${_reset}    %s\n" "$1"; }
warn()  { printf "${_yellow}[warn]${_reset}  %s\n" "$1"; }
error() { printf "${_red}[error]${_reset} %s\n" "$1"; }
dim()   { printf "${_dim}[ok]${_reset}    %s\n" "$1"; }

vdim()  { if $VERBOSE; then dim "$1"; fi; }
vinfo() { if $VERBOSE; then info "$1"; fi; }

# --- Counters -----------------------------------------------------------------

cnt_ok=0
cnt_changed=0
cnt_warned=0
cnt_drift=0

# --- Pre-flight checks -------------------------------------------------------

if ! command -v sqlite3 &>/dev/null; then
  error "sqlite3 is required but not installed"
  exit 1
fi

if ! command -v gh &>/dev/null; then
  error "gh (GitHub CLI) is required but not installed"
  exit 1
fi

if ! gh auth status &>/dev/null; then
  error "gh is not authenticated — run 'gh auth login'"
  exit 1
fi

# --- DB init ------------------------------------------------------------------

init_db() {
  if [ ! -d "$(dirname "$DB_PATH")" ]; then
    mkdir -p "$(dirname "$DB_PATH")"
  fi

  sqlite3 "$DB_PATH" "
    CREATE TABLE IF NOT EXISTS snapshots (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      issue_number INTEGER NOT NULL,
      body TEXT NOT NULL,
      line_count INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
    );
    CREATE INDEX IF NOT EXISTS idx_issue_date
      ON snapshots(issue_number, created_at DESC);
  "
  vinfo "Database ready at ${DB_PATH}"
}

# --- Helpers ------------------------------------------------------------------

enforce_retention() {
  local issue="$1"
  local total
  total=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM snapshots WHERE issue_number = $issue;")

  if [ "$total" -gt "$MAX_SNAPSHOTS_PER_ISSUE" ]; then
    sqlite3 "$DB_PATH" "
      DELETE FROM snapshots
      WHERE issue_number = $issue
        AND id NOT IN (
          SELECT id FROM snapshots
          WHERE issue_number = $issue
          ORDER BY created_at DESC
          LIMIT $MAX_SNAPSHOTS_PER_ISSUE
        );
    "
    local pruned=$((total - MAX_SNAPSHOTS_PER_ISSUE))
    vinfo "Retention: pruned ${pruned} old snapshot(s) for issue #${issue}"
  fi
}

sql_escape_body() {
  printf '%s' "$1" | sed "s/'/''/g"
}

# --- Subcommands --------------------------------------------------------------

do_snapshot() {
  local issue="$1"

  vinfo "Fetching issue #${issue} from GitHub..."
  local body
  body=$(gh issue view "$issue" --json body -q .body 2>/dev/null) || {
    error "Failed to fetch issue #${issue} — does it exist?"
    cnt_warned=$((cnt_warned + 1))
    return
  }

  if [ -z "$body" ]; then
    warn "Issue #${issue} has empty body — nothing to snapshot"
    cnt_warned=$((cnt_warned + 1))
    return
  fi

  local line_count
  line_count=$(printf '%s' "$body" | wc -l | tr -d ' ')

  if $CHECK_MODE; then
    warn "Would snapshot issue #${issue} (${line_count} lines)"
    cnt_drift=$((cnt_drift + 1))
    return
  fi

  local escaped
  escaped=$(sql_escape_body "$body")

  sqlite3 "$DB_PATH" "
    INSERT INTO snapshots (issue_number, body, line_count)
    VALUES ($issue, '$escaped', $line_count);
  "

  local saved_lines
  saved_lines=$(sqlite3 "$DB_PATH" "
    SELECT line_count FROM snapshots
    WHERE issue_number = $issue
    ORDER BY created_at DESC
    LIMIT 1;
  ")

  if [ "$saved_lines" != "$line_count" ]; then
    error "Validation failed: snapshot for #${issue} — expected ${line_count} lines, got ${saved_lines}"
    cnt_warned=$((cnt_warned + 1))
    return
  fi

  enforce_retention "$issue"
  ok "Snapshot saved: issue #${issue} (${line_count} lines)"
  cnt_changed=$((cnt_changed + 1))
}

do_snapshot_all() {
  local issues
  issues=$(gh issue list --state open --json number -q '.[].number' | sort -n)

  if [ -z "$issues" ]; then
    info "No open issues found"
    cnt_ok=$((cnt_ok + 1))
    return
  fi

  local count
  count=$(printf '%s\n' "$issues" | wc -l | tr -d ' ')
  info "Found ${count} open issue(s)"

  for issue in $issues; do
    do_snapshot "$issue"
  done
}

do_list() {
  local query

  if [ -n "$ISSUE_NUMBER" ]; then
    query="SELECT id, issue_number, line_count, created_at FROM snapshots WHERE issue_number = $ISSUE_NUMBER ORDER BY created_at DESC;"
    vinfo "Listing snapshots for issue #${ISSUE_NUMBER}"
  else
    query="SELECT id, issue_number, line_count, created_at FROM snapshots ORDER BY issue_number, created_at DESC;"
    vinfo "Listing all snapshots"
  fi

  local result
  result=$(sqlite3 -header -column "$DB_PATH" "$query" 2>/dev/null) || {
    error "Database not initialized — run a snapshot first"
    exit 1
  }

  if [ -z "$result" ]; then
    if [ -n "$ISSUE_NUMBER" ]; then
      info "No snapshots for issue #${ISSUE_NUMBER}"
    else
      info "No snapshots in database"
    fi
    cnt_ok=$((cnt_ok + 1))
    return
  fi

  printf '%s\n' "$result"
  cnt_ok=$((cnt_ok + 1))
}

do_restore() {
  local issue="$1"

  vinfo "Reading latest snapshot for issue #${issue}..."
  local latest_body
  latest_body=$(sqlite3 "$DB_PATH" "
    SELECT body FROM snapshots
    WHERE issue_number = $issue
    ORDER BY created_at DESC
    LIMIT 1;
  " 2>/dev/null) || {
    error "Database not initialized — run a snapshot first"
    exit 1
  }

  if [ -z "$latest_body" ]; then
    error "No snapshots found for issue #${issue}"
    exit 1
  fi

  local snapshot_lines
  snapshot_lines=$(sqlite3 "$DB_PATH" "
    SELECT line_count FROM snapshots
    WHERE issue_number = $issue
    ORDER BY created_at DESC
    LIMIT 1;
  ")

  vinfo "Fetching current body from GitHub..."
  local current_body current_lines
  current_body=$(gh issue view "$issue" --json body -q .body)
  current_lines=$(printf '%s' "$current_body" | wc -l | tr -d ' ')

  info "Current body: ${current_lines} lines"
  info "Snapshot body: ${snapshot_lines} lines"

  if [ "$current_body" = "$latest_body" ]; then
    ok "Issue #${issue} body matches latest snapshot — no restore needed"
    cnt_ok=$((cnt_ok + 1))
    return
  fi

  if $CHECK_MODE; then
    warn "Would restore issue #${issue} from snapshot (${snapshot_lines} lines)"
    cnt_drift=$((cnt_drift + 1))
    return
  fi

  local tmp_file
  tmp_file=$(mktemp /tmp/issue-restore-XXXXXX.md)
  printf '%s' "$latest_body" > "$tmp_file"

  local restored_lines
  restored_lines=$(wc -l < "$tmp_file" | tr -d ' ')
  if [ "$restored_lines" -lt 1 ]; then
    error "Snapshot body is empty — aborting restore to prevent damage"
    rm -f "$tmp_file"
    exit 1
  fi

  gh issue edit "$issue" --body-file "$tmp_file"
  rm -f "$tmp_file"

  local verify_body verify_lines
  verify_body=$(gh issue view "$issue" --json body -q .body)
  verify_lines=$(printf '%s' "$verify_body" | wc -l | tr -d ' ')

  if [ "$verify_lines" -ne "$snapshot_lines" ]; then
    error "Validation failed: expected ${snapshot_lines} lines after restore, got ${verify_lines}"
    cnt_warned=$((cnt_warned + 1))
    return
  fi

  ok "Issue #${issue} restored from snapshot (${snapshot_lines} lines)"
  cnt_changed=$((cnt_changed + 1))
}

do_cleanup() {
  local issue="$1"

  local count
  count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM snapshots WHERE issue_number = $issue;" 2>/dev/null) || {
    error "Database not initialized"
    exit 1
  }

  if [ "$count" -eq 0 ]; then
    info "No snapshots for issue #${issue}"
    cnt_ok=$((cnt_ok + 1))
    return
  fi

  if $CHECK_MODE; then
    warn "Would delete ${count} snapshot(s) for issue #${issue}"
    cnt_drift=$((cnt_drift + 1))
    return
  fi

  sqlite3 "$DB_PATH" "DELETE FROM snapshots WHERE issue_number = $issue;"
  ok "Deleted ${count} snapshot(s) for issue #${issue}"
  cnt_changed=$((cnt_changed + 1))
}

do_status() {
  if [ -f "$DB_PATH" ]; then
    local total_snapshots total_issues
    total_snapshots=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM snapshots;" 2>/dev/null || echo "0")
    total_issues=$(sqlite3 "$DB_PATH" "SELECT COUNT(DISTINCT issue_number) FROM snapshots;" 2>/dev/null || echo "0")
    info "DB: ${DB_PATH}"
    info "Snapshots: ${total_snapshots} across ${total_issues} issue(s)"
    cnt_ok=$((cnt_ok + 1))
  else
    warn "No database found at ${DB_PATH}"
    cnt_drift=$((cnt_drift + 1))
  fi
}

# --- Main logic ---------------------------------------------------------------

init_db

case "$SUBCOMMAND" in
  snapshot)
    if [ -z "$ISSUE_NUMBER" ]; then
      error "Usage: issue-backup snapshot <number>"
      exit 1
    fi
    do_snapshot "$ISSUE_NUMBER"
    ;;
  snapshot-all)
    do_snapshot_all
    ;;
  restore)
    if [ -z "$ISSUE_NUMBER" ]; then
      error "Usage: issue-backup restore <number>"
      exit 1
    fi
    do_restore "$ISSUE_NUMBER"
    ;;
  list)
    do_list
    ;;
  cleanup)
    if [ -z "$ISSUE_NUMBER" ]; then
      error "Usage: issue-backup cleanup <number>"
      exit 1
    fi
    do_cleanup "$ISSUE_NUMBER"
    ;;
  "")
    if $CHECK_MODE; then
      do_status
    else
      error "No subcommand provided (try --help)"
      exit 1
    fi
    ;;
  *)
    error "Unknown subcommand: ${SUBCOMMAND} (try --help)"
    exit 1
    ;;
esac

# --- Validation ---------------------------------------------------------------

if ! $CHECK_MODE; then
  validation_ok=true

  if [ ! -f "$DB_PATH" ]; then
    error "Database file missing after operation: ${DB_PATH}"
    validation_ok=false
  elif ! sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM snapshots;" &>/dev/null; then
    error "Database corrupted — cannot read snapshots table"
    validation_ok=false
  fi

  if $validation_ok; then
    vinfo "Validation passed"
  fi
fi

# --- Summary ------------------------------------------------------------------

echo ""
if $CHECK_MODE; then
  if [ "$cnt_drift" -eq 0 ]; then
    printf "${_green}✓ Everything in sync.${_reset} No changes needed.\n"
  else
    printf "${_yellow}⚠ %d item(s) would change.${_reset} Run without --check to apply.\n" "$cnt_drift"
  fi
else
  if [ "$cnt_changed" -gt 0 ] || [ "$cnt_ok" -gt 0 ] || [ "$cnt_warned" -gt 0 ]; then
    printf "${_green}✓ Done.${_reset}"
    parts=""
    if [ "$cnt_changed" -gt 0 ]; then parts="$parts ${cnt_changed} saved,"; fi
    if [ "$cnt_ok" -gt 0 ]; then      parts="$parts ${cnt_ok} already ok,"; fi
    if [ "$cnt_warned" -gt 0 ]; then  parts="$parts ${cnt_warned} warning(s),"; fi
    parts="$(echo "$parts" | sed 's/,$//')"
    if [ -n "$parts" ]; then printf " %s." "$parts"; fi
    echo ""
  fi
fi
