---
description: Uninstall a skill by name (local or global).
argument-hint: <skill-name>
allowed-tools: Bash, AskUserQuestion, Read, Glob
---

The user wants to uninstall the skill: `$ARGUMENTS`

**Step 1 — Locate the skill:** Check both locations:
- **Local:** `.claude/skills/$ARGUMENTS/` in the current project directory
- **Global:** `~/www/claude/.brain/skills/$ARGUMENTS/`

**Step 2 — If found in both or unclear:** Use `AskUserQuestion` with selectable options `["Local (this project)", "Global (.brain/)", "Both"]` to confirm which to remove.

If found in only one location, proceed directly — no need to ask.

**Step 3 — Remove:** Delete the skill directory (`rm -rf`). If removing globally, also update `~/www/claude/.brain/STRUCTURE.md` if the skill was listed there.

**Step 4 — Confirm** removal with the skill name and which location was cleaned.
