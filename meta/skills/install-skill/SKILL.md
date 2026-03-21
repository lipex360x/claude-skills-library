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

If the npx command fails (non-zero exit, network error, package not found), report the error to the user and stop — do not proceed with a partial or missing install.

### 3.4 Identify and validate the installed skill

Find the new skill directory in the project's `.claude/skills/`. Read its `SKILL.md` — if the file is missing or has no frontmatter (`name`, `description`), the package is malformed. Warn the user with the specific issue and stop because a skill without valid SKILL.md frontmatter won't be discoverable.

**Quality gate:** Confirm the SKILL.md has at minimum `name`, `description`, and `user-invocable` in the frontmatter. If `description` lacks trigger phrases (e.g., "Use this skill when..."), flag it to the user as a quality concern — the skill may not activate reliably without them.

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

If `setup.sh` fails, check the error output — common causes are missing plugin.json or broken directory structure. Report the error and stop because the skill won't be discoverable without a valid symlink.

### 3.8 Clean up npx leftovers

Remove artifacts left by npx in the project's working directory:
- Empty `.claude/skills/` directory
- `.agents/` directory (if created by npx)
- `skills-lock.json` file

Only remove these if they were created by the install — check they are empty or npx-generated before deleting.

### 3.9 Update STRUCTURE.md

Read `~/www/claude/skills-library/STRUCTURE.md`. Find the section for the target plugin group. Add a new entry following the existing format:

```
- `<skill-name>` — <short description from frontmatter>
```

Insert alphabetically within the group. If a new group was created, add a new section following the pattern of existing groups in the table.

**Quality gate:** After editing, re-read STRUCTURE.md and verify the new entry appears in the correct plugin row, is alphabetically ordered, and the skill count in the table header is accurate.

### 3.10 Update READMEs

Update two READMEs inline (do not invoke other skills — this step is self-contained):

1. **Skill README** — Read the skill's SKILL.md frontmatter and body. Create or update `<group>/skills/<skill-name>/README.md` with: skill name, one-line description, trigger phrases (extracted from the `description` field), install command (`npx skills add <package>`), and usage examples.
2. **skills-library README** — Read the root `README.md`. Add the new skill to the plugin's table row following the existing format (alphabetical order within the group). If a new group was created, add a new table row.

Both READMEs must be updated — never skip this step.

### 3.11 Verify before pushing

Before committing, verify the installation end-to-end:

1. **Symlink exists** — confirm `~/.claude/skills/<skill-name>` points to the correct directory in skills-library
2. **SKILL.md is valid** — re-read the final SKILL.md and confirm frontmatter is intact (npx artifacts or moves can corrupt files)
3. **STRUCTURE.md entry** — confirm the skill appears in the correct plugin row
4. **README entries** — confirm both the skill README and root README reference the new skill

If any check fails, fix the issue before proceeding. This gate catches problems that are hard to diagnose after pushing.

### 3.12 Push to GitHub

Stage all files touched in this session (skill files, STRUCTURE.md, READMEs) in the skills-library repo. Commit with a conventional message following the pattern `feat(<plugin>): add <skill-name> skill`.

```bash
cd ~/www/claude/skills-library && git add <files> && git commit -m "feat(<plugin>): add <skill-name> skill" && git push
```

If the push fails (auth error, rejected push, network issue), report the specific error to the user. Common fix: `git pull --rebase` then retry. The installation is not complete until changes are pushed to GitHub.

### 3.13 Report

Report to the user:
- Skill name and description
- Which group it was added to
- Symlink created at `~/.claude/skills/<skill-name>`
- STRUCTURE.md, READMEs updated
- Pushed to GitHub

## Anti-patterns

- **Installing without checking for duplicates** — always run step 3.2 first. Overwriting an existing skill without the user's consent can destroy customizations.
- **Skipping STRUCTURE.md update** — the skill will exist on disk but be invisible to anyone navigating the repo via STRUCTURE.md. Always update the index.
- **Leaving npx artifacts in the project** — `.agents/`, empty `.claude/skills/`, or `skills-lock.json` left behind pollute the project's working directory. Clean up in step 3.8.
- **Pushing without verifying** — skipping step 3.11 means broken symlinks, missing entries, or corrupted SKILL.md files get committed. Always verify before push.
- **Invoking other skills mid-install** — README generation and push must be done inline. Cross-skill invocations create hidden dependencies that break when skills are used in isolation.
