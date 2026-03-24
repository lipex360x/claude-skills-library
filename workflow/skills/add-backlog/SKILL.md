---
name: add-backlog
description: >-
  Create a GitHub issue and add it to the project board's Backlog column. Use
  this skill when the user says "add to backlog", "create backlog issue",
  "backlog add", "new issue for backlog", or wants to register a task for
  later — even if they don't explicitly say "backlog."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - AskUserQuestion
argument-hint: <description>
---

# Add Backlog

Create a GitHub issue with structured acceptance criteria and add it to the project board's **Backlog** column. Ensures every issue is board-tracked, scope-analyzed, and blocker-aware.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `description` | $ARGUMENTS | no | Non-empty string describing the issue | AUQ: "What should the backlog issue be about?" |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| GitHub issue | GitHub API | yes | Markdown body |
| Board card | GitHub Projects | yes | Status field = Backlog |
| Blocked issue updates | GitHub API | yes | Comments + body edits |
| Report | stdout | no | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GitHub issues | `gh issue` CLI | R/W | JSON / Markdown |
| Project board | GitHub Projects API | R/W | GraphQL |
| Available skills | `skills-library/*/skills/*/SKILL.md` | R | Glob |
| Board setup reference | `references/project-board-setup.md` | R | Markdown |
| Board operations reference | `references/project-board-operations.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI (`gh`) required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo with a GitHub remote → if not: "Must run inside a GitHub-linked repo." — stop.

</pre_flight>

## Steps

### 1. Analyze scope

Before creating anything, reason about whether the request contains multiple independent concerns. If it does, propose splitting into separate issues using `AskUserQuestion` with options like `["One issue", "Split into N issues"]` — show the proposed titles for each.

Only split when concerns are genuinely independent (different features, different areas of the codebase). Related tasks within the same feature stay together.

### 2. Structure the issue

Structure each issue body with:
- **What:** one paragraph describing the feature/task
- **Why:** motivation or context (prevents rework when picking up later)
- **Acceptance criteria:** 2-4 concrete, verifiable items as checkboxes

### 3. Detect relevant skills

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

If a matching skill is found, add an `## Implementation note` section to the issue body before the Size line. The note format depends on whether the work will likely be executed by the lead directly or by parallel agents:

```markdown
## Implementation note

Use `/skill-name` to [action] — it enforces [quality checks, review process, standards]. Do not [manual alternative].
```

**Agent-friendly issues.** When the issue involves repetitive, independent work across many targets (e.g., updating 38 READMEs, adding headers to all files), agents will likely execute it. Agents cannot invoke skills — they need the skill's quality criteria distilled into the issue body. In this case, add context that helps `/start-issue` build self-contained agent prompts:
- Reference the skill as a **quality standard**, not an invocation instruction (e.g., "Use `/create-readme` review mode as the quality reference" instead of "Run `/create-readme` on each file")
- Include audit data, golden examples, or format specifications that agents can consume directly
- List which existing outputs are "EXCELLENT" quality and can serve as templates

If no skill matches, skip this section. Do not force a match — only reference skills with clear relevance.

**Quality check:** Before moving on, verify the skill match is genuine. A loose topical overlap is not a match — the skill must directly implement the issue's core work.

### 4. Labels and Size

Use `AskUserQuestion` to ask which labels to apply (fetch available labels with `gh label list`). If no labels exist, skip labels.

Ask for **Size** using `AskUserQuestion` with options `["XS (< 1h)", "S (1-2h)", "M (half day)", "L (full day)", "XL (multi-day)"]`. Size helps with prioritization when picking from the backlog later.

### 5. Detect blocker impact

Before creating the issue, check if it could block existing open issues. This prevents silent dependency gaps that only surface when someone starts working on a blocked issue.

**5a. Fetch open issues from board**

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

**5b. Analyze overlap**

Compare the **new issue's scope** (routes, schema, components, UI areas) against each open issue. An existing issue is potentially blocked when the new issue would change something the existing issue depends on — examples:

- New issue adds a route layer → existing issues referencing the old route structure are blocked
- New issue changes DB schema → existing issues that query affected tables are blocked
- New issue restructures a component hierarchy → existing issues that modify those components are blocked

Only flag **direct, clear dependencies** — not loose topical overlap.

**5c. Present blockers for approval**

If potential blockers are found, present them via `AskUserQuestion` with the blocked issue numbers and reasons. If no blockers found, proceed without modification.

**5d. Store approved blockers** — keep the list for Step 8.

### 6. Review draft

Before creating the issue, review the complete draft:

