# .docs/ Directory Structure

The `.docs/` directory is the consolidated home for all project documentation that agents read during planning, implementation, and review. The `/start-new-project` skill scaffolds this directory during project setup.

## Files to scaffold

| File | Source template | Purpose |
|------|----------------|---------|
| `.docs/project.md` | `templates/project.md` | Source of Truth — purpose, domain, users, business rules, boundaries |
| `.docs/architecture.md` | `templates/architecture.md` | Codebase knowledge cache — stack, layers, patterns, key flows |
| `.docs/quality.md` | `templates/quality-standards.md` | Non-negotiable code quality rules adapted to the project stack |
| `.docs/issues/` | Empty directory with `.gitkeep` | Issue body backups and compacted summaries |
| `.docs/reviews/` | Empty directory with `.gitkeep` | PR review notes and post-merge learnings |

## Scaffolding commands

```bash
mkdir -p .docs/issues .docs/reviews
touch .docs/issues/.gitkeep .docs/reviews/.gitkeep
# Copy and fill templates:
# cp <skill-templates>/project.md .docs/project.md
# cp <skill-templates>/architecture.md .docs/architecture.md
# cp <skill-templates>/quality-standards.md .docs/quality.md
```

## Conventions

- **Lowercase filenames only** inside `.docs/` (e.g., `architecture.md`, not `ARCHITECTURE.md`).
- **project.md** is filled during `/start-new-project` Step 4 (after clarifying questions provide domain knowledge).
- **architecture.md** is filled during Phase 1 implementation as the stack and patterns take shape.
- **quality.md** is adapted to the project's specific stack during the Phase 1 quality standards checkbox.
- Subdirectories (`issues/`, `reviews/`) start empty and are populated by workflow skills during development.

## Why .docs/ instead of root files

1. **Declutters the repo root** — no ARCHITECTURE.md, QUALITY.md, etc. competing with README.md and config files.
2. **Single discovery point** — agents know all project docs live in `.docs/`, reducing search overhead.
3. **Clear ownership** — `.docs/` is maintained by the development workflow, not by CI or build tools.
4. **Gitkeep subdirectories** — ensures the structure exists even before content is generated.
