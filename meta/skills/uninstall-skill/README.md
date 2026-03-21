# uninstall-skill

> Uninstall a skill by name, local or global.

Safely removes an installed skill from either the current project or the global skills-library. Handles symlink cleanup, permission checks, `setup.sh` re-registration, and `STRUCTURE.md` updates.

## Usage

```text
/uninstall-skill <skill-name>
```

> [!TIP]
> Also activates when you say "uninstall skill", "remove skill", "delete skill", or want to remove an installed skill.

## How it works

1. **Locate the skill** — Searches both local (`.claude/skills/`) and global (`skills-library/`) locations. Suggests similar names if not found.
2. **Confirm scope** — If found in both locations, asks which to remove (local, global, or both)
3. **Pre-removal safety checks** — Detects symlinks, verifies write permissions before any destructive operation
4. **Remove** — Deletes the skill directory, removes symlinks, runs `setup.sh` for global removals, updates `STRUCTURE.md`
5. **Post-removal verification** — Confirms directory, symlinks, and index are clean
6. **Report** — Presents a structured removal summary with any warnings

## Directory structure

```text
uninstall-skill/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill uninstall-skill
```
