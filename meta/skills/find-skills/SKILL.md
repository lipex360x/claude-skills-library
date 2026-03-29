---
name: find-skills
model: sonnet
description: >-
  Discover and install agent skills from the open skills ecosystem. Use when the
  user says "find a skill", "is there a skill for X", "search skills", "how do I
  do X", "can you do X", "extend capabilities", "add a skill", or wants to
  search for tools, templates, or workflows — even if they don't explicitly say
  "find" or "skill."
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Find Skills

Discover and install skills from the open agent skills ecosystem.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `search-query` | $ARGUMENTS or conversation | yes | Non-empty string describing what kind of skill is needed | AUQ: "What kind of skill are you looking for?" |
| `domain-filter` | conversation | no | Domain keyword (e.g., "react", "testing", "deploy") | — |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Skill recommendation | stdout | no | Markdown with install command |
| Installed skill | `.claude/skills/<name>/` or `skills-library/<plugin>/skills/<name>/` | yes (if installed) | Skill directory |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Skills CLI | `npx skills` | R | CLI output |
| skills.sh leaderboard | `https://skills.sh/` | R | HTML |
| Installed skills | `.claude/skills/`, `skills-library/*/skills/` | R | Directories |

</external_state>

## Pre-flight

<pre_flight>

1. Search intent extractable from arguments or conversation → if not: AUQ "What kind of skill are you looking for?" — stop if no answer.
2. `npx` is available → if not: "npx required. Install Node.js: https://nodejs.org/" — stop.

</pre_flight>

## Steps

### 1. Identify the need

Extract the domain (e.g., React, testing, deployment) and the specific task (e.g., writing tests, reviewing PRs) from the user's question. Map vague requests to concrete search terms — "make my app faster" becomes "react performance".

### 2. Check the leaderboard

Fetch the [skills.sh leaderboard](https://skills.sh/) to find well-known skills first, because battle-tested skills with high install counts are safer than unknown ones. Top skills include:

- `vercel-labs/agent-skills` — React, Next.js, web design (100K+ installs each)
- `anthropics/skills` — Frontend design, document processing (100K+ installs)

### 3. Search the ecosystem

If the leaderboard doesn't cover the need, run the CLI search:

```bash
npx skills find [query]
```

Examples:
- "how do I make my React app faster?" → `npx skills find react performance`
- "can you help with PR reviews?" → `npx skills find pr review`
- "I need to create a changelog" → `npx skills find changelog`

Try alternative terms if the first search returns nothing — "deploy" → "deployment", "ci-cd".

### 4. Verify quality

Never recommend a skill based solely on search results, because low-quality skills can introduce bad patterns or security risks. Verify:

1. **Install count** — prefer 1K+ installs. Be cautious with anything under 100, because low counts mean limited community vetting.
2. **Source reputation** — official sources (`vercel-labs`, `anthropics`, `microsoft`) are more trustworthy than unknown authors.
3. **GitHub stars** — a repo with <100 stars warrants skepticism.

### 5. Present options and confirm

Present each matching skill with: name, description, install count, source, install command, and link. Only present skills that passed the quality verification in Step 4. Ask the user which skill to install (or none). Never install without explicit user consent.

### 6. Install

Install the selected skill only after user confirmation:

```bash
npx skills add <owner/repo@skill> -g -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

### 7. Verify installation

Confirm the skill was installed correctly by checking that the skill directory exists and the SKILL.md is valid. If the installation failed, report the error and suggest manual installation.

### 8. Report

Present concisely:
- **What was done** — search query used, skills found, skill installed (or none)
- **Quality check** — install count, source reputation, stars for recommended skill
- **Installation** — path where skill was installed (or "user declined")
- **Audit results** — self-audit summary
- **Errors** — issues encountered (or "none")

## Next action

Run `/install-skill` if the user wants to install a found skill into the global skills-library with full registration.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — search intent extracted, npx available
2. **Steps completed?** — search performed, quality verified before recommendation
3. **Output exists?** — skill recommendation presented or installed
4. **Anti-patterns clean?** — no unvetted skills recommended, no install without consent
5. **Approval gates honored?** — user explicitly confirmed before installation

</self_audit>

## Content audit

> _Skipped: "N/A — skill does not generate verifiable content (search and install workflow)."_

## Error handling

| Failure | Strategy |
|---------|----------|
| `npx` not available | Report error, suggest installing Node.js — stop |
| `npx skills find` returns no results | Try alternative search terms, then offer to help directly |
| Network error fetching leaderboard | Skip leaderboard, proceed with CLI search |
| Installation fails | Report specific error, suggest manual installation |
| Skill has no SKILL.md | Warn user about quality concern, suggest alternatives |

## Anti-patterns

- **Recommending unvetted skills.** Never recommend a skill without checking install count, source reputation, and stars — because low-quality skills introduce bad patterns or security risks.
- **Installing without user consent.** Always ask before installing — because the user must explicitly confirm the choice.
- **Trusting search results blindly.** Search results rank by relevance, not quality — because quality must be verified separately.
- **Recommending overlapping skills.** Check what the user already has installed before suggesting — because duplicate functionality adds confusion and maintenance burden.
- **Recommending skills for simple tasks.** If the task is straightforward and doesn't need specialized knowledge, help directly — because adding a dependency for a one-off task is unnecessary overhead.

## Guidelines

- **Quality over quantity.** Present only skills that pass the quality verification — because a curated recommendation is more valuable than a long list of untested options.

- **Leaderboard first.** Check well-known, battle-tested skills before running CLI search — because high-install-count skills have more community vetting and are more likely to work reliably.

- **Graceful degradation.** If the leaderboard is unreachable or CLI search fails, offer to help with the task directly — because the user's goal is to solve a problem, not necessarily to install a skill.

- **No silent installs.** Always present the skill details and get explicit confirmation before installing — because installing modifies the user's environment and should be a conscious decision.
