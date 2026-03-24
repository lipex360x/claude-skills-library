---
name: capture-voice
description: >-
  Analyzes the current conversation to capture the user's writing voice for
  content generation — posts, articles, social media that sound like them, not
  AI-generated. Use this skill when the user runs /capture-voice, when triggered
  by the PreCompact hook, or whenever voice profile analysis is needed. Also use
  it when the user asks to update or check their voice profile, says "meu estilo",
  "como eu falo", "aprenda meu jeito", or wants content that sounds like them —
  even if they don't explicitly say "voice" or "myvoice."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# MyVoice

Capture the user's **writing voice** from conversations and persist it to a voice profile. The goal: generate content (posts, articles, social media) that sounds like the user wrote it — not like an AI wrote it.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| Conversation context | Current session | yes | At least 3 user messages with substantive text (not commands or one-word approvals) | Inform user there isn't enough signal to extract patterns — stop |
| Voice profile path | Implicit or $ARGUMENTS | no | File exists or template available at `templates/voice-profile.md` | Create from template |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Voice profile | User's memory directory (e.g., `memory/voice-profile.md`) | yes | Markdown with YAML frontmatter |
| Changelog entry | Appended to voice profile | yes | `### YYYY-MM-DD HH:MM` section |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Voice profile | `memory/voice-profile.md` (user's memory dir) | R/W | Markdown with YAML frontmatter |
| Profile template | `templates/voice-profile.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Count user messages with substantive text (exclude single-word responses, tool commands, approvals like "sim", "ok", "approved") → if fewer than 3: "Not enough conversation to analyze — need at least 3 substantive messages." — stop.
2. Check if another capture-voice agent is running by reading profile frontmatter for `locked: true` → if locked: "Another capture-voice run is in progress." — skip this run.
3. Voice profile path is resolvable → if file doesn't exist and template `templates/voice-profile.md` is missing: "No profile or template found." — stop.

</pre_flight>

## Steps

Run this as a **background agent** with tools: `Read`, `Write`, `Edit`, `Glob`, `Grep`. Do NOT block the main conversation.

### 1. Acquire lock and load profile

Set `locked: true` in the profile's frontmatter (or create the profile from `templates/voice-profile.md` with `locked: true`). This prevents concurrent runs from colliding.

Pass to the agent: the full conversation history, the profile file path, and the template path.

### 2. Validate input

Count user messages with substantive text (exclude single-word responses, tool commands, and approvals like "sim", "ok", "approved"). If fewer than 3, release the lock (`locked: false`), inform the user there isn't enough conversation to analyze, and stop.

### 3. Analyze conversation

Scan all user messages in this conversation. Focus on **writing style markers that would appear in published content** — not on how they interact with tools or Claude.

Extract:

- **Vocabulario e expressoes**: girias, expressoes recorrentes, palavras-chave que definem o tom (ex: "esse cara", "bora", "rsrsrs")
- **Estrutura de frases**: frases curtas vs. longas, uso de virgulas, fragmentos, ritmo da escrita
- **Tom e energia**: quando e direto, quando elabora, humor, ironia, nivel de formalidade
- **Recursos retoricos**: como constroi argumentos, usa analogias, faz transicoes, cria engajamento
- **Pontuacao e estilo**: uso de reticencias, exclamacoes, emojis, "kkk"/"rsrs", capitalizacao

Each observation must be specific enough that another AI could write a post in the user's voice using only the profile. "Escreve de forma informal" is useless. "Usa frases curtas e imperativas, intercala pt-BR com termos tecnicos em ingles sem traduzir" is actionable.

**Ignore these** — they are interaction patterns, not writing voice:
- How they use CLI flags or commands
- How they approve/reject Claude's proposals
- Tool preferences or workflow habits

### 4. Deduplicate and validate

Compare findings against the existing profile:

- **Already captured?** Skip it — do not add duplicate or near-duplicate entries.
- **Only seen once?** Skip it — require at least 2 messages showing the same pattern before recording. One-off phrasing is noise, not signal.
- **Contradicts existing?** Note the evolution (e.g., "Antes usava X, agora prefere Y") rather than deleting the old entry.

If no genuinely new patterns found, release the lock and stop here. Do not create empty changelog entries.

### 5. Consolidate before appending

Before adding new observations, scan each section for entries that overlap or could be merged. Combine redundant entries into a single, sharper observation — the profile should stay lean, not grow indefinitely. This prevents bloat from multiple runs capturing variations of the same pattern.

### 6. Draft and validate updates

Draft the proposed changes without writing them yet. For each new or modified entry, validate against the quality test: "Se eu usar so esse perfil para escrever um post, vai soar como o usuario escreveu?" Discard entries that fail this test — they are too vague or too generic.

Review the draft as a whole: does it introduce contradictions with existing entries? Does it duplicate existing observations in different words? Trim until every entry earns its place.

### 7. Write updates and release lock

Merge validated observations into the relevant profile sections. Each entry:

- One line, concise and specific
- Written in **Portuguese** — the profile must sound natural for pt-BR content generation
- Includes a concrete example in quotes when possible

Then:
- Add a changelog entry using `### YYYY-MM-DD HH:MM` format (24h, local time) summarizing what was added or consolidated
- Update the `updated` field in the frontmatter to today's date
- Set `locked: false` in the frontmatter to release the lock

If the write fails for any reason (file permission, disk full), log the error to the user and ensure `locked: false` is set — never leave a stale lock.

### 8. Report

<report>

Present concisely:
- **Patterns found:** count of new observations extracted from conversation
- **Patterns added:** count after deduplication and validation (with brief list)
- **Consolidated:** entries merged to reduce redundancy (if any)
- **Audit results:** content audit summary (voice profile quality checks)
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Run `/write-content` to generate content using the updated voice profile.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — at least 3 substantive messages analyzed, no lock conflict
2. **Steps completed?** — all steps executed or explicitly skipped with reason
3. **Profile updated?** — voice profile file has new entries and changelog, `locked: false`
4. **Anti-patterns clean?** — no generic observations, no single-message patterns, no duplicates, no typos captured as style
5. **Lock released?** — `locked: false` in frontmatter, even if an error occurred

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Before finalizing the voice profile update, verify:

1. **Observations are actionable?** — each entry is specific enough that another AI could reproduce the user's voice from it alone. Test: "Usa frases curtas e imperativas" is actionable; "Escreve de forma casual" is not.
2. **Pattern frequency validated?** — every recorded pattern appeared in at least 2 separate user messages. One-off phrasing was filtered out.
3. **No interaction patterns leaked?** — entries describe writing voice for published content, not CLI usage, tool preferences, or Claude interaction habits.
4. **No contradictions introduced?** — new entries are consistent with existing profile entries. Evolutions are noted, not overwritten.
5. **Examples are real?** — quoted examples in entries come from actual user messages in this session, not fabricated.
6. **Profile stays lean?** — redundant entries were consolidated before appending. Profile is not bloated with overlapping observations.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Fewer than 3 substantive messages | Inform user, release lock, stop — no partial analysis |
| Profile locked by another run | Skip this run silently — no queuing or waiting |
| Write failure (permissions, disk) | Log error to user, force `locked: false` — never leave stale lock |
| Template missing | Report path and suggest creating `templates/voice-profile.md` — stop |
| No new patterns found | Release lock, report "no new patterns" — do not create empty changelog |

## Anti-patterns

- **Generic observations.** "Escreve de forma casual" says nothing useful — because another AI cannot reproduce the user's voice from vague descriptors. Every entry must be specific and actionable.
- **Over-reading single messages.** One joke does not mean "usa humor constantemente" — because single-message patterns are noise, not signal. Require at least 2 messages showing the same pattern.
- **Duplicating with different words.** "Usa portugues informal" and "Prefere tom casual em pt-BR" are the same observation — because profile bloat makes it harder for content generators to prioritize patterns.
- **Capturing content, not style.** "Trabalha com CLI tools" is project context, not voice — because the profile must describe *how* the user writes, not *what* they write about.
- **Capturing Claude interaction patterns.** "Usa /push para commitar" is workflow, not writing voice — because tool usage habits are irrelevant to content generation.
- **Capturing typos as style.** "pdoe" for "pode" is a typing artifact, not a voice pattern — because including typos in the profile would produce content with intentional errors.
- **Empty changelog entries.** "Atualizado voice profile" is useless — because changelogs must name what was added (e.g., "Adicionados 3 marcadores de vocabulario").

## Guidelines

- **Append-only for observations.** Never delete previous entries — because a run with limited context might discard patterns accurately captured from richer conversations. Consolidation (merging redundant entries) is the only form of editing.

- **False negatives over false positives.** When in doubt about whether something is a pattern, skip it — because false negatives are cheap (next run catches it) while false positives pollute the profile permanently.

- **Profile serves content generation.** Every entry should help produce text that sounds authentically like the user — because the profile is the foundation for `/write-content` and similar skills, not a personality assessment.
