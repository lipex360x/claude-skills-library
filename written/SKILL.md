---
name: written
description: Help the user create compelling written content and marketing copy — LinkedIn posts, articles, social media, memos, emails, landing pages, headlines, CTAs, value propositions — that sounds authentically like them and drives action. Use when the user says "write a post", "review this text", "polish this draft", "write copy for", "improve this copy", "rewrite this page", "marketing copy", "headline help", "CTA copy", "value proposition", "tagline", "hero section", "make this more compelling", or wants content that is clear, concise, and persuasive — even if they don't explicitly say "written" or "copywriting."
---

# Written

Create compelling written content and persuasive copy that sounds like the user wrote it — not like AI. Combines storytelling science, conversion copywriting principles, insights from 38 product leaders, and the user's personal voice profile.

## Process

### 1. Load voice profile

Read the user's voice profile from `~/.brain/memory/voice-profile.md`. This is the foundation — every piece of content must sound like the user wrote it. The profile contains vocabulary, sentence rhythm, tone, rhetorical devices, and punctuation style.

### 2. Clarify intent

Before writing, understand:
- **Format** — post, article, email, memo, landing page, headline, tagline?
- **Audience** — who is reading? (LinkedIn connections, technical community, customers, investors)
- **Goal** — what should the reader feel, think, or do after reading?
- **Tone register** — the user's default is casual/direct, but some contexts need adjustment

For **marketing copy**, also gather:
- What type of page? (homepage, landing page, pricing, feature, about)
- What is the ONE primary action visitors should take?
- What problem is the audience trying to solve?
- What makes this different from alternatives?
- Any proof points? (numbers, testimonials, case studies)

If `.agents/product-marketing-context.md` exists, read it first and only ask for gaps.

Use `AskUserQuestion` with concrete options when the user gives a vague brief.

### 3. Choose the structure

Pick the best framework for the content type:

**ABT (And, But, Therefore) — universal backbone:**
Context (And) → Conflict (But) → Resolution (Therefore). Forces narrative tension into even a single paragraph. Use as the skeleton of any piece, then layer detail on top.

**Story Circle — for narrative posts:**
Simplified hero's journey: You → Need → Go → Search → Find → Take → Return → Change. For short-form, hit at minimum: comfort (1), need (2), find (5), change (8).

**Pixar's Story Spine — for storytelling:**
"Once upon a time [situation]. Every day [routine]. One day [disruption]. Because of that [consequence]. Because of that [escalation]. Until finally [resolution]." Each "because of that" creates causal chain — consequence, not sequence.

**StoryBrand — when the reader is the hero:**
You are the guide, not the hero. The reader has a problem. You offer a plan. Show success and failure cost. Use when empowering the reader, not showcasing the author.

**Pyramid Principle — for business writing:**
Conclusion first, supporting evidence below. The reader should get the point from the first paragraph alone.

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
- Never use: "I'm excited to announce...", "In today's world...", "Have you ever wondered...?"

**Narrative arc:**
- **Open loops** — start a thread without closing it. The brain treats unresolved information like an open browser tab (Zeigarnik effect).
- **One peak moment** — every piece needs one moment of high intensity: a surprising stat, emotional reveal, or contrarian insight. The peak-end rule means this moment and the ending are disproportionately remembered.
- **Causal chains, not lists** — "because of that" beats "and then." Each event should cause the next, not just follow it.
- **The guide, not the hero** — show the work, let readers draw conclusions. Demonstrate, don't lecture.

**Copywriting principles:**
- **Clarity over cleverness** — if you must choose, choose clear. "Use" not "utilize," "help" not "facilitate."
- **Benefits over features** — features are what it does; benefits are what that means for the reader.
- **Specificity over vagueness** — "Cut weekly reporting from 4 hours to 15 minutes" beats "Save time on your workflow."
- **Customer language over company language** — mirror how the audience actually talks about their problems.
- **Active over passive** — "We generate reports" not "Reports are generated."
- **Confident over qualified** — remove "almost," "very," "really."
- **Show over tell** — describe the outcome instead of using adverbs.
- **Honest over sensational** — fabricated statistics erode trust and create liability.

