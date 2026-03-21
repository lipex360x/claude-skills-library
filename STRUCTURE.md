# Skills Library — Directory Structure

Quick reference for navigating the repository. Read this before exploring — it tells you where things are and what each level means.

## Hierarchy

```
skills-library/
├── CLAUDE.md                         # Repo rules (always loaded)
├── README.md                         # Public docs, plugin index, install commands
├── STRUCTURE.md                      # This file
├── skills-lock.json                  # Lock file for installed skills
├── templates/                        # Shared templates (not skill-specific)
└── <plugin>/                         # One directory per plugin (domain group)
    ├── .claude-plugin/
    │   └── plugin.json               # Plugin manifest (name, description, version)
    └── skills/
        └── <skill-name>/
            ├── SKILL.md              # Required. Frontmatter + instructions (<500 lines)
            ├── README.md             # Public-facing docs (install, usage, triggers)
            ├── references/           # Optional. Detailed guides loaded on demand
            └── templates/            # Optional. Output formats, starter structures
```

## Plugins (8)

| Plugin | Domain | Skills |
|--------|--------|--------|
| **workflow** | GitHub workflow: issues, branches, PRs, commits | add-backlog, close-pr, grill-me, list-backlog, list-issues, open-pr, push, start-issue, start-new-project, tdd |
| **content** | Content creation, voice profiling, publishing, mental unblocking | approve-post, capture-voice, inspire-me, write-content |
| **design** | Visual design: diagrams, design systems, presentations | create-diagram, create-excalidraw, create-webview, extract-design-system |
| **database** | Database optimization and best practices | review-postgres |
| **deploy** | Deployment and infrastructure | deploy-vercel |
| **gws** | Google Workspace: Gmail filters, inbox management | check-gmail |
| **meta** | Claude Code skill/hook management and analysis | audit-skill, capture-analysis, create-continuation, create-hook, create-readme, create-skill, find-skills, improve-codebase-architecture, install-skill, plan-skill, sync-claude, uninstall-skill |
| **tasks** | Task visibility board management | clean-tasks, close-tasks, open-tasks |

## How to navigate

- **Know the plugin?** Go directly to `<plugin>/skills/<skill-name>/SKILL.md`
- **Looking for a skill?** Check the table above or `README.md` for the full index
- **Creating a skill?** Use `/create-skill`. Place it in the right plugin under `skills/`
- **Need plugin metadata?** Read `<plugin>/.claude-plugin/plugin.json`

## Key files at root

| File | Purpose | When to read |
|------|---------|--------------|
| `CLAUDE.md` | Repo-wide rules for editing skills | Always loaded automatically |
| `README.md` | Full plugin/skill index with install commands | When you need skill descriptions or install syntax |
| `STRUCTURE.md` | This file — directory map | Before exploring the repo to orient yourself |
| `skills-lock.json` | Tracks installed skill versions | When debugging install issues |
