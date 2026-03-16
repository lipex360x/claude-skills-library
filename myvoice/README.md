# MyVoice

Capture your writing voice from conversations and generate content that sounds like you — not like AI.

## Overview

MyVoice is a Claude Code skill that analyzes your conversations to build a persistent **voice profile**. The profile captures vocabulary, sentence structure, tone, rhetorical patterns, and punctuation habits — everything needed to generate posts, articles, and social media content in your authentic voice.

The skill runs as a background agent: it observes how you write, extracts patterns, and appends them to a voice profile stored at `~/.brain/memory/voice-profile.md`.

## How It Works

| Step | What happens |
|------|-------------|
| **Load** | Reads your existing voice profile (or creates one from the template) |
| **Analyze** | Scans all user messages in the current conversation for writing style markers |
| **Deduplicate** | Compares findings against the existing profile — skips duplicates and one-off patterns |
| **Consolidate** | Merges redundant entries to keep the profile lean |
| **Write** | Appends new observations with concrete examples and timestamps |

> [!IMPORTANT]
> MyVoice captures **writing voice**, not interaction patterns. How you use CLI commands, approve proposals, or navigate tools is ignored — only patterns relevant to published content are recorded.

## Activation

The skill activates when you:

- Run `/myvoice`
- Trigger the `PreCompact` hook
- Ask to update or check your voice profile
- Say things like "meu estilo", "como eu falo", or "aprenda meu jeito"
- Request content that sounds like you

## What Gets Captured

- **Vocabulário e expressões** — slang, recurring phrases, tone-defining words
- **Estrutura e ritmo** — sentence length, fragments, writing rhythm
- **Tom e energia** — directness, humor, irony, formality level
- **Recursos retóricos** — argument construction, analogies, transitions
- **Pontuação e estilo** — ellipses, exclamations, emoji usage, "kkk"/"rsrs"

> [!TIP]
> Each observation must be specific enough that another AI could write a post in your voice using only the profile. "Escreve de forma informal" is too vague — "Usa frases curtas e imperativas, intercala pt-BR com termos técnicos em inglês sem traduzir" is actionable.

## Files

```
myvoice/
├── SKILL.md                      # Skill definition and instructions
└── templates/
    └── voice-profile.md          # Template for new voice profiles
```

## Design Principles

- **Append-only** — observations are never deleted; consolidation (merging redundant entries) is the only form of editing
- **Pattern over noise** — a pattern must appear in at least 2 messages before being recorded
- **Portuguese-native** — the profile is written in pt-BR for natural content generation
- **No false positives** — when in doubt, skip it. Missing a pattern is cheap; polluting the profile is permanent

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill myvoice
```
