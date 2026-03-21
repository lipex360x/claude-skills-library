# Audit Report: close-pr

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 6 trigger phrases: "close pr", "merge pr", "merge pull request", "merge this", "land the pr" |
| 2 | Description: WHAT + WHEN? | ✅ | "Merge the open pull request... write detailed implementation summary... move card to Done" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'merge'" |
| 4 | Body: under 500 lines? | ✅ | 204 lines |
| 5 | Body: imperative form? | ✅ | "Find the PR", "Write the comment", "Merge the PR" |
| 6 | Body: constraints reasoned? | ✅ | Guidelines section (lines 191-204) explains WHY for each constraint: implementation summaries as memory, key decisions, unblock notifications, English content, no local paths, ARCHITECTURE.md as living memory, target branch respect |
| 7 | Body: numbered steps? | ✅ | 9 numbered steps (1-9) with sub-steps (7a-7c) |
| 8 | Body: output formats defined? | ✅ | Step 3 defines implementation summary format (lines 53-73). Step 9 defines report items |
| 9 | Body: input contract? | ⚠️ | No explicit $ARGUMENTS or input parsing. Implicitly uses current branch. Could state "no arguments needed — operates on the current branch's PR" |
| 10 | Quality: repeated at key points? | ✅ | Quality emphasized in Guidelines: "specific and concrete — file paths, test names, route URLs" (line 81), "Generic summaries are useless" |
| 11 | Quality: anti-patterns named? | ⚠️ | Implicit anti-patterns in guidelines ("Generic summaries are useless", "No local paths") but no dedicated anti-patterns list |
| 12 | Quality: refinement step? | ❌ | No review gate before merging. The summary is written and posted without user review. ARCHITECTURE.md is updated and committed without approval |
| 13 | Quality: error handling? | ⚠️ | Step 1 handles "no open PR". Step 2 handles target branch mismatch. No handling for: merge conflicts, failed merge, issue not found, board not found (Step 6 says "skip" but no error message) |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference file |
| 20 | Structure: large refs have TOC? | ✅ | project-board-operations.md has clear sections |
| 21 | Structure: self-contained? | ⚠️ | References `/close-pr` Step 8 format in add-backlog context (line 146 of add-backlog references this skill). Within close-pr itself, references "same dependency format used by /list-backlog, /list-issues" — but this is in add-backlog, not close-pr. close-pr itself references `start-new-project` at line 96 for ARCHITECTURE.md structure |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 14/20

## Priority fixes (ordered by impact)

1. **Add explicit input contract** — State at the top: "No arguments. Operates on the current branch's open PR."
2. **Add anti-patterns section** — Name: vague implementation summaries, merging without checking issue tasks, skipping ARCHITECTURE.md update, force-merging with conflicts, auto-committing ARCHITECTURE.md changes without review.
3. **Add refinement/review gate** — The implementation summary and ARCHITECTURE.md changes are significant artifacts. Consider presenting the summary draft to the user before posting, especially for complex PRs.
4. **Improve error handling** — Add explicit handling for merge conflicts (suggest rebase), failed merge (explain and stop), missing issue (degrade gracefully with clear message).
5. **Cross-skill reference** — Line 96 references "same structure as start-new-project" for ARCHITECTURE.md. Should inline the expected structure or reference a shared template.
