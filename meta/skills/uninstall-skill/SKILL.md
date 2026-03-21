---
name: uninstall-skill
description: Uninstall a skill by name, local or global. Use this skill when the user says "uninstall skill", "remove skill", "delete skill", "skill uninstall", or wants to remove an installed skill — even if they don't explicitly say "uninstall."
user-invocable: true
allowed-tools: Bash, AskUserQuestion, Read, Glob, Edit
argument-hint: <skill-name>
---

The user wants to uninstall the skill: `$ARGUMENTS`

## 1. Locate the skill

Search both locations for a skill matching `$ARGUMENTS`:

- **Local:** `.claude/skills/$ARGUMENTS/` in the current project directory
- **Global:** `~/www/claude/skills-library/` — search all `<plugin>/skills/` directories for a matching skill name

```bash
# Local check
ls -d .claude/skills/$ARGUMENTS/ 2>/dev/null

# Global check — search all plugins
find ~/www/claude/skills-library/*/skills -maxdepth 1 -type d -name "$ARGUMENTS" 2>/dev/null
```

**If not found in either location**, search for similar names before failing — the user may have misspelled:

```bash
# Fuzzy search across both locations
ls .claude/skills/ 2>/dev/null | grep -i "<partial>"
find ~/www/claude/skills-library/*/skills -maxdepth 1 -type d 2>/dev/null | xargs -I{} basename {} | grep -i "<partial>"
```

If similar names exist, present them with `AskUserQuestion` as selectable options. If no matches at all, report clearly: "Skill `$ARGUMENTS` not found in local (`.claude/skills/`) or global (`skills-library/`) locations."

## 2. Confirm scope

If found in **both** locations, use `AskUserQuestion` with selectable options `["Local (this project)", "Global (skills-library/)", "Both"]` to confirm which to remove.

If found in only one location, proceed directly — no confirmation needed because the action is unambiguous.

## 3. Pre-removal safety checks

Before deleting, verify these conditions because `rm -rf` on a skill directory is irreversible:

**3a. Symlink detection.** Check if the directory is a symlink (global skills are symlinked into `~/.claude/skills/`):

```bash
ls -la <skill-path>
```

If the target is a symlink, follow it to the real source and delete the source — removing only the symlink leaves orphaned files. If removing a global skill, also remove the corresponding symlink in `~/.claude/skills/`.

**3b. Permission check.** Verify write access before attempting deletion:

```bash
test -w <skill-parent-directory> && echo "writable" || echo "no write access"
```

If no write access, report the error and stop — don't attempt `sudo` or workarounds.

## 4. Remove

Delete the skill directory:

```bash
rm -rf <skill-path>
```

**For global removals**, also:

1. Remove the symlink in `~/.claude/skills/$ARGUMENTS` if it exists
2. Run `setup.sh` to clean any stale symlinks — this is essential because `setup.sh` manages the symlink registry, and skipping it leaves orphaned references that cause confusing "skill not found" errors in future sessions:

```bash
bash ~/.brain/scripts/setup.sh
```

3. Update `~/www/claude/skills-library/STRUCTURE.md` — find the skill entry in the plugin's table row and remove it. Use the `Edit` tool to make the change precise.

**For local removals**, clean up the parent directory if empty:

```bash
rmdir .claude/skills/ 2>/dev/null  # only removes if empty
```

## 5. Post-removal verification

Verify the removal was clean:

```bash
# Confirm directory is gone
test -d <skill-path> && echo "FAIL: directory still exists" || echo "OK: removed"

# For global: confirm symlink is gone
test -L ~/.claude/skills/$ARGUMENTS && echo "FAIL: symlink still exists" || echo "OK: symlink clean"

# For global: confirm STRUCTURE.md was updated
grep -c "$ARGUMENTS" ~/www/claude/skills-library/STRUCTURE.md
```

If any check fails, report the specific failure and attempt to fix it.

## 6. Report

Present a removal summary:

```
✓ Uninstalled: <skill-name>
  Location:    <local | global (<plugin-name> plugin) | both>
  Directory:   removed
  Symlink:     removed (global only)
  STRUCTURE:   updated (global only)
  setup.sh:    re-run (global only)
```

Include warnings if any post-removal checks failed.

## Anti-patterns

- **Deleting without checking symlinks first** — removing only the symlink target leaves a dangling symlink in `~/.claude/skills/` that causes "skill not found" errors
- **Skipping `setup.sh` after global removal** — leaves stale symlinks that confuse skill discovery and autocomplete
- **Not updating `STRUCTURE.md`** — the directory index becomes stale, misleading future codebase exploration
- **Using `sudo` to bypass permission errors** — if permissions block deletion, it's a signal that something is wrong (wrong path, system-owned file); escalating privileges on `rm -rf` is dangerous
- **Deleting a skill that other skills reference** — currently skills are self-contained by design, but always verify the skill directory contains only standard files (SKILL.md, README.md, references/, templates/) before removing
