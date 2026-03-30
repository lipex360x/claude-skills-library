# Claude Skills Library

> Production-ready skills for Claude Code — organized as plugins.

A collection of **39 skills** across **8 plugins**, each following a canonical 13-section skeleton that ensures consistency, quality, and self-auditing. Every skill is a `/command` — invoke it by name and it handles the rest.

[Installation](#installation) • [Skill anatomy](#skill-anatomy) • [Plugins](#plugins) • [Adding new skills](#adding-new-skills)

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

> [!NOTE]
> Requires [Claude Code](https://claude.ai/code) installed.

## Skill anatomy

Every skill follows a **13-section canonical skeleton** in its `SKILL.md`. Sections marked **never skip** must always contain real content — the rest use `> _Skipped: "reason"_` when not applicable.

| # | Section | XML tag | Skippable | Purpose |
|---|---------|---------|-----------|---------|
| 1 | Frontmatter | — | no | Name, description, tools, triggers |
| 2 | Title + Intro | — | no | One-line summary of what and why |
| 3 | Input contract | `<input_contract>` | yes | Expected inputs, validation, fallbacks |
| 4 | Output contract | `<output_contract>` | yes | Artifacts created, paths, format |
| 5 | External state | `<external_state>` | yes | Resources read/written outside skill dir |
| 6 | Pre-flight | `<pre_flight>` | **never** | Environment checks before work begins |
| 7 | Steps | — | no | Numbered workflow (`### 1.`, `### 2.`, ..., `### N. Report`) |
| 8 | Next action | — | yes | What to do after skill completes |
| 9 | Self-audit | `<self_audit>` | **never** | Verification checklist before Report |
| 10 | Content audit | `<content_audit>` | yes | Output quality checks |
| 11 | Error handling | — | yes | Failure modes + recovery strategies |
| 12 | Anti-patterns | — | **never** | Named failure modes with reasoning |
| 13 | Guidelines | — | **never** | Principles with "because" context |

### Frontmatter

```yaml
---
name: skill-name                    # Lowercase, verb-subject (e.g., push, create-skill)
description: >-                     # Pushy description — triggers + "even if" clause
  Action summary. Use when... even if they don't explicitly say "X."
user-invocable: true                # true for /commands, false for auto-triggered
allowed-tools:                      # Only tools the skill actually uses
  - Read
  - Bash
  - AskUserQuestion
argument-hint: "[optional-arg]"     # Optional — shows in autocomplete
---
```

### Skill directory

```text
<skill-name>/
├── SKILL.md              # Required — 13-section skeleton (<500 lines)
├── README.md             # Required — public docs (usage, triggers, install)
├── skill-meta.json       # Required — metadata for auditing and registry
├── references/           # Optional — detailed guides loaded on demand
├── templates/            # Optional — output formats, starter structures
└── scripts/              # Optional — executable code (rare)
```

Sections longer than ~15 lines are extracted to `references/` with a `Read references/...` pointer in the SKILL.md — keeping the main file under 500 lines.

### Plugin directory

```text
<plugin>/
├── .claude-plugin/
│   └── plugin.json       # Plugin manifest (name, description, version)
└── skills/
    └── <skill-name>/     # Each skill follows the anatomy above
```

[Back to top](#claude-skills-library)

## Plugins

Skills are organized into **8 plugin groups** by domain. Each plugin is a directory containing related skills. Invoke any skill directly by name (e.g., `/push`, `/create-skill`).

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

### meta

> Claude Code skill, hook, and command management and analysis.

| Skill | Description |
|-------|-------------|
| [audit-skill](./meta/skills/audit-skill/) | Evaluate existing skills against the quality review checklist and produce structured audit reports. |
| [capture-analysis](./meta/skills/capture-analysis/) | Capture skill gaps, workflow frictions, and pattern improvements as structured entries. |
| [create-continuation](./meta/skills/create-continuation/) | Generate a continuation prompt for seamless session handoffs to a new conversation. |
| [create-hook](./meta/skills/create-hook/) | Guide for creating or improving Claude Code hooks. |
| [create-readme](./meta/skills/create-readme/) | Create or review a README.md for the project. |
| [create-script](./meta/skills/create-script/) | Create bash scripts with the right structure — operational template for stateful scripts, direct for utilities. |
| [create-skill](./meta/skills/create-skill/) | Guide for creating, reviewing, and improving Claude Code skills. |
| [find-skills](./meta/skills/find-skills/) | Discover and install agent skills from the open ecosystem. |
| [improve-codebase-architecture](./meta/skills/improve-codebase-architecture/) | Explore a codebase for architectural friction and propose deep-module refactors as GitHub issue RFCs. |
| [install-skill](./meta/skills/install-skill/) | Install a skill from an npx skills link with local or global selection. |
| [plan-skill](./meta/skills/plan-skill/) | Plan and spec out a skill from raw input — produces a structured spec consumed by `/create-skill`. |
| [sync-claude](./meta/skills/sync-claude/) | Synchronize the Claude Code environment (skills-library + .brain) across machines — pull, rebuild symlinks, verify. |
| [uninstall-skill](./meta/skills/uninstall-skill/) | Uninstall a skill by name, local or global. |
| [update-script](./meta/skills/update-script/) | Audit and upgrade existing bash scripts to follow operational patterns — flags, dry-run, validation, idempotency. |
| [update-skill](./meta/skills/update-skill/) | Scoped edits to existing skills — reads skill-meta.json, modifies affected sections, verifies skeleton compliance. |

[Back to top](#claude-skills-library)

---

### learning

> Guided learning sessions with TDD, progressive hints, and study guides.

| Skill | Description |
|-------|-------------|
| [teach-me](./learning/skills/teach-me/) | Guided TDD teaching sessions — reads student code, provokes with questions, explains only when asked. Supports replay mode and gist-based study guides. |

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

Use `/create-skill` to scaffold a new skill. It walks you through intent, triggers, and structure, then generates a `SKILL.md` with correct frontmatter and all 13 skeleton sections.

Key rules:

- **Under 500 lines** — extract detail to `references/` with Read pointers
- **Never-skip sections** — Pre-flight, Self-audit, Anti-patterns, and Guidelines always have real content
- **Self-contained** — no cross-skill dependencies; each skill includes everything it needs
- **Progressive disclosure** — inline summary + `Read references/...` pointer for sections > ~15 lines

> [!TIP]
> Run `/audit-skill` after editing to verify skeleton compliance and catch quality gaps.
