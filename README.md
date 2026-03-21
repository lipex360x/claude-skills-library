# Claude Skills Library

> Production-ready skills for Claude Code — organized as plugins.

## Contents

- [Installation](#installation)
- [Plugins](#plugins)
  - [workflow](#workflow) — GitHub workflow automation
  - [content](#content) — Content creation and publishing
  - [design](#design) — Visual design and diagrams
  - [database](#database) — Database optimization
  - [deploy](#deploy) — Deployment and infrastructure
  - [gws](#gws) — Google Workspace automation
  - [meta](#meta) — Skill and hook management
  - [tasks](#tasks) — Task visibility board
- [Adding new skills](#adding-new-skills)

## Installation

Install all skills:

```bash
npx skills add lipex360x/claude-skills-library --all
```

Install a specific skill:

```bash
npx skills add lipex360x/claude-skills-library --skill {skill-name}
```

Common flags: `--copy` (no symlinks), `-a claude-code` (Claude Code only), `-y` (skip prompts).

## Plugins

Skills are organized into **8 plugin groups** by domain. Invoke any skill directly by name (e.g., `/push`, `/create-skill`). There are **37 skills** in total.

---

### workflow

> GitHub workflow automation: issues, branches, PRs, commits.

| Skill | Description |
|-------|-------------|
| [add-backlog](./workflow/skills/add-backlog/) | Create a GitHub issue and add it to the project board's Backlog column. |
| [cancel-issue](./workflow/skills/cancel-issue/) | Cancel an issue — close with reason, move to Cancelled, unblock dependents, clean up branches/PRs. |
| [close-pr](./workflow/skills/close-pr/) | Merge the current branch's PR, write implementation summary, notify unblocked issues, and move card to Done. |
| [grill-me](./workflow/skills/grill-me/) | Deep structured interview about a plan, feature, or project — extracts decisions, constraints, and context. |
| [list-backlog](./workflow/skills/list-backlog/) | List backlog issues with size, priority, and dependency status in a table. |
| [list-issues](./workflow/skills/list-issues/) | List all open issues grouped by board column with priority sorting and next-issue suggestion. |
| [open-pr](./workflow/skills/open-pr/) | Create a pull request from the current branch, linking it to the open issue. |
| [push](./workflow/skills/push/) | Commit, push, and update GitHub issue checkboxes in one command. |
| [start-issue](./workflow/skills/start-issue/) | Pull an issue and start implementation with an expanded step-by-step plan. |
| [start-new-project](./workflow/skills/start-new-project/) | Plan and scaffold a new project from a prompt with structured GitHub issues. |
| [tdd](./workflow/skills/tdd/) | Execute Test-Driven Development with strict red-green-refactor discipline. |

[Back to top](#claude-skills-library)

---

### content

> Content creation, voice profiling, and publishing.

| Skill | Description |
|-------|-------------|
| [approve-post](./content/skills/approve-post/) | Approve the current draft, generate English translation, and publish to local files and Google Drive. |
| [capture-voice](./content/skills/capture-voice/) | Analyze conversations to capture the user's writing voice for authentic content generation. |
| [inspire-me](./content/skills/inspire-me/) | Guided exploration session to unblock thinking on any topic — career, creativity, business, health. |
| [write-content](./content/skills/write-content/) | Create compelling written content and marketing copy that sounds authentically like the user. |

[Back to top](#claude-skills-library)

---

### design

> Visual design: diagrams, design systems, and artboards.

| Skill | Description |
|-------|-------------|
| [create-diagram](./design/skills/create-diagram/) | Create professional diagrams using a spec-driven workflow with HTML preview and Excalidraw export. |
| [create-excalidraw](./design/skills/create-excalidraw/) | Generate Excalidraw diagrams from natural language with design-first aesthetics and icon library support. |
| [create-webview](./design/skills/create-webview/) | Create data-driven HTML presentations from structured sources (Excel, PPTX, CSV → SQLite → JSON → HTML slides → PDF). |
| [extract-design-system](./design/skills/extract-design-system/) | Analyze a design image and create a full design system project with separated artboards. |

[Back to top](#claude-skills-library)

---

### database

> Database optimization and best practices.

| Skill | Description |
|-------|-------------|
| [review-postgres](./database/skills/review-postgres/) | Postgres performance optimization and best practices from Supabase. |

[Back to top](#claude-skills-library)

---

### deploy

> Deployment and infrastructure management.

| Skill | Description |
|-------|-------------|
| [deploy-vercel](./deploy/skills/deploy-vercel/) | Deploy, manage, and develop projects on Vercel from the command line. |

[Back to top](#claude-skills-library)

---

### gws

> Google Workspace automation: Gmail filters, inbox management.

| Skill | Description |
|-------|-------------|
| [check-gmail](./gws/skills/check-gmail/) | Scan Gmail inbox, detect filter gaps, and update filters with structured user decisions. |

[Back to top](#claude-skills-library)

---

### meta

> Claude Code skill, hook, and command management and analysis.

| Skill | Description |
|-------|-------------|
| [audit-skill](./meta/skills/audit-skill/) | Evaluate existing skills against the quality review checklist and produce structured audit reports. |
| [capture-analysis](./meta/skills/capture-analysis/) | Capture skill gaps, workflow frictions, and pattern improvements as structured entries. |
| [create-continuation](./meta/skills/create-continuation/) | Generate a continuation prompt for seamless session handoffs to a new conversation. |
| [create-hook](./meta/skills/create-hook/) | Guide for creating or improving Claude Code hooks. |
| [create-readme](./meta/skills/create-readme/) | Create or review a README.md for the project. |
| [create-skill](./meta/skills/create-skill/) | Guide for creating, reviewing, and improving Claude Code skills. |
| [find-skills](./meta/skills/find-skills/) | Discover and install agent skills from the open ecosystem. |
| [improve-codebase-architecture](./meta/skills/improve-codebase-architecture/) | Explore a codebase for architectural friction and propose deep-module refactors as GitHub issue RFCs. |
| [install-skill](./meta/skills/install-skill/) | Install a skill from an npx skills link with local or global selection. |
| [plan-skill](./meta/skills/plan-skill/) | Plan and spec out a skill from raw input — produces a structured spec consumed by `/create-skill`. |
| [sync-claude](./meta/skills/sync-claude/) | Synchronize the Claude Code environment (skills-library + .brain) across machines — pull, rebuild symlinks, verify. |
| [uninstall-skill](./meta/skills/uninstall-skill/) | Uninstall a skill by name, local or global. |

[Back to top](#claude-skills-library)

---

### tasks

> Task visibility board management.

| Skill | Description |
|-------|-------------|
| [clean-tasks](./tasks/skills/clean-tasks/) | Remove completed tasks from the task visibility board. |
| [close-tasks](./tasks/skills/close-tasks/) | Close the task visibility board and stop task tracking for the session. |
| [open-tasks](./tasks/skills/open-tasks/) | Reopen the task visibility board and resume task tracking. |

[Back to top](#claude-skills-library)

## Adding new skills

Use `/create-skill` to scaffold a new skill with the standard template. It walks you through intent, triggers, structure, and generates the `SKILL.md` with correct frontmatter.

> [!TIP]
> Each skill directory contains a `SKILL.md` with full instructions, trigger phrases, and workflow details. Click any skill link above to explore.
