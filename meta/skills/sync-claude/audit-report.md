# Audit Report: sync-claude

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 10 triggers including Portuguese: "sync claude", "sync skills", "sync brain", "pull skills", "update claude code", "update skills", "atualiza skills", "sincroniza" |
| 2 | WHAT + WHEN | ✅ | What: "Synchronize the Claude Code environment across machines". When: user wants to bring environment up to date |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "sync."` |
| 4 | Under 500 lines | ✅ | 121 lines |
| 5 | Imperative form | ✅ | "Verify both directories exist", "Check for uncommitted changes", "Run setup.sh", "Compare skills-library" |
| 6 | Constraints reasoned | ✅ | "Data loss on a config repo is painful because there's no easy recovery path" (line 117), "Stash is safe, reset is not" (line 118), "a partial sync is better than no sync" (line 121) |
| 7 | Numbered steps | ✅ | 6 numbered steps |
| 8 | Output formats defined | ✅ | Report format in step 6 (lines 98-111) with clear structure |
| 9 | Input contract | ✅ | `allowed-tools` defined. External state table (lines 12-17) clearly documents required resources |
| 10 | Quality repeated at key points | ✅ | Guidelines reinforce safety at every decision point (lines 116-121) |
| 11 | Anti-patterns named | ⚠️ | Guidelines implicitly name anti-patterns (force-push, reset, auto-fix) but no explicit "Anti-patterns" section with structured entries |
| 12 | Refinement step | ⚠️ | Step 5 (verify sync) acts as verification but doesn't loop back — discrepancies are reported but not resolved |
| 13 | Error handling | ✅ | Excellent — every step has AskUserQuestion fallbacks: missing dirs (step 1), dirty trees (step 2), pull failures (step 3). Options always include abort/skip |
| 14 | Standard layout | ✅ | SKILL.md + README |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ✅ | No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set, `allowed-tools` defined |

## Score: 14/16

## Priority fixes (ordered by impact)

1. **Anti-patterns section** — Convert implicit anti-patterns in guidelines to an explicit section: force-pulling, resetting dirty trees, auto-fixing discrepancies, running setup.sh before pulling.
2. **Refinement step** — After reporting discrepancies, offer actionable resolution options (re-run setup.sh, manually fix orphaned symlinks) instead of just listing them.
