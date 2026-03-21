# Audit Report: capture-analysis

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 7 trigger phrases including Portuguese ("analisa isso", "estuda isso"), plus "lessons learned" |
| 2 | WHAT + WHEN | ✅ | What: "Capture skill gaps, workflow frictions, and pattern improvements". When: trigger phrases + "wants to record a finding" |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "analysis."` |
| 4 | Under 500 lines | ✅ | 98 lines |
| 5 | Imperative form | ✅ | "Check if", "Read it", "Append the entry", "Tell the user" |
| 6 | Constraints reasoned | ✅ | "this file contains session-specific learnings, not project code" (line 18), "Mixed entries are harder to implement" (line 88) |
| 7 | Numbered steps | ✅ | 5 numbered steps + Remove entry flow |
| 8 | Output formats defined | ✅ | Entry template (lines 47-62) with clear markdown structure |
| 9 | Input contract | ⚠️ | Handles `$ARGUMENTS` for "remove N" but no explicit required/optional section or validation rules for the main input |
| 10 | Quality repeated at key points | ✅ | Guidelines section reinforces project-agnostic, one-concern-per-entry, actionable proposals |
| 11 | Anti-patterns named | ✅ | 4 anti-patterns explicitly listed (lines 94-98): project-specific content, vague entries, duplicates, one-time fixes |
| 12 | Refinement step | ✅ | Stale entry awareness (line 92) acts as implicit review; dedup check before writing (line 40) |
| 13 | Error handling | ⚠️ | Handles missing file and vague input, but no handling for malformed `remove N` (e.g., N out of range) |
| 14 | Standard layout | ⚠️ | SKILL.md + README only. No references/ or templates/ — the entry template is inline, which works at 98 lines but could be extracted |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ✅ | No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set |

## Score: 14/16

## Priority fixes (ordered by impact)

1. **Input contract** — Add explicit validation for `remove N` argument (what if N is out of range, not a number, or file has no entries). Add a brief input contract section listing required vs optional inputs.
2. **Error handling for remove** — Specify behavior when N doesn't exist or file is empty.
