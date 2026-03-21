# Audit Report: create-readme

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 6 triggers: "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", "wants documentation for a repository" |
| 2 | WHAT + WHEN | ✅ | What: "Create or review a README.md". When: user mentions readme or wants documentation. Auto-detects mode |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "readme."` |
| 4 | Under 500 lines | ✅ | 56 lines |
| 5 | Imperative form | ✅ | "Check if README.md exists", "Scan the project", "Draft the README", "Present findings" |
| 6 | Constraints reasoned | ✅ | "Those have dedicated files" for LICENSE/CONTRIBUTING (line 52), "English maximizes reach" (line 48) |
| 7 | Numbered steps | ✅ | 4 numbered steps (detect mode, create, review, formatting) |
| 8 | Output formats defined | ⚠️ | Formatting rules defined (step 4) but no explicit output format for review mode — says "numbered list of specific, actionable improvements" but no template |
| 9 | Input contract | ❌ | No explicit input contract. No $ARGUMENTS handling, no required/optional params. Relies entirely on mode auto-detection |
| 10 | Quality repeated at key points | ⚠️ | Formatting rules in step 4, but quality isn't reinforced at create/review steps |
| 11 | Anti-patterns named | ❌ | No anti-patterns section. Common pitfalls like emoji overuse mentioned in rules but not structured as anti-patterns |
| 12 | Refinement step | ⚠️ | "Present the draft to the user before writing" (create mode) and "let the user choose" (review mode) — user refinement but no self-check |
| 13 | Error handling | ❌ | No handling for: empty project (nothing to scan), non-git project, binary-only project, existing README in non-root location |
| 14 | Standard layout | ✅ | SKILL.md + README + references/ with 5 reference files |
| 15 | References one level deep | ✅ | All references in `references/` — one level |
| 16 | Self-contained | ✅ | No cross-skill dependencies. References are local |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ⚠️ | Missing `user-invocable: true` in frontmatter — the description list in CLAUDE.md shows it as invocable, but the frontmatter omits it |

## Score: 10/16

## Priority fixes (ordered by impact)

1. **Add `user-invocable: true`** — Frontmatter is missing this field. Without it, the skill may not appear in `/` autocomplete.
2. **Anti-patterns section** — Add common README anti-patterns: emoji soup, wall-of-text install instructions, outdated badges, copy-paste boilerplate that doesn't match the project.
3. **Error handling** — Define behavior for edge cases: empty project, no package.json, monorepo with multiple READMEs.
4. **Input contract** — Accept optional arguments like target directory path or mode override (create/review).
5. **Review output format** — Define a template for review findings (e.g., line number, current text, suggested improvement, why).
