# Audit Report: open-pr

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 6 trigger phrases: "create pr", "open pr", "pr create", "make a pull request", "submit for review" |
| 2 | Description: WHAT + WHEN? | ✅ | "Create a pull request from the current branch, linking it to the open issue" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'pull request'" |
| 4 | Body: under 500 lines? | ✅ | 158 lines |
| 5 | Body: imperative form? | ✅ | "Determine", "Extract", "Build", "Verify", "Create" |
| 6 | Body: constraints reasoned? | ✅ | Guidelines (lines 147-158) explain WHY: scope transfers preserve traceability, bidirectional comments, every skip leaves a trace, technical context in transfers, no local paths |
| 7 | Body: numbered steps? | ✅ | 7 numbered steps with sub-steps (4a, 4b) |
| 8 | Body: output formats defined? | ✅ | Step 3 defines PR body format. Step 6 defines report format. Scope transfer comment templates defined (lines 63-104) |
| 9 | Body: input contract? | ✅ | Header has `argument-hint: [title]`. Step 3 line 24: "Use $ARGUMENTS if provided" |
| 10 | Quality: repeated at key points? | ✅ | "No local paths" emphasized in guidelines. Traceability emphasized in both scope transfer steps and guidelines |
| 11 | Quality: anti-patterns named? | ⚠️ | Implicit anti-patterns in guidelines ("Don't force transfers", "every skip leaves a trace") but no dedicated anti-patterns list with explicit "Avoid these" section |
| 12 | Quality: refinement step? | ✅ | Step 4a is a thorough readiness check with checkbox verification and user decision points for each unchecked item |
| 13 | Quality: error handling? | ✅ | Step 1 handles main branch. Step 2 handles missing issue ("proceed without linking"). Step 4b handles test markers. Step 5 handles missing board. Step 7 offers merge-now vs wait |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: applicable? | N/A | No subagents |
| 18 | Structure: standard layout? | ✅ | SKILL.md, references/, README.md |
| 19 | Structure: references one level deep? | ✅ | Single reference file |
| 20 | Structure: large refs have TOC? | ✅ | project-board-operations.md has clear sections |
| 21 | Structure: self-contained? | ⚠️ | Line 143 invokes `/close-pr` directly. This is a deliberate workflow chain (user chose "merge now"), but it's a cross-skill invocation dependency |
| 22 | Structure: README generated? | ✅ | README.md exists |
| 23 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 17/20

## Priority fixes (ordered by impact)

1. **Add explicit anti-patterns section** — Consolidate the implicit anti-patterns from guidelines into a dedicated "Avoid these anti-patterns" list: silently dropping unchecked items, creating PRs with test markers, force-pushing to get around conflicts, generic PR summaries, local paths in PR body.
2. **Cross-skill invocation** — Line 143 calls `/close-pr`. This is an intentional UX flow but creates a runtime dependency. Add a fallback: "If /close-pr is unavailable, run `gh pr merge --merge --delete-branch` directly."
3. **Minor: Step 4b specificity** — "Grep test files for .fixme, .skip, .todo, and only markers" should specify file patterns to search (e.g., `**/*.test.{ts,js}`, `**/*.spec.{ts,js}`).
