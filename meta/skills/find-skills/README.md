# find-skills

> Discover and install agent skills from the open skills ecosystem.

Helps users find and install skills when they need specialized capabilities. Searches the skills ecosystem, verifies quality by checking install counts and source reputation, and offers to install directly.

## Usage

```text
/find-skills
```

> [!TIP]
> Also activates when you say "how do I do X", "find a skill for X", "is there a skill for X", "can you do X", or express interest in extending agent capabilities.

## How it works

1. **Understand the need** — Identifies the domain and specific task from the user's request
2. **Check the leaderboard** — Browses [skills.sh](https://skills.sh/) for popular, battle-tested skills
3. **Search for skills** — Runs `npx skills find [query]` to discover matches
4. **Verify quality** — Checks install count (1K+ preferred), source reputation, and GitHub stars
5. **Present and install** — Shows options with context, then offers to install with `npx skills add`

## Directory structure

```text
find-skills/
└── SKILL.md              # Core instructions and workflow
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill find-skills
```
