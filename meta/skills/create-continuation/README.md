# create-continuation

> Generate a continuation prompt to paste into a new Claude Code conversation.

Captures branch state, conversation decisions, and pending work into a concise handoff prompt (~40 lines max). Prioritizes context that a fresh session cannot recover from git alone — decisions, preferences, and deferred ideas.

## Usage

```text
/create-continuation
```

> [!TIP]
> Also activates when you say "let's continue later", "save context", "continuation prompt", "hand off to a new session", or want to prepare a handoff for a new conversation.

## How it works

1. **Analyze conversation** — Extracts decisions, pending requests, and preferences from the full conversation history
2. **Gather git state** — Collects branch name, uncommitted changes, recent commits, and modified files
3. **Read related issue** — Finds the related GitHub issue from the branch name and checks pending checkboxes
4. **Generate prompt** — Builds a structured continuation prompt with branch state, completed work, pending items, and conversation context
5. **Review and trim** — Enforces the ~40 line limit, removes diffs/code blocks, replaces imperative language with state descriptions
6. **Copy to clipboard** — Copies to clipboard via `pbcopy`/`xclip` and displays in a fenced code block
7. **Report** — Shows prompt length, sources used, and clipboard status

## Directory structure

```text
create-continuation/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-continuation
```
