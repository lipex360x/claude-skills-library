# find-skills

Discover and install agent skills from the open skills ecosystem when users need specialized capabilities.

## Trigger phrases

- "How do I do X" (where X might have an existing skill)
- "Find a skill for X" or "Is there a skill for X"
- "Can you do X" (where X is a specialized capability)
- Also activates when users express interest in extending agent capabilities or mention a specific domain (design, testing, deployment, etc.)

## How it works

1. **Understand the need** — Identify the domain and specific task from the user's request
2. **Check the leaderboard** — Browse [skills.sh](https://skills.sh/) for popular, battle-tested skills before running CLI searches
3. **Search for skills** — Run `npx skills find [query]` to discover matching skills
4. **Verify quality** — Check install count (1K+ preferred), source reputation, and GitHub stars before recommending
5. **Present and install** — Show options with install counts, then offer to install with `npx skills add`

## Usage

```
/find-skills
```

**Example:** User asks "how do I make my React app faster?" — the skill searches for React performance skills, verifies quality, and presents the best options with install commands.

> [!TIP]
> The skill prioritizes well-known sources like `vercel-labs/agent-skills` and `anthropics/skills` that have 100K+ installs.

## Common skill categories

| Category        | Example queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Directory structure

```
find-skills/
└── SKILL.md    # Core instructions and workflow
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill find-skills
```
