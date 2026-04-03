---
name: install-skill
description: >-
  Install a skill from an npx skills link, with local or global selection. Use
  this skill when the user says "install skill", "add skill", "skill install",
  or provides an npx skills command — even if they don't explicitly say
  "install."
user-invocable: true
allowed-tools:
  - Bash
  - AskUserQuestion
  - Read
  - Write
  - Edit
  - Glob
argument-hint: <npx-skills-add-command>
---

# Install Skill

Install a skill from the open skills ecosystem into the local project or global skills-library, with full registration and verification.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `npx-command` | $ARGUMENTS | yes | Valid `npx skills add` command string | AUQ: "Provide the npx skills add command" |
| `scope` | AUQ | yes | One of: local, global | AUQ with options `["Local (this project)", "Global (skills-library/)"]` |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Installed skill | `.claude/skills/<name>/` (local) or `skills-library/<plugin>/skills/<name>/` (global) | yes | Skill directory |
| Symlink | `~/.claude/skills/<name>` (global only) | yes | Symlink |
| STRUCTURE.md entry | `skills-library/STRUCTURE.md` (global only) | yes | Markdown |
| Skill README | `<plugin>/skills/<name>/README.md` (global only) | yes | Markdown |
| Root README entry | `skills-library/README.md` (global only) | yes | Markdown |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| skills-library repo | `~/www/claude/skills-library/` | R/W | Git repo |
| Skills symlinks | `~/.claude/skills/` | R/W | Symlinks |
| setup.sh | `~/.brain/scripts/setup.sh` | R | Bash script |
| STRUCTURE.md | `skills-library/STRUCTURE.md` | R/W | Markdown |
| Root README | `skills-library/README.md` | R/W | Markdown |
| npx registry | npm registry | R | Network |

</external_state>

## Pre-flight

<pre_flight>

1. `npx` is available → if not: "npx required. Install Node.js: https://nodejs.org/" — stop.
2. $ARGUMENTS contains a valid npx skills add command → if not: AUQ "Provide the npx skills add command" — stop if no answer.
3. User specified scope (local/global) → if not: AUQ with options `["Local (this project)", "Global (skills-library/)"]`.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Ask scope (if not specified)

If the user didn't specify local or global, use `AskUserQuestion` with selectable options `["Local (this project)", "Global (skills-library/)"]`.

### 2. Execute local install (if local scope)

Run the npx command as-is with `--copy -a claude-code -y` flags appended (if not already present). The skill lands in the project's `.claude/skills/`. Done — skip to Report step.

### 3. Sync skills-library (global only)

Pull latest changes from the remote to ensure the local skills-library is up to date:

```bash
cd ~/www/claude/skills-library && git pull
```

If the pull fails (e.g. uncommitted changes, merge conflicts), warn the user and ask whether to proceed anyway or resolve first.

### 4. Check for duplicates (global only)

Extract the skill name from the npx command. Check if it already exists in `skills-library/*/skills/` or `~/.claude/skills/`. If found, use `AskUserQuestion` with options `["Reinstall (overwrite existing)", "Cancel installation"]`. Only proceed if the user explicitly chooses to reinstall.

### 5. Run npx (global only)

Run the npx command with `--copy -a claude-code -y` flags. If the command fails (non-zero exit, network error, package not found), report the error and stop.

### 6. Validate installed skill (global only)

Find the new skill directory in `.claude/skills/`. Read its SKILL.md — if missing or has no frontmatter (`name`, `description`), the package is malformed. Warn and stop.

**Quality gate:** Confirm SKILL.md has at minimum `name`, `description`, and `user-invocable` in frontmatter. If `description` lacks trigger phrases, flag as a quality concern.

**Model selection:** If the skill's frontmatter has no `model:` field, evaluate its complexity. Operational skills (clear script, API calls, structured data, CLI commands) get `model: sonnet`. Analytical/creative skills (deep reasoning, architecture, creative writing) keep the default (opus). Add the field to the frontmatter if missing.

### 7. Determine target plugin group (global only)

Analyze the skill's description and purpose to determine which plugin group it belongs to:

