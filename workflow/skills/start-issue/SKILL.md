---
name: start-issue
description: >-
  Pull an issue and start implementation — reads the issue, expands acceptance
  criteria into a detailed step-by-step plan with checkboxes, rewrites the issue,
  creates branch and tasks. Use this skill when the user says "start issue",
  "work on issue #N", "pull from backlog", "start #N", or wants to begin
  implementing an issue — even if they don't explicitly say "issue."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TeamCreate
  - WebSearch
  - WebFetch
---

# Start Issue

Turn an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then set up the branch and tasks. One approval gate: the proposed plan. Everything else is automated.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `issue-number` | $ARGUMENTS | no | Positive integer (accepts `#N` or `N`) | AUQ with Backlog/Todo issues from project board |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Rewritten issue body | GitHub API | yes | Markdown with Steps + checkboxes |
| Feature branch | git | yes | `feat/<number>-<slug>` |
| Board card update | GitHub Projects | yes | Status → In Progress |
| Task list | TaskCreate | no | One task per Step |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GitHub issue | `gh issue view` | R/W | Markdown body |
| Project board | GitHub Projects API | R/W | GraphQL |
| ARCHITECTURE.md | project root | R/W | Markdown |
| Step template | `templates/step-template.md` | R | Markdown |
| Board operations | `references/project-board-operations.md` | R | Markdown |
| Board setup | `references/project-board-setup.md` | R | Markdown |
| CDP practices | `references/cdp-best-practices.md` | R | Markdown |
| Dev guidelines | `references/development-guidelines.md` | R | Markdown |
| TDD methodology | `references/tdd-methodology.md` | R | Markdown |
| Execution strategy | `references/execution-strategy.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. Working tree is clean → if dirty: warn user about uncommitted changes, suggest stashing.

</pre_flight>

## Steps

### 1. Select issue

Parse `$ARGUMENTS` for an issue number. Accept both direct numbers (`2`) and index references (`#2`).

If no argument provided, query the project board for issues in the **Backlog** and **Todo** columns:

```bash
PROJECT_NUMBER=$(gh project list --owner "@me" --format json | jq -r '.projects[0].number')
gh project item-list "$PROJECT_NUMBER" --owner "@me" --format json | jq '[
  .items[]
  | select(.status == "Backlog" or .status == "Todo")
  | {number: .content.number, title: .content.title, status: .status}
  | "#\(.number) — \(.title) [\(.status)]"
]'
```

Present the list with `AskUserQuestion` for the user to pick one.

If no board exists, prompt the user with `AskUserQuestion` offering `["Yes, create a board", "No, cancel"]`. If they choose to create one, read `references/project-board-setup.md` and set up the full board (7 status columns, Priority and Size fields). If they cancel, stop — board tracking is required for all workflow skills.

If the board has no items in Backlog or Todo, inform the user and stop.

### 2. Analyze the issue

Fetch the issue body:

```bash
gh issue view <number> --json body,title,labels -q '{title: .title, labels: [.labels[].name], body: .body}'
```

Extract: **Title** (branch slug), **What/Why** (context), **Acceptance criteria** (checkboxes to expand).

**Read issue comments for context.** Fetch comments before analyzing the codebase:

```bash
gh issue view <number> --json comments --jq '.comments[] | {author: .author.login, body: .body}'
```

Scan comments for: file paths, scope transfers from `/open-pr` or `/close-pr`, partial completion notes, blocker resolutions, implementation hints. Store as **comment insights** to narrow exploration scope.

**Analyze the current codebase.** Start by checking for `ARCHITECTURE.md` at the project root. If it exists, read it first — it contains stack, layers, patterns, schema, auth model, and routes (~2k tokens vs ~53k for full exploration). Only spawn an exploration agent if ARCHITECTURE.md is missing, incomplete, or stale.

Apply comment insights to narrow exploration — if comments point to specific files, target those instead of a full scan. If comments plus ARCHITECTURE.md provide sufficient context, skip exploration entirely.

**If ARCHITECTURE.md doesn't exist, create it.** Explore the codebase and generate it at the project root. This file is the living context document — `/close-pr` updates it after each merge.

If ARCHITECTURE.md exists but is stale, update it with what you discover during exploration.

