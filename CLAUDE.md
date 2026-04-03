# Skills Library

Repository of reusable Claude Code skills.

## Rules

- **Always load `/create-skill` when creating or editing skills.** Run the review checklist (`references/review-checklist.md`) after every edit. Skills edited without the checklist ship with quality gaps (cross-skill dependencies, missing reasoning, missing anti-patterns).
- **Dual sync.** Every change must be applied in both this repo and `~/.claude/skills/` (symlinked to `.brain/skills/`). Verify with `diff -rq` after sync.
- **Skills must be self-contained.** No cross-skill dependencies — each skill must include all references it needs in its own `references/` directory.
- **Keep SKILL.md under 500 lines.** Extract detail to `references/` with Read tool instructions.
- **Project-agnostic content only.** Skills must not reference specific frameworks, tools, or project structures. Use placeholders and examples in parentheses.
- **Step tracking is mandatory at runtime.** When a skill is invoked, the agent MUST: (1) set `"skill-active": true` and `"skill-active-name": "<skill-name>"` in `.claude/project-setup.json` before the first step, (2) produce visible output for every numbered step (tool call, table, or explicit statement — mental completion is not completion), (3) set `"skill-active": false` and remove `"skill-active-name"` after post-flight completes. A Stop hook blocks the agent from stopping while the flag is true. When waiting for a background sub-agent, set `skill-active` to `false` during the wait to prevent stop-hook loops, then re-enable when active work resumes. This is enforced by `~/.brain/hooks/templates/skill-step-enforcer.sh`.
