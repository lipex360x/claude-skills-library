# Audit Report: open-pr

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 6 trigger phrases ("create pr", "open pr", "pr create", "make a pull request", "submit for review", "open a PR for the current branch") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Create a pull request from the current branch, linking it to the open issue") + triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'pull request'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 151 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Validate branch", "Link to issue", "Build PR content", "Create and report" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Scope transfer rationale: "bidirectional comments ensure anyone reading either issue understands the full history" (line 143), skip justification: "exists specifically to prevent silent drops" (line 147), "Draft the justification from conversation context when possible — don't make the user write it from scratch" (line 147) |
| 7 | SKILL.md: numbered steps | ✅ pass | 6 numbered steps with clear headers, sub-steps (4a, 4b) |
| 8 | SKILL.md: output formats | ✅ pass | PR body template defined (lines 26-34), scope transfer comment format (lines 65-86), report format (lines 133-137) |
| 9 | SKILL.md: input contract | ⚠️ partial | `argument-hint: [title]` in frontmatter indicates optional title argument. But no formal input contract table with validation rules |
| 10 | Quality: repeated at key points | ✅ pass | Traceability reinforced in Step 4 (transfer comments), guidelines ("Scope transfers preserve traceability"), and anti-pattern avoidance |
| 11 | Quality: anti-patterns named | ⚠️ partial | Guidelines mention what to avoid ("Don't force transfers", "No local paths in comments") but no explicit anti-patterns section systematically listing failure modes |
| 12 | Quality: refinement step | ✅ pass | Step 4a serves as refinement — user reviews unchecked items and decides disposition (move, create, skip, mark done) before PR creation |
| 13 | Quality: error handling | ⚠️ partial | Step 1 handles "on main" case. Step 4b handles test markers. But: no handling for gh CLI failures, no branch exists on remote, issue not found, project board API failures |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/project-board-operations.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | `allowed-tools: Bash, Read, Grep, AskUserQuestion` declared, `disable-model-invocation: false` explicit, `argument-hint` present |

## Score: 14/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add formal input contract table** — `argument-hint: [title]` exists but no structured table with validation, type, required/optional, on-invalid behavior.
2. **Add explicit anti-patterns section** — Guidelines hint at what to avoid but don't systematically name failure modes (e.g., creating PR without pushing, silently dropping unchecked items, posting scope transfers without context).
3. **Expand error handling** — Missing graceful degradation for gh CLI failures, remote branch issues, and project board API errors.

## Recommended action

- [ ] Run `/create-skill open-pr` with this report to apply fixes
