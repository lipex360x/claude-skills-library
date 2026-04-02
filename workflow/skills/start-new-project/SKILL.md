---
name: start-new-project
description: >-
  Plan and scaffold a new project from a prompt. Asks clarifying questions,
  proposes a phased GitHub issue structure with checkboxes, creates the issue
  and feature branch. Use when the user says "start a new project", "new project",
  "let's build X", "plan a project", "create an issue for X", "I want to build",
  or provides a project idea wanting structured planning — even if they don't
  explicitly say "new project."
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
  - TeamCreate
---

# Start New Project

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates ensure the user stays in control: once after clarifying questions, once after the proposed structure.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `project-idea` | $ARGUMENTS or conversation | no | Free text describing what to build | AUQ: "What do you want to build?" |
| `grill-output` | `.claude/grill-output.md` | no | Structured `/grill-me` output file | Offer to run `/grill-me` first |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| GitHub issue(s) | GitHub API | yes | Markdown with Phases + Steps + checkboxes |
| Project board | GitHub Projects | yes | 7 columns, Priority + Size fields |
| Feature branch | git | yes | `feature/<slug>` or `feature/<number>-<slug>` |
| Labels | GitHub API | yes | Priority + type labels |
| Topics | GitHub API | yes | Repo topics derived from stack + domain |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Issue template | `templates/issue-template.md` | R | Markdown |
| Phase planning guide | `references/phase-planning-guide.md` | R | Markdown |
| Board setup | `references/project-board-setup.md` | R | Markdown |
| Playwright practices | `references/playwright-practices.md` | R | Markdown |
| TDD methodology | `references/tdd-methodology.md` | R | Markdown |
| Architecture template | `templates/architecture.md` | R | Markdown |
| Quality standards template | `templates/quality-standards.md` | R | Markdown |
| Dev scripts template | `templates/dev-scripts.md` | R | Markdown |
| Issue backup templates | `templates/issue-backup.sh`, `templates/pre-issue-edit-hook.sh` | R | Bash scripts |

</external_state>

## Pre-flight

<pre_flight>

1. `which gh` → if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. `gh auth status` → if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
4. Remote origin exists → if not: "No remote configured. Set up with `gh repo create`." — stop.

</pre_flight>

## Steps

### 1. Check for grill-me output

Check if `.claude/grill-output.md` exists in the current working directory.

**If found:** read it as primary input — skip most clarifying questions since the user already went through a deep interview. Still ask about gaps (e.g., deployment, project name). Inform: "Found grill-me output — using it as the planning base."

**If not found:** use `AskUserQuestion` to suggest running `/grill-me` first:
- **"Run /grill-me first (Recommended)"** — stop and inform: "Run `/grill-me` first, then come back with `/start-new-project`."
- **"Skip, continue with my prompt"** — proceed with Step 2.

### 2. Parse the prompt

Extract from user input or grill-output:
- **Project name / slug** — derive from description if not obvious (kebab-case)
- **Tech stack hints** — languages, frameworks, libraries
- **Scope indicators** — "MVP", "production", "prototype", etc.
- **Domain** — web app, CLI, library, API, monorepo, mobile

If no argument and no grill-output, ask the user what they want to build.

### 3. Ask clarifying questions

If grill-output consumed, only ask about gaps. Otherwise, 3-5 targeted questions:

1. **Platform** — web, CLI, library, API, mobile?
2. **Tech stack** — language, framework, database?
3. **Scope** — MVP or production-ready? First milestone?
4. **Key features** — 3 most important things?
5. **Deployment** — Docker, Vercel, npm, local-only?
6. **Existing code** — new repo or adding to existing codebase?

Skip questions the prompt already answers. **Wait for answers.** This is the first approval gate.

### 4. Propose the phase structure

Read `templates/issue-template.md` for format. Read `references/phase-planning-guide.md` for decomposition heuristics.

Decompose into **Phases** (numbered, grouped by theme) and **Steps** (concrete milestones). Each step has checkboxes with specific, verifiable actions and file paths when known.

**Test isolation detection.** If the tech stack from Step 3 includes a database (postgres, mysql, sqlite, supabase, firebase, mongo, redis with persistence, or any ORM like prisma, drizzle, typeorm, sequelize), the plan MUST include test environment isolation as an early Phase 1 step. Include checkboxes for: (1) `docker-compose.test.yml` with isolated DB on high port, (2) `.env.test` with local container URLs, (3) runtime safety guard in global test setup, (4) test runner config to load `.env.test`, (5) `beforeAll`/`afterAll` for migrate/teardown, (6) configure Husky with `pre-commit` hook running lint + type-check and `pre-push` hook running tests + build. Read `references/guidelines.md` § "Test isolation via docker-compose" for the full requirements. This step must come before any test checkboxes that hit the database.

Present the full issue body in a fenced code block: Overview, Phases, Steps, Reference files table, Verification section.

Sizing: 2-4 phases, 3-8 steps per phase, 2-6 checkboxes per step.

