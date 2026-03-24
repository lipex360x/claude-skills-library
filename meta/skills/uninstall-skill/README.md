# uninstall-skill

> Uninstall a skill by name, local or global.

Full removal pipeline with pre-deletion safety checks: verifies the target contains SKILL.md before any `rm -rf`, detects symlinks, checks write permissions, and confirms scope when the skill exists in both local and global locations. Global removals also clean up symlinks, re-run `setup.sh`, and update STRUCTURE.md. Includes post-removal verification to confirm clean state.

## Usage

```text
/uninstall-skill <skill-name>
```

> [!TIP]
> Also activates when you say "uninstall skill", "remove skill", "delete skill", "skill uninstall", "get rid of a skill", "I don't need this skill anymore", or want to remove an installed skill.

### Examples

```text
/uninstall-skill deploy-vercel     # remove a skill by name
/uninstall-skill                   # prompted for skill name
```

> [!WARNING]
> This skill permanently deletes the skill directory and its contents. There is no undo — removed files cannot be recovered unless they exist in a git history.

## How it works

1. **Locate the skill** — Searches both local (`.claude/skills/`) and global (`skills-library/`) locations; suggests similar names via fuzzy matching if not found
2. **Confirm scope** — If found in both locations, asks which to remove (local, global, or both) via AUQ. Proceeds directly if found in only one location
3. **Pre-removal safety checks** — Detects symlinks, verifies write permissions, confirms target path contains SKILL.md before any deletion
4. **Remove** — Deletes the skill directory. For global: also removes symlink in `~/.claude/skills/`, runs `setup.sh`, and updates STRUCTURE.md. For local: cleans up empty parent directory
5. **Post-removal verification** — Confirms directory is gone, symlinks are clean, and index entries are removed
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
