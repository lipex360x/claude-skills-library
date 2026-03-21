# Audit Report: tdd

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 6 trigger phrases: "tdd", "test first", "red green refactor", "write tests", "test driven", "let's TDD this" |
| 2 | Description: WHAT + WHEN? | ✅ | "Execute Test-Driven Development with strict red-green-refactor discipline. Guides the agent through vertical slices" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'TDD'" |
| 4 | Body: under 500 lines? | ✅ | 132 lines |
| 5 | Body: imperative form? | ✅ | "Parse", "Read the codebase", "List the behaviors", "Write the test first", "Implement just enough" |
| 6 | Body: constraints reasoned? | ✅ | Guidelines explain WHY for each constraint: vertical slices (line 110-111), test behavior not implementation (line 112-113), mock at boundaries (line 114-115), one assertion per test (line 116-117), test names as specs (line 118) |
| 7 | Body: numbered steps? | ✅ | 5 numbered steps with RED/GREEN/REFACTOR sub-structure in Step 4 |
| 8 | Body: output formats defined? | ✅ | Step 5 defines verification report: tests added, code added/modified, refactors performed, behaviors skipped |
| 9 | Body: input contract? | ✅ | Line 15: "Parse $ARGUMENTS for the feature or behavior to implement. If no argument, ask" |
| 10 | Quality: repeated at key points? | ✅ | "Vertical slices only" in title, Step 4, and Guidelines. "Never refactor while RED" in Step 4 and referenced methodology |
| 11 | Quality: anti-patterns named? | ✅ | Lines 124-132: 8 explicit anti-patterns including "Writing all tests first", "Testing private methods", "Mocking internal collaborators", "Tests that verify HOW instead of WHAT", "Skipping RED step", "Refactoring while RED", "Adding speculative features" |
| 12 | Quality: refinement step? | ✅ | Step 4 REFACTOR phase is the built-in refinement: "After GREEN, look for refactor candidates" with 5 specific signals |
| 13 | Quality: error handling? | ✅ | Step 4 RED: "If the test passes immediately, it's testing nothing useful — investigate" (line 67). GREEN: "If it fails, fix the implementation — not the test" (line 78). Step 3: "If the interface needs to change, confirm with the user" (line 52) |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference: tdd-methodology.md |
| 20 | Structure: large refs have TOC? | ✅ | tdd-methodology.md (192 lines) has full TOC with anchor links |
| 21 | Structure: self-contained? | ✅ | No cross-skill dependencies. Fully self-contained with its own methodology reference |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 20/20

## Priority fixes (ordered by impact)

1. **None critical.** This skill is well-structured, self-contained, and covers all checklist items.
2. **Minor enhancement:** Step 2 could include guidance on estimating the number of behaviors to test (avoid scope creep — suggest 3-7 behaviors for a focused session, split larger features into multiple /tdd invocations).
3. **Minor: allowed-tools missing** — Header has no `allowed-tools` field. Should declare `Bash, Read, Edit, Write, Grep, Glob` to match the skill's needs (codebase reading, test writing, test execution).