**Mandatory split rule.** If plan has **more than 8 steps**, split into one issue per Phase. Each issue has 3-8 steps, is independently completable, with its own verification. The Overview is shared. Steps renumbered from 1 within each issue.

If Agent Teams is enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), add **Execution mode** section at the top of the issue body with teammate assignments. Rules: identify sequential prefix, group independent steps by layer, mark blocked teammates, 2-4 teammates max. Specify tool access per teammate.

**Quality standards (mandatory).** Every project plan MUST include a Phase 1 checkbox to create `quality.md` at the project root. This file defines non-negotiable code quality rules adapted to the project's specific stack. Read `templates/quality-standards.md` for the structure. The file must include: Shared DON'Ts/DOs (fail-first, vertical TDD, named constants, no workarounds), Backend DON'Ts/DOs (rich entities, value objects, no anemic models — adapted to the project's backend language), Frontend DON'Ts/DOs (if applicable — adapted to the project's frontend framework), and Patterns section with concrete code examples in the project's languages. The `/start-issue` skill reads this file in pre-flight and validates every checkbox against its DON'Ts — so completeness matters.

**Dev startup/teardown scripts (mandatory for multi-service projects).** When the project has backend services, databases, or any infrastructure that needs orchestration, the plan MUST include a Phase 1 step to create `scripts/dev-start.sh` and `scripts/dev-stop.sh`. Read `templates/dev-scripts.md` for the full pattern. The startup script brings up the entire local environment in order (infra → migrations → seed → test user → services → health check). The teardown script kills everything cleanly. Both scripts must be referenced in the `## Scripts` section of ARCHITECTURE.md. These scripts are stack-agnostic — adapt to the project's actual infrastructure (Docker, Supabase CLI, local processes, etc.).

**Issue body backup (mandatory).** Every project plan MUST include a Phase 1 checkbox to scaffold issue body protection. Copy `templates/issue-backup.sh` to `.claude/scripts/`, `templates/pre-issue-edit-hook.sh` to `.claude/hooks/`, register the hook in `.claude/settings.json`, and add `.claude/issues.db` to `.gitignore`. Read `references/guidelines.md` § "Issue body backup" for the full checklist. After creating the issues in Step 6, run `issue-backup.sh snapshot-all` to seed the backup database.

**Infrastructure abstraction (mandatory for projects with external dependencies).** When the project uses databases, external APIs, auth providers, or any service that could be swapped in the future, the plan MUST include a Phase 1 step to establish Repository interfaces (`Protocol`/`interface`) in the domain layer and Port/Adapter pattern for external services. Repository interfaces define data access contracts (`ThreadRepository`, `UserRepository`). Ports define external service contracts (`AuthPort`, `StoragePort`). Concrete implementations live in an `infra/<provider>/` layer (e.g., `infra/supabase/`, `infra/aws/`). Services depend on interfaces, never on implementations — this enables swapping infrastructure (Supabase → AWS, local auth → Cognito) by changing only the adapter with zero changes to domain or service code. Include this in the quality.md Backend DOs and add concrete interface examples in the Patterns section. Read `templates/quality-standards.md` § "Repository pattern" and § "Port/Adapter pattern" for the code templates.

**Linter ignore audit (mandatory).** Every phase's final verification step MUST include: `- [ ] Audit linter ignore rules — review knip.json ignores, eslint-disable, noqa; remove if no longer needed, add justification comment if still required`. Suppression rules added during development tend to accumulate and become permanent workarounds. This checkpoint forces a cleanup pass before each phase is tagged as complete.

Before presenting, review critically: tighten vague checkboxes, remove redundancy, ensure TDD order, verify file paths.

**Wait for approval.** This is the second (and final) approval gate. Iterate until approved.

### 5. Repo scaffolding (labels + milestone + topics)

**Labels** — check with `gh label list`. If priority labels missing, offer to create P0/P1/P2 and type labels. Adapt to existing label schemes.

**Milestone (optional)** — create only when user requests or project has clear versioning:

```bash
gh api repos/{owner}/{repo}/milestones -f title="<name>" -f description="<goal>"
```

**Topics** — derive from the tech stack, domain, and key patterns discussed. Add via:

```bash
gh repo edit --add-topic "topic1,topic2,topic3"
```

Topic sources (combine as applicable):
- **Stack:** languages (typescript, python), frameworks (nextjs, hono, react), ORMs (drizzle, prisma), runtimes (bun, node)
- **Domain:** the project's purpose (flashcards, ecommerce, cli-tool, api)
- **Patterns:** architectural approaches (ddd, tdd, monorepo)
- **Infra:** deployment targets (vercel, aws, docker)

Keep to 10-20 topics. Use lowercase, hyphenated. Match existing GitHub topic conventions (e.g., `tailwindcss` not `tailwind-css`).

### 6. Create the GitHub issues

Create issues sequentially (first may reference later ones by number):

```bash
gh issue create --title "<title>" --body "<approved body>"
```

