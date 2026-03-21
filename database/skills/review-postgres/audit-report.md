# Audit Report: review-postgres

Plugin: database
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ⚠️ | Describes WHAT and WHEN but lacks "even if" pattern. No trigger for "my query is slow", "optimize this SQL", "schema review" |
| 2 | WHAT + WHEN in description? | ✅ | "Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations" |
| 3 | "Even if" pattern? | ❌ | Missing — should include "even if they don't explicitly mention Postgres" |
| 4 | Under 500 lines? | ✅ | 64 lines |
| 5 | Imperative form? | ⚠️ | Mixed — "Reference these guidelines when:" is passive; body is mostly declarative rather than imperative steps |
| 6 | Constraints reasoned? | N/A | No rigid ALWAYS/NEVER constraints present |
| 7 | Numbered steps? | ❌ | No numbered steps — body is a reference table + "How to Use" section with no process flow |
| 8 | Output formats defined? | ❌ | No output format specified — doesn't say what the review result should look like |
| 9 | Input contract? | ❌ | No input contract — doesn't define what input it expects (SQL file? schema? query?) |
| 10 | Quality repeated at key points? | ❌ | No quality gates or checkpoints |
| 11 | Anti-patterns named? | ❌ | No anti-patterns section |
| 12 | Refinement step? | ❌ | No refinement or iteration step |
| 13 | Error handling patterns? | ❌ | No error handling |
| 14 | Invoked with realistic input? | N/A | Audit scope — not tested |
| 15 | Activation tested? | N/A | Audit scope — not tested |
| 16 | Failure modes checked? | N/A | Audit scope — not tested |
| 17 | Subagents — context complete? | N/A | No subagents |
| 18 | Standard layout? | ⚠️ | Has SKILL.md, references/, README.md, plus AGENTS.md and CLAUDE.md (non-standard extras). No templates/ but not needed |
| 19 | References one level deep? | ✅ | All references are in `references/` flat directory |
| 20 | Large refs have TOC? | ⚠️ | `_sections.md` serves as TOC for references, but individual large refs not checked |
| 21 | Self-contained? | ✅ | No cross-skill dependencies |
| 22 | README generated? | ✅ | Present and well-structured |
| 23 | CLAUDE.md compliance? | ⚠️ | Has its own CLAUDE.md (duplicates SKILL.md content) — unusual for a skill, may cause confusion |

## Score: 6/17

(Excluding N/A items)

## Priority fixes (ordered by impact)

1. **Add numbered process steps** — The skill reads like a reference catalog, not an actionable process. Add steps: 1) Identify what user needs reviewed, 2) Read relevant reference files, 3) Apply rules, 4) Present findings in structured format
2. **Define output format** — Specify what a review result looks like (table of findings? inline comments? severity ratings?)
3. **Add input contract** — Define expected inputs: SQL queries, schema files, migration files, or general "review my database"
4. **Add anti-patterns section** — Common Postgres mistakes the skill should catch (missing indexes on FK columns, sequential scans on large tables, etc.)
5. **Improve description with "even if" pattern** — Add triggers like "even if they don't explicitly say Postgres" or "even if they're just writing a migration"
6. **Add quality checkpoints** — E.g., "After review, verify all CRITICAL rules were checked"
7. **Remove duplicate CLAUDE.md** — CLAUDE.md duplicates SKILL.md content; consider removing or making it a symlink
