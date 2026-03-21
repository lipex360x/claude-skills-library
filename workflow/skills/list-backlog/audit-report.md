# Audit Report: list-backlog

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 5 trigger phrases ("list backlog", "show backlog", "backlog list", "what's in the backlog", "see pending backlog items") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("List open backlog issues with table summary and size sorting") + multiple triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'backlog'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 67 lines, very lean |
| 5 | SKILL.md: imperative form | ✅ pass | "Detect repo URL", "Fetch issues", "Process and sort", "Present results" |
| 6 | SKILL.md: constraints reasoned | ⚠️ partial | Sorting rules clearly stated but not reasoned (why this order?). Dependency detection rules stated without rationale. "Use /start-issue to start working on one" — good but minimal |
| 7 | SKILL.md: numbered steps | ✅ pass | 4 numbered steps with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Step 4 shows exact table format with column definitions, link pattern, status format, and call-to-action |
| 9 | SKILL.md: input contract | ⚠️ partial | Arguments section documents `[asc|desc]` with defaults, but no formal input contract table with validation for invalid arguments (e.g., what if user passes "medium"?) |
| 10 | Quality: repeated at key points | ❌ fail | Quality expectations stated once in output format. No guidelines section, no reinforcement at multiple points |
| 11 | Quality: anti-patterns named | ❌ fail | No anti-patterns listed. Common failure modes unaddressed: silently truncating at 100 issues, incorrect dependency detection, showing stale data |
| 12 | Quality: refinement step | N/A | Read-only display skill — no output to refine |
| 13 | Quality: error handling | ⚠️ partial | Step 2 handles "milestone doesn't exist or no issues" case. But: no handling for gh CLI unavailable, not a git repo, API errors, dependency check failures |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ⚠️ partial | SKILL.md + README.md only. No references/ or templates/. Output format could be a shared template with list-issues for consistency |
| 19 | Structure: references depth | N/A | No references |
| 20 | Structure: large refs have TOC | N/A | No references |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | `allowed-tools: Bash` declared, `disable-model-invocation: false` explicit, verb-subject naming |

## Score: 9/18 (applicable items)

## Priority fixes (ordered by impact)

1. **Add guidelines section with quality reinforcement** — Currently no quality expectations beyond the output format. Add guidelines covering dependency detection accuracy, handling large backlogs, and data freshness.
2. **Add anti-patterns section** — Name failure modes: silently truncating results, false dependency detection, recommending blocked issues.
3. **Expand error handling** — Add graceful degradation for gh CLI failures, API errors, and non-GitHub repos.
4. **Add formal input contract table** — Arguments are documented but lack validation rules for invalid inputs.
5. **Add constraints reasoning** — Explain why the sorting and formatting rules exist.

## Recommended action

- [ ] Run `/create-skill list-backlog` with this report to apply fixes
