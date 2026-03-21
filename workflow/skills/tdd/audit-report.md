# Audit Report: tdd

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 7 trigger phrases ("tdd", "test first", "red green refactor", "write tests", "test driven", "let's TDD this", plus natural description) |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Execute Test-Driven Development with strict red-green-refactor discipline") + multiple trigger contexts |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'TDD'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 132 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Understand what to build", "Plan behaviors to test", "Design interface for testability", "Execute the loop" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Constraints well-reasoned throughout: "Horizontal slicing produces tests that verify imagined behavior" (line 110), "Mocking internal collaborators couples tests to implementation" (line 114), "A test that checks 5 things is really 5 tests crammed together" (line 116) |
| 7 | SKILL.md: numbered steps | ✅ pass | 5 numbered steps with clear headers plus RED/GREEN/REFACTOR sub-steps |
| 8 | SKILL.md: output formats | ✅ pass | Step 2 shows behavior list format, Step 5 defines verification report format (tests added, code modified, refactors, skipped behaviors) |
| 9 | SKILL.md: input contract | ⚠️ partial | Step 1 mentions "$ARGUMENTS" but no formal input contract table. Missing validation rules for when arguments are invalid or ambiguous |
| 10 | Quality: repeated at key points | ✅ pass | TDD discipline reinforced in Steps (RED/GREEN/REFACTOR), Guidelines (7 items), and Anti-patterns (8 items) |
| 11 | Quality: anti-patterns named | ✅ pass | 8 specific anti-patterns listed (lines 124-132): horizontal slicing, testing private methods, mocking internals, HOW vs WHAT, external verification, skipping RED, refactoring while RED, speculative features |
| 12 | Quality: refinement step | ✅ pass | REFACTOR phase is explicitly the refinement step after each GREEN, with guidelines on what to look for |
| 13 | Quality: error handling | ⚠️ partial | Handles test-passes-immediately case (line 67: "investigate before proceeding") and test-fails-after-GREEN (line 79: "fix implementation, not the test"). Missing handling for framework not found, test runner errors, or build failures |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/tdd-methodology.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ⚠️ partial | No `allowed-tools` in frontmatter. The skill uses Bash (test runners), Read (codebase analysis), Edit (writing code/tests) but doesn't declare them |

## Score: 15/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add `allowed-tools` to frontmatter** — Skill uses Bash, Read, Edit, and potentially Grep but none are declared.
2. **Add formal input contract table** — $ARGUMENTS is referenced but lacks structured validation (type, required/optional, on-invalid behavior).
3. **Add error handling for tool/framework failures** — Missing guidance for when the test runner isn't found, build fails, or the test framework is unknown.

## Recommended action

- [ ] Run `/create-skill tdd` with this report to apply fixes
