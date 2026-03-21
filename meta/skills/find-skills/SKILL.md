---
name: find-skills
description: Discover and install agent skills from the open skills ecosystem. Use when the user says "find a skill", "is there a skill for X", "search skills", "how do I do X", "can you do X", "extend capabilities", "add a skill", or wants to search for tools, templates, or workflows — even if they don't explicitly say "find" or "skill."
user-invocable: true
---

# Find Skills

Discover and install skills from the open agent skills ecosystem.

## Input

- **Required:** A search intent — either explicit (`$ARGUMENTS` as search query) or implicit (extracted from the user's question)
- **Optional:** Domain filter (e.g., "react", "testing", "deploy")

If no search intent can be extracted, ask the user what kind of skill they're looking for before proceeding.

## Skills CLI

The Skills CLI (`npx skills`) is the package manager for the open skills ecosystem.

- `npx skills find [query]` — search for skills by keyword
- `npx skills add <package>` — install a skill
- `npx skills check` — check for updates
- `npx skills update` — update all installed skills

Browse skills at: https://skills.sh/

## Steps

### Step 1: Identify the need

Extract the domain (e.g., React, testing, deployment) and the specific task (e.g., writing tests, reviewing PRs) from the user's question. Map vague requests to concrete search terms — "make my app faster" becomes "react performance".

### Step 2: Check the leaderboard

Fetch the [skills.sh leaderboard](https://skills.sh/) to find well-known skills first, because battle-tested skills with high install counts are safer than unknown ones. Top skills include:

- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### Step 3: Search the ecosystem

If the leaderboard doesn't cover the need, run the CLI search:

```bash
npx skills find [query]
```

Examples:
- "how do I make my React app faster?" → `npx skills find react performance`
- "can you help with PR reviews?" → `npx skills find pr review`
- "I need to create a changelog" → `npx skills find changelog`

Try alternative terms if the first search returns nothing — "deploy" → "deployment", "ci-cd".

### Step 4: Verify quality

Never recommend a skill based solely on search results, because low-quality skills can introduce bad patterns or security risks. Verify:

1. **Install count** — prefer 1K+ installs. Be cautious with anything under 100, because low counts mean limited community vetting.
2. **Source reputation** — official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — a repo with <100 stars warrants skepticism.

### Step 5: Present options and confirm

Present each matching skill with: name, description, install count, source, install command, and link. Use this format:

```
I found a skill that might help! The "react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.
(185K installs)

To install it:
npx skills add vercel-labs/agent-skills@react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/react-best-practices
```

Ask the user which skill to install (or none). Never install without explicit user consent.

### Step 6: Install

Install the selected skill only after user confirmation:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

### Step 7: Verify installation

Confirm the skill was installed correctly by checking that the skill directory exists and the SKILL.md is valid. If the installation failed, report the error and suggest manual installation.

## Common skill categories

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## When no skills are found

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest creating a custom skill with `npx skills init`

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```

## Anti-patterns

- **Recommending unvetted skills** — never recommend a skill without checking install count, source reputation, and stars. Low-quality skills introduce bad patterns
- **Installing without user consent** — always ask before installing. The user must explicitly confirm the choice
- **Trusting search results blindly** — search results rank by relevance, not quality. Verify quality separately
- **Recommending overlapping skills** — check what the user already has installed before suggesting a skill that duplicates existing functionality
- **Recommending skills for simple tasks** — if the task is straightforward and doesn't need specialized knowledge, help directly instead of adding a dependency
