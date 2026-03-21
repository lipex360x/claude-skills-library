# Audit Report: grill-me

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 6 trigger phrases including Portuguese ("me entrevista", "quero detalhar isso") and English ("stress-test this idea", "let's flesh this out") |
| 2 | Description: WHAT + WHEN? | ✅ | "Deep structured interview... extracts decisions, constraints, and context to generate PRD input" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'grill'" |
| 4 | Body: under 500 lines? | ✅ | 103 lines |
| 5 | Body: imperative form? | ✅ | "Choose interview language", "Capture the starting point", "Conduct the interview" |
| 6 | Body: constraints reasoned? | ✅ | Guidelines explain WHY: "Smart options demonstrate competence" (line 89), "Depth > breadth" (line 91), "Don't invent decisions" (line 93), "Codebase as oracle" (line 97) |
| 7 | Body: numbered steps? | ✅ | 6 numbered steps |
| 8 | Body: output formats defined? | ✅ | Step 6 references `templates/grill-output.md` which defines a complete structured template (74 lines) |
| 9 | Body: input contract? | ✅ | Lines 13-15: "/grill-me or /grill-me <brief description>" with behavior for both cases |
| 10 | Quality: repeated at key points? | ✅ | "Every question uses AskUserQuestion with options" repeated as Rule 1 (line 54) and reinforced in anti-patterns (line 99) |
| 11 | Quality: anti-patterns named? | ✅ | Lines 98-103: 5 explicit anti-patterns including "Open-ended questions without options", "Generic options", "Skipping branches", "Generating output without checkpoint", "Mixing interview with solutioning" |
| 12 | Quality: refinement step? | ✅ | Step 5 "Alignment checkpoint" with 3 options including "Need to adjust" which loops back |
| 13 | Quality: error handling? | ⚠️ | Step 3 handles greenfield vs existing codebase detection. No handling for: user abandoning mid-interview, AskUserQuestion failures, codebase too large to explore |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, templates/, README.md — full standard layout |
| 19 | Structure: references one level deep? | ✅ | Single reference: interview-branches.md |
| 20 | Structure: large refs have TOC? | ✅ | interview-branches.md (124 lines) has clear branch headers serving as TOC |
| 21 | Structure: self-contained? | ✅ | No cross-skill dependencies. Mentions "/write-a-prd" only as a suggestion to the user (line 80), not a dependency |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 18/20

## Priority fixes (ordered by impact)

1. **Minor: error handling** — Add guidance for mid-interview abandonment (save partial progress to grill-output.md with a "partial" marker) and codebase exploration limits (set a token budget for code reading).
2. **Minor: allowed-tools missing** — Header has no `allowed-tools` field. Should declare `AskUserQuestion, Bash, Read, Glob, Grep` to match the skill's needs (codebase exploration in Step 3).
