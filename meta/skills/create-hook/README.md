# create-hook

> Guide the user through creating or improving Claude Code hooks — from choosing the right event to writing the script and registering in settings.json.

End-to-end factory for Claude Code hooks. Covers all 9 hook events (PreToolUse, PostToolUse, PreCompact, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, Notification), both hook types (command and prompt), and both scopes (local project and global .brain/). Defaults to `command` type because bash hooks are deterministic (0% fail rate) and cost zero tokens.

## Usage

```text
/create-hook
```

> [!TIP]
> Also activates when you say "create a hook", "new hook", "add a hook", "improve a hook", mention "PostToolUse", "PreToolUse", "PreCompact", "SessionStart", or want event-driven automation.

### Examples

```text
/create-hook                                    # interactive — asks what the hook should do
```

Also triggered by natural language:

```text
"add a hook that reminds me to update issues"   # describes intent directly
"create a PreToolUse hook for Bash"             # specifies event and matcher
```

## How it works

1. **Understand the intent** — Clarifies what the hook should do (remind, validate, block, inject context), when it triggers, and whether it blocks or informs
2. **Choose the event** — Maps intent to the right hook event using a decision guide (prevent = PreToolUse, react = PostToolUse, context at start = SessionStart, capture before loss = PreCompact)
3. **Choose the hook type** — Defaults to `command` (bash, 0 tokens); uses `prompt` only when LLM reasoning is genuinely needed
4. **Write the matcher** — Configures event filtering (tool name for Pre/PostToolUse, empty string for all events of that type)
5. **Write the script** — Creates the bash script following a standard template: `set -e`, stdin JSON parsing via `jq`, filter logic, action, and output message
6. **Determine location** — Asks local (`.claude/hooks/`) or global (`~/.brain/hooks/templates/`) via AUQ
7. **Register in settings.json** — Adds the hook entry to the appropriate settings file with event, matcher, command, and timeout
8. **Test the hook** — Verifies correct firing, no false positives, and clean exit codes
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
