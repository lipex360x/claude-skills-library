# Audit Report: list-backlog

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 5 trigger phrases: "list backlog", "show backlog", "backlog list", "what's in the backlog" |
| 2 | Description: WHAT + WHEN? | ✅ | "List open backlog issues with table summary and size sorting" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'backlog'" |
| 4 | Body: under 500 lines? | ✅ | 93 lines |
| 5 | Body: imperative form? | ✅ | "Run", "Store", "Find", "Query", "Present" |
| 6 | Body: constraints reasoned? | ⚠️ | Sorting logic is defined but not reasoned (why these sort orders?). Dependency detection logic lacks reasoning for the chosen patterns |
| 7 | Body: numbered steps? | ✅ | 5 numbered steps |
| 8 | Body: output formats defined? | ✅ | Step 5 defines exact table format with markdown links, status column, and footer suggestion |
| 9 | Body: input contract? | ✅ | Lines 15-19: "/list-backlog [asc|desc]" with behavior for each option and default |
| 10 | Quality: repeated at key points? | ❌ | No quality reminders. Output format defined once but no emphasis on accuracy of dependency detection or data freshness |
| 11 | Quality: anti-patterns named? | ❌ | No anti-patterns section. Missing: stale board data, false positive blockers, incorrect size parsing |
| 12 | Quality: refinement step? | N/A | Read-only skill — displays data, doesn't create artifacts requiring refinement |
| 13 | Quality: error handling? | ⚠️ | Step 2 handles missing board ("say so and stop"). Step 3 handles empty backlog. No handling for: gh CLI errors, malformed issue bodies, board query timeouts |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference file |
| 20 | Structure: large refs have TOC? | ✅ | project-board-operations.md has clear sections |
| 21 | Structure: self-contained? | ⚠️ | Line 93 references `/start-issue` by name in the footer suggestion. Acceptable as UX guidance (not a dependency), but couples the display text to another skill's existence |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 13/20

## Priority fixes (ordered by impact)

1. **Add anti-patterns section** — Name: false-positive blocker detection (topical overlap vs real dependency), stale board data shown as current, showing closed issues as blockers, truncating long titles in table.
2. **Add quality emphasis** — At Step 4 dependency detection: "Only flag direct, clear dependencies — not loose topical overlap. Verify referenced issues are actually open before flagging as blocked."
3. **Improve error handling** — Add graceful degradation for gh CLI failures and malformed issue bodies (skip the issue with a note rather than failing entirely).
4. **Add constraints reasoning** — Explain why size-based sorting exists (helps prioritize by effort) and why dependency detection uses those specific patterns (canonical format from add-backlog/close-pr).
