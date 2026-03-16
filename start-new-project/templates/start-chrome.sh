#!/bin/bash
#
# Template: Chrome CDP launcher (shell script)
# Version: 1.0
# Created: 2026-03-16
# Method: Adapted from claude-design-canvas production setup
# Sources:
#   - Chrome DevTools Protocol docs
#   - Playwright connectOverCDP API
#
# Constraints:
#   - Requires jq for JSON parsing
#   - Chrome/Chromium must be installed
#   - Port 9222 must be free
#   - User data dir at $HOME/.claude/chrome-debug persists sessions
#
# Usage: Copy to .claude/start-chrome.sh in the target project.
# Launch: .claude/start-chrome.sh
# Connect: playwright.chromium.connectOverCDP('http://localhost:9222')

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SETTINGS="$SCRIPT_DIR/project-settings.json"

if [ ! -f "$SETTINGS" ]; then
  echo "Error: $SETTINGS not found"
  echo "Create .claude/project-settings.json with chrome.tabs configuration."
  exit 1
fi

# Read tab URLs from project-settings.json
TABS=$(jq -r '.chrome.tabs | to_entries[] | .value | if startswith("http") then . elif startswith("localhost") then "http://" + . else "https://" + . end' "$SETTINGS" 2>/dev/null)

# Detect Chrome binary across macOS, Linux, and Windows (Git Bash / WSL)
CHROME=""
case "$(uname -s)" in
  Darwin)
    if [ -d "/Applications/Google Chrome.app" ]; then
      CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    fi
    ;;
  MINGW*|MSYS*|CYGWIN*)
    for path in \
      "/c/Program Files/Google/Chrome/Application/chrome.exe" \
      "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
      "$LOCALAPPDATA/Google/Chrome/Application/chrome.exe"; do
      if [ -f "$path" ]; then
        CHROME="$path"
        break
      fi
    done
    ;;
esac

# Fallback: try common commands on PATH (Linux, WSL, or any OS)
if [ -z "$CHROME" ]; then
  for cmd in google-chrome google-chrome-stable chromium chromium-browser chrome; do
    if command -v "$cmd" &>/dev/null; then
      CHROME="$cmd"
      break
    fi
  done
fi

if [ -z "$CHROME" ]; then
  echo "Error: Google Chrome not found."
  echo "Install it from https://www.google.com/chrome/ or via:"
  case "$(uname -s)" in
    Darwin)        echo "  brew install --cask google-chrome" ;;
    MINGW*|MSYS*|CYGWIN*) echo "  winget install Google.Chrome" ;;
    *)             echo "  sudo apt install google-chrome-stable  # Debian/Ubuntu"
                   echo "  sudo dnf install google-chrome-stable  # Fedora" ;;
  esac
  exit 1
fi

"$CHROME" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.claude/chrome-debug" \
  $TABS &
