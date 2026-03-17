# create-continuation

> Generate a continuation prompt to paste into a new Claude Code conversation.

Produces a ready-to-paste prompt that lets you resume work seamlessly across sessions. Analyzes the full conversation history and git state to capture decisions, pending work, and context that would otherwise be lost.

## Usage

```text
/create-continuation
```

> [!TIP]
> Also activates when you say "let's continue later", "save context", "continuation prompt", "prepare a handoff", or are hitting context limits and need to switch sessions.

## How it works

1. **Analyze the conversation** — Extracts decisions made, pending requests, and deferred ideas from the full conversation history
2. **Gather git state** — Runs `git status`, `git log`, `git diff`, and checks the current branch and related issue
3. **Generate the prompt** — Produces a markdown block covering what was completed, what's pending, branch state, and conversation context
4. **Copy to clipboard** — Automatically copies using `pbcopy` (macOS) or `xclip` (Linux)

> [!IMPORTANT]
> The output provides **context, not instructions** — it describes what exists and what you were working toward, avoiding imperative language that could cause the next session to act without confirming.

## Directory structure

```text
create-continuation/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-continuation
```
