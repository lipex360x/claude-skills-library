# Audit Report: list-issues

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 5 trigger phrases: "list issues", "show issues", "what issues are open", "issues list" |
| 2 | Description: WHAT + WHEN? | ✅ | "List all open issues grouped by board column with priority sorting and next-issue suggestion" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'issues'" |
| 4 | Body: under 500 lines? | ✅ | 88 lines |
| 5 | Body: imperative form? | ✅ | "Run", "Store", "Find", "Query", "Fetch", "Present" |
| 6 | Body: constraints reasoned? | ⚠️ | Workflow order for grouping is defined (line 64) but not reasoned. Priority sorting within groups is stated but not explained (why P0 first?) |
| 7 | Body: numbered steps? | ✅ | 7 numbered steps |
| 8 | Body: output formats defined? | ✅ | Step 6 defines exact table format per status group. Step 7 defines "Suggested next" format |
| 9 | Body: input contract? | ⚠️ | No explicit input contract. No $ARGUMENTS parsing. Should state "no arguments — lists all open issues for the current repo" |
| 10 | Quality: repeated at key points? | ❌ | No quality reminders at any point |
| 11 | Quality: anti-patterns named? | ❌ | No anti-patterns section |
| 12 | Quality: refinement step? | N/A | Read-only skill — displays data |
| 13 | Quality: error handling? | ⚠️ | Step 2 handles missing board. No handling for: gh CLI errors, issues with no board items at all, repos with 100+ issues (limit 100 in query) |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference file |
| 20 | Structure: large refs have TOC? | ✅ | project-board-operations.md has clear sections |
| 21 | Structure: self-contained? | ✅ | No cross-skill references in the body. "Suggested next" is generic guidance |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 12/20

## Priority fixes (ordered by impact)

1. **Add anti-patterns section** — Name: showing Done/Cancelled issues as "open", false-positive blocker detection, suggesting blocked issues as "next", truncating output for large boards without pagination.
2. **Add input contract** — State explicitly: "No arguments. Lists all open issues for the current repo."
3. **Add quality emphasis** — At Step 7 (suggest next): "Never suggest a blocked issue. If all Ready/Todo/Backlog issues are blocked, say so explicitly instead of suggesting a blocked one."
4. **Improve error handling** — Handle: no open issues at all, limit of 100 issues (warn user if truncated), gh CLI failures.
5. **Add constraints reasoning** — Explain workflow column order (matches natural issue lifecycle), priority sorting rationale (critical first so user sees highest priority immediately).
