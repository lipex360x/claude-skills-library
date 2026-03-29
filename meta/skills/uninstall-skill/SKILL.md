---
name: uninstall-skill
model: sonnet
description: >-
  Uninstall a skill by name, local or global. Use this skill when the user says
  "uninstall skill", "remove skill", "delete skill", "skill uninstall", "get rid
  of a skill", "I don't need this skill anymore", or wants to remove an
  installed skill — even if they don't explicitly say "uninstall."
user-invocable: true
allowed-tools:
  - Bash
  - AskUserQuestion
  - Read
  - Glob
  - Edit
argument-hint: <skill-name>
---

# Uninstall Skill

Remove an installed skill from the local project or global skills-library, with full cleanup of symlinks, indexes, and registry.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `skill-name` | $ARGUMENTS | yes | Must match a directory in `.claude/skills/` (local) or `skills-library/*/skills/` (global) | Fuzzy search similar names and present via AUQ; if no matches, report not found |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Removed skill directory | `.claude/skills/<name>/` or `skills-library/<plugin>/skills/<name>/` | no (deleted) | — |
| Removed symlink | `~/.claude/skills/<name>` (global only) | no (deleted) | — |
| Updated STRUCTURE.md | `skills-library/STRUCTURE.md` (global only) | yes | Markdown |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Local skills | `.claude/skills/` | R/W | Directories |
| Global skills | `~/www/claude/skills-library/*/skills/` | R/W | Directories |
| Skills symlinks | `~/.claude/skills/` | R/W | Symlinks |
| setup.sh | `~/.brain/scripts/setup.sh` | R | Bash script |
| STRUCTURE.md | `skills-library/STRUCTURE.md` | R/W | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. $ARGUMENTS is non-empty → if empty: AUQ "Which skill do you want to uninstall?" — stop if no answer.
2. Skill exists in at least one location (local `.claude/skills/` or global `skills-library/*/skills/`) → if not found: fuzzy search similar names and present via AUQ; if still no match: "Skill `$ARGUMENTS` not found" — stop.

</pre_flight>

## Steps

### 1. Locate the skill

Search both locations for a skill matching $ARGUMENTS:

- **Local:** `.claude/skills/$ARGUMENTS/` in the current project directory
- **Global:** `~/www/claude/skills-library/` — search all `<plugin>/skills/` directories

If not found in either location, search for similar names before failing — the user may have misspelled. If similar names exist, present with AUQ as selectable options.

### 2. Confirm scope

If found in **both** locations, use AUQ with options `["Local (this project)", "Global (skills-library/)", "Both"]`.

If found in only one location, proceed directly — no confirmation needed because the action is unambiguous.

### 3. Pre-removal safety checks

Before deleting, verify these conditions because `rm -rf` on a skill directory is irreversible:

**Symlink detection.** Check if the directory is a symlink. If removing a global skill, also identify the corresponding symlink in `~/.claude/skills/`.

**Permission check.** Verify write access before attempting deletion. If no write access, report the error and stop — don't attempt `sudo` or workarounds.

### 4. Remove

Double-check the resolved path before deleting — confirm it points to a skill directory (contains SKILL.md) and not a parent or unrelated path.

```bash
# Safety: verify the path contains SKILL.md before deleting
test -f <skill-path>/SKILL.md || echo "ABORT: path does not contain SKILL.md"
rm -rf <skill-path>
```

**For global removals**, also:
1. Remove the symlink in `~/.claude/skills/$ARGUMENTS`
2. Run `setup.sh` to clean stale symlinks — essential because `setup.sh` manages the symlink registry:

```bash
bash ~/.brain/scripts/setup.sh
```

3. Update `skills-library/STRUCTURE.md` — find and remove the skill entry using the Edit tool.

**For local removals**, clean up the parent directory if empty:

```bash
rmdir .claude/skills/ 2>/dev/null  # only removes if empty
```

### 5. Post-removal verification

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

### 6. Report

Present concisely:
- **What was done** — skill name, scope (local/global/both), plugin group (global)
- **Artifacts removed** — directory, symlink, STRUCTURE.md entry
- **setup.sh** — re-run status (global only)
- **Audit results** — self-audit summary
- **Errors** — issues encountered (or "none")

## Next action

> _Skipped: "Session complete — no follow-up needed."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — skill name provided, skill found in at least one location
2. **Steps completed?** — directory removed, symlink cleaned (global), STRUCTURE.md updated (global), setup.sh re-run (global)
3. **Output exists?** — skill directory no longer exists at original path
4. **Anti-patterns clean?** — symlinks checked before deletion, no `sudo` used, STRUCTURE.md updated
5. **Approval gates honored?** — scope confirmed when skill found in both locations

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (removal workflow)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| Skill not found | Fuzzy search similar names, present via AUQ — stop if still no match |
| No write permission | Report error — stop (never use `sudo`) |
| `rm -rf` target has no SKILL.md | Abort deletion — report path mismatch |
| `setup.sh` fails | Report error, suggest manual symlink cleanup |
| STRUCTURE.md edit fails | Report error, provide manual edit instructions |

## Anti-patterns

- **Deleting without checking symlinks first.** Removing only the symlink target leaves a dangling symlink in `~/.claude/skills/` — because dangling symlinks cause "skill not found" errors in future sessions.
- **Skipping `setup.sh` after global removal.** Leaves stale symlinks — because the symlink registry becomes inconsistent with the actual skill state.
- **Not updating STRUCTURE.md.** The directory index becomes stale — because STRUCTURE.md is the source of truth for codebase navigation.
- **Using `sudo` to bypass permission errors.** If permissions block deletion, it's a signal something is wrong — because escalating privileges on `rm -rf` is dangerous and masks the real issue.
- **Deleting without verifying SKILL.md exists.** A wrong target with `rm -rf` is unrecoverable — because the safety check (SKILL.md presence) prevents accidentally deleting unrelated directories.

## Guidelines

- **Safety first.** Always verify the target contains SKILL.md before `rm -rf` — because a wrong path is unrecoverable. Double-check symlink resolution and directory contents.

- **Clean removal is complete removal.** Directory, symlink, STRUCTURE.md entry, and setup.sh re-run — because partial cleanup leaves inconsistent state that causes confusing errors later.

- **No escalation.** If permissions block the operation, stop and report — because `sudo rm -rf` on user skill directories is never the right answer.

- **Fuzzy matching over hard failure.** When the exact name isn't found, search for similar names before reporting "not found" — because typos are common and a helpful suggestion saves the user a retry.
