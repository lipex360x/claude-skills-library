#!/bin/bash
# PostToolUse Hook — Compact issue backup after PR merge
# Matches: Bash commands containing "gh pr merge"
# Returns: Confirmation that issue snapshots were compacted
set -e

INPUT=$(cat)

# --- Filter ---
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
echo "$COMMAND" | grep -q "gh pr merge" || exit 0

# --- Extract PR number ---
PR_NUMBER=$(echo "$COMMAND" | grep -oE 'gh pr merge ([0-9]+)' | grep -oE '[0-9]+' || true)

if [ -z "$PR_NUMBER" ]; then
  PR_NUMBER=$(gh pr list --state merged --limit 1 --json number -q '.[0].number' 2>/dev/null || true)
fi

if [ -z "$PR_NUMBER" ]; then
  exit 0
fi

# --- Find linked issue ---
ISSUE_NUMBER=$(gh pr view "$PR_NUMBER" --json body -q '.body' 2>/dev/null | grep -oE 'Closes #([0-9]+)' | grep -oE '[0-9]+' | head -1 || true)

if [ -z "$ISSUE_NUMBER" ]; then
  exit 0
fi

# --- Compact ---
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")
SCRIPT="$GIT_ROOT/.claude/scripts/issue-backup.sh"

if [ ! -x "$SCRIPT" ]; then
  exit 0
fi

RESULT=$(bash "$SCRIPT" compact "$ISSUE_NUMBER" 2>&1 || true)

if echo "$RESULT" | grep -q "Compacted"; then
  cat <<MSG
[hook] Issue #${ISSUE_NUMBER} backup compacted after PR #${PR_NUMBER} merge (kept latest snapshot only).
MSG
fi

exit 0