**CDP detection (for web projects).** Check:
1. **CDP already configured?** Look for `.claude/project-settings.json` with `chrome.cdp` field. Store the `pages` map for verification checkboxes.
2. **Web project with frontend?** Check for frontend framework signals (react, vue, svelte, next, etc.). Store the result for Step 3.

### 2b. Determine execution strategy

Run `echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to check if Agent Teams is enabled (value `1`). If not enabled, strategy is always **Sequential** — skip the rest of this step.

If enabled, read `references/execution-strategy.md` for the full decision matrix. After building the plan in Step 3 (but before presenting), classify each step as sequential or parallelizable, then evaluate:

1. **Are parallelizable steps present?** → if no: **Sequential**
2. **Is the work templated?** (same pattern repeated on independent targets, no shared state, no feedback needed) → if yes: **Agent**
3. **Do parallel steps share state or need coordination?** (same files, exchanging data, iterative feedback) → if yes: **Teammate**
4. **Default** for parallelizable steps without clear signals → **Agent** (simpler, cheaper)

Store the chosen strategy — it determines the "Execution strategy" section in Step 3 and the spawn behavior in Step 7.

### 2c. Enforce development standards

Before proposing any plan, verify non-negotiable standards. If any are missing, the plan must compensate:

1. **TDD is mandatory.** Scan for TDD references. If absent, enforce test-first checkboxes in every behavioral Step. Read `references/tdd-methodology.md`.
2. **No workarounds.** The plan must solve problems at root. Hardcoded values, temporary flags, monkey-patches signal the Step is incomplete.
3. **No unnecessary code comments.** Only allowed for genuinely non-obvious logic. Never include "add comments" checkboxes.

### 3. Propose the detailed plan

Read `templates/step-template.md` for the expected format.

Transform acceptance criteria into Steps with checkboxes. Each criterion typically expands into 1-3 Steps with 2-6 concrete checkboxes.

**Apply CDP detection result from Step 2:**
- **CDP already configured**: use `pages` map for verification checkboxes. If new routes, include checkbox to update `pages`.
- **Web project without CDP**: include Step 1 — Configure CDP. Read `references/cdp-best-practices.md`.
- **Not a web project**: skip CDP entirely.

Present the full proposed issue body in a fenced code block with: **What**, **Why**, **Acceptance criteria** (original), **Steps** (new detailed breakdown).

Sizing: 2-8 Steps total, 2-6 checkboxes per Step. Each checkbox = one focused action.

**Mandatory split rule.** If plan has **more than 8 steps**, split into multiple smaller issues — all added to Backlog. Each issue independently completable with 3-8 steps.

If Agent Teams is enabled, add an **Execution strategy** section at the top of the issue body (before What/Why) based on the strategy chosen in Step 2b. Read `references/execution-strategy.md` for the strategy templates (Agent, Teammate, Sequential). Also add inline reminders in parallelizable steps. Read `references/guidelines.md` § "Verification is part of the plan" and § "Checkbox ownership with Agent Teams" for the verification matrix and ownership rules.

**Include a task preview** after the fenced code block listing Step titles as bullet points.

Present the plan and use `AskUserQuestion` with options `["Approved", "I want to adjust"]`. This is the **single and only** approval gate.

- **"Approved"** — proceed immediately to Step 4. No additional confirmation.
- **"I want to adjust"** — apply changes, re-present, repeat until approved.

### 4. Update the issue

After approval, rewrite the issue body and assign:

```bash
gh issue edit <number> --body "<approved body>" --add-assignee @me
```

If split rule triggered, create additional issues and add to Backlog. Add cross-references and preserve labels.

### 5. Create branch linked to issue

```bash
git checkout main && git pull
gh issue develop <number> --name feat/<number>-<slug> --checkout
git push -u origin feat/<number>-<slug>
```

Derive `<slug>` from issue title (kebab-case, max 40 chars).

### 5b. Board transitions and blocker check

Read `references/project-board-operations.md` for the full command reference.

Find the project board. If no board exists, offer to create one via `references/project-board-setup.md`.

**Check for blockers.** Scan issue body for `> Blocked by #N`. If blocking issue is still open, flag with AUQ.

**Move card to "Ready"** → then after plan approval, **move to "In Progress"**.

Check if Priority and Size are set. If missing, infer from plan (P0/P1/P2 and S/M/L/XL based on step count). Set with `gh project item-edit`.

### 6. Create tasks

Parse Steps from the approved plan. Create a `TaskCreate` for each Step (not each checkbox). Set up `addBlockedBy` dependencies between sequential tasks.

