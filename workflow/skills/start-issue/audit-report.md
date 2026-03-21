# Audit Report: start-issue

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 5 trigger phrases ("start issue", "work on issue #N", "pull from backlog", "start #N", "begin implementing an issue") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Pull an issue and start implementation — reads the issue, expands acceptance criteria into detailed step-by-step plan") + triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'issue'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 288 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Select issue", "Analyze the issue", "Propose the detailed plan", "Update the issue", "Create branch", "Create tasks" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Extensively reasoned: ARCHITECTURE.md rationale ("~2k tokens vs ~53k", line 40), TDD reasoning ("TDD-ordered checkboxes ARE the enforcement mechanism", line 228), mandatory split rule reasoned (line 102), no workarounds reasoning ("invisible tech debt", line 271) |
| 7 | SKILL.md: numbered steps | ✅ pass | 8 numbered steps with sub-steps (2b, 2c, 5b), clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Issue body format defined (What/Why/Acceptance criteria/Steps), summary format in Step 8 |
| 9 | SKILL.md: input contract | ⚠️ partial | Step 1 accepts issue number or "#N" format with AUQ fallback. But no formal input contract table with validation rules and on-invalid behavior |
| 10 | Quality: repeated at key points | ✅ pass | TDD mandatory reinforced in Step 2c and guidelines (line 228). No workarounds in 2c and guidelines (line 271). Agent Teams check in 2b and Step 7. ARCHITECTURE.md in Step 2 and guidelines (line 269) |
| 11 | Quality: anti-patterns named | ✅ pass | 11 explicit anti-patterns (lines 277-288): TDD order, generic checkboxes, mixed concerns, missing verification, over-expansion, duplicating criteria, local paths, workarounds, unnecessary comments, missing Agent Teams check, wrong Agent Teams placement |
| 12 | Quality: refinement step | ✅ pass | Step 3: "review the plan with a critical eye: tighten vague checkboxes, remove redundancy, ensure TDD order". AUQ approval gate with "Aprovado"/"Quero ajustar" loop |
| 13 | Quality: error handling | ⚠️ partial | Step 1 handles missing argument (AUQ), no milestone/issues (stop). Step 5b handles no project board (AUQ to create). But: no handling for gh CLI failures, issue fetch errors, branch creation conflicts, stale issue body during edit |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | ✅ pass | Agent Teams integration well-documented (Steps 2b, 3, 7). Execution mode section placement emphasized. Teammate spawning with user approval gate. Tool access for teammates implied through step assignments |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + 4 references (cdp-best-practices, project-board-operations, project-board-setup, tdd-methodology) + templates/step-template.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep |
| 20 | Structure: large refs have TOC | N/A | Would need to check each reference file size |
| 21 | Structure: self-contained | ✅ pass | All references local. No cross-skill runtime dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ⚠️ partial | No `allowed-tools` in frontmatter. Skill uses Bash, Read, Grep, AskUserQuestion, TaskCreate, TeamCreate but none declared. No `disable-model-invocation` (correct default). Naming follows verb-subject convention |

## Score: 16/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add `allowed-tools` to frontmatter** — Skill uses Bash, Read, Grep, AskUserQuestion, TaskCreate, and TeamCreate but none are declared. This is especially important given the subagent and task management integration.
2. **Add formal input contract table** — Issue number input accepts multiple formats (bare number, #N) but lacks formalized validation.
3. **Expand error handling** — Missing graceful degradation for: gh CLI failures, branch creation conflicts (branch already exists), concurrent issue edits (stale body), TaskCreate failures.

## Recommended action

- [ ] Run `/create-skill start-issue` with this report to apply fixes
