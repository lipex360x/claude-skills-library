# Audit Report: add-backlog

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 5 trigger phrases ("add to backlog", "create backlog issue", "backlog add", "new issue for backlog", "register a task for later") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Create a GitHub issue in the project's Backlog milestone") + multiple triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'backlog'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 122 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Analyze scope", "Structure the issue", "Labels and Size", "Detect blocker impact", "Create", "Update blocked issues" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Scope splitting reasoned: "Only split when concerns are genuinely independent" (line 17). Blocker detection reasoned: "This prevents silent dependency gaps" (line 35). Dependency format reasoned: "follows the same dependency format used by /close-pr" (line 96) |
| 7 | SKILL.md: numbered steps | ✅ pass | 8 numbered steps with clear headers, sub-steps (4a-4d) |
| 8 | SKILL.md: output formats | ✅ pass | Step 8 defines report format (issue URL, size, board status, blocked issues). Issue body format defined in Step 2 (What/Why/Acceptance criteria) |
| 9 | SKILL.md: input contract | ⚠️ partial | `argument-hint: <description>` in frontmatter. Step 1 says "Parse $ARGUMENTS... If empty, ask." But no formal input contract table with type/validation/on-invalid |
| 10 | Quality: repeated at key points | ⚠️ partial | Blocker detection quality reinforced across steps 4a-4d. But no guidelines section to reinforce overall quality standards |
| 11 | Quality: anti-patterns named | ❌ fail | No anti-patterns section. Missing failure mode warnings: creating duplicate issues, over-splitting simple requests, false-positive blocker detection, missing milestone |
| 12 | Quality: refinement step | ✅ pass | Step 4c is user approval gate for blockers. Step 1 is approval gate for scope splitting. Step 3 uses AUQ for labels/size |
| 13 | Quality: error handling | ⚠️ partial | Step 2 handles empty input. Step 4a fetches issues. But: no handling for missing Backlog milestone (what if it doesn't exist?), gh CLI failures, label creation failures, project board API failures |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/project-board-operations.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies (references /close-pr format but only for documentation, not a runtime dependency) |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | `allowed-tools: Bash, AskUserQuestion` declared, no `disable-model-invocation: true`, verb-subject naming, `argument-hint` present |

## Score: 13/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add anti-patterns section** — No failure modes listed. Critical gaps: creating duplicate issues, over-splitting trivial requests, false-positive blocker detection, not creating Backlog milestone when missing.
2. **Add guidelines section** — No quality reinforcement beyond the steps. Guidelines should cover: English for issue content, concise acceptance criteria, avoiding duplicates.
3. **Expand error handling** — Missing: Backlog milestone doesn't exist (should it auto-create?), gh CLI failures, label not found.
4. **Add formal input contract table** — argument-hint exists but no structured validation.

## Recommended action

- [ ] Run `/create-skill add-backlog` with this report to apply fixes