| Group | Purpose |
|---|---|
| `workflow` | GitHub workflow: issues, branches, PRs, commits |
| `content` | Content creation, voice profiling, publishing |
| `design` | Visual design: diagrams, design systems |
| `database` | Database optimization and best practices |
| `deploy` | Deployment and infrastructure |
| `meta` | Claude Code skill/hook/command management and analysis |
| `tasks` | Task visibility board management |

If the match is clear, proceed without asking. If ambiguous, use AUQ listing groups plus a suggested new group name. If a new group is needed, create the plugin directory structure with `plugin.json`.

### 8. Move skill to skills-library (global only)

Move from `.claude/skills/<name>/` to `~/www/claude/skills-library/<group>/skills/<name>/`.

### 9. Register and clean up (global only)

Run `setup.sh` to create the symlink and register the skill:

```bash
bash ~/.brain/scripts/setup.sh
```

Clean up npx leftovers: empty `.claude/skills/`, `.agents/`, `skills-lock.json`. Only remove if created by the install.

### 10. Update indexes (global only)

Update `STRUCTURE.md` — add the skill entry alphabetically within the target plugin group. Update both the skill README and the root `skills-library/README.md` with the new skill.

### 11. Verify before pushing (global only)

Verify end-to-end:
1. **Symlink exists** — `~/.claude/skills/<name>` points to correct directory
2. **SKILL.md is valid** — frontmatter intact after move
3. **STRUCTURE.md entry** — skill appears in correct plugin row
4. **README entries** — both skill README and root README reference the new skill

If any check fails, fix before proceeding.

### 12. Push to GitHub (global only)

Stage all touched files, commit with `feat(<plugin>): add <skill-name> skill`, and push.

### 13. Report

Present concisely:
- **What was done** — skill name, scope (local/global), plugin group
- **Artifacts** — symlink path, STRUCTURE.md updated, READMEs updated
- **Pushed** — commit hash and branch (global only)
- **Audit results** — self-audit summary
- **Errors** — issues encountered (or "none")

## Next action

Test the installed skill by running `/<skill-name>` in a new conversation to verify it activates correctly.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — npx available, command valid, scope selected
2. **Steps completed?** — list any skipped steps with reason (local installs skip steps 3-12)
3. **Output exists?** — skill directory exists at declared path, symlink valid (global)
4. **Anti-patterns clean?** — duplicates checked, STRUCTURE.md updated, npx artifacts cleaned
5. **Approval gates honored?** — user confirmed scope and duplicate handling

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (installation workflow)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `npx` not available | Report error, suggest installing Node.js — stop |
| `git pull` fails | Warn user, AUQ `["Proceed anyway", "Resolve first"]` |
| npx command fails | Report specific error — stop (no retry) |
| SKILL.md missing or malformed | Warn about specific issue — stop |
| `setup.sh` fails | Report error, check plugin.json and directory structure — stop |
| Push fails | Report error, suggest `git pull --rebase` then retry |

## Anti-patterns

- **Installing without checking for duplicates.** Always check first — because overwriting an existing skill without consent can destroy customizations.
- **Skipping STRUCTURE.md update.** The skill exists on disk but is invisible to repo navigation — because STRUCTURE.md is the directory index.
- **Leaving npx artifacts in the project.** `.agents/`, empty `.claude/skills/`, `skills-lock.json` pollute the working directory — because they are transient install artifacts, not project files.
- **Pushing without verifying.** Skipping verification means broken symlinks or missing entries get committed — because these are hard to diagnose after pushing.
- **Invoking other skills mid-install.** README generation and push must be done inline — because cross-skill invocations create hidden dependencies that break isolation.

## Guidelines

- **Local is simple, global is thorough.** Local install is a single npx command. Global install includes full registration (symlink, STRUCTURE.md, READMEs, push) — because global skills are shared infrastructure that must be properly indexed.

- **Verify before push.** The end-to-end verification gate catches problems that are hard to diagnose after pushing — because a broken symlink or missing STRUCTURE.md entry silently breaks skill discovery.

- **Clean up after yourself.** npx leaves artifacts (`.agents/`, `skills-lock.json`) that don't belong in the project — because install artifacts are transient and shouldn't persist.

- **Self-contained execution.** All steps (README generation, STRUCTURE.md update, push) happen inline — because depending on other skills creates hidden coupling.