**Voice authenticity:**
- Use the user's actual expressions, not polished equivalents. If the profile says "pô", use "pô" — not "puxa."
- Match sentence rhythm: short imperatives mixed with occasional longer reflections.
- Preserve code-switching (pt-BR + English technical terms without translation).
- Use punctuation as the user does: "..." for reflective pauses, extended vowels for emotion.

**Content quality (from 38 product leaders):**
- Focus on the *how*, not the *what* — readers already agree with the premise, they want specifics (Wes Kao).
- Concision is density, not brevity — every sentence must carry weight (Wes Kao).
- Full sentences expose logic gaps — bullet fragments hide shallow thinking (Wes Kao).
- Writing clarifies thinking — the draft is a tool for organizing thoughts, not just output (Julie Zhuo).
- Specificity is credibility — "347 to 12,400 in 6 months" beats "I grew my audience" (Claude Hopkins).
- Start right before you get eaten by the bear — cut the preamble, begin at the point of highest tension (Wes Kao).

Read `references/guest-insights.md` for all 61 insights from 38 guests.

**Transitions:**
- Never jump topics without a bridge. Use the last image/idea of a section to introduce the next.
- Emotional → technical transitions need a human connector: "E falando em fazer sozinho... a parte mais solitária foi X."
- If two paragraphs feel disconnected, either the connection is missing or one doesn't belong.

Read `references/natural-transitions.md` for transition phrase libraries and AI tells to avoid.

### 5. CTA copy (for marketing pages)

**Weak CTAs (avoid):** Submit, Sign Up, Learn More, Click Here, Get Started.

**Strong CTAs:** Start Free Trial, Get [Specific Thing], See [Product] in Action, Create Your First [Thing].

**Formula:** [Action Verb] + [What They Get] + [Qualifier if needed]

### 6. Review against checklist

Before presenting the draft, validate every item. This is not optional — present the results to the user.

**Story structure:**
- [ ] Can you identify the ABT (And/But/Therefore) backbone?
- [ ] Is there a clear peak moment (most intense/surprising point)?
- [ ] Does the ending land strong? (peak-end rule — last line is remembered most)
- [ ] Are there open loops that keep the reader scrolling?
- [ ] Does every section connect causally to the next? (no topic jumps without bridges)

**Voice and authenticity:**
- [ ] Does it sound like the user wrote it? Read it imagining their voice.
- [ ] Does it avoid AI tells? (no "In today's world...", no "Let me share...", no "I'm excited to announce...")
- [ ] Is the user positioned as guide/builder, not guru/teacher?

**Hook and attention:**
- [ ] Does the opening create tension or curiosity in the first 210 characters?
- [ ] Is there preamble that can be cut? (first 2 paragraphs are usually candidates)
- [ ] Would you click "see more" if you saw only the first 2 lines while scrolling?

**Content quality:**
- [ ] Does every paragraph pass the "so what?" test?
- [ ] Are claims specific, not vague? (numbers > adjectives)
- [ ] Are technical concepts accessible to non-technical readers?
- [ ] Is the call-to-action clear? (follow, comment, stay tuned, click, buy)

**Platform limits:**
- [ ] Count characters with `wc -c` (exclude frontmatter). LinkedIn: 1000-1500 regular, up to 3000 narrative. If over limit, trim before presenting — don't ask the user to cut.

**Copywriting quality (for marketing copy):**
- [ ] Jargon that could confuse outsiders?
- [ ] Sentences trying to do too much?
- [ ] Passive voice constructions?
- [ ] Exclamation points? (remove them)
- [ ] Marketing buzzwords without substance?

### 7. Polish, don't add

