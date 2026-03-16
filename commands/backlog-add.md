---
description: Create a backlog issue in the project's Backlog milestone.
argument-hint: <description>
allowed-tools: Bash, AskUserQuestion
---

Create a GitHub issue in the "Backlog" milestone for the current repo.

Parse `$ARGUMENTS` as the issue description. If empty, ask the user what to add.

**Analyze scope first.** Before creating anything, reason about whether the request contains multiple independent concerns. If it does, propose splitting into separate issues using `AskUserQuestion` with options like `["Uma issue só", "Dividir em N issues"]` — show the proposed titles for each. Only split when concerns are genuinely independent (different features, different areas of the codebase). Related tasks within the same feature stay together.

Structure each issue body with:
- **What:** one paragraph describing the feature/task
- **Why:** motivation or context (prevents rework when picking up later)
- **Acceptance criteria:** 2-4 concrete, verifiable items as checkboxes

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip.

Create with: `gh issue create --title "<title>" --body "<body>" --milestone "Backlog"`

If the "Backlog" milestone doesn't exist, create it first:
`gh api repos/{owner}/{repo}/milestones --method POST -f title="Backlog" -f description="Itens adiados para implementação futura"`

Report: issue URL(s) and milestone.

All issue content in English. Communication with user follows their language.
