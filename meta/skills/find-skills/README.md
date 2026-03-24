# find-skills

> Discover and install agent skills from the open skills ecosystem.

Two-stage discovery pipeline: checks the skills.sh leaderboard for battle-tested options first (100K+ installs), then runs `npx skills find` with alternative search terms if needed. Verifies quality via install counts (1K+ preferred), source reputation, and GitHub stars before recommending — never installs without explicit user consent.

## Usage

```text
/find-skills <search query>
```

> [!TIP]
> Also activates when you say "find a skill", "is there a skill for X", "search skills", "how do I do X", "can you do X", "extend capabilities", or want to search for tools and workflows.

### Examples

```text
/find-skills react performance     # search for React optimization skills
/find-skills pr review             # find code review skills
/find-skills changelog             # search for changelog generation skills
```

> [!NOTE]
> Requires `npx` (Node.js) for CLI searches. Run `npm install -g npx` or install Node.js from https://nodejs.org/ if not available.

## How it works

1. **Identify the need** — Extracts domain and specific task from the user's question, mapping vague requests to concrete search terms (e.g., "make my app faster" becomes "react performance")
2. **Check the leaderboard** — Fetches skills.sh for well-known, high-install-count skills from trusted sources (vercel-labs, anthropics)
3. **Search the ecosystem** — Runs `npx skills find [query]` with alternative terms if initial search returns nothing ("deploy" -> "deployment", "ci-cd")
4. **Verify quality** — Checks install count (1K+ preferred), source reputation (official sources preferred), and GitHub stars (100+ baseline) before recommending
5. **Present options and confirm** — Shows matching skills with name, description, install count, source, and install command. Never installs without explicit user consent
6. **Install** — Installs the selected skill with `npx skills add` after user confirmation
7. **Verify installation** — Confirms the skill directory exists and SKILL.md is valid
8. **Report** — Shows search results, quality checks, installation status, and any errors

## Directory structure

```text
find-skills/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill find-skills
```
