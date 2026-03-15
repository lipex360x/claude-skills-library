# prompt-continue

Generate a continuation prompt to paste into a new Claude Code conversation, so you can resume work seamlessly across sessions.

## Trigger phrases

- "continue later"
- "save context" / "continuation prompt"
- "prepare a handoff"
- Also activates when the user is hitting context limits or wants to switch to a fresh conversation window

## How it works

1. **Analyze the conversation** — Extracts decisions made, pending requests, and deferred ideas from the full conversation history
2. **Gather git state** — Runs `git status`, `git log`, `git diff`, and checks the current branch and related issue
3. **Generate the prompt** — Produces a ready-to-paste markdown block covering what was completed, what's pending, branch state, and conversation context
4. **Copy to clipboard** — Automatically copies the prompt using `pbcopy` (macOS) or `xclip` (Linux) and confirms

The output provides **context, not instructions** — it describes what exists and what the user was working toward, avoiding imperative language that could cause the next session to act without confirming.

## Usage

```
/prompt-continue
```

The skill generates a fenced code block with the continuation prompt and copies it to your clipboard. Paste it into a new conversation to pick up where you left off.

## Directory structure

```
prompt-continue/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add https://github.com/lipex360x/claude-skills-library --skill prompt-continue
```