### 7. Spawn workers (automatic when Execution strategy is present)

If the approved issue body contains an "Execution strategy" section, spawn workers immediately — no second approval. The strategy determines the spawn mechanism:

**Agent strategy:**
- Use `Agent` tool with `run_in_background: true` for each batch
- Each agent receives full instructions in its prompt (golden example + target list)
- No `TeamCreate`, no internal tasks — agents return results and die
- Lead collects results via completion notifications, validates, marks issue checkboxes
- GitHub issue checkboxes are the **sole tracker** — no local task board duplication

**Teammate strategy:**
- Use `TeamCreate` + `Agent` with `team_name` for coordinated workers
- Each teammate receives the standardized prompt pattern pointing to the issue
- Teammates must have explicit tool access: `Bash`, `Read`, `Write`, `Edit`, `Grep`, `Glob`, `Agent`, `TaskCreate`, `TaskUpdate` at minimum
- **Checkbox ownership:** teammates track progress via internal tasks. Lead monitors via `TaskList`, verifies output, then marks issue checkboxes. This prevents race conditions
- **Shutdown protocol** required when teammates complete their batch

**Sequential strategy:** Skip this step — lead executes directly.

**Progressive audit (both strategies).** Do NOT wait for all workers to finish before auditing. As each worker reports completion, immediately spawn a background audit agent to verify that worker's output against the verification matrix. This overlaps audit work with remaining agent execution, significantly reducing total wall-clock time. The consolidation step (final Step) collects all audit results — by then, most or all audits are already done.

Example timeline with 4 agents:
1. Agent 3 finishes → spawn audit-agent-3 in background
2. Agent 1 finishes → spawn audit-agent-1 in background (audit-3 still running)
3. Audit-agent-3 completes → results stored
4. Agent 2 finishes → spawn audit-agent-2 in background
5. Audit-agent-1 completes → results stored
6. Agent 4 finishes → spawn audit-agent-4 in background
7. ... consolidation step: most audits already done, minimal wait

### 8. Report

Present concisely:
- **What was done** — issue analyzed, plan approved, branch created, tasks set up
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered (or "none")
- **Next step** — "Start working on Step 1" or teammate status if Agent Teams active

## Next action

Begin working on Step 1 of the approved plan. If Agent Teams is active, teammates are already executing.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, repo valid, working tree clean
2. **Steps completed?** — issue rewritten, branch created, board updated, tasks created
3. **Output exists?** — issue body updated on GitHub, branch pushed, card in "In Progress"
4. **Anti-patterns clean?** — no generic checkboxes, TDD order enforced, no local paths in issue
5. **Approval gate honored?** — user explicitly approved the plan before execution

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Checkboxes concrete?** — every checkbox has file paths or specific actions, no vague "implement X"
2. **TDD order correct?** — test checkbox before implementation in every behavioral Step
3. **Plan structure matches template?** — What/Why/Acceptance criteria/Steps format
4. **Split rule respected?** — if 8+ steps, plan was split into multiple issues

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue not found | Report number and suggest `gh issue list` → stop |
| No board exists | Offer to create one via AUQ → proceed or stop |
| Board has no Backlog/Todo items | Inform user → stop |
| Branch already exists | Offer to checkout existing or create new → AUQ |
| Agent Teams check fails | Default to sequential execution (no Execution strategy section) |

## Anti-patterns

Read `references/anti-patterns.md` for the full list (13 items). Key traps:

- **Generic checkboxes without file paths.** "Add tests" instead of specifying the test file and expected behavior — because vague checkboxes produce vague implementations.
- **Skipping Agent Teams check.** Proposing a plan without checking the env var first — because if enabled, the Execution mode section is mandatory.
- **Multiple agents editing the same issue body.** Last write wins, earlier edits silently lost — because GitHub's issue API has no merge.

## Guidelines

Read `references/guidelines.md` for the full list (20 items). Key principles:

- **TDD is mandatory, not optional.** Every Step with new behavior MUST include test checkbox before implementation — because the TDD-ordered checkboxes ARE the enforcement mechanism.
- **Codebase-aware plans.** Always read the codebase before planning — because generic checkboxes like "implement the feature" are a failure mode.
- **Steps are work sessions.** Each Step = focused work session you can complete, commit, and verify — because too large loses focus, too small adds overhead.
