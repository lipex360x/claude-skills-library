#!/usr/bin/env bash
# validate-issue.sh — Validate issue checkbox tags against development rules
#
# Checks structural rules (tag presence, ordering, dependencies), semantic
# rules (RED mentions test, GREEN doesn't write tests), sizing limits,
# and UI chain enforcement. This is the backbone of the issue-driven
# development process — every issue must pass before work begins.
#
# Configuration: validate-issue.config.json (same directory)
# - thresholds: max_steps, max_checkboxes_error, max_checkboxes_warn, max_checkbox_chars
# - levels: per-rule severity (error, warn, off)
#
# Usage:
#   validate-issue.sh <issue-number>            Validate and report
#   validate-issue.sh <issue-number> --verbose  Show passing checks too
#   validate-issue.sh --help                    Show this help
#
# Tags: [RED] [GREEN] [INFRA] [WIRE] [E2E] [PW] [HUMAN] [DOCS] [AUDIT]
# Expected order: RED → GREEN → INFRA → WIRE → E2E → PW → HUMAN → DOCS → AUDIT

set -euo pipefail

# ─── Flags ────────────────────────────────────────────────

ISSUE_NUMBER=""
VERBOSE=false

for arg in "$@"; do
    case "$arg" in
        --verbose) VERBOSE=true ;;
        --help|-h)
            sed -n '/^# Usage:/,/^$/p' "$0" | sed 's/^# \?//'
            exit 0
            ;;
        *) ISSUE_NUMBER="$arg" ;;
    esac
done

if [ -z "$ISSUE_NUMBER" ]; then
    printf "\033[0;31m[error]\033[0m Usage: validate-issue.sh <issue-number> [--verbose]\n"
    exit 1
fi

# ─── Config ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/validate-issue.config.json"

cfg_threshold() {
    local key="$1" default="$2"
    if [ -f "$CONFIG_FILE" ]; then
        jq -r ".thresholds.$key // $default" "$CONFIG_FILE" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

cfg_level() {
    local key="$1" default="$2"
    if [ -f "$CONFIG_FILE" ]; then
        jq -r ".levels.$key // \"$default\"" "$CONFIG_FILE" 2>/dev/null || echo "$default"
    else
        echo "$default"
    fi
}

MAX_STEPS=$(cfg_threshold "max_steps" "8")
MAX_CB_ERROR=$(cfg_threshold "max_checkboxes_error" "8")
MAX_CB_WARN=$(cfg_threshold "max_checkboxes_warn" "6")
MAX_CB_CHARS=$(cfg_threshold "max_checkbox_chars" "200")

# ─── Output helpers ───────────────────────────────────────

if [ -t 1 ]; then
    _green="\033[0;32m" _yellow="\033[1;33m"
    _red="\033[0;31m" _cyan="\033[0;36m" _reset="\033[0m"
else
    _green="" _yellow="" _red="" _cyan="" _reset=""
fi

pass() { if $VERBOSE; then printf "${_green}  ✓${_reset} %s\n" "$1"; fi; }
warn() { printf "${_yellow}  ⚠${_reset} %s\n" "$1"; WARNINGS=$((WARNINGS + 1)); }
fail() { printf "${_red}  ✗${_reset} %s\n" "$1"; ERRORS=$((ERRORS + 1)); }
section() { printf "\n${_cyan}%s${_reset}\n" "$1"; }

# emit — route a configurable rule to fail, warn, or skip
emit() {
    local rule="$1" msg="$2" default="${3:-warn}"
    local level
    level=$(cfg_level "$rule" "$default")
    case "$level" in
        error) fail "$msg" ;;
        warn)  warn "$msg" ;;
        off)   if $VERBOSE; then pass "$msg (suppressed)"; fi ;;
    esac
}

# ─── Pre-flight ───────────────────────────────────────────

if ! command -v gh >/dev/null 2>&1; then
    printf "${_red}[error]${_reset} gh CLI is required\n"
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    printf "${_red}[error]${_reset} jq is required (brew install jq)\n"
    exit 1
fi

BODY=$(gh issue view "$ISSUE_NUMBER" --json body -q '.body')
if [ -z "$BODY" ]; then
    printf "${_red}[error]${_reset} Could not fetch issue #%s\n" "$ISSUE_NUMBER"
    exit 1
fi

ERRORS=0
WARNINGS=0

section "Validating issue #$ISSUE_NUMBER"

# ═══════════════════════════════════════════════════════════
# LAYER 1: Issue structure
# ═══════════════════════════════════════════════════════════

# Rule: ## What section required
if echo "$BODY" | grep -q '^## What'; then
    pass "Section '## What' found"
else
    fail "Missing '## What' section — issue must explain what is being built"
fi

# Rule: ## Why section required
if echo "$BODY" | grep -q '^## Why'; then
    pass "Section '## Why' found"
