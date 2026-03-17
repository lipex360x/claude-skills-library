# create-hook

> Guide the user through creating or improving Claude Code hooks — from event selection to script writing and registration.

Step-by-step guide for building Claude Code hooks. Hooks are bash scripts (or prompts) triggered by events — deterministic, zero-fail-rate enforcement that runs outside the LLM.

## Usage

```text
/create-hook
```

> [!TIP]
> Also activates when you say "create a hook", "new hook", "add a hook", "improve a hook", or mention event names like "PostToolUse", "PreToolUse", "PreCompact", "SessionStart".

## How it works

1. **Understand the intent** — Asks what should happen, when it should trigger, and whether it should block or inform
2. **Choose the event** — Matches intent to the right hook event (PreToolUse, PostToolUse, PreCompact, Stop, SessionStart, etc.)
3. **Choose the type** — Defaults to `command` (bash, 0 tokens) unless LLM reasoning is genuinely needed (`prompt`)
4. **Write the matcher** — Configures which events trigger the hook with appropriate filtering
5. **Write the script** — Follows a structured template with `set -e`, stdin parsing, and concise output
6. **Determine location** — Local (project) or global (`.brain/`)
7. **Register in settings.json** — Adds the hook to the appropriate config file
8. **Test and review** — Validates against a checklist before finalizing

## Directory structure

```text
create-hook/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-hook
```
