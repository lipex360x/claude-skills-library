# Skills Library

Repository of reusable Claude Code skills.

## Rules

- **Always load `/create-skill` when creating or editing skills.** Run the review checklist (`references/review-checklist.md`) after every edit. Skills edited without the checklist ship with quality gaps (cross-skill dependencies, missing reasoning, missing anti-patterns).
- **Dual sync.** Every change must be applied in both this repo and `~/.claude/skills/` (symlinked to `.brain/skills/`). Verify with `diff -rq` after sync.
- **Skills must be self-contained.** No cross-skill dependencies — each skill must include all references it needs in its own `references/` directory.
- **Keep SKILL.md under 500 lines.** Extract detail to `references/` with Read tool instructions.
- **Project-agnostic content only.** Skills must not reference specific frameworks, tools, or project structures. Use placeholders and examples in parentheses.
