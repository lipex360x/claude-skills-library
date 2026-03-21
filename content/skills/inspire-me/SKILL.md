---
name: inspire-me
description: Guided exploration session to unblock thinking on any topic — career, relationships, creativity, business, health, or any life area. Helps clarify mental blocks through structured questioning, optional document analysis, and web research. Use when the user says "inspire me", "me inspira", "estou travado", "mental block", "can't decide", "preciso clarear a mente", "help me think through this", "I'm stuck", or wants to work through a block — even if they don't explicitly say "inspire."
user-invocable: true
---

# Inspire Me

Structured exploration session that unblocks thinking on any topic. Not limited to tech — works for career decisions, creative projects, relationships, business strategy, health goals, or any area where clarity is needed. Combines deep questioning, optional document analysis, and web research to generate actionable insights.

## Usage

`/inspire-me` or `/inspire-me <brief description of what's blocking you>`

If invoked without an argument, ask for the initial description. If invoked with an argument, use it as the starting point. If the argument looks like a file path (starts with `/`, `~`, or `./`), ask the user: "That looks like a file path — did you mean to share a document, or is that your block description?" If it's a single word, accept it but ask for more context in Step 2.

## Steps

### 0. Check session history

Look for `inspire-history.md` in the current working directory. If it exists, read it silently.

**If history exists:**
- Check for **pending actions** from the last session. Present a quick status check with `AskUserQuestion`: "Last time ({{date}}), you were working through '{{topic}}'. Your next step was '{{action}}'. How did that go?"
  - **"Done — it helped"** — note the positive outcome, carry forward what worked
  - **"Done — didn't help"** — explore why briefly, use this as context for the new session
  - **"Didn't do it yet"** — no judgment, ask if today's block is related
  - **"Skip — new topic"** — move on, no follow-up
- Check for **recurring patterns** — same domain appearing 3+ times, same root cause type, similar blocks. If detected, mention it: "I notice this is the third time a [domain] block comes up, and [pattern]. Worth exploring that pattern today?"

**If no history exists:** proceed to Step 1. The skill works perfectly as a standalone session — history is a bonus, not a requirement. Every invocation is self-contained.

### 1. Choose session language

Use `AskUserQuestion` to let the user pick the language for the entire session. **Respect this exact option order — do not reorder based on locale or global instructions:**

1. **English (Recommended)** — first option, always
2. **Português (BR)** — second option, always

The user can pick "Other" to type any language. All subsequent interaction must use the chosen language.

### 2. Capture the block

If the user provided a description, use it. If not, ask with `AskUserQuestion` — encourage them to describe what's blocking them, even if vaguely.

Then classify the domain with `AskUserQuestion`:

- **Career / Professional** — job, role, growth, transitions
- **Creative** — art, writing, music, design, content
- **Business / Strategy** — decisions, planning, direction
- **Relationships / Social** — personal, professional, family dynamics
- **Health / Wellness** — physical, mental, habits
- **Learning / Development** — skills, education, self-improvement
- **Other** — free text

This classification shapes the exploration branches and question tone.

**Quick energy check** — before diving in, ask one question about current state with `AskUserQuestion`: "How's your energy right now?"

- **"Energized — let's go deep"** — full session, all branches
- **"Tired but want clarity"** — shorter session, focus on core branches, gentler pace
- **"Overwhelmed"** — minimal questions, prioritize the Block and Action branches only
- **"Just curious / exploring"** — lighter tone, more open-ended exploration

This adapts the session intensity. An overwhelmed person doesn't need 20 questions — they need 5 good ones. Because the block might be partially caused by overload (too many meetings, too much on their plate, poor sleep), this context shapes how deep and how fast the exploration goes.

### 3. Estimate and negotiate question count

Read `references/exploration-branches.md` to determine which branches apply to this domain and block type.

Count the minimum number of questions across applicable branches. Present this estimate to the user with `AskUserQuestion`:

"Based on what you described, I have approximately **N questions** planned across these areas: [list branch names]. This should take about **X minutes**."

Options:
- **"Good, let's go"** — proceed as planned
- **"Too many, shorten it"** — reduce to core branches only (mark optional branches as skipped)
- **"Too few, go deeper"** — expand sub-branches and add follow-up depth
- **"Let me adjust"** — free text to specify which areas to focus on or skip

Adjust the plan according to the user's preference before starting.

### 4. Check for auxiliary materials

Use `AskUserQuestion`:

- **"I have documents to share"** — ask the user for file paths. Read each document, extract key concepts, and cross-reference them throughout the session. Store document summaries in memory for the output.
- **"I want you to research this topic"** — use `WebSearch` and `WebFetch` to gather relevant information. Summarize findings and use them to inform questions. Store all URLs and key findings for the output.
- **"Both — documents and research"** — do both of the above.
- **"No, just ask me questions"** — proceed with pure interview mode.