Before finalizing, ask: "How can I make what's here more polished?" — not "What else can I add?" AI tends to add more when the answer is refining what exists. Tighten sentences, strengthen verbs, cut filler.

### 8. Present and iterate

Present the draft with brief notes on key decisions. Iterate based on feedback — refine what exists, don't add more.

### 9. Refinement mode (`r:`)

When the user sends a message starting with `r:`, treat it as a refinement request on the last draft. Apply the user's specific changes while keeping all /written principles active — voice profile, narrative structure, anti-patterns, platform limits, and checklist. After applying changes:
1. Re-run `wc -c` to verify platform limits.
2. Flag if a requested change conflicts with a principle (e.g., "add this paragraph" would push over 3000 chars, or break the peak-end rule). Explain the conflict briefly and suggest an alternative — but if the user insists, apply it.
3. Save the updated version to the same file (increment version in frontmatter).

## Platform-specific guidelines

### LinkedIn
- **Hook**: first 2-3 lines must stop the scroll. No context, no greeting — start with the punch. 210 characters before truncation.
- **Length**: 1000-1500 characters for regular posts. Up to 3000 for narrative/story posts.
- **Line breaks**: generous. White space is readability. One idea per block. Mobile-first.
- **Hashtags**: 3-5 at the end, mix broad (#AI, #OpenSource) with niche (#BuildInPublic, #DevLife).
- **Cliffhanger**: if part of a series, end with curiosity — Zeigarnik effect.
- **Comments > likes**: LinkedIn weights comments 8x more. End with a specific question, not generic "what do you think?"
- **Respond early**: reply to first comments quickly for algorithmic momentum.

### Marketing pages
- Read `references/copy-frameworks.md` for page structure templates (landing, feature, pricing, about, enterprise).
- One idea per section. Build a logical persuasive flow down the page.
- Each section should advance one argument toward the CTA.

## Anti-patterns

- **AI voice** — "I'm thrilled to share...", "In an era of...", "Let me take you on a journey..." — instant credibility killers.
- **Over-explaining** — show, don't explain. "Here's what I built" beats "Let me walk you through my thought process on why I decided to..."
- **Polishing away personality** — "rsrsrs" in the right context is more authentic than a perfectly structured paragraph.
- **Generic hooks** — "Have you ever wondered...?" is dead. Start with a specific, concrete fact or image.
- **Motivational fluff** — no "never give up" energy. Show the work, let results speak.
- **AAA (And, And, And)** — listing facts without conflict. No tension = no engagement. Always have a "but."
- **Topic jumps** — switching emotional → technical without a bridge. The reader's brain needs a transition.
- **Vague superlatives** — "great results", "amazing tool." Specificity is credibility; vagueness is forgettable.
- **Hero positioning** — "I'm going to teach you..." — the user is a builder sharing the journey, not a guru.
- **Redundant stats** — repeating the same number 3+ times dilutes impact. Max 2x: once in narrative, once in climax.
- **Post-climax appendix** — adding new sections after the peak moment weakens the ending. Peak-end rule: cut or move to a follow-up piece.
- **Recap paragraphs** — if the narrative already showed the journey, a summary paragraph is redundant.

## Storytelling science (quick reference)

- **Dopamine** — released in anticipation of learning. Curiosity gaps trigger it. Hook creates the spike, content delivers reward.
- **Mirror neurons** — first-person stories activate mirroring. Show emotion, don't just state facts.
- **Oxytocin** — vulnerability and struggle trigger trust chemistry. Confession hooks outperform tactical ones.
- **Zeigarnik effect** — unfinished tasks stay cognitively active. Open loops and cliffhangers exploit this.
- **Peak-end rule** — people judge by the most intense moment and the ending. Strong ending > consistently good with flat end.
- **Specificity = memory** — novel details trigger dopamine and encode into long-term memory. "139 testes" is remembered; "comprehensive test coverage" is forgotten.
