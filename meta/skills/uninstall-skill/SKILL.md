---
name: uninstall-skill
description: Uninstall a skill by name, local or global. Use this skill when the user says "uninstall skill", "remove skill", "delete skill", "skill uninstall", or wants to remove an installed skill — even if they don't explicitly say "uninstall."
user-invocable: true
allowed-tools: Bash, AskUserQuestion, Read, Glob
argument-hint: <skill-name>
---

The user wants to uninstall the skill: `$ARGUMENTS`

## 1. Locate the skill

Check both locations:
- **Local:** `.claude/skills/$ARGUMENTS/` in the current project directory
- **Global:** `~/www/claude/skills-library/` (search all plugin directories for a matching skill name)

## 2. Confirm scope

If found in both or unclear, use `AskUserQuestion` with selectable options `["Local (this project)", "Global (skills-library/)", "Both"]` to confirm which to remove.

If found in only one location, proceed directly.

## 3. Remove

Delete the skill directory (`rm -rf`). If removing globally, also update `~/www/claude/.brain/STRUCTURE.md` if the skill was listed there.

## 4. Confirm

Report removal with the skill name and which location was cleaned.
