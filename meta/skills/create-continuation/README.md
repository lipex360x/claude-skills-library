# create-continuation

> Generate a continuation prompt to paste into a new Claude Code conversation.

Captures branch state, conversation decisions, and pending work into a concise handoff prompt (~40 lines max) and copies it to the clipboard. Prioritizes context that a fresh session cannot recover from git alone — architectural decisions, user preferences, and deferred ideas. The generated prompt starts with a "do NOT take action" framing header so the new session reads before doing.

## Usage

```text
/create-continuation
```

> [!TIP]
> Also activates when you say "let's continue later", "save context", "continuation prompt", "hand off to a new session", or want to prepare a handoff for a new conversation.

### Examples

```text
/create-continuation       # generate prompt from current session context
```

Also triggered by natural language:

```text
"save context for later"   # same effect via model invocation
"let's continue tomorrow"  # same effect via model invocation
```

> [!NOTE]
> Requires a git repository for full context gathering. Works without git but produces a lighter prompt from conversation context only.

## How it works

1. **Analyze conversation** — Extracts decisions, pending requests, and preferences from the full conversation history. Focuses on situational awareness, not action items
2. **Gather git state** — Collects branch name, uncommitted changes, recent commits, and modified files in parallel
3. **Read related issue** — Finds the related GitHub issue from the branch name and checks pending checkboxes
4. **Generate prompt** — Builds a structured prompt with a "do NOT take action" header, branch state, completed work, pending items, and conversation context
5. **Review and trim** — Enforces the ~40 line limit, removes diffs/code blocks, replaces imperative language with state descriptions
6. **Copy to clipboard** — Copies to clipboard via `pbcopy`/`xclip` and displays in a fenced code block for review
7. **Report** — Shows prompt length, sources used (conversation, git, issue), and clipboard status

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
