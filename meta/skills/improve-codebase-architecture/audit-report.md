# Audit Report: improve-codebase-architecture

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 9 triggers: "improve architecture", "refactor modules", "codebase review", "make code agent-friendly", "deep modules", "module boundaries", "architectural friction", "simplify codebase", "restructure code" |
| 2 | WHAT + WHEN | ✅ | What: "Explore codebase for architectural friction, propose deep-module refactors as GitHub issue RFCs". When: user wants better testability, maintainability, or simpler architecture |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "architecture."` |
| 4 | Under 500 lines | ✅ | 109 lines |
| 5 | Imperative form | ✅ | "Use the Agent tool", "Present a numbered list", "Spawn 3 sub-agents", "Create a refactor RFC" |
| 6 | Constraints reasoned | ✅ | Excellent reasoning: "A module with 1 method hiding 500 lines of logic is better than 10 modules with 50 lines each — because the 1-method module is trivially testable" (line 88) |
| 7 | Numbered steps | ✅ | 6 numbered steps |
| 8 | Output formats defined | ✅ | Candidate list format (step 2), sub-agent output format (step 4), RFC via reference template |
| 9 | Input contract | ⚠️ | No explicit required/optional. Implicitly requires a codebase to explore, but not stated |
| 10 | Quality repeated at key points | ✅ | Guidelines section (lines 86-109) reinforces deep module principles, vertical slices, test preservation |
| 11 | Anti-patterns named | ✅ | 5 anti-patterns (lines 104-109): refactoring without reading, rewrites instead of deepening, ignoring tests, vague issues, over-splitting |
| 12 | Refinement step | ✅ | Steps 3-5: frame problem → compare 3 designs → user picks. Iterative refinement built into the flow |
| 13 | Error handling | ⚠️ | No explicit error handling for: empty codebase, no friction found, sub-agent failures, `gh` CLI not available |
| 14 | Standard layout | ✅ | SKILL.md + README + references/ (2 files: dependency-categories.md, rfc-template.md) |
| 15 | References one level deep | ✅ | All references in `references/` — one level |
| 16 | Self-contained | ✅ | References are local. No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set |
| 19 | Subagent: context complete | ✅ | Each agent gets "file paths, coupling details, dependency category, what's being hidden" plus a design constraint |
| 20 | Subagent: tool access explicit | ❌ | No `allowed-tools` or tool access specified for the 3 sub-agents |
| 21 | Subagent: two-phase build | ⚠️ | Not explicitly mentioned. Agents produce output in one pass |
| 22 | Subagent: race conditions | ✅ | Agents run in parallel but output is "presented sequentially, then compared" — no race condition risk |

## Score: 16/20

## Priority fixes (ordered by impact)

1. **Subagent tool access** — Specify which tools the sub-agents need (Read, Glob, Grep at minimum). Without explicit tool access, agents may lack necessary capabilities.
2. **Error handling** — Add handling for: no architectural friction found (celebrate it), sub-agent failure (retry or proceed with remaining designs), `gh` CLI unavailable.
3. **Input contract** — State explicitly: requires a codebase with source files. Define behavior for tiny projects (< 5 files) where architecture analysis isn't meaningful.
4. **Subagent two-phase build** — Consider specifying that agents first outline their approach, then produce the full design — reduces wasted work if the agent misunderstands the brief.
