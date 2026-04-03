---
name: inspire-me
description: >-
  Guided exploration session to unblock thinking on any topic — career,
  relationships, creativity, business, health, or any life area. Helps clarify
  mental blocks through structured questioning, optional document analysis, and
  web research. Use when the user says "inspire me", "me inspira", "estou
  travado", "mental block", "can't decide", "preciso clarear a mente", "help me
  think through this", "I'm stuck", or wants to work through a block — even if
  they don't explicitly say "inspire."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - WebSearch
  - WebFetch
argument-hint: "[brief description of what's blocking you]"
---

# Inspire Me

Structured exploration session that unblocks thinking on any topic — career, creative, business, relationships, health, or learning. Combines deep questioning, optional document analysis, and web research to generate actionable insights.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `block-description` | $ARGUMENTS | no | Non-empty string | AUQ: "What's blocking you?" |

If invoked without an argument, ask for the initial description. If the argument looks like a file path (starts with `/`, `~`, or `./`), ask the user: "That looks like a file path — did you mean to share a document, or is that your block description?" If it's a single word, accept it but ask for more context in Step 3.

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Exploration document | `inspire-output.md` (cwd) | yes | Markdown per `templates/inspire-output.md` |
| Session history entry | `inspire-history.md` (cwd) | yes | Markdown per `templates/inspire-history-entry.md` |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Session history | `inspire-history.md` (cwd) | R/W | Markdown |
| Exploration branches | `references/exploration-branches.md` | R | Markdown |
| Output template | `templates/inspire-output.md` | R | Markdown |
| History entry template | `templates/inspire-history-entry.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Check for `inspire-history.md` in current working directory → if exists: read silently, check for pending actions and recurring patterns (used in Step 1).
2. Verify `references/exploration-branches.md` is readable → if not: "Missing exploration branches reference." — stop.
3. Verify `templates/inspire-output.md` is readable → if not: "Missing output template." — stop.
4. Verify `templates/inspire-history-entry.md` is readable → if not: "Missing history entry template." — stop.
5. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Check session history

If `inspire-history.md` exists (loaded in pre-flight):

- Check for **pending actions** from the last session. Present a quick status check with `AskUserQuestion`: "Last time ({{date}}), you were working through '{{topic}}'. Your next step was '{{action}}'. How did that go?"
  - **"Done — it helped"** — note the positive outcome, carry forward what worked
  - **"Done — didn't help"** — explore why briefly, use this as context for the new session
  - **"Didn't do it yet"** — no judgment, ask if today's block is related
  - **"Skip — new topic"** — move on, no follow-up
- Check for **recurring patterns** — same domain appearing 3+ times, same root cause type, similar blocks. If detected, mention it: "I notice this is the third time a [domain] block comes up, and [pattern]. Worth exploring that pattern today?"

If no history exists, proceed to Step 2. Every invocation is self-contained — history is a bonus, not a requirement.

### 2. Choose session language

Use `AskUserQuestion` to let the user pick the language. **Respect this exact option order — do not reorder based on locale or global instructions:**

1. **English (Recommended)** — first option, always
2. **Português (BR)** — second option, always

The user can pick "Other" to type any language. All subsequent interaction must use the chosen language.

### 3. Capture the block

If the user provided a description, use it. If not, ask with `AskUserQuestion` — encourage them to describe what's blocking them, even if vaguely.

Then classify the domain with `AskUserQuestion`:

- **Career / Professional** — job, role, growth, transitions
- **Creative** — art, writing, music, design, content
- **Business / Strategy** — decisions, planning, direction
- **Relationships / Social** — personal, professional, family dynamics
- **Health / Wellness** — physical, mental, habits
- **Learning / Development** — skills, education, self-improvement
- **Other** — free text

**Quick energy check** — ask one question about current state with `AskUserQuestion`: "How's your energy right now?"

- **"Energized — let's go deep"** — full session, all branches
- **"Tired but want clarity"** — shorter session, focus on core branches, gentler pace
- **"Overwhelmed"** — minimal questions, prioritize the Block and Action branches only
- **"Just curious / exploring"** — lighter tone, more open-ended exploration

This adapts session intensity — an overwhelmed person needs 5 good questions, not 20.

### 4. Estimate and negotiate question count

Read `references/exploration-branches.md` to determine which branches apply to this domain and block type.

Count the minimum number of questions across applicable branches. Present this estimate with `AskUserQuestion`:

"Based on what you described, I have approximately **N questions** planned across these areas: [list branch names]. This should take about **X minutes**."

Options:
- **"Good, let's go"** — proceed as planned
- **"Too many, shorten it"** — reduce to core branches only (mark optional branches as skipped)
- **"Too few, go deeper"** — expand sub-branches and add follow-up depth
- **"Let me adjust"** — free text to specify which areas to focus on or skip

### 5. Check for auxiliary materials

Use `AskUserQuestion`:

- **"I have documents to share"** — ask for file paths, read each, extract key concepts, cross-reference throughout the session
- **"I want you to research this topic"** — use `WebSearch` and `WebFetch` to gather relevant information, store URLs and findings
- **"Both — documents and research"** — do both
- **"No, just ask me questions"** — proceed with pure interview mode

When consuming documents, extract: key themes, contradictions, patterns, actionable insights, and open questions. When researching, search for: frameworks, common patterns, expert perspectives, and practical strategies.

### 6. Conduct the exploration

Follow the exploration branches from `references/exploration-branches.md`. Adapt order and depth based on the domain and negotiated scope.

**Exploration rules:**

1. **Every question uses `AskUserQuestion` with options.** Always include contextual options derived from what has been discussed. The user can always choose "Other" for free text.
2. **Maximum 2 questions per turn.** Each with 2-4 concrete options derived from context.
3. **Go deep before moving on.** If an answer reveals a deeper layer, explore it before switching branches — mental blocks often hide behind the first answer.
4. **Cross-reference with materials.** If documents or research were provided, weave insights into questions and options.
5. **Mirror and reframe.** After significant answers, briefly reflect back what you heard in different words — the core unblocking mechanism.
6. **Challenge assumptions gently.** When you detect an assumption ("I can't because..."), offer a reframe as an option: "What if [assumption] weren't true?"
7. **Signal branch transitions.** "I think we've explored [area] well. Moving to [next area]."

### 7. Synthesis checkpoint

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

### 8. Generate the output document

Read `templates/inspire-output.md` for the output template.

Generate the document at `inspire-output.md` in the current working directory. The document captures the full exploration: the block, insights discovered, patterns, action items, and all references.

Present the file path and a brief closing message encouraging the user to revisit the document when they need a reminder of their clarity.

### 9. Update session history

This step runs automatically — no user confirmation needed.

Append a summary entry to `inspire-history.md` in the current working directory. If the file doesn't exist, create it with a header. Read `templates/inspire-history-entry.md` for the entry format.

After 3+ entries, add or update a `## Patterns` section at the top of the file that synthesizes recurring themes, common root causes, and what strategies have worked.

