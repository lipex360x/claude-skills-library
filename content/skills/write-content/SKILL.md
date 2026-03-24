---
name: write-content
description: >-
  Help the user create compelling written content and marketing copy — LinkedIn
  posts, articles, social media, memos, emails, landing pages, headlines, CTAs,
  value propositions — that sounds authentically like them and drives action. Use
  when the user says "write a post", "review this text", "polish this draft",
  "write copy for", "improve this copy", "rewrite this page", "marketing copy",
  "headline help", "CTA copy", "value proposition", "tagline", "hero section",
  "make this more compelling", or wants content that is clear, concise, and
  persuasive — even if they don't explicitly say "written" or "copywriting."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - WebSearch
---

# Write Content

Create compelling written content and persuasive copy that sounds like the user wrote it — not like AI. Combines storytelling science, conversion copywriting principles, insights from 38 product leaders, and the user's personal voice profile.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `format` | conversation | yes | One of: post, article, email, memo, landing-page, tagline, headline | AUQ with format options |
| `audience` | conversation | yes | Non-empty string describing target readers | AUQ: "Who is reading this?" |
| `goal` | conversation | yes | What the reader should feel, think, or do | AUQ: "What should the reader do after reading?" |
| `tone-register` | conversation | no | Defaults to voice profile | — |
| `page-type` | conversation | marketing only | homepage, landing, pricing, feature, about | AUQ with page type options |
| `primary-action` | conversation | marketing only | What visitors should do | AUQ: "What is the ONE action visitors should take?" |
| `problem` | conversation | marketing only | Audience problem to solve | AUQ: "What problem is the audience trying to solve?" |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Draft file | `./draft-{slug}.md` | yes | Markdown with YAML frontmatter |
| Review checklist | stdout | no | Markdown checklist |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Voice profile | `~/.brain/memory/voice-profile.md` | R | Markdown |
| Product marketing context | project root (if exists) | R | Markdown |
| Copy frameworks | `references/copy-frameworks.md` | R | Markdown |
| Guest insights | `references/guest-insights.md` | R | Markdown |
| Natural transitions | `references/natural-transitions.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Voice profile exists at `~/.brain/memory/voice-profile.md` → if missing: AUQ with options `["Run /capture-voice first", "Describe my style manually"]` — stop if neither.
2. User provided format, audience, and goal → if missing any: AUQ to gather required inputs.
3. If marketing copy: user provided page-type, primary-action, and problem → if missing: AUQ to gather.
4. If product-marketing-context file exists in project root, read it and only ask for gaps.

</pre_flight>

## Steps

### 1. Load voice profile

Read the user's voice profile from `~/.brain/memory/voice-profile.md`. This is the foundation — every piece of content must sound like the user wrote it. The profile contains vocabulary, sentence rhythm, tone, rhetorical devices, and punctuation style.

### 2. Clarify intent

Gather required inputs per the Input contract. For marketing copy, also gather page-type, primary-action, problem, differentiators (optional), and proof points (optional).

Use `AskUserQuestion` with concrete options when the user gives a vague brief.

### 3. Choose the structure

Pick the best framework for the content type:

**ABT (And, But, Therefore) — universal backbone:**
Context (And) → Conflict (But) → Resolution (Therefore). Forces narrative tension into even a single paragraph.

**Story Circle — for narrative posts:**
Simplified hero's journey. For short-form, hit at minimum: comfort (1), need (2), find (5), change (8).

**Pixar's Story Spine — for storytelling:**
"Once upon a time… Every day… One day… Because of that… Until finally…" Each "because of that" creates causal chain — consequence, not sequence.

**StoryBrand — when the reader is the hero:**
You are the guide, not the hero. The reader has a problem. You offer a plan. Show success and failure cost.

**Pyramid Principle — for business writing:**
Conclusion first, supporting evidence below. The reader gets the point from the first paragraph alone.

**Problem-Solution-Benefit — for marketing copy:**
Articulate the problem better than the reader can. Present solution. Show specific outcome. Read `references/copy-frameworks.md` for headline formulas, page templates, and section-by-section guidance.

### 4. Draft with voice and precision

Write the first draft applying the voice profile and chosen structure.

**Hook (first 210 characters — you have 300ms):**
LinkedIn truncates here. This is the only line that matters for "see more" clicks.
- **Data hook**: specific numbers that create contrast ("5 dias. 80 commits. Zero experiência com IA.")
- **Contrarian hook**: challenge a belief ("Stop networking. It's ruining your career.")
- **Confession hook**: vulnerability that creates trust ("I almost quit last week.")
- **Curiosity gap**: open loop that demands resolution ("There's one thing nobody tells you about [X].")
- Never use: "I'm excited to announce...", "In today's world...", "Have you ever wondered...?" — these are the most recognized AI writing tells.

**Narrative arc:**
- **Open loops** — start a thread without closing it (Zeigarnik effect).
- **One peak moment** — every piece needs one moment of high intensity. The peak-end rule means this moment and the ending are disproportionately remembered.
- **Causal chains, not lists** — "because of that" beats "and then."
- **The guide, not the hero** — show the work, let readers draw conclusions.

**Copywriting principles:**
- Clarity over cleverness — "Use" not "utilize," "help" not "facilitate."
- Benefits over features — features are what it does; benefits are what that means for the reader.
- Specificity over vagueness — "Cut weekly reporting from 4 hours to 15 minutes" beats "Save time."
- Customer language over company language — mirror how the audience talks about their problems.
- Active over passive, confident over qualified, show over tell, honest over sensational.

**Voice authenticity:**
- Use the user's actual expressions, not polished equivalents. If the profile says "pô", use "pô."
- Match sentence rhythm: short imperatives mixed with occasional longer reflections.
- Preserve code-switching (pt-BR + English technical terms without translation).

**Content quality (from 38 product leaders):**
- Focus on the *how*, not the *what* — readers want specifics (Wes Kao).
- Concision is density, not brevity — every sentence must carry weight (Wes Kao).
- Specificity is credibility — "347 to 12,400 in 6 months" beats "I grew my audience" (Claude Hopkins).
- Start right before you get eaten by the bear — cut the preamble, begin at highest tension (Wes Kao).

Read `references/guest-insights.md` for all 61 insights from 38 guests.

**Transitions:**
- Never jump topics without a bridge. Use the last image/idea of a section to introduce the next.
- If two paragraphs feel disconnected, either the connection is missing or one doesn't belong.

Read `references/natural-transitions.md` for transition phrase libraries and AI tells to avoid.

### 5. CTA copy (for marketing pages)

**Weak CTAs (avoid):** Submit, Sign Up, Learn More, Click Here, Get Started — generic labels that don't tell the reader what they'll get.

**Strong CTAs:** Start Free Trial, Get [Specific Thing], See [Product] in Action, Create Your First [Thing].

**Formula:** [Action Verb] + [What They Get] + [Qualifier if needed]

### 6. Review against checklist

Before presenting the draft, validate every item. Present the results to the user.

**Story structure:**
- [ ] ABT backbone identifiable?
- [ ] Clear peak moment?
- [ ] Strong ending? (peak-end rule)
- [ ] Open loops that keep the reader scrolling?
- [ ] Causal connections between sections?

**Voice and authenticity:**
- [ ] Sounds like the user wrote it?
- [ ] No AI tells? ("In today's world...", "Let me share...", "I'm excited to announce...")
- [ ] User positioned as guide/builder, not guru/teacher?

**Hook and attention:**
- [ ] Opening creates tension or curiosity in first 210 characters?
- [ ] Preamble cut? (first 2 paragraphs are usually candidates)

**Content quality:**
- [ ] Every paragraph passes the "so what?" test?
- [ ] Claims specific, not vague? (numbers > adjectives)
- [ ] CTA clear?

**Platform limits:**
- [ ] Character count verified with `wc -c`. LinkedIn: 1000-1500 regular, up to 3000 narrative. Trim before presenting.

**Copywriting quality (marketing copy):**
- [ ] No jargon, no passive voice, no exclamation points, no buzzwords without substance?

### 7. Polish, don't add

Ask: "How can I make what's here more polished?" — not "What else can I add?" Tighten sentences, strengthen verbs, cut filler.

### 8. Present and iterate

Present the draft with brief notes on key decisions. Iterate based on feedback — refine what exists, don't add more.

### 9. Refinement mode (`r:`)

When the user sends a message starting with `r:`, treat it as a refinement request on the last draft. Apply changes while keeping all principles active. After applying:
1. Re-run `wc -c` to verify platform limits.
2. Flag if a change conflicts with a principle — explain briefly and suggest alternative. If user insists, apply it.
3. Save updated version to same file (increment version in frontmatter).

**Draft file convention:** Save drafts as `draft-{slug}.md` with frontmatter:
```yaml
---
type: draft
format: linkedin-post | article | email | landing-page | tagline
version: 1
date: YYYY-MM-DD
---
```

### 10. Report

<report>

Present concisely:
- **Format:** content type and structure framework used
- **Draft:** file path and character count
- **Checklist:** summary of review results (pass/warn/fail)
- **Voice match:** confidence level based on profile alignment
- **Audit results:** content audit summary
- **Errors:** issues encountered (or "none")

</report>

## Next action

Share the draft with the intended audience, or run `r:` with refinement instructions for another iteration.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — voice profile loaded, all required inputs gathered
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — draft file created at declared path with correct frontmatter
4. **Voice match?** — re-read draft against voice profile for tone drift
5. **Anti-patterns clean?** — scan draft for AI tells and generic hooks
6. **Platform limits respected?** — character count within bounds for target platform

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Voice fidelity?** — compare draft vocabulary, sentence rhythm, and tone against voice profile markers. Flag any sentence that sounds more like "AI writing" than the user's natural voice
2. **Hook effectiveness?** — first 210 characters create genuine tension or curiosity, not generic openings
3. **Claim accuracy?** — all statistics, quotes, and factual claims are verifiable. Use WebSearch to confirm any claim not provided directly by the user
4. **Structure coherence?** — chosen framework (ABT, Story Circle, etc.) is consistently applied throughout, not abandoned mid-draft
5. **Persuasion integrity?** — benefits are real and specific, not fabricated or exaggerated. CTAs match actual offering
6. **Platform compliance?** — character count, formatting, and conventions match target platform requirements

Audit is scoped to content generated in THIS session.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Voice profile missing | AUQ: "Run `/capture-voice` or describe your style" → stop if neither |
| Product context file not found | Proceed without — gather all context from user |
| `wc -c` unavailable | Estimate character count manually, warn user |
| Draft file write fails | Present draft in stdout, warn about file creation failure |
| User brief too vague | AUQ with concrete options to narrow scope |

## Anti-patterns

- **AI voice.** "I'm thrilled to share...", "In an era of...", "Let me take you on a journey..." — because these are instant credibility killers that signal AI-generated content to experienced readers.
- **Over-explaining.** Show, don't explain. "Here's what I built" beats "Let me walk you through my thought process..." — because verbose preambles lose readers before the content starts.
- **Polishing away personality.** "rsrsrs" in the right context is more authentic than a perfectly structured paragraph — because voice fidelity matters more than grammatical perfection.
- **Generic hooks.** "Have you ever wondered...?" is dead — because readers have seen it thousands of times and scroll past instantly.
- **AAA (And, And, And).** Listing facts without conflict — because no tension means no engagement. Always have a "but."
- **Topic jumps.** Switching emotional → technical without a bridge — because the reader's brain needs a transition to follow.
- **Vague superlatives.** "Great results", "amazing tool" — because specificity is credibility; vagueness is forgettable.
- **Hero positioning.** "I'm going to teach you..." — because the user is a builder sharing the journey, not a guru lecturing.
- **Post-climax appendix.** Adding new sections after the peak moment — because it weakens the ending per peak-end rule.
- **Adding instead of polishing.** When the draft needs work, AI tends to add more rather than refine what exists — because more words rarely equal better content.

Read `references/storytelling-science.md` for the neuroscience behind these patterns (dopamine, mirror neurons, oxytocin, Zeigarnik effect, peak-end rule).

## Guidelines

- **Voice is non-negotiable.** Every piece of content must sound like the user wrote it. When in doubt between "correct" and "authentic," choose authentic — because AI-sounding content defeats the entire purpose of this skill.

- **Density over length.** Concision is not brevity — it is ensuring every sentence carries weight. Cut filler words, redundant stats, and recap paragraphs — because readers respect their time being valued.

- **Structure serves story.** Choose the framework (ABT, Story Circle, Pyramid) that best serves the content, not the one that's easiest to fill — because forcing content into the wrong structure produces awkward writing.

- **Platform-aware writing.** LinkedIn: 210-char hook, 1000-3000 chars, generous line breaks, 3-5 hashtags, end with specific question (comments > likes). Marketing pages: one idea per section, logical persuasive flow toward CTA. Read `references/copy-frameworks.md` for page structure templates.

- **Iterate, don't restart.** When the user gives feedback, refine the existing draft. Starting over wastes the thinking embedded in the current version — because first drafts capture insights that rewrites often lose.
