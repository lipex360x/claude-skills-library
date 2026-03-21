# Audit Report: add-backlog

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 5 trigger phrases plus "even if they don't explicitly say backlog" |
| 2 | Description: WHAT + WHEN? | ✅ | "Create a GitHub issue and add it to the project board's Backlog column" + trigger contexts |
| 3 | Description: "even if" pattern? | ✅ | Present: "even if they don't explicitly say 'backlog'" |
| 4 | Body: under 500 lines? | ✅ | 172 lines |
| 5 | Body: imperative form? | ✅ | Steps use imperative: "Parse", "Create", "Present" |
| 6 | Body: constraints reasoned? | ⚠️ | Most constraints implicit. Step 4b explains WHY blocker detection matters (line 90-96), but Step 2b skill detection table lacks reasoning for why it exists |
| 7 | Body: numbered steps? | ✅ | 8 numbered steps (1-8) including sub-steps (4a-4d) |
| 8 | Body: output formats defined? | ✅ | Step 8 defines report format with 4 items |
| 9 | Body: input contract? | ✅ | Line 11: "Parse $ARGUMENTS as the issue description. If empty, ask the user" |
| 10 | Quality: repeated at key points? | ⚠️ | No quality reminders at decision points. Step 2b skill detection could benefit from a quality check |
| 11 | Quality: anti-patterns named? | ❌ | No anti-patterns section. Missing patterns like: creating issues without board tracking, skipping scope analysis, vague acceptance criteria |
| 12 | Quality: refinement step? | ❌ | No review/refinement of the issue before creation. Goes straight from structure to labels to create |
| 13 | Quality: error handling? | ⚠️ | Step 7 handles missing board. No handling for: gh CLI failures, invalid issue body, label creation failures |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only, not tested live |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout? | ⚠️ | Has SKILL.md, references/, README.md. No templates/ — acceptable since no templated output |
| 19 | Structure: references one level deep? | ✅ | Single reference file at one level |
| 20 | Structure: large refs have TOC? | ✅ | project-board-operations.md is 129 lines, has clear sections |
| 21 | Structure: self-contained? | ❌ | Line 156 references `references/project-board-setup.md` but only `project-board-operations.md` exists. Missing file = broken reference. Also references `/close-pr` (line 146) and `/list-backlog`, `/list-issues` — cross-skill dependency |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English content, no local paths, project-agnostic |

## Score: 13/20

## Priority fixes (ordered by impact)

1. **Missing reference file** — Line 156 references `references/project-board-setup.md` which does not exist in this skill. Either add the file (copy from start-issue) or remove the reference and inline the setup instructions.
2. **Add anti-patterns section** — Name common failure modes: creating issues without board tracking, vague acceptance criteria without verifiable items, skipping scope analysis for multi-concern requests, forcing skill matches in Step 2b.
3. **Add refinement step** — Before creating the issue (Step 5), add a step to review the draft: tighten acceptance criteria, verify skill match is genuine, confirm scope is single-concern.
4. **Cross-skill references** — Line 146 mentions `/close-pr`, `/list-backlog`, `/list-issues` by name. These should be described by behavior, not by skill name, to maintain self-containment.
5. **Error handling** — Add graceful degradation for gh CLI failures (no internet, auth issues, rate limits).