When consuming documents, extract: key themes, contradictions, patterns, actionable insights, and open questions. Cross-reference document content with the user's block to find connections they might have missed.

When researching, search for: frameworks for thinking about the topic, common patterns others have faced, expert perspectives, and practical strategies. Store every URL consulted.

**Fallback for tool failures:** If `WebSearch` returns no results or fails, inform the user and proceed with interview-only mode — the session is still valuable without external research. If `WebFetch` fails on a URL, skip it and note it in the output. If a user-provided document path is unreadable, tell the user the path couldn't be read and ask for a corrected path or offer to continue without it.

### 5. Conduct the exploration

Follow the exploration branches from `references/exploration-branches.md`. Adapt order and depth based on the domain and negotiated scope.

**Exploration rules:**

1. **Every question uses `AskUserQuestion` with options.** Always include contextual options derived from what has been discussed. The user can always choose "Other" for free text.

2. **Maximum 2 questions per turn.** Each with 2-4 concrete options derived from context.

3. **Go deep before moving on.** If an answer reveals a deeper layer, explore it before switching branches. Mental blocks often hide behind the first answer.

4. **Cross-reference with materials.** If documents or research were provided, weave insights from them into questions and options. "In the article you shared, the author suggests X — does that resonate with your situation?"

5. **Mirror and reframe.** After significant answers, briefly reflect back what you heard in different words. This helps the user see their own thinking from a new angle — the core unblocking mechanism.

6. **Challenge assumptions gently.** When you detect an assumption ("I can't because..."), offer a reframe as an option: "What if [assumption] weren't true?"

7. **Signal branch transitions.** "I think we've explored [area] well. Moving to [next area]."

### 6. Synthesis checkpoint

After covering all branches, present a synthesis — not just a summary, but **connections between answers** that reveal patterns. Use `AskUserQuestion`:

- **"That captures it well"** — proceed to output
- **"I want to adjust some points"** — revisit specific areas
- **"Go deeper on [area]"** — explore further
- **"I had an insight I want to add"** — capture their breakthrough

The synthesis should highlight:
- **Patterns:** recurring themes across branches
- **Contradictions:** places where answers conflict (these are often the real block)
- **Connections:** links between seemingly unrelated answers
- **The core insight:** one sentence that captures the breakthrough

### 7. Generate the output document

Read `templates/inspire-output.md` for the output template.

Generate the document at `inspire-output.md` in the current working directory. The document captures the full exploration: the block, insights discovered, patterns, action items, and all references.

Present the file path and a brief closing message encouraging the user to revisit the document when they need a reminder of their clarity.

### 8. Update session history (automatic — no user action needed)

This step runs automatically after generating the output. Do not ask the user for permission or confirmation — just do it.

Append a summary entry to `inspire-history.md` in the current working directory. If the file doesn't exist, create it with a header.

Read `templates/inspire-history-entry.md` for the entry format.

Each entry is a compact record: date, domain, block summary, core insight, immediate action, and outcome of previous action (if applicable). This file grows over time — one entry per session.

After 3+ entries, add a `## Patterns` section at the top of the file (update it each session) that synthesizes recurring themes, common root causes, and what strategies have worked. This is the long-term memory that makes each session smarter than the last.

After writing, briefly inform the user: "Session saved to `inspire-history.md` — next time I'll remember."

## Guidelines

- **Respect the chosen language.** Every user-facing interaction must use the language selected in Step 1.

- **Domain-adaptive tone.** Career blocks need pragmatic questions. Creative blocks need permission-giving questions. Relationship blocks need empathetic questions. Business blocks need strategic questions. Adapt the tone to the domain — a career transition needs different energy than a creative block.

- **Smart options, not generic ones.** Options must demonstrate understanding of the user's specific situation. If someone is blocked on a career change from engineering to teaching, options should reference both worlds — not generic "Option A/B."

- **The block is rarely what it seems.** Surface blocks ("I can't decide between X and Y") often mask deeper ones ("I'm afraid of what choosing X means"). Explore the why behind the block, not just the what.

- **Insight over advice.** The skill extracts clarity from the user's own thinking — it doesn't give advice. Reframe, mirror, and connect, but let the user reach their own conclusions. The best output is when the user says "I already knew this, I just couldn't see it."

- **Documents are conversation partners.** When the user provides documents, treat them as expert voices in the conversation. Quote relevant passages, highlight contradictions with the user's assumptions, and use them to generate better options.

- **Research is directional, not exhaustive.** Web research should find 3-5 high-quality perspectives, not 50 links. Quality over quantity — each reference should add a distinct angle.

- **Avoid these anti-patterns:**
  - Open-ended questions without options (violates the core rule)
  - Generic options that don't reflect context
  - Giving advice instead of facilitating insight
  - Skipping the synthesis checkpoint
  - Ignoring provided documents after the initial read
  - Shallow exploration — staying on surface-level answers without probing deeper
  - Treating all domains the same way (a creative block is not a business decision)