- **Acceptance criteria are verifiable** — each checkbox describes a concrete, testable outcome
- **Scope is single-concern** — if the issue touches unrelated areas, go back to Step 1 and split
- **Skill match is genuine** — if Step 3 added an implementation note, confirm the skill directly implements the core work
- **Why section has real motivation** — not just restating the What

This refinement step prevents low-quality issues that cause rework when picked up later.

### 7. Create issue

```bash
gh issue create --title "<title>" --body "<body>"
```

### 8. Update blocked issues

For each issue approved as blocked in Step 5c:

1. **Add dependency annotation** — fetch the blocked issue body, prepend `> Depends on #N` (where N is the newly created issue number) below existing dependency lines, and update with `gh issue edit`.

2. **Add a comment** on the blocked issue explaining the new dependency using the canonical `Depends on #N` pattern.

### 9. Add to project board

Check if a project board exists:

```bash
gh project list --owner "@me" --format json | jq '.projects[] | {number, title}'
```

**If no board exists**, prompt the user with `AskUserQuestion` offering `["Yes, create a board", "No, cancel issue creation"]`. If they choose to create one, read `references/project-board-setup.md` and set up the full board (7 status columns, Priority and Size fields). If they choose to cancel, stop — board tracking is required for all workflow skills.

**Once a board exists** (or was just created):

1. Add the issue to the board: `gh project item-add <project-number> --owner "@me" --url <issue-url>`
2. Set status to **"Backlog"**
3. Set **Size** to the value chosen in Step 4

Read `references/project-board-operations.md` for the full command reference.

### 10. Report

Present concisely:
- **What was done** — issue created with URL, size, and board column (Backlog)
- **Blocked issues updated** — list issue numbers updated with dependency annotations, or "none"
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

Run `/start-issue <number>` when ready to begin implementation.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — `gh` authenticated, inside a GitHub-linked repo
2. **Steps completed?** — scope analyzed, issue structured, board updated
3. **Output exists?** — issue URL accessible, board card in Backlog column
4. **Anti-patterns clean?** — no vague acceptance criteria, no untracked issues, no forced skill matches
5. **Approval gates honored?** — user confirmed labels, size, and blocker selections

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Acceptance criteria verifiable?** — each checkbox describes a concrete, testable outcome (not vague goals)
2. **Skill match genuine?** — if referenced, the skill directly implements the core work
3. **Dependency annotations correct?** — `Depends on #N` references use the correct issue number
4. **Board state consistent?** — card exists in Backlog with correct Size field

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Network error | Report error with details → stop (no silent retry) |
| Rate limit | Report the limit and suggest waiting → stop |
| Label creation failure | Proceed without labels and note in report |
| Board not found | AUQ to create board or cancel → stop if cancel |
| Issue creation failure | Report error with full `gh` output → stop |

## Anti-patterns

- **Creating issues without board tracking.** Every issue must be added to the project board — because an issue not on the board is invisible to workflow skills and will be forgotten.
- **Vague acceptance criteria.** "Improve the UI" is not verifiable — because each checkbox must describe a concrete, testable outcome to be useful when picked up later.
- **Skipping scope analysis.** Multi-concern issues cause merge conflicts and unclear ownership — because always checking before creating prevents rework downstream.
- **Forcing skill matches.** Referencing a skill that only loosely relates to the issue — because it misleads whoever picks it up. Only match when the skill directly implements the core work.
- **Re-fetching project items per operation.** Each `item-list` call consumes GraphQL rate limit points — because the 5,000 points/hour limit is shared across all `gh project` commands.

## Guidelines

- **Board tracking is mandatory.** No issue exists without a board card — workflow skills depend on board state for status tracking, prioritization, and reporting.

- **English for all issue content.** Issue titles, bodies, and comments are always in English. Communication with the user follows their language preference.

- **Single-concern issues.** Each issue should represent one coherent unit of work — splitting keeps ownership clear and PRs reviewable.

- **Dependency annotations follow the canonical pattern.** `Depends on #N` / `> **Blocks** #N` — the same format used by merge and listing skills for consistency across the workflow.

- **Batch API calls.** When operating on multiple board items, fetch the item list once and parse locally — never re-fetch per item.

- **Skill references are for `/start-issue`, not for agents.** When referencing a skill in the Implementation note, write it as a quality standard that `/start-issue` can distill into agent prompts — not as an invocation command. Agents cannot call `Skill()`, so "Use `/create-readme`" in the issue body is only useful if the lead executes directly. For agent-friendly issues, include the skill's quality criteria, golden examples, and format specs so `/start-issue` can embed them in self-contained steps.
