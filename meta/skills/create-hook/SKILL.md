---
name: create-hook
description: Guide the user through creating or improving Claude Code hooks — from choosing the right event to writing the script and registering in settings.json. Use this skill when the user mentions "create a hook", "new hook", "add a hook", "improve a hook", "PostToolUse", "PreToolUse", "PreCompact", "SessionStart", or wants event-driven automation — even if they don't explicitly say "hook."
user-invocable: true
---

# Create Hook

Step-by-step guide for building Claude Code hooks. Hooks are bash scripts (or prompts) triggered by events — deterministic, zero-fail-rate enforcement that runs outside the LLM.

## Input contract

- **Required:** intent — what the hook should do (the action and when it should fire)
- **Optional:** event (must be one of: `PreToolUse`, `PostToolUse`, `PreCompact`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`, `Notification`), type (`command` or `prompt`), location (`local` or `global`)

If the user provides only the intent, derive the remaining inputs through the process steps below.

## Process

### 1. Understand the intent

Ask the user:
- What should happen? (the action — remind, validate, block, inject context)
- When should it trigger? (the event — after a commit, before compaction, at session start)
- Should it block or just inform? (blocking = non-zero exit code)

Use `AskUserQuestion` with concrete options when clarifying ambiguous decisions.

### 2. Choose the event

Match the user's intent to the right hook event:

| Event | When it fires | Common use cases |
|-------|--------------|------------------|
| `PreToolUse` | Before a tool executes | Validate inputs, block dangerous commands, require confirmation |
| `PostToolUse` | After a tool completes | Post-commit reminders, result validation, logging |
| `PreCompact` | Before context compaction | Capture data from full context (voice analysis, summaries) |
| `Stop` | When Claude finishes responding | Final checks, cleanup reminders |
| `SubagentStop` | When a subagent finishes | Aggregate results, trigger follow-ups |
| `SessionStart` | At conversation start | Inject project context, load state, display status |
| `SessionEnd` | When conversation ends | Save state, cleanup |
| `UserPromptSubmit` | When user sends a message | Input preprocessing, routing |
| `Notification` | When a notification fires | Alert handling |

**Decision guide:**
- Need to **prevent** something? → `PreToolUse` (can block with non-zero exit)
- Need to **react** to something? → `PostToolUse` (inform after the fact)
- Need **context at start**? → `SessionStart`
- Need to **capture before context loss**? → `PreCompact`

### 3. Choose the hook type

| Type | When to use | Token cost |
|------|-------------|------------|
| `command` (bash script) | Deterministic logic, pattern matching, file checks | **0 tokens** |
| `prompt` (instruction text) | Needs LLM reasoning, content analysis, judgment calls | Variable |

**Default to `command`** — bash hooks are deterministic (0% fail rate) and cost nothing. Use `prompt` only when the hook genuinely needs LLM reasoning (e.g., "check if the code follows our style guide").

### 4. Write the matcher

The matcher filters which events trigger the hook. Format depends on the event:

- **Empty string `""`** — match all events of this type
- **Tool name** — for `PreToolUse`/`PostToolUse`: `"Bash"`, `"Edit"`, `"Write"`
- **Pattern** — match specific conditions in the script itself (via `jq` on stdin)

For fine-grained filtering, use a broad matcher and filter inside the script:

```bash
# Match all Bash calls, but only act on git commit
TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
[ "$TOOL" = "Bash" ] || exit 0
echo "$INPUT" | jq -r '.tool_input.command // ""' | grep -q "git commit" || exit 0
```

### 5. Write the script

Follow this template structure:

```bash
#!/bin/bash
# <Event> Hook — <one-line description>
# Matches: <what this hook triggers on>
# Returns: <what Claude sees in the output>
set -e

INPUT=$(cat)

# --- Filter (skip if not relevant) ---
# [matcher logic here — exit 0 early if not applicable]

# --- Action ---
# [the actual work — file checks, pattern matching, context gathering]

# --- Output (what Claude sees) ---
cat <<'MSG'
[Message to display]
MSG

exit 0
```

**Script rules:**
- **Always `set -e`** — fail fast on errors.
- **Always `exit 0` for no-ops** — a non-zero exit on PreToolUse blocks the tool call. Only return non-zero intentionally to block.
- **Read stdin once** — `INPUT=$(cat)` captures the JSON input. Parse with `jq`.
- **Output = message** — everything sent to stdout becomes a message Claude sees. Keep it concise.
- **No side effects** — hooks inform and remind. Don't modify files, commit, or push from a hook. If the hook needs to trigger an action, output a reminder and let Claude do it.
- **Idempotent** — running twice should produce the same result or gracefully skip.
- **Graceful degradation** — if a required file or tool is missing, `exit 0` silently. Don't crash on missing dependencies.

**Input JSON format (PreToolUse/PostToolUse):**

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'feat: add auth'"
  }
}
```

### 6. Determine location

Use `AskUserQuestion` with options `["Local (this project)", "Global (.brain/)"]`.

- **Local:** Write script to `.claude/hooks/<name>.sh` in the project. Register in `.claude/settings.json`.
- **Global:** Write script to `~/www/claude/.brain/hooks/templates/<name>.sh`. Register in `~/www/claude/.brain/config/settings.json`. Update `~/www/claude/.brain/STRUCTURE.md`.

### 7. Register in settings.json

Add the hook to the appropriate `settings.json`:

```json
{
  "hooks": {
    "<Event>": [
      {
        "matcher": "<matcher or empty string>",
        "hooks": [
          {
            "type": "command",
            "command": "bash <path-to-script>"
          }
        ]
      }
    ]
  }
}
```

**For global hooks:** use `~/.brain/hooks/templates/<name>.sh` in the command path.
**For local hooks:** use relative path `.claude/hooks/<name>.sh`.

If the event already has hooks registered, append to the existing array — don't overwrite.

### 8. Test the hook

Trigger the event manually and verify:
- The hook fires on the right events
- The hook stays silent on unrelated events (no false positives)
- The output message is concise and actionable
- The script exits cleanly (no errors, no hangs)

### 9. Review

Validate before finalizing:

- [ ] Event matches the intent? (prevention = PreToolUse, reaction = PostToolUse, etc.)
- [ ] Type is `command` unless LLM reasoning is genuinely needed?
- [ ] Matcher is specific enough? (not triggering on every Bash call when it should only match `git commit`)
- [ ] Script uses `set -e` and handles missing dependencies gracefully?
- [ ] Output is concise — one clear message, not a wall of text?
- [ ] Script is idempotent — running twice is harmless?
- [ ] Registered in the correct settings.json (local vs global)?
- [ ] No side effects — hook informs, doesn't act?
- [ ] STRUCTURE.md updated (for global hooks)?

Present the review to the user before writing the file.

## Hook vs Command vs Skill — when to use which

| Use a **hook** when... | Use a **command** when... | Use a **skill** when... |
|---|---|---|
| Must happen automatically, every time | User explicitly triggers with `/name` | Multi-step workflow with references |
| Event-driven (after commit, at start) | On-demand action | Needs LLM reasoning throughout |
| Zero-fail-rate enforcement needed | Single focused action | Coordinates subagents |
| Deterministic logic, no LLM needed | <30 lines of instructions | Should auto-trigger by description |

## Anti-patterns

- **Side effects in hooks.** Hooks should inform, not act. A hook that runs `git push` or edits files creates unpredictable behavior — the user didn't ask for it, and it can't be reviewed before execution.
- **Overly broad matchers.** A PostToolUse hook with `matcher: ""` that doesn't filter internally fires on every single tool call — thousands per session. Always filter to the specific tool and input pattern you care about.
- **Prompt hooks for deterministic logic.** If the check is "does this file exist?" or "does this string match?", use a bash script (0 tokens). Prompt hooks cost tokens and add latency. Reserve them for genuine judgment calls.
- **Non-zero exit by accident.** On `PreToolUse`, a non-zero exit **blocks the tool call**. Use `|| exit 0` guards generously to prevent accidental blocking. Only exit non-zero when you intentionally want to prevent the action.
- **Chatty output.** Hooks run frequently. A 10-line message after every `git commit` creates noise. Keep output to 1-3 lines — a clear reminder or status, not a tutorial.
- **Hardcoded absolute paths.** Use `$HOME/.brain/` or relative paths, not `/Users/someone/`.
