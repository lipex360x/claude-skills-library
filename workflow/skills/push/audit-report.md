# Audit Report: push

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 5 trigger phrases ("push", "commit and push", "ship it", "/push", "finalize work and sync issue tracking"), supports flags (-y, -nh) |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Commit, push, and update GitHub issue checkboxes") + multiple trigger contexts |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly mention the issue" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 118 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Gather state", "Analyze and group changes", "Stage and commit" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Constraints explained with reasoning: "Never amend — amending after a hook failure modifies the wrong commit" (line 67), "Never force-push" with explanation (line 76), secrets scan rationale (line 113) |
| 7 | SKILL.md: numbered steps | ✅ pass | 6 numbered steps with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Step 6 defines concise summary format with specific fields (commit hash, push status, checkboxes updated, remaining count) |
| 9 | SKILL.md: input contract | ⚠️ partial | Flags section documents -y and -nh, but no formal input contract table with validation rules. Missing explicit handling for invalid flag combinations or unrecognized flags |
| 10 | Quality: repeated at key points | ✅ pass | Key constraints ("never amend", "never force-push", "never stage secrets") stated in steps AND reinforced in guidelines |
| 11 | Quality: anti-patterns named | ✅ pass | Implicit through guidelines: force-pushing, amending, staging secrets. Could be more explicitly listed as anti-patterns section |
| 12 | Quality: refinement step | ✅ pass | Commit message approval gate serves as refinement/review step (Step 2), skippable with -y |
| 13 | Quality: error handling | ✅ pass | Hook failure handling (line 67: fix, re-stage, new commit), push rejection handling (line 76: explain, suggest rebase, ask user), graceful degradation for missing gh CLI (line 116) |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/issue-update-guide.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ⚠️ partial | No `allowed-tools` in frontmatter. The skill uses Bash and Read implicitly but doesn't declare them. No `disable-model-invocation` (correct default per CLAUDE.md rules) |

## Score: 16/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add `allowed-tools` to frontmatter** — Skill uses Bash (git commands, gh CLI), Read (for issue bodies), but doesn't declare them in frontmatter. Other workflow skills like close-pr and open-pr declare their tools.
2. **Add formal input contract table** — Flags are documented but lack a structured input contract table with validation rules for invalid inputs.

## Recommended action

- [ ] Run `/create-skill push` with this report to apply fixes
