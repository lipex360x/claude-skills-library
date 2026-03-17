---
name: add-backlog
description: Create a GitHub issue in the project's Backlog milestone. Use this skill when the user says "add to backlog", "create backlog issue", "backlog add", "new issue for backlog", or wants to register a task for later — even if they don't explicitly say "backlog."
user-invocable: true
allowed-tools: Bash, AskUserQuestion
argument-hint: <description>
---

Create a GitHub issue in the "Backlog" milestone for the current repo.

Parse `$ARGUMENTS` as the issue description. If empty, ask the user what to add.

## 1. Analyze scope

Before creating anything, reason about whether the request contains multiple independent concerns. If it does, propose splitting into separate issues using `AskUserQuestion` with options like `["One issue", "Split into N issues"]` — show the proposed titles for each.

Only split when concerns are genuinely independent (different features, different areas of the codebase). Related tasks within the same feature stay together.

## 2. Structure the issue

Structure each issue body with:
- **What:** one paragraph describing the feature/task
- **Why:** motivation or context (prevents rework when picking up later)
- **Acceptance criteria:** 2-4 concrete, verifiable items as checkboxes

## 3. Labels and Size

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip labels.

Ask for **Size** using `AskUserQuestion` with options `["XS (< 1h)", "S (1-2h)", "M (half day)", "L (full day)", "XL (multi-day)"]`. Size helps with prioritization when picking from the backlog later.

## 4. Create

Create with: `gh issue create --title "<title>" --body "<body>" --milestone "Backlog"`

## 5. Add to project board

Check if a project board exists for the repo:

```bash
gh project list --owner "@me" --format json | jq '.projects[] | {number, title}'
```

**If a board exists:**

1. Add the issue to the board: `gh project item-add <project-number> --owner "@me" --url <issue-url>`
2. Set status to **"Backlog"**
3. Set **Size** to the value chosen in Step 3

Read `references/project-board-operations.md` for the full command reference.

**If no board exists**, skip this step — the issue is still tracked via the Backlog milestone.

## 6. Report

Present:
- Issue URL
- Size assigned
- Board status (added to board, or milestone-only)