else
    fail "Missing '## Why' section — issue must explain motivation"
fi

# Rule: Acceptance criteria with checkboxes
ac_count=$(echo "$BODY" | sed -n '/^## Acceptance criteria/,/^## /p' | grep -c '^\- \[' || true)
if [ "$ac_count" -eq 0 ]; then
    fail "Missing acceptance criteria — needs '## Acceptance criteria' with ≥1 checkbox"
else
    pass "Acceptance criteria: $ac_count checkbox(es)"
fi

# Rule: Step count 2-max
step_count=$(echo "$BODY" | grep -c '^## Step [0-9]' || true)
if [ "$step_count" -lt 2 ]; then
    fail "Too few steps ($step_count) — minimum is 2"
elif [ "$step_count" -gt "$MAX_STEPS" ]; then
    fail "Too many steps ($step_count) — maximum is $MAX_STEPS, split into multiple issues"
else
    pass "Step count: $step_count (within 2-$MAX_STEPS)"
fi

# Rule: Sequential step numbering (no gaps, no duplicates)
expected_num=1
numbering_ok=true
while IFS= read -r step_line; do
    actual_num=$(echo "$step_line" | grep -oE '[0-9]+' | head -1)
    if [ "$actual_num" != "$expected_num" ]; then
        fail "Step numbering gap: expected Step $expected_num, found Step $actual_num"
        numbering_ok=false
    fi
    expected_num=$((expected_num + 1))
done <<< "$(echo "$BODY" | grep '^## Step [0-9]')"
if $numbering_ok; then pass "Step numbering: sequential"; fi

# Rule: Step title format — must use em dash (—), not hyphen (-)
while IFS= read -r step_line; do
    if ! echo "$step_line" | grep -q '—'; then
        step_n=$(echo "$step_line" | grep -oE '[0-9]+' | head -1)
        fail "Step $step_n title uses hyphen instead of em dash (—)"
    fi
done <<< "$(echo "$BODY" | grep '^## Step [0-9]')"

# ═══════════════════════════════════════════════════════════
# LAYER 2-5: Per-step validation
# ═══════════════════════════════════════════════════════════

STEP_NUM=0
STEP_TITLE=""
STEP_TAGS=""
CHECKBOX_COUNT=0
LAST_RED_OR_GREEN=""
CHECKBOX_TEXTS=""
HAS_FRONTEND_UI=false

