# capture-voice

> Analyzes the current conversation to capture the user's writing voice for content generation.

Background voice profiler that extracts writing style patterns from live conversations and persists them to a reusable voice profile. Requires at least 2 occurrences of a pattern before recording it, enforces a locking mechanism for concurrent safety, and consolidates redundant entries to keep the profile lean. All observations are written in Portuguese with concrete quoted examples, making the profile directly usable by `/write-content`.

## Usage

```text
/capture-voice
```

> [!TIP]
> Also activates when triggered by the PreCompact hook, or when you say "meu estilo", "como eu falo", "aprenda meu jeito", or ask to update/check your voice profile.

### Examples

```text
/capture-voice              # analyze current conversation and update voice profile
```

Also triggered automatically:

```text
"aprenda meu jeito"         # same effect via model invocation
"update my voice profile"   # same effect via model invocation
```

## How it works

1. **Acquire lock and load profile** — Sets `locked: true` in the profile frontmatter to prevent concurrent writes; creates from template if no profile exists
2. **Validate input** — Checks for at least 3 substantive user messages (excludes single-word responses, commands, approvals); stops if insufficient
3. **Analyze conversation** — Scans user messages for writing style markers: vocabulary, sentence structure, tone, rhetorical devices, and punctuation habits. Ignores CLI interaction patterns and workflow habits
4. **Deduplicate and validate** — Compares findings against the existing profile, skipping duplicates and patterns seen only once
5. **Consolidate before appending** — Merges redundant entries into sharper observations to prevent profile bloat
6. **Draft and validate updates** — Drafts proposed changes and validates each against the quality test: "Could another AI reproduce the user's voice from this entry alone?"
7. **Write updates and release lock** — Appends validated observations in Portuguese with concrete examples, adds a timestamped changelog entry, and releases the lock
8. **Report** — Summarizes patterns found, added, consolidated, and any errors

[↑ Back to top](#capture-voice)

## Directory structure

```text
capture-voice/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── templates/
    └── voice-profile.md  # Template for new voice profiles with YAML frontmatter structure
```

[↑ Back to top](#capture-voice)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-voice
```
