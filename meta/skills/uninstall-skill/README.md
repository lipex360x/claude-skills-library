# uninstall-skill

> Uninstall a skill by name, local or global.

Safely removes an installed skill from either the current project or the global skills-library. Handles symlink cleanup, permission checks, `setup.sh` re-registration, and `STRUCTURE.md` updates with pre-removal safety verification.

## Usage

```text
/uninstall-skill <skill-name>
```

> [!TIP]
> Also activates when you say "uninstall skill", "remove skill", "delete skill", "skill uninstall", "get rid of a skill", "I don't need this skill anymore", or want to remove an installed skill.

## How it works

1. **Locate the skill** — Searches both local (`.claude/skills/`) and global (`skills-library/`) locations; suggests similar names via fuzzy matching if not found
2. **Confirm scope** — If found in both locations, asks which to remove (local, global, or both)
3. **Pre-removal safety checks** — Detects symlinks, verifies write permissions, confirms target contains SKILL.md before any deletion
4. **Remove** — Deletes the skill directory, removes symlinks, runs `setup.sh` (global), updates `STRUCTURE.md` (global)
5. **Post-removal verification** — Confirms directory, symlinks, and index entries are clean
6. **Report** — Shows skill name, scope, removed artifacts, and any warnings

## Directory structure

```text
uninstall-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill uninstall-skill
```
