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

Skills are organized into **7 plugin groups** by domain. Invoke any skill directly by name (e.g., `/push`, `/create-skill`). There are **29 skills** in total.

---

### workflow

> GitHub workflow automation: issues, branches, PRs, commits.

| Skill | Description |
|-------|-------------|
| [add-backlog](./workflow/skills/add-backlog/) | Create a GitHub issue in the project's Backlog milestone. |
| [create-pr](./workflow/skills/create-pr/) | Create a pull request from the current branch, linking it to the open issue. |
| [list-backlog](./workflow/skills/list-backlog/) | List open backlog issues with numbered summary for selection. |
| [list-issues](./workflow/skills/list-issues/) | List all open issues grouped by milestone with priority sorting and next-issue suggestion. |
| [merge-pr](./workflow/skills/merge-pr/) | Merge the open pull request for the current branch and switch back to main. |
| [push](./workflow/skills/push/) | Commit, push, and update GitHub issue checkboxes in one command. |
| [start-backlog](./workflow/skills/start-backlog/) | Pull a backlog issue and start implementation with an expanded step-by-step plan. |
| [start-new-project](./workflow/skills/start-new-project/) | Plan and scaffold a new project from a prompt with structured GitHub issues. |

[Back to top](#claude-skills-library)

---

### content

> Content creation, voice profiling, and publishing.

| Skill | Description |
|-------|-------------|
| [approve-post](./content/skills/approve-post/) | Approve the current draft, generate English translation, and publish to local files and Google Drive. |
| [capture-voice](./content/skills/capture-voice/) | Analyze conversations to capture the user's writing voice for authentic content generation. |
| [write-content](./content/skills/write-content/) | Create compelling written content and marketing copy that sounds like the user wrote it. |

[Back to top](#claude-skills-library)

---

### design

> Visual design: diagrams, design systems, and artboards.

| Skill | Description |
|-------|-------------|
| [create-diagram](./design/skills/create-diagram/) | AI-powered Draw.io diagram creation, editing, and replication with a YAML design system supporting 6 themes. |
| [extract-design-system](./design/skills/extract-design-system/) | Analyze a design image and create a full design system project with separated artboards. |

[Back to top](#claude-skills-library)

---

### database

> Database optimization and best practices.

| Skill | Description |
|-------|-------------|
| [optimize-postgresql](./database/skills/optimize-postgresql/) | PostgreSQL-specific development assistant focusing on advanced data types, JSONB, full-text search, and extensions. |
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

### meta

> Claude Code skill, hook, and command management and analysis.

| Skill | Description |
|-------|-------------|
| [capture-analysis](./meta/skills/capture-analysis/) | Capture skill gaps, workflow frictions, and pattern improvements as structured entries. |
| [create-command](./meta/skills/create-command/) | Guide for creating or improving Claude Code slash commands. |
| [create-continuation](./meta/skills/create-continuation/) | Generate a continuation prompt for seamless session handoffs to a new conversation. |
| [create-hook](./meta/skills/create-hook/) | Guide for creating or improving Claude Code hooks. |
| [create-readme](./meta/skills/create-readme/) | Create or review a README.md for the project. |
| [create-skill](./meta/skills/create-skill/) | Guide for creating, reviewing, and improving Claude Code skills. |
| [find-skills](./meta/skills/find-skills/) | Discover and install agent skills from the open ecosystem. |
| [generate-readme-blueprint](./meta/skills/generate-readme-blueprint/) | Generate README.md by analyzing project documentation structure. |
| [install-skill](./meta/skills/install-skill/) | Install a skill from an npx skills link, with local or global selection. |
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
