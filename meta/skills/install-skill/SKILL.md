---
name: install-skill
description: Install a skill from an npx skills link, with local or global selection. Use this skill when the user says "install skill", "add skill", "skill install", or provides an npx skills command — even if they don't explicitly say "install."
user-invocable: true
allowed-tools: Bash, AskUserQuestion, Read, Write, Edit, Glob
argument-hint: <npx-skills-add-command>
---

The user wants to install a skill. The full npx command is: `$ARGUMENTS`

## 1. Ask scope (if not specified)

If the user didn't specify local or global, use `AskUserQuestion` with selectable options `["Local (this project)", "Global (skills-library/)"]`.

## 2. Local install

Run the npx command as-is with `--copy -a claude-code -y` flags appended (if not already present). The skill lands in the project's `.claude/skills/`. Done — no further steps.

## 3. Global install

### 3.1 Sync skills-library

Pull latest changes from the remote to ensure the local skills-library is up to date before installing anything:

```bash
cd ~/www/claude/skills-library && git pull
```

If the pull fails (e.g. uncommitted changes, merge conflicts), warn the user and ask whether to proceed anyway or resolve first.

### 3.2 Check for duplicates

Extract the skill name from the npx command (typically the last argument, e.g. `npx skills add @user/skill-name` → `skill-name`). Then check if it already exists:

```bash
ls -d ~/www/claude/skills-library/*/skills/*/ 2>/dev/null | grep -i "<skill-name>"
ls -d ~/.claude/skills/*/ 2>/dev/null | grep -i "<skill-name>"
```

If the skill already exists, use `AskUserQuestion` with selectable options:
- `["Reinstall (overwrite existing)", "Cancel installation"]`

Explain which group the existing skill is in. Only proceed if the user explicitly chooses to reinstall. If they cancel, stop immediately.

### 3.3 Run npx

Run the npx command with `--copy -a claude-code -y` flags. By default npx installs into the project's `.claude/skills/`.

### 3.4 Identify the installed skill

Find the new skill directory in the project's `.claude/skills/`. Read its `SKILL.md` frontmatter to get the skill name and description.

### 3.5 Determine the target plugin group

The skills-library uses plugin groups to organize skills. Current groups and their purposes:

| Group | Purpose |
|---|---|
| `workflow` | GitHub workflow: issues, branches, PRs, commits |
| `content` | Content creation, voice profiling, publishing |
| `design` | Visual design: diagrams, design systems |
| `database` | Database optimization and best practices |
| `deploy` | Deployment and infrastructure |
| `meta` | Claude Code skill/hook/command management and analysis |
| `tasks` | Task visibility board management |

Analyze the skill's description and purpose to determine which group it belongs to. If the match is clear, proceed without asking. If ambiguous or no group fits, use `AskUserQuestion` with selectable options listing the existing groups plus a suggested new group name. Example:

```
["workflow", "content", "design", "database", "deploy", "meta", "tasks", "testing (new)"]
```

If a new group is needed:
1. Ask for the group name and one-line description with `AskUserQuestion` (free text).
2. Create the plugin directory structure:
   ```
   ~/www/claude/skills-library/<group-name>/
     .claude-plugin/
       plugin.json    ← {"name":"<group-name>","description":"<description>","version":"1.0.0"}
     skills/
   ```

### 3.6 Move the skill

Move the skill directory from the project's `.claude/skills/<skill-name>/` to `~/www/claude/skills-library/<group>/skills/<skill-name>/`.

### 3.7 Register the skill

Run `setup.sh` to create the symlink in `~/.claude/skills/` and register the new skill for discovery:

```bash
bash ~/.brain/scripts/setup.sh
```

This is idempotent — it scans all plugins, creates missing symlinks, and cleans stale ones. Without this step, the skill won't appear in `/` autocomplete in new sessions.

### 3.8 Clean up npx leftovers

Remove artifacts left by npx in the project's working directory:
- Empty `.claude/skills/` directory
- `.agents/` directory (if created by npx)
- `skills-lock.json` file

Only remove these if they were created by the install — check they are empty or npx-generated before deleting.

### 3.9 Update STRUCTURE.md

Read `~/www/claude/.brain/STRUCTURE.md`. Find the section for the target plugin group. Add a new entry following the existing format:

```
- `<skill-name>` — <short description from frontmatter>
```

Insert alphabetically within the group. If a new group was created, add a new section following the pattern:

```
**<group-name>** — <group description>
- `<skill-name>` — <short description>
```

Insert the new group section alphabetically among existing groups.

### 3.10 Report

Report to the user:
- Skill name and description
- Which group it was added to
- Symlink created at `~/.claude/skills/<skill-name>`
- STRUCTURE.md updated
