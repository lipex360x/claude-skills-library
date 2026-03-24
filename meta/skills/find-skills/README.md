# find-skills

> Discover and install agent skills from the open skills ecosystem.

Searches the skills ecosystem for capabilities matching your needs, verifies quality by checking install counts and source reputation, and offers to install directly. Checks the skills.sh leaderboard for battle-tested options before running CLI searches.

## Usage

```text
/find-skills <search query>
```

> [!TIP]
> Also activates when you say "find a skill", "is there a skill for X", "search skills", "how do I do X", "can you do X", "extend capabilities", or want to search for tools and workflows.

## How it works

1. **Identify the need** — Extracts domain and specific task from the user's question, mapping vague requests to concrete search terms
2. **Check the leaderboard** — Fetches skills.sh for well-known, high-install-count skills first
3. **Search the ecosystem** — Runs `npx skills find [query]` with alternative terms if initial search returns nothing
4. **Verify quality** — Checks install count (1K+ preferred), source reputation, and GitHub stars before recommending
5. **Present options and confirm** — Shows matching skills with details; never installs without explicit user consent
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
