# Audit Report: find-skills

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ⚠️ | Lists capability questions ("how do I do X", "find a skill for X") but lacks concrete workflow triggers. Missing action verbs that would trigger auto-invocation |
| 2 | WHAT + WHEN | ⚠️ | What: "discover and install agent skills". When: user asks questions — but "looking for functionality that might exist" is vague |
| 3 | "Even if" pattern | ❌ | No "even if" clause in description |
| 4 | Under 500 lines | ✅ | 142 lines |
| 5 | Imperative form | ❌ | Uses descriptive prose: "This skill helps you discover" (line 8), "How to Help Users Find Skills" (line 36). Should be "Discover and install" / "Find skills" |
| 6 | Constraints reasoned | ⚠️ | Some reasoning: "Be cautious with anything under 100" (installs, line 71) but many steps lack "because" justification |
| 7 | Numbered steps | ✅ | 6 numbered steps |
| 8 | Output formats defined | ✅ | Example response format (lines 85-94), example for no results (lines 137-142) |
| 9 | Input contract | ❌ | No explicit required/optional. No $ARGUMENTS handling. No validation rules for search queries |
| 10 | Quality repeated at key points | ❌ | Quality criteria mentioned once in Step 4 (verify quality) but not reinforced elsewhere |
| 11 | Anti-patterns named | ❌ | No anti-patterns section. Common failures like recommending unvetted skills, trusting search results blindly, or installing without user consent are not named |
| 12 | Refinement step | ❌ | No refinement or review step. Skill goes from search → present → install with no validation loop |
| 13 | Error handling | ✅ | "When No Skills Are Found" section (lines 128-142) with fallback behavior |
| 14 | Standard layout | ✅ | SKILL.md + README |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ✅ | No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ❌ | Missing `user-invocable: true` in frontmatter |

## Score: 7/16

## Priority fixes (ordered by impact)

1. **Add `user-invocable: true`** — Frontmatter missing this required field.
2. **"Even if" pattern in description** — Add: `even if they don't explicitly say "find" or "search."` to catch implicit triggers.
3. **Imperative form** — Rewrite "This skill helps you discover" → "Discover and install skills from the open agent skills ecosystem." Rewrite "How to Help Users Find Skills" → "Find skills".
4. **Anti-patterns section** — Add: recommending low-install-count skills, installing without user consent, trusting search results without verification, recommending skills that overlap with already-installed ones.
5. **Input contract** — Define: required (search intent or query), optional ($ARGUMENTS as direct search query). Add validation for empty queries.
6. **Refinement step** — After presenting options, verify the user's choice against quality criteria before installing.
