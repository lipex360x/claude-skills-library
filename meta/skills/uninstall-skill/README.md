# uninstall-skill

> Uninstall a skill by name, local or global.

Removes an installed skill from either the current project or the global skills-library, cleaning up directories and updating `STRUCTURE.md` as needed.

## Usage

```text
/uninstall-skill <skill-name>
```

> [!TIP]
> Also activates when you say "uninstall skill", "remove skill", "delete skill", or want to remove an installed skill.

## How it works

1. **Locate the skill** — Checks both local (`.claude/skills/`) and global (`skills-library/`) locations
2. **Confirm scope** — If found in both locations, asks which to remove (local, global, or both)
3. **Remove** — Deletes the skill directory and updates `STRUCTURE.md` if removing globally
4. **Confirm** — Reports which skill was removed and from which location

## Directory structure

```text
uninstall-skill/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill uninstall-skill
```
