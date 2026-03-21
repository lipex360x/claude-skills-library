# Audit Report: close-pr

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 6 trigger phrases ("close pr", "merge pr", "merge pull request", "merge this", "land the pr", "finalize and merge") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Merge the open pull request... write implementation summary... move card to Done") + multiple triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'merge'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 228 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Find the PR", "Determine target branch", "Write implementation summary", "Merge the PR" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Target branch check explained ("not every project merges to main", line 228), ARCHITECTURE.md rationale ("This file carries context across issues", line 226), implementation summary rationale ("Six months from now, the issue is the first place someone looks", line 216) |
| 7 | SKILL.md: numbered steps | ✅ pass | 11 numbered steps (1-11) with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Step 3 shows detailed implementation summary markdown format, Step 11 defines concise report format |
| 9 | SKILL.md: input contract | ❌ fail | No input contract at all. No arguments section, no validation. The skill implicitly takes no arguments but should document that (or at minimum state it takes none) |
| 10 | Quality: repeated at key points | ✅ pass | Quality reinforced in steps (summary specificity, line 81), guidelines (6 items), and architectural update rationale |
| 11 | Quality: anti-patterns named | ⚠️ partial | Guidelines state what to do and not to do, but no explicit "anti-patterns" section. "Generic summaries ('improved the auth system') are useless" (line 81) is the closest, but anti-patterns are not systematically listed |
| 12 | Quality: refinement step | ⚠️ partial | No explicit refinement/polish step. The skill runs through steps sequentially with no user review gate. The implementation summary and ARCHITECTURE.md update are written and posted without user approval |
| 13 | Quality: error handling | ⚠️ partial | Step 1 handles "no open PR" case. Step 2 handles mismatched target branch. But: no handling for gh CLI failures, merge conflicts, failed project board operations, or missing milestone |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/project-board-operations.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | `allowed-tools: Bash, Read` declared, `disable-model-invocation: false` explicit, verb-subject naming |

## Score: 13/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add input contract** — Even if the skill takes no arguments, document it explicitly. Consider whether it should accept a PR number as optional input for cases where the user isn't on the correct branch.
2. **Add explicit anti-patterns section** — Quality guidelines exist but failure modes aren't systematically named. Examples: posting vague summaries, skipping ARCHITECTURE.md update on architectural changes, force-merging when checks fail.
3. **Add error handling for tool failures** — Missing graceful degradation for: merge conflicts, project board API failures, milestone API failures, gh CLI unavailability.
4. **Add refinement/approval gate** — The implementation summary is posted without user review. Consider adding a confirmation step before posting the comment (especially since it's public and permanent).

## Recommended action

- [ ] Run `/create-skill close-pr` with this report to apply fixes
