# Skills Library Audit — 2026-03-21

## Summary

33 skills audited across 8 plugins. Sorted by score percentage (lowest first).

| Skill | Plugin | Score | % | Critical gaps |
|-------|--------|-------|---|---------------|
| review-postgres | database | 6/17 | 35% | No steps, no output format, no input contract |
| deploy-vercel | deploy | 7/17 | 41% | No steps, no output format, no input contract |
| approve-post | content | 8/19 | 42% | No error handling, no input contract, cross-skill dep |
| find-skills | meta | 7/16 | 44% | Missing `user-invocable`, no "even if" pattern, not imperative |
| uninstall-skill | meta | 7/16 | 44% | No error handling, no constraints reasoning, no anti-patterns |
| capture-voice | content | 14/26 | 54% | Subagent tool access, race conditions, no input contract |
| list-issues | workflow | 12/20 | 60% | No anti-patterns, no input contract, no quality emphasis |
| create-readme | meta | 10/16 | 63% | Missing `user-invocable`, no anti-patterns, no error handling |
| install-skill | meta | 10/16 | 63% | Cross-skill deps, no anti-patterns, no refinement step |
| close-tasks | tasks | 7/11 | 64% | No safety check, no error handling, no anti-patterns |
| open-tasks | tasks | 7/11 | 64% | No error handling, no verification, no anti-patterns |
| list-backlog | workflow | 13/20 | 65% | No anti-patterns, no quality emphasis, weak error handling |
| add-backlog | workflow | 13/20 | 65% | **Broken reference file**, no anti-patterns, no refinement |
| close-pr | workflow | 14/20 | 70% | No input contract, no anti-patterns, no refinement gate |
| write-content | content | 15/21 | 71% | Cross-skill dependency, missing voice profile fallback |
| clean-tasks | tasks | 8/11 | 73% | No error handling, no refinement, no anti-patterns |
| extract-design-system | design | 17/23 | 74% | No error handling, MCP dep undocumented, no refinement |
| create-continuation | meta | 12/16 | 75% | No refinement step, no error handling, no input contract |
| create-excalidraw | design | 16/21 | 76% | fontFamily contradiction, no refinement, no input contract |
| improve-codebase-architecture | meta | 16/20 | 80% | Subagent tool access, error handling, no input contract |
| check-gmail | gws | 14/17 | 82% | No refinement step, no input contract, external deps |
| open-pr | workflow | 17/20 | 85% | No anti-patterns section, cross-skill invocation |
| push | workflow | 17/20 | 85% | No anti-patterns section, cross-skill invocation |
| inspire-me | content | 19/22 | 86% | Testing gaps, error handling for external tools |
| capture-analysis | meta | 14/16 | 88% | No input contract, error handling for remove |
| sync-claude | meta | 14/16 | 88% | No anti-patterns, no refinement step |
| grill-me | workflow | 18/20 | 90% | Minor: error handling, missing allowed-tools |
| start-issue | workflow | 20/22 | 91% | Minor: subagent tool access, guidelines density |
| start-new-project | workflow | 20/22 | 91% | Minor: subagent tool access, gh CLI error handling |
| create-hook | meta | 15/16 | 94% | Minor: no input contract |
| create-webview | design | 21/22 | 95% | Minor: large refs missing TOC |
| tdd | workflow | 20/20 | 100% | None |
| create-diagram | design | 23/23 | 100% | None |

## Fix batches (grouped by fix type)

### Batch 1: Add anti-patterns section (16 skills)
list-issues, list-backlog, add-backlog, close-pr, open-pr, push, find-skills, uninstall-skill, create-readme, install-skill, sync-claude, clean-tasks, close-tasks, open-tasks, review-postgres, deploy-vercel

### Batch 2: Add input contract (15 skills)
review-postgres, deploy-vercel, approve-post, find-skills, uninstall-skill, capture-voice, list-issues, create-readme, close-pr, create-continuation, create-excalidraw, improve-codebase-architecture, check-gmail, capture-analysis, create-hook

### Batch 3: Add error handling patterns (14 skills)
review-postgres, deploy-vercel, approve-post, uninstall-skill, close-tasks, open-tasks, clean-tasks, create-readme, create-continuation, extract-design-system, capture-analysis, inspire-me, grill-me, start-new-project

### Batch 4: Add refinement/verification step (11 skills)
review-postgres, deploy-vercel, add-backlog, close-pr, install-skill, sync-claude, clean-tasks, check-gmail, create-continuation, create-excalidraw, extract-design-system

### Batch 5: Fix cross-skill dependencies (4 skills)
approve-post, write-content, install-skill, open-pr

### Batch 6: Fix subagent patterns (4 skills)
capture-voice, improve-codebase-architecture, start-issue, start-new-project

## Top 5 most critical skills to fix

1. **review-postgres** (6/17, 35%) — barely functional as a skill; needs complete restructuring with steps, output format, and input contract
2. **deploy-vercel** (7/17, 41%) — same issues as review-postgres; missing all structural elements
3. **approve-post** (8/19, 42%) — no error handling, no input contract, cross-skill dependency
4. **find-skills** (7/16, 44%) — missing user-invocable flag, not imperative, no "even if" pattern
5. **uninstall-skill** (7/16, 44%) — no error handling, no reasoning on constraints, no anti-patterns

## Common patterns

- **Most common gap:** anti-patterns section (16/33 skills missing it)
- **Second most common:** input contract (15/33 skills)
- **Third:** error handling patterns (14/33 skills)
- **Minimum threshold recommendation:** 75% (approximately 12/16 or equivalent)
- **Skills below 75%:** 19 out of 33 — significant remediation needed
