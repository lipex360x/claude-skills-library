# capture-voice

> Analyze conversations to capture the user's writing voice for authentic content generation.

Builds and maintains a persistent voice profile by extracting writing style patterns from conversations. The profile powers content generation that sounds like you wrote it -- not like AI. Runs as a background agent without blocking the main conversation.

## Usage

```text
/capture-voice
```

> [!TIP]
> Also activates via the PreCompact hook, or when you say "meu estilo", "como eu falo", "aprenda meu jeito", or ask to update/check your voice profile.

## How it works

1. **Load profile** -- Reads the existing voice profile from `~/.brain/memory/voice-profile.md` (or creates one from the template)
2. **Analyze conversation** -- Scans all user messages for writing style markers: vocabulary, sentence structure, tone, rhetorical devices, and punctuation habits
3. **Deduplicate** -- Compares findings against the existing profile, skipping duplicates and one-off patterns (requires 2+ messages showing the same pattern)
4. **Consolidate** -- Merges redundant entries to keep the profile lean
5. **Write updates** -- Appends new observations in Portuguese with concrete examples and a timestamped changelog entry

> [!IMPORTANT]
> Captures **writing voice** only, not interaction patterns. CLI usage, tool preferences, and workflow habits are ignored -- only patterns relevant to published content are recorded.

## Directory structure

```text
capture-voice/
├── SKILL.md              # Core instructions
└── templates/
    └── voice-profile.md  # Template for new voice profiles
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-voice
```
