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

## 2b. Detect relevant skills

Before finalizing the issue body, scan the issue scope against available skills to determine if execution should use a specific skill. List available skills:

```bash
ls skills-library/*/skills/*/SKILL.md 2>/dev/null || Glob: */skills/*/SKILL.md
```

Match the issue scope against skill purposes:

| Issue scope | Skill to reference |
|-------------|-------------------|
| Creating a new skill | `/create-skill` |
| Auditing skill quality | `/audit-skill` |
| Creating a diagram | `/create-diagram` |
| Creating a presentation | `/create-webview` |
| Scaffolding a new project | `/start-new-project` |
| Writing content (posts, copy) | `/write-content` |
| Designing a system from an image | `/extract-design-system` |
| Database optimization | `/review-postgres` |
| Deploying to Vercel | `/deploy-vercel` |
| Any other work that maps to a `/command` | Reference it |

If a matching skill is found, add an `## Implementation note` section to the issue body before the Size line:

```markdown
## Implementation note

Use `/skill-name` to [action] — it enforces [quality checks, review process, standards]. Do not [manual alternative].
```

If no skill matches, skip this section. Do not force a match — only reference skills with clear relevance.

## 3. Labels and Size

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip labels.

Ask for **Size** using `AskUserQuestion` with options `["XS (< 1h)", "S (1-2h)", "M (half day)", "L (full day)", "XL (multi-day)"]`. Size helps with prioritization when picking from the backlog later.

## 4. Detect blocker impact

Before creating the issue, check if it could block existing open issues. This prevents silent dependency gaps that only surface when someone starts working on a blocked issue.

### 4a. Fetch open issues

```bash
gh issue list --milestone "Backlog" --state open --json number,title,body --limit 100
```

### 4b. Analyze overlap

Compare the **new issue's scope** (routes, schema, components, UI areas) against each open issue. An existing issue is potentially blocked when the new issue would change something the existing issue depends on — examples:

- New issue adds a route layer (`/[course]/[subject]`) → existing issues referencing the old route structure are blocked
- New issue changes DB schema (new table, FK changes) → existing issues that query affected tables are blocked
- New issue restructures a component hierarchy → existing issues that modify those components are blocked

Only flag **direct, clear dependencies** — not loose topical overlap. "Both touch CSS" is not a blocker; "new issue changes the route structure that the other issue's breadcrumbs depend on" is.

### 4c. Present blockers for approval

If potential blockers are found, present them to the user via `AskUserQuestion` with `multiSelect: true`:

```
question: "This issue may block the following existing issues. Select which ones to mark as blocked:"
options:
  - label: "#27 — Add breadcrumb back-navigation"
    description: "Route structure changes affect breadcrumb paths"
  - label: "#28 — Favorite lessons with localStorage"
    description: "Route changes affect lesson URL keys in localStorage"
  - label: "None — no blockers"
    description: "Skip blocker detection"
```

If the user selects "None" or no blockers are found, proceed to Step 5 without modifications.

### 4d. Store approved blockers

Keep the list of approved blocked issue numbers — they will be updated in Step 6 after the new issue is created (because we need the new issue number for the `Depends on #N` reference).

## 5. Create

Create with: `gh issue create --title "<title>" --body "<body>" --milestone "Backlog"`

## 6. Update blocked issues

For each issue approved as blocked in Step 4c:

1. **Add dependency annotation** to the blocked issue's body. Fetch the current body, prepend `> Depends on #N` (where N is the newly created issue number) below any existing dependency lines, and update:

   ```bash
   gh issue view <blocked-number> --json body -q '.body'
   gh issue edit <blocked-number> --body "<updated body with dependency>"
   ```

2. **Add a comment** on the blocked issue explaining the new dependency:

   ```markdown
   ## New dependency

   #<new-number> (<new title>) was created and introduces changes that this issue depends on. Marking as blocked until #<new-number> is resolved.
   ```

This follows the same dependency format used by `/close-pr` (Step 8) for unblocking — `Depends on #N` is the canonical pattern detected by `/list-backlog`, `/list-issues`, and `/close-pr`.

## 7. Add to project board

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

## 8. Report

Present:
- Issue URL
- Size assigned
- Board status (added to board, or milestone-only)
- Blocked issues updated (list issue numbers, or "none")
