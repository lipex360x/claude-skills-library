# capture-voice

> Analyze conversations to capture the user's writing voice for authentic content generation.

Builds and maintains a persistent voice profile by extracting writing style patterns from conversations. The profile powers content generation that sounds like you wrote it -- not like AI. Runs as a background agent without blocking the main conversation.

## Usage

```text
/capture-voice
```

> [!TIP]
> Also activates via the PreCompact hook, or when you say "meu estilo", "como eu falo", "aprenda meu jeito", or ask to update/check your voice profile.

## Input contract

- **Conversation context** (required) — at least 3 substantive user messages
- **Voice profile path** (optional) — defaults to `memory/voice-profile.md`

## How it works

1. **Acquire lock** — Sets `locked: true` in the profile frontmatter to prevent concurrent writes
2. **Validate input** — Checks for at least 3 substantive user messages; stops if insufficient
3. **Analyze conversation** — Scans user messages for writing style markers: vocabulary, sentence structure, tone, rhetorical devices, and punctuation habits
4. **Deduplicate** — Compares findings against the existing profile, skipping duplicates and one-off patterns (requires 2+ messages showing the same pattern)
5. **Consolidate** — Merges redundant entries to keep the profile lean
6. **Draft and validate** — Drafts proposed changes and validates each against the quality test before writing
7. **Write and release lock** — Appends validated observations in Portuguese with concrete examples, adds a timestamped changelog entry, and releases the lock

> [!IMPORTANT]
> Captures **writing voice** only, not interaction patterns. CLI usage, tool preferences, and workflow habits are ignored -- only patterns relevant to published content are recorded.

## Agent details

- **Tools:** `Read`, `Write`, `Edit`, `Glob`, `Grep`
- **Concurrency:** lock-based via frontmatter `locked: true/false` — concurrent runs are skipped

## Directory structure

```text
capture-voice/
├── SKILL.md              # Core instructions
├── README.md             # This file
└── templates/
    └── voice-profile.md  # Template for new voice profiles
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-voice
```
