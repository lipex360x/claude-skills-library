# Audit Report: inspire-me

Plugin: content
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: Pushy enough? | PASS | Lists 9 trigger phrases including "estou travado", "mental block", "I'm stuck", "help me think through this" (line 3) |
| 2 | Description: WHAT + WHEN? | PASS | States what ("Guided exploration session to unblock thinking") and when ("Use when the user says...") in the description field (line 3) |
| 3 | Description: "Even if" pattern? | PASS | Includes "even if they don't explicitly say 'inspire.'" (line 3) |
| 4 | Body: Under 500 lines? | PASS | SKILL.md is 177 lines, well under the 500-line limit |
| 5 | Body: Imperative form? | PASS | Uses imperative throughout: "Capture the block" (line 42), "Classify the domain" (line 46), "Cross-reference all inputs" (line 102 of exploration-branches.md) |
| 6 | Body: Constraints reasoned? | PASS | Constraints include reasoning, e.g., "Because the block might be partially caused by overload..." (line 65), "Mental blocks often hide behind the first answer" (line 107) |
| 7 | Body: Numbered steps? | PASS | 9 numbered steps (0-8), clearly ordered |
| 8 | Body: Output formats defined? | PASS | Two templates defined: `inspire-output.md` (86 lines, detailed sections) and `inspire-history-entry.md` (40 lines) |
| 9 | Body: Input contract? | PARTIAL | Accepts optional argument (`/inspire-me <description>`) and handles missing input (line 15), but no explicit validation rules for malformed input |
| 10 | Quality: Repeated at key points? | PASS | Quality guidance woven throughout: domain-adaptive tone (line 157), smart options (line 159), insight over advice (line 163), exploration rules (lines 100-114) |
| 11 | Quality: Anti-patterns named? | PASS | 7 explicit anti-patterns listed at lines 169-176: open-ended questions without options, generic options, giving advice, skipping synthesis, ignoring documents, shallow exploration, treating all domains the same |
| 12 | Quality: Refinement step? | PASS | Synthesis checkpoint (Step 6, lines 116-130) with options to adjust, go deeper, or add insights |
| 13 | Quality: Error handling patterns? | PARTIAL | Handles missing input (line 15), missing history (line 31), and user energy adaptation (lines 58-65), but no handling for WebSearch/WebFetch failures or unreadable documents |
| 14 | Testing: Invoked with realistic input? | FAIL | No evidence of testing with realistic input in any file |
| 15 | Testing: Activation tested (3+ trigger phrases)? | FAIL | No testing evidence; trigger phrases are defined but not verified |
| 16 | Testing: Failure modes checked? | FAIL | No failure mode testing documented |
| 17 | Subagents: Agent context complete? | N/A | No subagents used |
| 18 | Subagents: Tool access explicit? | N/A | No subagents used |
| 19 | Subagents: Two-phase build? | N/A | No subagents used |
| 20 | Subagents: Race conditions mitigated? | N/A | No subagents used |
| 21 | Structure: Standard layout? | PASS | Has SKILL.md, references/, templates/ — all present and properly structured |
| 22 | Structure: References one level deep? | PASS | Single reference file at `references/exploration-branches.md`, no nesting |
| 23 | Structure: Large refs have TOC? | PARTIAL | `exploration-branches.md` is 151 lines with 7 branches + a summary table — no TOC, but the summary table at the end (lines 138-150) partially compensates |
| 24 | Structure: Self-contained? | PASS | No cross-skill dependencies. Uses only standard tools (AskUserQuestion, WebSearch, WebFetch, Read) |
| 25 | Structure: README generated? | PASS | README.md present with trigger phrases, how-it-works summary, usage examples, directory structure, and installation command |
| 26 | Compliance: CLAUDE.md compliance? | PASS | Under 500 lines, self-contained, no cross-skill deps, no local paths in public content |

## Score: 19/22

(Excluding 4 N/A subagent checks from denominator)

## Priority fixes (ordered by impact)

1. **Testing: Invoke with realistic input** — No evidence any of the 3 testing checks were performed. Run the skill with at least 2 real scenarios (e.g., career block, creative block) and document results. This is the highest-impact gap because the skill has complex multi-branch flow with 10-25 questions that could break in practice.

2. **Error handling for external tools** — Steps 4 references WebSearch/WebFetch (lines 88-89) but has no guidance for when these tools fail (network errors, no results, blocked sites) or when user-provided document paths are invalid. Add a brief fallback instruction (e.g., "If WebSearch returns no results, inform the user and proceed with interview-only mode").

3. **Input validation** — The input contract (line 15) handles present vs absent argument but doesn't address edge cases: what if the user provides a file path instead of a description? What if the description is a single word? Add brief validation guidance.

4. **TOC for exploration-branches.md** — At 151 lines with 7 branches, adding a linked TOC at the top would improve navigability, especially since the skill reads this file at runtime (Step 3, line 69).