Apply labels. For multi-issue projects, include phase number in title. Assign to milestones if created.

**Error recovery:** if creation fails mid-flow, report what succeeded and provide `gh issue create` commands for remainder.

### 7. Create project board

Always create a board — even with a single issue. Read `references/project-board-setup.md`.

1. Create project — `gh project create --title "<name>" --owner "@me"`
2. **Configure Status field (mandatory)** — GitHub creates boards with only 3 default columns (Todo, In Progress, Done). Immediately run the `updateProjectV2Field` mutation from `references/project-board-setup.md` § 2 to replace them with the full 7: Backlog, Todo, Ready, In Progress, In review, Done, Cancelled. Do NOT skip this step — workflow skills depend on all 7 columns.
3. Create Priority field — P0, P1, P2
4. Create Size field — XS, S, M, L, XL
5. Add issues to project — `gh project item-add` for each
6. Set initial values — Backlog status, priority and size from plan

**Priority:** P0 for blocking/foundational, P1 for core features, P2 for nice-to-haves.
**Size:** 1-2 steps = S, 3-4 = M, 5-6 = L, 7+ = XL.

**Blocks notation:** add `> **Blocked by** #N` and `> **Blocks** #N` to dependent issues.

**Error recovery:** report what succeeded/failed, provide commands to retry. Board failures don't block branch creation.

### 8. Create the feature branch

```bash
git checkout main && git pull origin main
git checkout -b feature/<slug>
git push -u origin feature/<slug>
```

Optionally prefix with issue number: `feature/<number>-<slug>`.

### 9. Report

Present concisely:
- **What was done** — issues created, board configured, topics added, branch created
- **Issue URL(s)** — linked
- **Project board** — link (7 columns, priority and size configured)
- **Branch name** — ready for development
- **Total steps and checkboxes** — scope summary
- **Priority and size** per issue
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered (or "none")
- **Reminder** — use `closes #N` in PR descriptions
- **Next step** — "Start with Step 1"

## Post-flight

<post_flight>

After presenting the Report, verify external state:

1. **All issues exist on GitHub?** — for each created issue, `gh issue view <N> --json number` must succeed.
2. **Board has 7 Status columns?** — query Status field options and verify all 7 present (Backlog, Todo, Ready, In Progress, In review, Done, Cancelled).
3. **All issues have Priority and Size set?** — query board items and verify no null fields.
4. **Branch exists on remote?** — `git ls-remote origin feature/<slug>` must return a commit hash.
5. **Repo topics are lowercase-hyphenated?** — `gh repo view --json repositoryTopics` — no underscores or camelCase.
6. **If split rule triggered:** verify max 8 steps per issue (count checkboxes in each issue body).

If any check fails, report the specific failure and the fix command.

</post_flight>

## Next action

Run `/start-issue <number>` to begin working on the first issue (Phase 1).

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — gh authenticated, repo valid, remote exists
2. **Steps completed?** — issues created, board configured, branch pushed
3. **Output exists?** — issues on GitHub, board with 7 columns, topics on repo, branch on remote
4. **Anti-patterns clean?** — no generic checkboxes, TDD order enforced, no local paths
5. **Approval gates honored?** — both gates (questions + structure) got user approval

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Checkboxes concrete?** — every checkbox has file paths or specific actions
2. **TDD order correct?** — test before implementation in every behavioral step
3. **Phase structure balanced?** — no phase with 10+ steps, split rule respected
4. **Board fields set?** — every issue has priority and size assigned
5. **Linter ignore audit present?** — each phase's final verification step includes a checkbox to audit linter suppression rules (knip ignores, eslint-disable, noqa). If missing, add it before presenting the plan.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" → stop |
| Issue creation fails mid-flow | Report successes, provide `gh` commands for remainder |
| Board setup fails | Report what succeeded, provide retry commands. Don't block branch creation |
| Label creation fails | Warn, continue without labels |
| Milestone creation fails | Warn, continue without milestone |

## Anti-patterns

Read `references/anti-patterns.md` for the full list (9 items). Key traps:

- **Monolithic issues with 10+ steps.** When the mandatory split rule should have triggered — because progress gets buried and milestone tracking becomes useless.
- **Front-loading detail on later phases.** Phase 1 precise, later phases high-level — because over-specifying Phase 3 wastes effort on assumptions that will change.
- **Generic checkboxes without file paths.** "Add tests" instead of specifying file and behavior — because vague checkboxes produce vague implementations.

## Guidelines

Read `references/guidelines.md` for the full list (19 items). Key principles:

- **TDD is mandatory, not optional.** Every step with new behavior MUST include test checkbox before implementation — because the TDD-ordered checkboxes ARE the enforcement mechanism.
- **Project-agnostic.** Works for any project type — web apps, CLIs, libraries, APIs, mobile, data pipelines. Questions and structure adapt to the domain.
- **Don't over-plan.** Later phases less detailed than early ones — because over-specifying when work hasn't started wastes effort on assumptions that will change.
