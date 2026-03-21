# Audit Report: create-hook

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 9 triggers: "create a hook", "new hook", "add a hook", "improve a hook", "PostToolUse", "PreToolUse", "PreCompact", "SessionStart", "event-driven automation" |
| 2 | WHAT + WHEN | ✅ | What: "Guide through creating or improving Claude Code hooks". When: mentions hook events or wants automation |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "hook."` |
| 4 | Under 500 lines | ✅ | 191 lines |
| 5 | Imperative form | ✅ | "Ask the user", "Match the user's intent", "Follow this template structure" |
| 6 | Constraints reasoned | ✅ | "bash hooks are deterministic (0% fail rate) and cost nothing" (line 51), "non-zero exit on PreToolUse blocks the tool call" (line 99) |
| 7 | Numbered steps | ✅ | 9 numbered steps |
| 8 | Output formats defined | ✅ | Script template (lines 74-95), settings.json format (lines 128-144) |
| 9 | Input contract | ⚠️ | Step 1 asks clarifying questions but no formal input contract (required: intent; optional: event, type, location) |
| 10 | Quality repeated at key points | ✅ | Script rules reinforce quality (lines 97-104), review checklist (step 9), decision guide (lines 39-42) |
| 11 | Anti-patterns named | ✅ | 6 anti-patterns with reasoning (lines 186-191): side effects, broad matchers, prompt for deterministic, accidental non-zero exit, chatty output, hardcoded paths |
| 12 | Refinement step | ✅ | Step 9 is a full review checklist with 9 items. "Present the review to the user before writing the file." |
| 13 | Error handling | ✅ | "Graceful degradation" (line 104), "exit 0 silently" for missing dependencies, guards against accidental blocking |
| 14 | Standard layout | ✅ | SKILL.md + README. At 191 lines, no references needed |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ✅ | No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set |

## Score: 15/16

## Priority fixes (ordered by impact)

1. **Input contract** — Add a brief section listing required input (what the hook should do) vs optional inputs (event, type, location) with validation rules (e.g., event must be one of the listed events).
