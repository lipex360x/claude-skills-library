# sync-claude

Synchronize the Claude Code environment (skills-library + .brain) across machines in one command.

## What it does

- Pulls latest from both `skills-library` and `.brain` git repos
- Rebuilds all symlinks via `setup.sh`
- Verifies the installation and reports discrepancies
- Handles dirty working trees and diverged branches gracefully

## Install

**Global (recommended):**

```bash
npx @anthropic-ai/claude-code-skills add lipex360x/claude-skills-library/meta/skills/sync-claude -a claude-code -y
```

**Local (project-only):**

```bash
npx @anthropic-ai/claude-code-skills add lipex360x/claude-skills-library/meta/skills/sync-claude --copy -a claude-code -y
```

## Usage

```
/sync-claude
```

Or use natural language:
- "sync my skills"
- "pull latest skills"
- "update claude code environment"
- "sync brain"

## Triggers

Activates when the user mentions syncing, pulling, or updating the Claude Code environment, skills, or brain config — even without saying "sync" explicitly.

## Plugin

`meta` — alongside `/install-skill`, `/uninstall-skill`
