---
name: prompt-continue
description: Generate a continuation prompt to paste into a new Claude Code conversation. Use this skill when the user wants to switch sessions, is hitting context limits, needs to hand off work to a fresh window, says "let's continue later", "save context", "continuation prompt", or asks to prepare a handoff for a new conversation — even if they don't explicitly say "continuation" or "handoff."
user-invocable: true
---

# Prompt Continue

Generate a continuation prompt the user can paste into a new Claude Code conversation to resume work seamlessly.

## Steps

1. **Analyze the full conversation** — this is the most important source. Extract: what was discussed, decisions made, what the user asked for next, pending requests or deferred ideas. Focus on context and situational awareness, not action items — the goal is to inform the next session, not command it.
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

- **Context, not instructions.** The prompt gives situational awareness so the next session can continue naturally. Avoid imperative language like "commit X" or "run Y" — describe what exists and what the user was working toward. Imperative prompts cause the next session to act without confirming, which surprises the user.

- **Match the user's language.** Write the continuation prompt in whatever language the user has been communicating in.

- After generating, copy to clipboard (use `pbcopy` on macOS, `xclip` on Linux, or inform the user if neither is available) and confirm.

- Show the prompt in a fenced code block so the user can review it.

## Anti-patterns

These are specific failure modes for continuation prompts — each one has caused real issues in handoffs:

- **Too long.** A continuation prompt over ~40 lines overwhelms the next session's context. Summarize ruthlessly — if the next agent needs detail, point to a file or issue, don't paste it inline.
- **Including full diffs or code blocks.** The next session can read files and run `git diff` itself. Embed references (`see src/auth.ts:45`), not content. Pasting code wastes tokens and goes stale immediately.
- **Imperative language that forces actions.** "Run the tests", "commit the changes", "fix the bug in auth.ts" — these cause the next session to act without confirming. Describe the state ("tests are failing on auth.ts:52") and let the next session decide.
- **Forgetting conversation decisions.** Code state is recoverable from git. What's NOT recoverable: why the user chose approach A over B, preferences expressed during the conversation, deferred ideas they want to revisit. These are the highest-value items to capture.
- **Omitting branch/issue context.** Without the branch name and issue number, the next session starts blind. Always include these — they're the fastest way to reconstruct full context.
