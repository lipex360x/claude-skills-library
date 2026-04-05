#!/bin/bash
# PreToolUse Hook — Snapshot issue body before gh issue edit
# Matches: Bash commands containing "gh issue edit"
# Returns: Confirmation that snapshot was saved (or silent skip)
set -e

INPUT=$(cat)

# --- Filter ---
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')
echo "$COMMAND" | grep -q "gh issue edit" || exit 0

# --- Extract issue number ---
ISSUE_NUMBER=$(echo "$COMMAND" | grep -oE 'gh issue edit ([0-9]+)' | grep -oE '[0-9]+')

if [ -z "$ISSUE_NUMBER" ]; then
  exit 0
fi

# --- Snapshot ---
GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")
SCRIPT="$GIT_ROOT/.claude/scripts/issue-backup.sh"

if [ ! -x "$SCRIPT" ]; then
  exit 0
fi

bash "$SCRIPT" snapshot "$ISSUE_NUMBER" >/dev/null 2>&1 || true

cat <<MSG
[hook] Issue #${ISSUE_NUMBER} body backed up before edit.
MSG

exit 0
