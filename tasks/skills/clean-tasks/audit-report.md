# Audit Report: clean-tasks

Plugin: tasks
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Multiple triggers: "clean tasks", "remove done tasks", "clear completed", "tv clean" with "even if" pattern |
| 2 | WHAT + WHEN in description? | ✅ | WHAT: "Remove completed tasks from the task visibility board". WHEN: trigger phrases listed |
| 3 | "Even if" pattern? | ✅ | "even if they don't explicitly say 'clean'" |
| 4 | Under 500 lines? | ✅ | 12 lines — extremely concise |
| 5 | Imperative form? | ✅ | "Use TaskList to find", "Use TaskUpdate with status deleted", "Confirm briefly" |
| 6 | Constraints reasoned? | N/A | No constraints needed for this simple skill |
| 7 | Numbered steps? | ✅ | 3 numbered steps |
| 8 | Output formats defined? | ⚠️ | "Confirm briefly how many tasks were removed" — minimal but adequate for scope |
| 9 | Input contract? | N/A | No input needed — operates on current task list |
| 10 | Quality repeated at key points? | N/A | Too simple to need quality repetition |
| 11 | Anti-patterns named? | ❌ | Missing — should note: "Don't delete pending or in-progress tasks" |
| 12 | Refinement step? | ❌ | No verification after deletion — should list remaining tasks |
| 13 | Error handling patterns? | ❌ | No handling for "no completed tasks found" case |
| 14 | Invoked with realistic input? | N/A | Audit scope — not tested |
| 15 | Activation tested? | N/A | Audit scope — not tested |
| 16 | Failure modes checked? | N/A | Audit scope — not tested |
| 17 | Subagents — context complete? | N/A | No subagents |
| 18 | Standard layout? | ✅ | SKILL.md + README.md — appropriate for simple skill |
| 19 | References one level deep? | N/A | No references needed |
| 20 | Large refs have TOC? | N/A | No references |
| 21 | Self-contained? | ✅ | No cross-skill dependencies |
| 22 | README generated? | ✅ | Present and well-structured |
| 23 | CLAUDE.md compliance? | ✅ | Follows all rules |

## Score: 8/11

(Excluding N/A items)

## Priority fixes (ordered by impact)

1. **Add error handling for empty case** — Handle "no completed tasks found" — confirm with "No completed tasks to clean"
2. **Add refinement step** — After deletion, briefly list remaining tasks so user sees current state
3. **Add anti-pattern** — "Don't delete pending or in-progress tasks — only completed ones"
