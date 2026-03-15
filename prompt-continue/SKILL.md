---
name: prompt-continue
description: Generate a continuation prompt to paste into a new Claude Code conversation. Use this skill when the user wants to switch sessions, is hitting context limits, needs to hand off work to a fresh window, says "let's continue later", "save context", "continuation prompt", or asks to prepare a handoff for a new conversation.
user-invocable: true
---

# Prompt Continue

Generate a continuation prompt the user can paste into a new Claude Code conversation to resume work seamlessly.

## Steps

1. **Analyze the full conversation** — this is the most important source. Extract: what was discussed, decisions made, what the user asked for next, pending requests or deferred ideas.
2. Run `git status -u` for uncommitted changes
3. Run `git log --oneline -5` for recent work
4. Run `git diff --stat` for modified files
5. Check the current branch and its related issue
6. Read the GitHub issue (if identifiable) to find pending checkboxes

## Output format

A markdown code block with a ready-to-paste prompt covering:

- **What was completed** (from commits AND conversation — both matter)
- **What's pending** (uncommitted changes, next steps, deferred requests)
- **Branch state** (clean/dirty, ahead/behind)
- **Conversation context** — decisions, preferences, anything the next session needs to know

**Example structure:**
```
Branch `feature/foo` (issue #N). Working tree dirty/clean — N files modified.

## What was done
- ...

## Where we left off
- ...

## Context
- ...
```

## Guidelines

- **Context, not instructions.** The prompt gives situational awareness so the next session can continue naturally. Avoid imperative language like "commit X" or "run Y" — describe what exists and what the user was working toward. The reason: imperative prompts cause the next session to act without confirming, which surprises the user.

- **Match the user's language** — write in whatever language the user has been using in the conversation.

- After generating, copy to clipboard via `pbcopy` and confirm to the user.

- Show the prompt in a fenced code block so the user can review it.
