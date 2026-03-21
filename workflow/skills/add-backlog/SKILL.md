---
name: add-backlog
description: Create a GitHub issue and add it to the project board's Backlog column. Use this skill when the user says "add to backlog", "create backlog issue", "backlog add", "new issue for backlog", or wants to register a task for later — even if they don't explicitly say "backlog."
user-invocable: true
allowed-tools: Bash, AskUserQuestion
argument-hint: <description>
---

Create a GitHub issue and add it to the project board's **Backlog** column.

Parse `$ARGUMENTS` as the issue description. If empty, ask the user what to add.

## Anti-patterns

Avoid these common failure modes:

- **Creating issues without board tracking** — every issue must be added to the project board. An issue not on the board is invisible to workflow skills and will be forgotten.
- **Vague acceptance criteria** — "improve the UI" is not verifiable. Each checkbox must describe a concrete, testable outcome.
- **Skipping scope analysis** — multi-concern issues cause merge conflicts and unclear ownership. Always check before creating.
- **Forcing skill matches** — referencing a skill that only loosely relates to the issue misleads whoever picks it up. Only match when the skill directly implements the core work.

## Error handling

If `gh` CLI commands fail (auth issues, network errors, rate limits):

1. **Auth failure** — suggest the user run `gh auth login` and retry
2. **Network error** — report the error and stop; do not retry silently
3. **Rate limit** — report the limit and suggest waiting before retrying
4. **Label creation failure** — proceed without labels and note it in the report

Never swallow errors silently — always surface failures to the user with actionable next steps.

## 1. Analyze scope

Before creating anything, reason about whether the request contains multiple independent concerns. If it does, propose splitting into separate issues using `AskUserQuestion` with options like `["One issue", "Split into N issues"]` — show the proposed titles for each.

Only split when concerns are genuinely independent (different features, different areas of the codebase). Related tasks within the same feature stay together.

## 2. Structure the issue

Structure each issue body with:
- **What:** one paragraph describing the feature/task
- **Why:** motivation or context (prevents rework when picking up later)
- **Acceptance criteria:** 2-4 concrete, verifiable items as checkboxes

## 2b. Detect relevant skills

Before finalizing the issue body, scan the issue scope against available skills to determine if execution should use a specific skill — because referencing the right skill in the issue ensures whoever picks it up follows the established quality process instead of implementing ad-hoc. List available skills:

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

**Quality check:** Before moving on, verify the skill match is genuine. A loose topical overlap is not a match — the skill must directly implement the issue's core work.

## 3. Labels and Size

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip labels.

Ask for **Size** using `AskUserQuestion` with options `["XS (< 1h)", "S (1-2h)", "M (half day)", "L (full day)", "XL (multi-day)"]`. Size helps with prioritization when picking from the backlog later.

## 4. Detect blocker impact

Before creating the issue, check if it could block existing open issues. This prevents silent dependency gaps that only surface when someone starts working on a blocked issue.

### 4a. Fetch open issues from board

Query the project board for items in the **Backlog** and **Todo** columns:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[0].number')
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog" or .status == "Todo")
  | {number: .content.number, title: .content.title, status: .status}
]'
```

For full issue bodies (needed for dependency analysis), fetch each issue individually:

```bash
gh issue view <number> --json number,title,body
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

If the user selects "None" or no blockers are found, proceed to Step 6 without modifications.

### 4d. Store approved blockers

Keep the list of approved blocked issue numbers — they will be updated in Step 7 after the new issue is created (because we need the new issue number for the `Depends on #N` reference).

## 5. Review draft

Before creating the issue, review the complete draft:

- **Acceptance criteria are verifiable** — each checkbox describes a concrete, testable outcome (not vague goals like "improve performance")
- **Scope is single-concern** — if the issue touches unrelated areas, go back to Step 1 and split
- **Skill match is genuine** — if Step 2b added an implementation note, confirm the skill directly implements the core work
- **Why section has real motivation** — not just restating the What

This refinement step prevents low-quality issues that cause rework when picked up later.

## 6. Create

Create the issue:

```bash
gh issue create --title "<title>" --body "<body>"
```

## 7. Update blocked issues

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

This follows the canonical `Depends on #N` pattern — the same format used by the PR merge skill for unblocking and by the issue listing skills for detecting blocked items.

## 8. Add to project board (mandatory)

Check if a project board exists for the repo:

```bash
gh project list --owner "@me" --format json | jq '.projects[] | {number, title}'
```

**If no board exists**, prompt the user with `AskUserQuestion` offering `["Yes, create a board", "No, cancel issue creation"]`. If they choose to create one, read `references/project-board-setup.md` and set up the full board (7 status columns, Priority and Size fields). If they choose to cancel, stop — board tracking is required for all workflow skills.

**Once a board exists** (or was just created):

1. Add the issue to the board: `gh project item-add <project-number> --owner "@me" --url <issue-url>`
2. Set status to **"Backlog"**
3. Set **Size** to the value chosen in Step 3

Read `references/project-board-operations.md` for the full command reference.

## 9. Report

Present:
- Issue URL
- Size assigned
- Board column: Backlog
- Blocked issues updated (list issue numbers, or "none")
