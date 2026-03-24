# create-hook

> Guide the user through creating or improving Claude Code hooks — from choosing the right event to writing the script and registering in settings.json.

Step-by-step guide for building Claude Code hooks. Hooks are bash scripts (or prompts) triggered by events like PreToolUse, PostToolUse, PreCompact, and SessionStart — deterministic, zero-fail-rate enforcement that runs outside the LLM.

## Usage

```text
/create-hook
```

> [!TIP]
> Also activates when you say "create a hook", "new hook", "add a hook", "improve a hook", mention "PostToolUse", "PreToolUse", "PreCompact", "SessionStart", or want event-driven automation.

## How it works

1. **Understand the intent** — Clarifies what the hook should do, when it triggers, and whether it blocks or informs
2. **Choose the event** — Maps intent to the right hook event (PreToolUse, PostToolUse, PreCompact, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, Notification)
3. **Choose the hook type** — Defaults to `command` (bash, 0 tokens); uses `prompt` only when LLM reasoning is needed
4. **Write the matcher** — Configures event filtering (tool name, empty string for all)
5. **Write the script** — Creates the bash script with `set -e`, stdin parsing, filter logic, and concise output
6. **Determine location** — Asks local (project) or global (.brain/) via AUQ
7. **Register in settings.json** — Adds the hook entry to the appropriate settings file
8. **Test the hook** — Verifies correct firing, no false positives, clean exit
9. **Review** — Validates against a 9-point checklist before finalizing
10. **Report** — Shows hook name, event, type, location, script path, and registration status

## Directory structure

```text
create-hook/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-hook
```
