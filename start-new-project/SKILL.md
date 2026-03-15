---
name: start-new-project
description: Plan and scaffold a new project from a prompt. Asks clarifying questions, proposes a phased GitHub issue structure with checkboxes, creates the issue and feature branch. Use when the user says "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", or provides a project idea wanting structured planning — even if they don't explicitly say "new project."
user-invocable: true
---

# Start New Project

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates ensure the user stays in control: once after clarifying questions, once after the proposed structure.

## Steps

### 1. Parse the prompt

Extract from the user's input:
- **Project name / slug** — if not obvious, derive from the description (kebab-case)
- **Tech stack hints** — languages, frameworks, libraries mentioned
- **Scope indicators** — "MVP", "production", "prototype", "just a quick..."
- **Domain** — web app, CLI, library, API, monorepo, mobile, etc.

If no argument was provided (bare `/start-new-project`), ask the user what they want to build before continuing.

### 2. Ask clarifying questions

Generate 3-5 targeted questions to fill gaps. Present as a numbered list. Common gaps:

1. **Platform** — web, CLI, library, API, mobile?
2. **Tech stack** — language, framework, database?
3. **Scope** — MVP or production-ready? What's the first milestone?
4. **Key features** — what are the 3 most important things it should do?
5. **Deployment** — where will it run? Docker, Vercel, npm, local-only?
6. **Existing code** — new repo or adding to an existing codebase?

Skip questions the prompt already answers. Adapt to the project type — a CLI tool needs different questions than a web app.

**Wait for the user's answers before proceeding.** This is the first approval gate.

### 3. Propose the phase structure

Read `templates/issue-template.md` for the expected format. Read `references/phase-planning-guide.md` for decomposition heuristics by project type.

Decompose the project into **Parts** (grouped by theme) and **Steps** (concrete milestones). Each step contains checkboxes with specific, verifiable actions — include file paths when the project structure is known.

Present the full issue body in a fenced code block. The structure should include:
- **Overview** with architecture description
- **Parts** grouped by theme (Part A, B, C...)
- **Numbered Steps** with concrete checkboxes
- **Reference files table** (if working in an existing codebase)
- **Verification section** — how to confirm the project works end-to-end

Sizing guidelines:
- 1-3 issues per project (each issue = independent milestone)
- 2-4 parts per issue
- 3-8 steps per part
- 2-6 checkboxes per step

**Wait for the user's approval before proceeding.** This is the second (and final) approval gate. The user may request changes — iterate until they approve.

### 4. Create the GitHub issue

After approval, create the issue:

```bash
gh issue create --title "<concise title>" --body "<approved body>"
```

Apply labels if the repo uses them (check with `gh label list`). Common: `enhancement`, `feature`, `phase-N`.

### 5. Create the feature branch

```bash
git checkout main
git pull origin main
git checkout -b feature/<slug>
git push -u origin feature/<slug>
```

The slug comes from step 1. If the issue number is known, optionally prefix: `feature/<number>-<slug>`.

### 6. Summary

Present:
- Issue URL (linked)
- Branch name
- Total steps and checkboxes count
- Suggest starting with Step 1

## Guidelines

- **Project-agnostic.** This skill works for any kind of project — web apps, CLIs, libraries, APIs, mobile, data pipelines, infrastructure. The questions and structure adapt to the domain.

- **English for all issue content.** Issues, checkboxes, and branch names are always in English. Communication with the user follows their language preference.

- **Checkboxes are verifiable actions.** Each checkbox should be completable in a single work session. "Implement the API" is too vague. "Create `src/routes/auth.ts` with login/logout endpoints" is concrete.

- **File paths when structure is known.** If the project builds on an existing codebase, include file paths in checkboxes. For greenfield projects, include paths once the structure is defined in early steps.

- **Don't over-plan.** Later phases can be less detailed than early ones. The first part should have precise checkboxes; the last part can be higher-level. The user will refine as they go.

- **One issue per milestone.** If the project has distinct milestones (e.g., "backend API" then "frontend"), create separate issues. Each issue should be independently completable and verifiable.