validate_step() {
    local num="$1"
    local title="$2"
    local tags="$3"
    local cb_count="$4"

    if [ "$num" -eq 0 ]; then return; fi

    section "Step $num — $title"

    # ── Layer 2: Sizing ───────────────────────────────────

    # Rule: Empty steps
    if [ "$cb_count" -eq 0 ]; then
        fail "Empty step — no checkboxes found"
        return
    fi

    # Rule: >warn threshold checkboxes
    if [ "$cb_count" -gt "$MAX_CB_WARN" ] && [ "$cb_count" -le "$MAX_CB_ERROR" ]; then
        emit "checkbox_count_warn" "$cb_count checkboxes — recommended maximum is $MAX_CB_WARN"
    fi

    # Rule: >error threshold checkboxes
    if [ "$cb_count" -gt "$MAX_CB_ERROR" ]; then
        fail "$cb_count checkboxes — maximum is $MAX_CB_ERROR, split this step"
    fi

    # ── Layer 3: Tag chain rules ──────────────────────────

    # Rule 1: GREEN requires RED
    if echo "$tags" | grep -q "GREEN" && ! echo "$tags" | grep -q "RED"; then
        fail "[GREEN] without [RED] — needs a failing test first (or should be [INFRA])"
    fi

    # Rule 2: E2E requires PW
    if echo "$tags" | grep -q "E2E" && ! echo "$tags" | grep -q "PW"; then
        fail "[E2E] without [PW] — E2E tests need Playwright verification"
    fi

    # Rule 3: PW requires HUMAN
    if echo "$tags" | grep -q "PW" && ! echo "$tags" | grep -q "HUMAN"; then
        fail "[PW] without [HUMAN] — visual verification needs human approval"
    fi

    # Rule 4: HUMAN requires PW
    if echo "$tags" | grep -q "HUMAN" && ! echo "$tags" | grep -q "PW"; then
        fail "[HUMAN] without [PW] — human validation without Playwright verification"
    fi

    # Rule 5: AUDIT mandatory
    if ! echo "$tags" | grep -q "AUDIT"; then
        fail "Missing [AUDIT] — every step needs a quality.md audit"
    fi

    # Rule 6: DOCS recommended with GREEN/WIRE
    if (echo "$tags" | grep -q "GREEN" || echo "$tags" | grep -q "WIRE") && ! echo "$tags" | grep -q "DOCS"; then
        emit "docs_recommended" "No [DOCS] — consider updating ARCHITECTURE.md after implementation"
    fi

    # Rule 7: AUDIT must be last tag
    local last_tag
    last_tag=$(echo "$tags" | tr ' ' '\n' | grep -v '^$' | tail -1)
    if echo "$tags" | grep -q "AUDIT" && [ "$last_tag" != "AUDIT" ]; then
        fail "[AUDIT] must be the last checkbox (found [$last_tag] after it)"
    fi

    # Rule 8: Tag sequence order
    local expected_order="RED GREEN INFRA WIRE E2E PW HUMAN DOCS AUDIT"
    local prev_pos=0
    for tag in $tags; do
        local pos=0 i=1
        for expected in $expected_order; do
            if [ "$tag" = "$expected" ]; then pos=$i; break; fi
            i=$((i + 1))
        done
        if [ "$pos" -gt 0 ] && [ "$pos" -lt "$prev_pos" ]; then
            emit "tag_ordering" "Tag order: [$tag] out of sequence — expected: RED → GREEN → INFRA → WIRE → E2E → PW → HUMAN → DOCS → AUDIT"
        fi
        if [ "$pos" -gt 0 ]; then prev_pos=$pos; fi
    done

    # Rule: UI chain — frontend work requires E2E + PW + HUMAN
    if $HAS_FRONTEND_UI; then
        if ! echo "$tags" | grep -q "E2E"; then
            fail "Frontend UI work without [E2E] — visible components need E2E tests"
        fi
        if ! echo "$tags" | grep -q "PW"; then
            fail "Frontend UI work without [PW] — visible components need visual verification"
        fi
        if ! echo "$tags" | grep -q "HUMAN"; then
            fail "Frontend UI work without [HUMAN] — visible components need human approval"
        fi
    fi

    # Rule: E2E without RED
    if echo "$tags" | grep -q "E2E" && ! echo "$tags" | grep -q "RED"; then
        emit "e2e_without_red" "[E2E] without [RED] — E2E tests without unit tests is fragile coverage"
    fi

    # Rule: Last AUDIT should be quality.md audit
    local audit_lines
    audit_lines=$(echo "$CHECKBOX_TEXTS" | grep '\[AUDIT\]' || true)
    if [ -n "$audit_lines" ]; then
        local last_audit
        last_audit=$(echo "$audit_lines" | tail -1 | tr '[:upper:]' '[:lower:]')
        if ! echo "$last_audit" | grep -qE 'quality\.md'; then
            emit "last_audit_quality" "Last [AUDIT] doesn't mention quality.md — the final audit should be the quality.md review"
        fi
    fi

    # Rule: Duplicate checkboxes
    local dupes
    dupes=$(echo "$CHECKBOX_TEXTS" | sed 's/^- \[.\] `\[[A-Z]*\]` //' | sort | uniq -d || true)
    if [ -n "$dupes" ]; then
        fail "Duplicate checkbox: $(echo "$dupes" | head -1)"
    fi

    # All passed
    pass "Tags:$tags"
}

# ─── Main parse loop ─────────────────────────────────────

while IFS= read -r line; do
    # Detect step headers
    if echo "$line" | grep -qE '^## Step [0-9]+ — '; then
        validate_step "$STEP_NUM" "$STEP_TITLE" "$STEP_TAGS" "$CHECKBOX_COUNT"
        STEP_NUM=$(echo "$line" | grep -oE '[0-9]+' | head -1)
        STEP_TITLE=$(echo "$line" | sed 's/^## Step [0-9]* — //')
        STEP_TAGS=""
        CHECKBOX_COUNT=0
        LAST_RED_OR_GREEN=""
        CHECKBOX_TEXTS=""
        HAS_FRONTEND_UI=false
        continue
    fi

    # Skip non-tagged checkbox lines
    if ! echo "$line" | grep -qE '^\- \[.\] `\[[A-Z0-9]+\]`'; then
        continue
    fi

    # Extract tag
    local_tag=$(echo "$line" | grep -oE '\[[A-Z0-9]+\]' | head -1 | tr -d '[]')
    if [ -z "$local_tag" ]; then
        fail "Checkbox without tag in Step $STEP_NUM: $line"
        continue
    fi

    STEP_TAGS="$STEP_TAGS $local_tag"
    CHECKBOX_COUNT=$((CHECKBOX_COUNT + 1))
    CHECKBOX_TEXTS="$CHECKBOX_TEXTS
