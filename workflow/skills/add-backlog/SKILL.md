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

Before creating anything, reason about whether the request contains multiple independent concerns. If it does, propose splitting into separate issues using `AskUserQuestion` with options like `["Uma issue só", "Dividir em N issues"]` — show the proposed titles for each.

Only split when concerns are genuinely independent (different features, different areas of the codebase). Related tasks within the same feature stay together.

## 2. Structure the issue

Structure each issue body with:
- **What:** one paragraph describing the feature/task
- **Why:** motivation or context (prevents rework when picking up later)
- **Acceptance criteria:** 2-4 concrete, verifiable items as checkboxes

## 3. Labels

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip.

## 4. Create

Create with: `gh issue create --title "<title>" --body "<body>" --milestone "Backlog"`
