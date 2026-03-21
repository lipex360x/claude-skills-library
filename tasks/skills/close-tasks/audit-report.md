# Audit Report: close-tasks

Plugin: tasks
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Multiple triggers: "close tasks", "stop tracking", "tv close", "hide tasks" with "even if" pattern |
| 2 | WHAT + WHEN in description? | ✅ | WHAT: "Close the task visibility board and stop task tracking". WHEN: trigger phrases listed |
| 3 | "Even if" pattern? | ✅ | "even if they don't explicitly say 'close'" |
| 4 | Under 500 lines? | ✅ | 12 lines |
| 5 | Imperative form? | ✅ | "Delete all tasks", "Set task-visibility.always-open to false", "Confirm briefly" |
| 6 | Constraints reasoned? | N/A | No constraints needed |
| 7 | Numbered steps? | ✅ | 3 numbered steps |
| 8 | Output formats defined? | ⚠️ | "Confirm briefly that the board is closed" — minimal but adequate |
| 9 | Input contract? | N/A | No input needed |
| 10 | Quality repeated at key points? | N/A | Too simple |
| 11 | Anti-patterns named? | ❌ | Missing — should note: "Don't close without confirming if there are in-progress tasks" |
| 12 | Refinement step? | ❌ | No verification that config was actually updated |
| 13 | Error handling patterns? | ❌ | No handling for: config file not found, already closed, tasks with in-progress status |
| 14 | Invoked with realistic input? | N/A | Audit scope — not tested |
| 15 | Activation tested? | N/A | Audit scope — not tested |
| 16 | Failure modes checked? | N/A | Audit scope — not tested |
| 17 | Subagents — context complete? | N/A | No subagents |
| 18 | Standard layout? | ✅ | SKILL.md + README.md |
| 19 | References one level deep? | N/A | No references |
| 20 | Large refs have TOC? | N/A | No references |
| 21 | Self-contained? | ⚠️ | References `~/.brain/config/behavior.config.json` — external dependency, but necessary for function |
| 22 | README generated? | ✅ | Present and well-structured |
| 23 | CLAUDE.md compliance? | ✅ | Follows all rules |

## Score: 7/11

(Excluding N/A items)

## Priority fixes (ordered by impact)

1. **Add safety check for in-progress tasks** — Before closing, warn if there are in-progress tasks that will be deleted. Use AskUserQuestion to confirm
2. **Add error handling** — Handle config file not found, already-closed board
3. **Add anti-pattern** — "Don't silently delete in-progress tasks without warning the user"
4. **Add verification step** — Read config after update to confirm the change took effect