$line"
    lower_line=$(echo "$line" | tr '[:upper:]' '[:lower:]')

    # ── Layer 2: Checkbox-level checks ────────────────────

    # Rule: Checkbox text length > threshold
    cb_text=$(echo "$line" | sed 's/^- \[.\] `\[[A-Z]*\]` //')
    if [ "${#cb_text}" -gt "$MAX_CB_CHARS" ]; then
        emit "checkbox_length" "Checkbox > $MAX_CB_CHARS chars — consider splitting: $(echo "$cb_text" | cut -c1-60)..."
    fi

    # Rule: Empty checkbox text
    if [ -z "$cb_text" ] || [ "$cb_text" = " " ]; then
        fail "Empty checkbox text after [$local_tag] — needs a description"
    fi

    # ── Layer 4: Semantic validation per tag ──────────────

    case "$local_tag" in
        RED)
            # Rule: RED must mention test
            if ! echo "$lower_line" | grep -qE 'test|spec|_test|\.test'; then
                fail "[RED] doesn't mention a test — RED is for writing failing tests"
            fi
            # Rule: TDD horizontal — RED after RED without GREEN
            if [ "$LAST_RED_OR_GREEN" = "RED" ]; then
                fail "[RED] after [RED] without [GREEN] — horizontal TDD (write one test, implement, repeat)"
            fi
            LAST_RED_OR_GREEN="RED"
            ;;
        GREEN)
            # Rule: GREEN before RED
            if ! echo "$STEP_TAGS" | grep -q "RED"; then
                fail "[GREEN] appears before [RED] — test must come first"
            fi
            # Rule: GREEN should not mention writing tests
            if echo "$lower_line" | grep -qE '\bwrite\b.*\btest\b|\bcreate\b.*\btest\b'; then
                emit "green_writes_tests" "[GREEN] mentions writing tests — should this be [RED]?"
            fi
            # Detect frontend UI work
            if echo "$lower_line" | grep -qE 'component|page|layout|frontend|sidebar|chat.*interface|ui'; then
                HAS_FRONTEND_UI=true
            fi
            LAST_RED_OR_GREEN="GREEN"
            ;;
        E2E)
            # Rule: E2E must mention test
            if ! echo "$lower_line" | grep -qE 'test|spec|\.spec|playwright'; then
                fail "[E2E] doesn't mention a test — E2E is for writing Playwright tests"
            fi
            ;;
        PW)
            # Rule: PW must mention verification
            if ! echo "$lower_line" | grep -qE 'screenshot|run.*test|verify|visual'; then
                emit "pw_mentions_visual" "[PW] doesn't mention screenshots or visual verification"
            fi
            ;;
        HUMAN)
            # Rule: HUMAN must mention user validation
            if ! echo "$lower_line" | grep -qE 'screenshot|approval|user|present|wait'; then
                emit "human_mentions_user" "[HUMAN] doesn't mention presenting to user or waiting for approval"
            fi
            ;;
        AUDIT)
            # Rule: AUDIT must mention quality.md or audit
            if ! echo "$lower_line" | grep -qE 'quality\.md|audit|review.*rule'; then
                emit "audit_mentions_quality" "[AUDIT] doesn't mention quality.md or audit"
            fi
            ;;
        DOCS)
            # Rule: DOCS should mention ARCHITECTURE.md
            if ! echo "$lower_line" | grep -qE 'architecture\.md|architecture'; then
                emit "docs_mentions_architecture" "[DOCS] doesn't mention ARCHITECTURE.md — DOCS convention is to update it"
            fi
            ;;
        INFRA)
            # Rule: INFRA should not mention writing tests
            if echo "$lower_line" | grep -qE '\bwrite\b.*\btest\b|\bcreate\b.*\btest\b'; then
                emit "infra_writes_tests" "[INFRA] mentions writing tests — should this be [RED] or [E2E]?"
            fi
            ;;
        WIRE)
            # Rule: WIRE must mention integration
            if ! echo "$lower_line" | grep -qE 'connect|integrat|endpoint|frontend.*backend|backend.*frontend'; then
                emit "wire_mentions_integration" "[WIRE] doesn't mention integration/connection between layers"
            fi
            # Detect frontend UI work
            if echo "$lower_line" | grep -qE 'frontend|component|streaming.*display|message.*display'; then
                HAS_FRONTEND_UI=true
            fi
            ;;
    esac
done <<< "$BODY"

# Validate last step
validate_step "$STEP_NUM" "$STEP_TITLE" "$STEP_TAGS" "$CHECKBOX_COUNT"

# ═══════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════

section "Summary"
printf "  Errors:   ${_red}%d${_reset}\n" "$ERRORS"
printf "  Warnings: ${_yellow}%d${_reset}\n" "$WARNINGS"

if [ -f "$CONFIG_FILE" ]; then
    printf "  Config:   ${_cyan}%s${_reset}\n" "$CONFIG_FILE"
fi

if [ "$ERRORS" -gt 0 ]; then
    printf "\n${_red}Validation failed with %d error(s).${_reset}\n" "$ERRORS"
    exit 1
else
    printf "\n${_green}Validation passed.${_reset}\n"
    exit 0
fi
