# continue-issue

Resume work on an in-progress issue from where it left off.

## What it does

Reads the GitHub issue body, identifies completed steps via checkboxes, recreates the task board matching issue state (completed steps get green ticks, current step shows spinner, pending steps stay empty), and immediately starts working on the next pending step.

## When to use

- Opening a new Claude Code conversation to continue an issue started with `/start-issue`
- After a session timeout or context window reset
- When you want to see progress status and resume working

## Usage

```
/continue-issue         # Auto-detects issue from current branch
/continue-issue 1       # Explicitly specify issue #1
/continue-issue #1      # Also accepts #N format
```

## How it works

1. **Detect issue** — from argument, branch name (`feat/<N>-*`), or "In Progress" board items
2. **Parse progress** — reads issue body, counts checked vs unchecked checkboxes per step
3. **Rebuild task board** — creates tasks matching issue state (completed/in_progress/pending)
4. **Load context** — reads ARCHITECTURE.md, quality.md, recent comments, git log
5. **Resume work** — starts executing the next pending step immediately

## Install

```bash
npx @anthropic-ai/claude-code skills add workflow:continue-issue
```

## Requirements

- GitHub CLI (`gh`) authenticated
- Issue created with `/start-issue` (must have `## Step N — Title` format)
- Git repository with remote origin
