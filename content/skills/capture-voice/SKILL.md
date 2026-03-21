---
name: capture-voice
description: Analyzes the current conversation to capture the user's writing voice for content generation — posts, articles, social media that sound like them, not AI-generated. Use this skill when the user runs /capture-voice, when triggered by the PreCompact hook, or whenever voice profile analysis is needed. Also use it when the user asks to update or check their voice profile, says "meu estilo", "como eu falo", "aprenda meu jeito", or wants content that sounds like them — even if they don't explicitly say "voice" or "myvoice."
---

# MyVoice

Capture the user's **writing voice** from conversations and persist it to a voice profile. The goal: generate content (posts, articles, social media) that sounds like the user wrote it — not like an AI wrote it.

## Input contract

- **Conversation context** (required) — at least 3 user messages with substantive text (not just commands or one-word approvals). If fewer than 3 analyzable messages exist, inform the user and stop — there is not enough signal to extract patterns.
- **Voice profile path** (optional) — path to the existing profile file. Default: the user's memory directory (e.g., `memory/voice-profile.md`). If the file doesn't exist, create it from `templates/voice-profile.md`.

## Instructions

Run this as a **background agent** with tools: `Read`, `Write`, `Edit`, `Glob`, `Grep`. Do NOT block the main conversation.

Before starting, check if another capture-voice agent is already running by looking for a lock indicator in the profile's frontmatter (`locked: true`). If locked, skip this run — concurrent writes corrupt the profile.

### 1. Acquire lock and load profile

Set `locked: true` in the profile's frontmatter (or create the profile from `templates/voice-profile.md` with `locked: true`). This prevents concurrent runs from colliding.

Pass to the agent: the full conversation history, the profile file path, and the template path.

### 2. Validate input

Count user messages with substantive text (exclude single-word responses, tool commands, and approvals like "sim", "ok", "approved"). If fewer than 3, release the lock (`locked: false`), inform the user there isn't enough conversation to analyze, and stop.

### 3. Analyze conversation

Scan all user messages in this conversation. Focus on **writing style markers that would appear in published content** — not on how they interact with tools or Claude.

Extract:

- **Vocabulário e expressões**: gírias, expressões recorrentes, palavras-chave que definem o tom (ex: "esse cara", "bora", "rsrsrs")
- **Estrutura de frases**: frases curtas vs. longas, uso de vírgulas, fragmentos, ritmo da escrita
- **Tom e energia**: quando é direto, quando elabora, humor, ironia, nível de formalidade
- **Recursos retóricos**: como constrói argumentos, usa analogias, faz transições, cria engajamento
- **Pontuação e estilo**: uso de reticências, exclamações, emojis, "kkk"/"rsrs", capitalização

Each observation must be specific enough that another AI could write a post in the user's voice using only the profile. "Escreve de forma informal" is useless. "Usa frases curtas e imperativas, intercala pt-BR com termos técnicos em inglês sem traduzir" is actionable.

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

Draft the proposed changes without writing them yet. For each new or modified entry, validate against the quality test: "Se eu usar só esse perfil para escrever um post, vai soar como o usuário escreveu?" Discard entries that fail this test — they are too vague or too generic.

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

## Anti-patterns

Avoid these specific traps:

- **Observações genéricas** — "escreve de forma casual" não diz nada. "Mistura pt-BR com termos técnicos em inglês sem traduzir, como 'skill', 'push', 'commit'" é acionável.
- **Over-reading single messages** — Uma piada isolada não significa "usa humor constantemente." Wait for patterns.
- **Duplicar com palavras diferentes** — "Usa português informal" e "Prefere tom casual em pt-BR" são a mesma observação. Pick the more specific one.
- **Capturar conteúdo, não estilo** — "Trabalha com CLI tools" é contexto de projeto, não voz. Capture *como* escreve, não *sobre o que* escreve.
- **Capturar interação com Claude** — "Usa /push -y para commitar" é workflow, não voz de escrita. Ignore padrões de uso de ferramentas.
- **Capturar typos como estilo** — Erros de digitação ("pdoe" por "pode", "faze" por "fazer") são artefatos de velocidade no chat, não padrões de escrita para conteúdo publicado. Nunca registrar typos como voz.
- **Changelog sem substância** — "Atualizado voice profile" é inútil. Name what was added: "Adicionados 3 marcadores de vocabulário (gírias pt-BR)."

## Guidelines

- The profile is append-only for observations — never delete previous entries, because a run with limited context might discard patterns that were accurately captured from richer conversations. Consolidation (merging redundant entries) is the only form of "editing."
- When in doubt about whether something is a pattern, skip it. False negatives are cheap (you'll catch it next run). False positives pollute the profile permanently.
- The profile is the foundation for content generation. Every entry should help produce text that sounds authentically like the user — not like a polished AI summary.
