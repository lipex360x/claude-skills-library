---
description: Install a skill from an npx skills link, with local/global selection.
argument-hint: <npx-skills-add-command>
allowed-tools: Bash, AskUserQuestion, Read, Write, Glob
---

The user wants to install a skill. The full npx command is: `$ARGUMENTS`

**Step 1 — Ask scope:** Use `AskUserQuestion` with selectable options `["Local (this project)", "Global (.brain/)"]` to determine where to install.

**Step 2 — Install:**

- **Local:** Run the npx command as-is with `--copy -a claude-code -y` flags appended (if not already present). The skill lands in the project's `.claude/skills/`. Done — no symlinks needed.
- **Global:** Run the npx command with `--copy -a claude-code -y` flags appended. By default npx installs into the project's `.claude/skills/`, so after install:
  1. **Verify symlink:** Check that `~/.claude/skills` is a symlink pointing to `~/www/claude/.brain/skills/`. If not, create it (or alert the user to run `setup.sh`)
  2. Find the skill directory created in the project's `.claude/skills/`
  3. Move it to `~/.claude/skills/` (which resolves to `.brain/skills/` via symlink)
  4. Clean up the local copy if one remains in the project
  5. **Clean up npx leftovers:** Remove any empty `.claude/skills/` directory, `.agents/` directory, and `skills-lock.json` file left behind by npx in the project's working directory. These are installation artifacts not needed after the skill is moved to `.brain/`.
  6. **Update STRUCTURE.md:** Read `~/www/claude/.brain/STRUCTURE.md`, find the `skills/` section, and add a new entry following the existing format: `- \`skill-name/SKILL.md\` — short description from the skill's frontmatter`. This step is MANDATORY for global installs — do not skip it.

**Step 3 — Verify:** Confirm the skill directory exists inside `~/www/claude/.brain/skills/` and that STRUCTURE.md was updated (for global installs). Report success with the skill name and location.
