---
name: create-hook
description: >-
  Guide the user through creating or improving Claude Code hooks — from choosing
  the right event to writing the script and registering in settings.json. Use
  this skill when the user mentions "create a hook", "new hook", "add a hook",
  "improve a hook", "PostToolUse", "PreToolUse", "PreCompact", "SessionStart",
  or wants event-driven automation — even if they don't explicitly say "hook."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - AskUserQuestion
---

# Create Hook

Step-by-step guide for building Claude Code hooks. Hooks are bash scripts (or prompts) triggered by events — deterministic, zero-fail-rate enforcement that runs outside the LLM.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `intent` | $ARGUMENTS or conversation | yes | Description of what the hook should do and when | AUQ: "What should the hook do, and when should it trigger?" |
| `event` | $ARGUMENTS or conversation | no | One of: PreToolUse, PostToolUse, PreCompact, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, Notification | Derive from intent in Step 2 |
| `type` | $ARGUMENTS or conversation | no | One of: command, prompt | Default to command (Step 3) |
| `location` | $ARGUMENTS or conversation | no | One of: local, global | AUQ with options in Step 6 |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Hook script | `.claude/hooks/<name>.sh` (local) or `~/.brain/hooks/templates/<name>.sh` (global) | yes | Bash script |
| Settings registration | `.claude/settings.json` (local) or `~/.brain/config/settings.json` (global) | yes | JSON |
| STRUCTURE.md update | `~/.brain/STRUCTURE.md` (global only) | yes | Markdown |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Local settings | `.claude/settings.json` | R/W | JSON |
| Global settings | `~/.brain/config/settings.json` | R/W | JSON |
| Hook scripts dir (local) | `.claude/hooks/` | W | Bash |
| Hook templates dir (global) | `~/.brain/hooks/templates/` | W | Bash |
| Structure file | `~/.brain/STRUCTURE.md` | R/W | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. User provided intent (what + when) → if missing: AUQ with concrete examples — stop if no response.
2. If location is global: verify `~/.brain/config/settings.json` exists → if missing: "Global settings not found. Run sync-claude first." — stop.
3. If location is local: verify `.claude/` directory exists → if missing: create it.

</pre_flight>

## Steps

### 1. Understand the intent

Clarify with the user:
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

**Default to `command`** — bash hooks are deterministic (0% fail rate) and cost nothing. Use `prompt` only when the hook genuinely needs LLM reasoning.

### 4. Write the matcher

The matcher filters which events trigger the hook:
- **Empty string `""`** — match all events of this type
- **Tool name** — for PreToolUse/PostToolUse: `"Bash"`, `"Edit"`, `"Write"`

For fine-grained filtering, use a broad matcher and filter inside the script:

```bash
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
- **Always `exit 0` for no-ops** — a non-zero exit on PreToolUse blocks the tool call.
- **Read stdin once** — `INPUT=$(cat)` captures the JSON input. Parse with `jq`.
- **Output = message** — stdout becomes a message Claude sees. Keep it concise.
- **No side effects** — hooks inform and remind. Don't modify files, commit, or push.
- **Idempotent** — running twice should produce the same result or gracefully skip.
- **Graceful degradation** — if a required file or tool is missing, `exit 0` silently.

### 6. Determine location

Use `AskUserQuestion` with options `["Local (this project)", "Global (.brain/)"]`.

- **Local:** Write script to `.claude/hooks/<name>.sh`. Register in `.claude/settings.json`.
- **Global:** Write script to `~/.brain/hooks/templates/<name>.sh`. Register in `~/.brain/config/settings.json`. Update `~/.brain/STRUCTURE.md`.

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

If the event already has hooks registered, append to the existing array — don't overwrite.

### 8. Test the hook

Trigger the event manually and verify:
- The hook fires on the right events
- The hook stays silent on unrelated events (no false positives)
- The output message is concise and actionable
- The script exits cleanly (no errors, no hangs)

### 9. Review

Validate before finalizing:

- [ ] Event matches the intent?
- [ ] Type is `command` unless LLM reasoning is genuinely needed?
- [ ] Matcher is specific enough?
- [ ] Script uses `set -e` and handles missing dependencies gracefully?
- [ ] Output is concise — one clear message, not a wall of text?
- [ ] Script is idempotent?
- [ ] Registered in the correct settings.json?
- [ ] No side effects — hook informs, doesn't act?
- [ ] STRUCTURE.md updated (for global hooks)?

Present the review to the user before writing the file.

### 10. Report

<report>

Present concisely:
- **Hook:** name, event, type, location
- **Script:** path to the created script
- **Registration:** settings.json path updated
- **Audit results:** self-audit + review checklist summary
- **Errors:** issues encountered (or "none")

</report>

## Next action

Test the hook by triggering its event in a live session. If it needs adjustment, describe what changed and re-run `/create-hook`.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — intent clarified, location determined
2. **Steps completed?** — script written, registered, tested
3. **Output exists?** — hook script at declared path, settings.json updated
4. **Review passed?** — all 9 review checks green
5. **Anti-patterns clean?** — no side effects, no broad matchers, no chatty output
6. **STRUCTURE.md updated?** — for global hooks only

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Script correctness?** — `set -e`, `INPUT=$(cat)`, proper exit codes
2. **Matcher specificity?** — not triggering on unrelated events
3. **Registration valid?** — JSON structure matches settings.json schema
4. **Idempotent?** — running the hook twice produces same result

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `jq` not available | Suggest install: `brew install jq` → stop |
| Settings.json malformed | Report parse error with path → stop |
| Hook script fails test | Show error output, suggest fix → do not register |
| Event name invalid | Show valid events table → AUQ to re-select |
| Permission denied on script | `chmod +x` and retry |

## Anti-patterns

- **Side effects in hooks.** Hooks should inform, not act. A hook that runs `git push` or edits files creates unpredictable behavior — because the user didn't ask for it and it can't be reviewed before execution.
- **Overly broad matchers.** A PostToolUse hook with `matcher: ""` that doesn't filter internally fires on every tool call — because thousands of triggers per session create noise and waste.
- **Prompt hooks for deterministic logic.** If the check is "does this file exist?", use bash (0 tokens) — because prompt hooks cost tokens and add latency for no benefit.
- **Non-zero exit by accident.** On PreToolUse, a non-zero exit blocks the tool call — because missing `|| exit 0` guards cause accidental blocking of legitimate operations.
- **Chatty output.** Hooks run frequently. A 10-line message after every tool call creates noise — because concise 1-3 line messages are actionable while walls of text are ignored.
- **Hardcoded absolute paths.** Use `$HOME/.brain/` or relative paths — because hardcoded paths break when the hook runs on a different machine.

## Guidelines

- **Default to `command` type.** Bash hooks are deterministic (0% fail rate) and cost nothing. Only use `prompt` when the hook genuinely needs LLM reasoning — because unnecessary prompt hooks waste tokens and add latency.

- **Hook vs command vs skill.** Use a hook when enforcement must happen automatically every time (event-driven, zero-fail-rate). Use a command when the user explicitly triggers with `/name`. Use a skill for multi-step workflows with references — because choosing the wrong mechanism leads to either missed enforcement or unnecessary complexity.

- **Inform, don't act.** Hooks output reminders and status. They do not modify files, commit, or push — because side effects in hooks are invisible to the user and can't be reviewed before execution.

- **Test before registering.** Always verify the hook fires correctly and stays silent on unrelated events — because a registered hook that misfires disrupts every session until someone debugs it.
