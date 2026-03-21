# Audit Report: start-new-project

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 7 trigger phrases ("start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", "project idea wanting structured planning") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Plan and scaffold a new project from a prompt") + triggers covering both planning and execution |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'new project'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 269 lines |
| 5 | SKILL.md: imperative form | ✅ pass | "Check for grill-me output", "Parse the prompt", "Ask clarifying questions", "Propose the phase structure", "Create the GitHub issues" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Extensively reasoned: mandatory split rule ("buries progress, makes milestone tracking useless", line 73), TDD reasoning ("TDD-ordered checkboxes ARE the enforcement mechanism", line 199), ARCHITECTURE.md reasoning ("~2k tokens vs ~53k tokens", line 252), no workarounds reasoning ("invisible tech debt that compounds", line 254) |
| 7 | SKILL.md: numbered steps | ✅ pass | 9 numbered steps with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Issue template format defined (phases, steps, checkboxes). References templates/issue-template.md. Summary format in Step 9 |
| 9 | SKILL.md: input contract | ⚠️ partial | Step 1 checks for grill-me output and Step 2 parses the prompt. But no formal input contract table. The skill accepts a bare invocation or description as argument — this should be formalized |
| 10 | Quality: repeated at key points | ✅ pass | TDD mandatory repeated in guidelines (line 199) with detailed reasoning. No workarounds repeated (line 254). File paths, English content, and split rules all reinforced in both steps and guidelines |
| 11 | Quality: anti-patterns named | ✅ pass | 9 explicit anti-patterns listed (lines 260-269): checkboxes without TDD order, generic checkboxes, mixed concerns, missing verification, monolithic issues, front-loading detail, local paths, workarounds, unnecessary comments |
| 12 | Quality: refinement step | ✅ pass | Two explicit approval gates: Step 3 (clarifying questions) and Step 4 ("review the plan with a critical eye... iterate until they approve") |
| 13 | Quality: error handling | ⚠️ partial | Step 1 handles missing grill-output with AUQ. Step 2 handles missing argument. But: no handling for gh CLI failures during issue creation, milestone creation failures, label creation conflicts, branch already exists |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | ⚠️ partial | Agent Teams integration documented (lines 75-98) with teammate spawning rules. But tool access for teammates not explicit in frontmatter (no `allowed-tools` declared at all) |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + 5 references + 6 templates + README.md. Comprehensive structure |
| 19 | Structure: references depth | ✅ pass | One level deep (all in references/) |
| 20 | Structure: large refs have TOC | N/A | Would need to check each reference file size |
| 21 | Structure: self-contained | ✅ pass | All references are local. Templates included in skill directory |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ⚠️ partial | No `allowed-tools` in frontmatter. Skill uses Bash, Read, AskUserQuestion, potentially Agent/TeamCreate but none declared. No `disable-model-invocation` (correct default). Naming follows verb-subject convention |

## Score: 15/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add `allowed-tools` to frontmatter** — Skill uses Bash, Read, AskUserQuestion, and potentially TeamCreate but none are declared. This is important given the subagent integration.
2. **Add formal input contract table** — Multiple input paths (bare invocation, description argument, grill-output file) should be formalized with validation rules.
3. **Expand error handling** — Missing graceful degradation for: gh CLI issue creation failures, milestone conflicts, label conflicts, branch already exists scenarios.
4. **Make teammate tool access explicit** — Agent Teams section describes teammate responsibilities but doesn't specify which tools each teammate gets.

## Recommended action

- [ ] Run `/create-skill start-new-project` with this report to apply fixes
