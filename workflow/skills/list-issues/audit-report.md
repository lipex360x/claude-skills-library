# Audit Report: list-issues

Plugin: workflow
Audited: 2026-03-21
Checklist version: current (runtime read)

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | ✅ pass | 5 trigger phrases ("list issues", "show issues", "what issues are open", "issues list", "overview of all open work") |
| 2 | Description: WHAT + WHEN | ✅ pass | Clear action ("List all open issues grouped by milestone with priority sorting and next-issue suggestion") + triggers |
| 3 | Description: "even if" pattern | ✅ pass | Present: "even if they don't explicitly say 'issues'" |
| 4 | SKILL.md: under 500 lines | ✅ pass | 63 lines, very lean |
| 5 | SKILL.md: imperative form | ✅ pass | "Detect repo URL", "Fetch issues", "Process issues", "Group and sort", "Present results", "Suggest next issue" |
| 6 | SKILL.md: constraints reasoned | ⚠️ partial | Constraints are stated but not always reasoned. "The # column must be a markdown link" — no explanation why. Dependency detection rules are stated but not reasoned |
| 7 | SKILL.md: numbered steps | ✅ pass | 6 numbered steps with clear headers |
| 8 | SKILL.md: output formats | ✅ pass | Step 5 shows exact table format with column definitions, markdown link pattern, and status format. Step 6 shows suggestion format |
| 9 | SKILL.md: input contract | ❌ fail | No input contract at all. No arguments section, no documentation of whether the skill accepts arguments (e.g., filter by milestone, repo path) |
| 10 | Quality: repeated at key points | ❌ fail | Quality expectations stated once in the output format section. No guidelines section, no reinforcement of standards at multiple points |
| 11 | Quality: anti-patterns named | ❌ fail | No anti-patterns listed. Common failure modes unaddressed: truncated issue lists (limit 100), incorrect dependency detection (false positives/negatives), suggesting blocked issues as next |
| 12 | Quality: refinement step | N/A | Read-only display skill — no output to refine |
| 13 | Quality: error handling | ❌ fail | No error handling at all. Missing: repo not a GitHub repo, gh CLI unavailable, no issues found (mentioned implicitly in step 2 but minimal), API rate limits, issues exceeding 100 limit |
| 14 | Testing: invoked with realistic input | N/A | Cannot verify from file content alone |
| 15 | Testing: activation tested (3+ phrases) | N/A | Cannot verify from file content alone |
| 16 | Testing: failure modes checked | N/A | Cannot verify from file content alone |
| 17 | Subagents: applicable? | N/A | No subagents used |
| 18 | Structure: standard layout | ⚠️ partial | SKILL.md + README.md only. No references/ or templates/ directories. The output table format could be extracted to a template for consistency with list-backlog |
| 19 | Structure: references depth | N/A | No references |
| 20 | Structure: large refs have TOC | N/A | No references |
| 21 | Structure: self-contained | ✅ pass | No cross-skill dependencies |
| 22 | Structure: README generated | ✅ pass | README.md exists |
| 23 | Compliance: CLAUDE.md compliance | ✅ pass | `allowed-tools: Bash` declared, `disable-model-invocation: false` explicit, verb-subject naming |

## Score: 9/19 (applicable items)

## Priority fixes (ordered by impact)

1. **Add error handling** — No graceful degradation for any failure scenario. At minimum: not a git repo, gh not authenticated, no issues found, API errors.
2. **Add anti-patterns section** — Name failure modes: suggesting blocked issues as next, silently truncating at 100 issues, false dependency detection.
3. **Add guidelines section** — Quality expectations need reinforcement. Currently just the steps with no quality guidance.
4. **Add input contract** — Document whether arguments are accepted (none, or potential filters).
5. **Add constraints reasoning** — Explain the "why" behind formatting rules.

## Recommended action

- [ ] Run `/create-skill list-issues` with this report to apply fixes
