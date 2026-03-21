# Audit Report: write-content

Plugin: content
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: Pushy enough? | PASS | Lists 12+ trigger phrases including "write a post", "review this text", "polish this draft", "marketing copy", "CTA copy", etc. (line 3) |
| 2 | Description: WHAT + WHEN? | PASS | Describes what ("create compelling written content and marketing copy") and when ("Use when the user says...") in a single sentence (line 3) |
| 3 | Description: "Even if" pattern? | PASS | Includes "even if they don't explicitly say 'written' or 'copywriting'" (line 3) |
| 4 | Under 500 lines? | PASS | SKILL.md is 206 lines, well under the 500-line limit |
| 5 | Imperative form? | PASS | Uses imperative throughout: "Read the user's voice profile" (line 14), "Pick the best framework" (line 37), "Write the first draft" (line 59) |
| 6 | Constraints reasoned? | PARTIAL | Some constraints are reasoned ("LinkedIn truncates here. This is the only line that matters for 'see more' clicks" line 62), but others are bare imperatives without reasoning: "Never use: 'I'm excited to announce...'" (line 67) lacks a "because" clause |
| 7 | Numbered steps? | PASS | 9 clearly numbered steps: "1. Load voice profile" through "9. Refinement mode" |
| 8 | Output formats defined? | PARTIAL | Checklist format defined (lines 121-151), platform limits specified (LinkedIn 1000-1500 chars, line 173), but no explicit output file format or naming convention for saved drafts |
| 9 | Input contract? | PARTIAL | Step 2 lists what to clarify (format, audience, goal, tone register, lines 19-22), and marketing-specific inputs (lines 25-29), but does not distinguish required vs optional inputs or define validation rules |
| 10 | Quality repeated at key points? | PASS | Quality criteria appear in step 4 (copywriting principles, lines 76-83), step 6 (full review checklist, lines 120-151), step 7 (polish guidance, line 155), and anti-patterns section (lines 186-197) |
| 11 | Anti-patterns named? | PASS | 12 anti-patterns explicitly named with explanations (lines 186-197): AI voice, over-explaining, polishing away personality, generic hooks, motivational fluff, AAA, topic jumps, vague superlatives, hero positioning, redundant stats, post-climax appendix, recap paragraphs |
| 12 | Refinement step? | PASS | Step 7 "Polish, don't add" (line 155) and step 9 "Refinement mode (r:)" (lines 161-166) |
| 13 | Error handling patterns? | PARTIAL | Handles vague briefs ("Use AskUserQuestion with concrete options" line 33), conflict between user request and principles (line 165: "Flag if a requested change conflicts with a principle"), but no handling for missing voice profile or missing product-marketing-context |
| 14 | Activation tested (3+ trigger phrases)? | NOT TESTED | No evidence of activation testing in skill files |
| 15 | Invoked with realistic input? | NOT TESTED | No evidence of testing with realistic input |
| 16 | Failure modes checked? | NOT TESTED | No evidence of failure mode testing |
| 17 | Subagents: N/A | N/A | No subagent usage in this skill |
| 18 | Standard layout? | PASS | Has SKILL.md, references/ directory, README.md |
| 19 | References one level deep? | PASS | All references are directly in references/ (copy-frameworks.md, guest-insights.md, natural-transitions.md) |
| 20 | Large refs have TOC? | PASS | All three reference files include a table of contents: copy-frameworks.md (lines 6-9), guest-insights.md (implicit by guest name headers), natural-transitions.md (lines 10-27) |
| 21 | Self-contained (no cross-skill deps)? | FAIL | natural-transitions.md line 272 references another skill: "See the seo-audit skill's `references/ai-writing-detection.md`" |
| 22 | README generated? | PASS | README.md exists with usage, how-it-works, directory structure, and installation sections |
| 23 | CLAUDE.md compliance? | PARTIAL | No local paths (~/.brain/) in public-facing files (README), but SKILL.md line 14 references `~/.brain/memory/voice-profile.md` and line 31 references `.agents/product-marketing-context.md` -- these are user-specific paths that may not exist for all users |

## Score: 15/21

(Excluding 3 NOT TESTED items and 1 N/A from denominator: 15 PASS out of 17 evaluable checks, with 4 PARTIAL and 1 FAIL counting as not passed)

## Priority fixes (ordered by impact)

1. **FAIL: Cross-skill dependency** -- `references/natural-transitions.md` line 272 references `seo-audit skill's references/ai-writing-detection.md`. Either inline the relevant AI tells list into this file or remove the reference. This violates the "self-contained, no cross-skill deps" rule.

2. **PARTIAL: Missing voice profile fallback** -- SKILL.md line 14 says "Read the user's voice profile from `~/.brain/memory/voice-profile.md`" but provides no fallback if the file does not exist. Add error handling: e.g., "If the voice profile does not exist, ask the user to describe their writing style before proceeding."

3. **PARTIAL: Input contract lacks required/optional distinction** -- Step 2 (lines 18-29) lists inputs to gather but never marks which are required vs optional. For example, "Format" and "Goal" seem required, while "Tone register" has a default. Make this explicit.

4. **PARTIAL: Bare constraints without reasoning** -- Line 67 ("Never use: 'I'm excited to announce...'") and line 110 ("Weak CTAs (avoid): Submit, Sign Up, Learn More") lack "because" clauses. Add brief reasoning (e.g., "because they signal AI-generated content and reduce credibility").

5. **PARTIAL: Output file format undefined** -- Step 9 line 166 mentions "Save the updated version to the same file (increment version in frontmatter)" but no step defines where the initial draft is saved, what filename convention to use, or what frontmatter format to follow.
