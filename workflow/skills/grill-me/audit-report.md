# Audit Report: grill-me

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 7 trigger phrases including PT-BR variants ("me entrevista", "quero detalhar isso", "vamos aprofundar"), plus "even if they don't explicitly say 'grill'" |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("Deep structured interview... to generate PRD input") + multiple trigger contexts |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'grill'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 103 lines, lean |
| 5 | SKILL.md: imperative form | ✅ pass | "Choose interview language", "Capture the starting point", "Conduct the interview" |
| 6 | SKILL.md: constraints reasoned | ✅ pass | Options contextualized with reasoning ("Options must reflect what has already been discussed"), anti-patterns explained with rationale |
| 7 | SKILL.md: numbered steps | ✅ pass | 6 numbered steps with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | References `templates/grill-output.md` for output template, output path specified (`.claude/grill-output.md`) |
| 9 | SKILL.md: input contract | ⚠️ partial | Usage section mentions optional argument but no formal input contract table with validation rules and type expectations |
| 10 | Quality: repeated at key points | ✅ pass | Quality rules reinforced in interview rules (lines 54-65) and guidelines section (lines 86-103) |
| 11 | Quality: anti-patterns named | ✅ pass | 5 specific anti-patterns listed (lines 98-103): open-ended questions without options, generic options, skipping branches, generating without checkpoint, mixing interview with solutioning |
| 12 | Quality: refinement step | ✅ pass | Step 5 "Alignment checkpoint" serves as explicit refinement/polish gate with options to adjust |
| 13 | Quality: error handling | ⚠️ partial | No explicit error handling for tool failures (e.g., what if AskUserQuestion fails, or codebase detection gives ambiguous results). Graceful degradation not addressed |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone — requires manual confirmation |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ✅ pass | SKILL.md + references/interview-branches.md + templates/grill-output.md + README.md |
| 19 | Structure: references depth | ✅ pass | One level deep (references/interview-branches.md) |
| 20 | Structure: large refs have TOC | N/A | Would need to check reference file size |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies detected |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | No `disable-model-invocation: true`, verb-subject naming ("grill-me"), user-invocable: true |

## Score: 15/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add formal input contract table** — SKILL.md has a Usage section but lacks the structured input contract table (Input | Source | Required | Validation | On invalid) that other skills use. The argument is described informally in "Usage" and Step 2.
2. **Add error handling patterns** — No explicit handling for tool failures or ambiguous codebase detection results. Add graceful degradation guidance for when AskUserQuestion or codebase exploration fails.

## Recommended action

- [ ] Run `/create-skill grill-me` with this report to apply fixes
