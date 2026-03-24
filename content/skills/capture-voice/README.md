# capture-voice

> Analyzes the current conversation to capture the user's writing voice for content generation.

Builds and maintains a persistent voice profile by extracting writing style patterns from conversations. The profile powers content generation that sounds like the user wrote it — not like AI. Focuses exclusively on writing voice markers, ignoring CLI interaction patterns and workflow habits.

## Usage

```text
/capture-voice
```

> [!TIP]
> Also activates when triggered by the PreCompact hook, or when you say "meu estilo", "como eu falo", "aprenda meu jeito", or ask to update/check your voice profile.

## How it works

1. **Acquire lock and load profile** — Sets `locked: true` in the profile frontmatter to prevent concurrent writes
2. **Validate input** — Checks for at least 3 substantive user messages; stops if insufficient
3. **Analyze conversation** — Scans user messages for writing style markers: vocabulary, sentence structure, tone, rhetorical devices, and punctuation habits
4. **Deduplicate and validate** — Compares findings against the existing profile, skipping duplicates and one-off patterns
5. **Consolidate before appending** — Merges redundant entries to keep the profile lean
6. **Draft and validate updates** — Drafts proposed changes and validates each against the quality test before writing
7. **Write updates and release lock** — Appends validated observations in Portuguese with concrete examples, adds a timestamped changelog entry, and releases the lock
8. **Report** — Summarizes patterns found, added, consolidated, and any errors

## Directory structure

```text
capture-voice/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── templates/
    └── voice-profile.md  # Template for new voice profiles
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-voice
```
