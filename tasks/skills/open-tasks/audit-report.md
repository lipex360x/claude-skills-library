# Audit Report: open-tasks

Plugin: tasks
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Multiple triggers: "open tasks", "show tasks", "tv open", "start tracking" with "even if" pattern |
| 2 | WHAT + WHEN in description? | ✅ | WHAT: "Reopen the task visibility board and resume task tracking". WHEN: trigger phrases listed |
| 3 | "Even if" pattern? | ✅ | "even if they don't explicitly say 'open'" |
| 4 | Under 500 lines? | ✅ | 12 lines |
| 5 | Imperative form? | ✅ | "Set task-visibility.always-open to true", "Resume creating and tracking tasks", "Confirm briefly" |
| 6 | Constraints reasoned? | N/A | No constraints needed |
| 7 | Numbered steps? | ✅ | 3 numbered steps |
| 8 | Output formats defined? | ⚠️ | "Confirm briefly that the board is open" — minimal but adequate |
| 9 | Input contract? | N/A | No input needed |
| 10 | Quality repeated at key points? | N/A | Too simple |
| 11 | Anti-patterns named? | ❌ | Missing — could note: "Don't recreate previously deleted tasks — only enable tracking for new ones" |
| 12 | Refinement step? | ❌ | No verification that config was actually updated |
| 13 | Error handling patterns? | ❌ | No handling for: config file not found, already open |
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

1. **Add error handling** — Handle config file not found, already-open board (idempotent response)
2. **Add verification step** — Read config after update to confirm the change took effect
3. **Add anti-pattern** — "Don't recreate previously deleted tasks — only enable tracking for new work"
