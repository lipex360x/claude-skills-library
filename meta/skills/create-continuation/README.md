# prompt-continue

Generate a continuation prompt to paste into a new Claude Code conversation, so you can resume work seamlessly across sessions.

## Trigger phrases

| Phrase | When it activates |
|--------|-------------------|
| `continue later` / `let's continue later` | Ending a session to resume later |
| `save context` / `continuation prompt` | Explicitly requesting a handoff prompt |
| `prepare a handoff` | Preparing context for a new conversation |

Also activates when hitting context limits, switching sessions, or handing off work to a fresh conversation window.

## How it works

1. **Analyze the conversation** — Extracts decisions made, pending requests, and deferred ideas from the full conversation history
2. **Gather git state** — Runs `git status`, `git log`, `git diff`, and checks the current branch and related issue
3. **Generate the prompt** — Produces a ready-to-paste markdown block covering what was completed, what's pending, branch state, and conversation context
4. **Copy to clipboard** — Automatically copies the prompt using `pbcopy` (macOS) or `xclip` (Linux) and confirms

> [!IMPORTANT]
> The output provides **context, not instructions** — it describes what exists and what the user was working toward, avoiding imperative language that could cause the next session to act without confirming.

## Usage

```
/prompt-continue
```

The skill generates a fenced code block with the continuation prompt and copies it to your clipboard. Paste it into a new conversation to pick up where you left off.

## Output structure

The generated prompt follows this structure:

```markdown
Branch `feature/foo` (issue #N). Working tree dirty/clean — N files modified.

## What was done
- ...

## Where we left off
- ...

## Context
- ...
```

## Directory structure

```
prompt-continue/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill prompt-continue
```