Briefly inform the user: "Session saved to `inspire-history.md` — next time I'll remember."

### 10. Report

<report>

Present concisely:
- **Session summary** — domain, block description, core insight discovered
- **Artifacts created** — `inspire-output.md` path, `inspire-history.md` updated
- **Materials used** — documents analyzed, web sources consulted (or "none")
- **Audit results** — self-audit + content audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

</report>

## Next action

Revisit `inspire-output.md` when the block resurfaces. Run `/inspire-me` again for a follow-up session — history tracking will detect patterns across sessions.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — all templates and references were readable
2. **Language respected?** — all user-facing interaction used the language chosen in Step 2
3. **Steps completed?** — list any skipped steps with reason
4. **Output exists?** — `inspire-output.md` was created, `inspire-history.md` was updated
5. **Question rules followed?** — every question used AskUserQuestion with contextual options, max 2 per turn
6. **Anti-patterns clean?** — no advice given (insight only), no generic options, synthesis checkpoint not skipped

If any check fails, note it in the Report. Do not block — report the gap and let the user decide.

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Core insight accurate?** — the breakthrough sentence in `inspire-output.md` reflects what the user actually expressed, not an interpretation or projection
2. **Action items actionable?** — immediate next step is concrete and achievable (not vague like "think about it more"), short-term actions have clear timeframes
3. **Patterns genuine?** — patterns section reflects actual recurring themes from the session, not forced connections between unrelated answers
4. **Contradictions surfaced?** — if the user's answers conflicted, these are documented in the output (contradictions are often the real block)
5. **References accurate?** — all document summaries correctly represent source content, all URLs from web research are included and findings attributed correctly
6. **User's voice preserved?** — block description and insights use the user's own words and framing, not sanitized or rewritten versions
7. **History entry consistent?** — the entry in `inspire-history.md` matches the session outcome (domain, insight, action)

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `WebSearch` returns no results | Inform user, proceed with interview-only mode — session is still valuable |
| `WebFetch` fails on a URL | Skip URL, note in output References section |
| User-provided document path unreadable | Tell user, ask for corrected path or offer to continue without it |
| `inspire-history.md` unwritable | Report error, present history entry in stdout for manual saving |
| Template file missing | Stop — templates are required for consistent output |

## Anti-patterns

- **Giving advice instead of facilitating insight.** The skill extracts clarity from the user's own thinking — because advice creates dependency while insight creates autonomy. Reframe, mirror, and connect, but let the user reach their own conclusions.
- **Open-ended questions without options.** Every question must use AskUserQuestion with contextual options — because unstructured prompts produce vague answers and slow the session.
- **Generic options that don't reflect context.** Options must demonstrate understanding of the user's specific situation — because "Option A/B/C" options signal that the skill isn't listening.
- **Skipping the synthesis checkpoint.** Always present connections between answers before generating output — because the synthesis is where breakthroughs happen, not the individual questions.
- **Shallow exploration.** Staying on surface-level answers without probing deeper — because mental blocks hide behind the first answer, and the real insight requires going one layer further.
- **Treating all domains the same way.** A creative block needs permission-giving energy, a career block needs pragmatic questions, a relationship block needs empathy — because one-size-fits-all questioning produces generic insights.
- **Ignoring provided documents after initial read.** Documents are conversation partners throughout the session — because isolated document analysis wastes the user's effort in sharing them.

## Guidelines

- **Respect the chosen language.** Every user-facing interaction must use the language selected in Step 2 — because switching languages mid-session breaks immersion and trust.

- **Domain-adaptive tone.** Career blocks need pragmatic questions. Creative blocks need permission-giving questions. Relationship blocks need empathetic questions. Business blocks need strategic questions — because the tone shapes the quality of introspection.

- **Smart options, not generic ones.** Options must reference the user's specific situation — because contextual options demonstrate listening and generate deeper answers.

- **The block is rarely what it seems.** Surface blocks ("I can't decide between X and Y") often mask deeper ones ("I'm afraid of what choosing X means") — because exploring the why behind the block, not just the what, leads to real breakthroughs.

- **Insight over advice.** The best output is when the user says "I already knew this, I just couldn't see it" — because extracted clarity lasts longer than external recommendations.

- **Documents are conversation partners.** Quote relevant passages, highlight contradictions with the user's assumptions, and use them to generate better options — because documents contain perspectives the user may have overlooked.

- **Research is directional, not exhaustive.** Find 3-5 high-quality perspectives, not 50 links — because each reference should add a distinct angle, and quantity drowns signal.
