# Audit Report: push

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 5 trigger phrases: "push", "commit and push", "ship it", "/push". Also mentions issue sync |
| 2 | Description: WHAT + WHEN? | ✅ | "Commit, push, and update GitHub issue checkboxes in one command" + flag descriptions + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly mention the issue" |
| 4 | Body: under 500 lines? | ✅ | 131 lines |
| 5 | Body: imperative form? | ✅ | "Run these in parallel", "Analyze all changes", "Stage and commit" |
| 6 | Body: constraints reasoned? | ✅ | Guidelines (lines 119-131) explain WHY for each: never force-push (others depend on history), never amend (modifies wrong commit after hook failure), never stage secrets, no gates by default (user chose automation), graceful degradation, ARCHITECTURE.md drift |
| 7 | Body: numbered steps? | ✅ | 7 numbered steps |
| 8 | Body: output formats defined? | ✅ | Step 6 defines summary format: commit hash/message, push status, checkboxes updated, remaining count |
| 9 | Body: input contract? | ✅ | Flags section (lines 13-16) defines `--confirm` and `-nh`. Step 1 handles clean working tree |
| 10 | Quality: repeated at key points? | ✅ | "Never force-push" in both Step 4 and Guidelines. "Never amend" in Step 3 and Guidelines. Secret scanning in Step 3 and Guidelines |
| 11 | Quality: anti-patterns named? | ⚠️ | Guidelines serve as implicit anti-patterns ("Never force-push", "Never amend", "Never stage secrets") but no dedicated "Avoid these" section with the full list |
| 12 | Quality: refinement step? | ✅ | `--confirm` flag provides optional refinement. Step 2 "If something looks wrong... stop and present via AskUserQuestion" |
| 13 | Quality: error handling? | ✅ | Step 3 handles hook failures (new commit, never amend). Step 4 handles push rejection (explain, suggest rebase, ask user). Step 5 handles missing issue (skip gracefully). Guidelines: graceful degradation if gh unavailable |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference: issue-update-guide.md |
| 20 | Structure: large refs have TOC? | ✅ | issue-update-guide.md (114 lines) has clear sections with headers |
| 21 | Structure: self-contained? | ⚠️ | Line 113 invokes `/open-pr` when all checkboxes complete. Same pattern as open-pr invoking /close-pr — intentional workflow chain but creates cross-skill dependency |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 17/20

## Priority fixes (ordered by impact)

1. **Add explicit anti-patterns section** — Consolidate into a dedicated list: force-pushing, amending after hook failure, staging secrets, committing unrelated files in one commit, skipping issue update when branch has an issue, auto-editing ARCHITECTURE.md (vs just noting drift).
2. **Cross-skill invocation** — Line 113 calls `/open-pr`. Add fallback behavior: if the skill is unavailable, suggest the user run it manually.
3. **Minor: ARCHITECTURE.md drift detection** — Line 131 is a dense paragraph. Consider extracting to a dedicated sub-step or reference for clarity.
