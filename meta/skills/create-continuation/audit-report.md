# Audit Report: create-continuation

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 8 trigger phrases: "switch sessions", "context limits", "hand off work", "continue later", "save context", "continuation prompt", "prepare a handoff" |
| 2 | WHAT + WHEN | ✅ | What: "Generate a continuation prompt to paste into a new conversation". When: session switching, context limits, handoff |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "continuation" or "handoff."` |
| 4 | Under 500 lines | ✅ | 75 lines |
| 5 | Imperative form | ✅ | "Analyze the full conversation", "Run `git status`", "Copy to clipboard" |
| 6 | Constraints reasoned | ✅ | Anti-patterns all include reasoning: "Pasting code wastes tokens and goes stale immediately" (line 72), "cause the next session to act without confirming" (line 73) |
| 7 | Numbered steps | ✅ | 6 numbered steps |
| 8 | Output formats defined | ✅ | Full example structure with framing header (lines 22-55) |
| 9 | Input contract | ⚠️ | No explicit required/optional — implicitly requires an active conversation with work history, but this is not stated |
| 10 | Quality repeated at key points | ⚠️ | Guidelines section exists but quality isn't reinforced at individual steps |
| 11 | Anti-patterns named | ✅ | 5 anti-patterns with reasoning (lines 69-75): too long, full diffs, imperative language, forgetting decisions, omitting branch context |
| 12 | Refinement step | ❌ | No review/refinement step before outputting. Skill generates and presents — no self-check against the anti-patterns |
| 13 | Error handling | ⚠️ | Mentions "inform the user if neither is available" for clipboard, but no handling for: no git repo, no commits, no issue found |
| 14 | Standard layout | ✅ | SKILL.md + README. No references needed at 75 lines |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ✅ | No cross-skill dependencies |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set |

## Score: 12/16

## Priority fixes (ordered by impact)

1. **Refinement step** — Add a step after generation that reviews the prompt against the anti-patterns list (length check, no code blocks, no imperative language, includes branch/issue).
2. **Error handling** — Add handling for edge cases: no git repo, no commits on branch, no identifiable issue. These are common in early-stage projects.
3. **Input contract** — State that the skill requires an active conversation with work history. Define behavior when conversation is minimal (e.g., user just started and wants to hand off immediately).
4. **Quality at key points** — Add a length check reminder at the output step: "If the prompt exceeds ~40 lines, summarize further."
