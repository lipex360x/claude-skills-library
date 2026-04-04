#!/usr/bin/env bash
# validate-issue.sh — Wrapper for validate-issue.py
#
# Delegates to the Python validator which reads rules from validate-issue.config.json.
# This wrapper exists so existing hooks and skills don't need path changes.
#
# Usage:
#   validate-issue.sh <issue-number>            Validate and report
#   validate-issue.sh <issue-number> --verbose  Show passing checks too
#   validate-issue.sh --help                    Show this help

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/validate-issue.py" "$@"
