---
name: create-continuation
description: Generate a continuation prompt to paste into a new Claude Code conversation. Use this skill when the user wants to switch sessions, is hitting context limits, needs to hand off work to a fresh window, says "let's continue later", "save context", "continuation prompt", or asks to prepare a handoff for a new conversation — even if they don't explicitly say "continuation" or "handoff."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Prompt Continue

Generate a continuation prompt the user can paste into a new Claude Code conversation to resume work seamlessly.

## Input contract

Requires an active conversation with work history (commits, decisions, or pending tasks). If the conversation is minimal (e.g., user just started and wants to hand off immediately), generate a lightweight prompt with branch/issue state only and note that no conversation context was available.

## Steps

1. **Analyze the full conversation** — this is the most important source. Extract: what was discussed, decisions made, what the user asked for next, pending requests or deferred ideas. Focus on context and situational awareness, not action items — the goal is to inform the next session, not command it.
2. Run `git status -u` for uncommitted changes. If not a git repo, skip steps 2-5 and note this in the prompt.
3. Run `git log --oneline -5` for recent work. If no commits exist on the branch, note that the branch is fresh.
4. Run `git diff --stat` for modified files
5. Check the current branch and its related issue. If no issue is identifiable, skip the issue section.
6. Read the GitHub issue (if identifiable) to find pending checkboxes
7. **Review before output** — Check the generated prompt against the anti-patterns list: Is it under ~40 lines? No code blocks or diffs pasted inline? No imperative language? Includes branch/issue context? Captures conversation decisions? If any check fails, revise before presenting.

## Output format

A markdown code block with a ready-to-paste prompt. The prompt **must start** with a framing header that tells the receiving session what this is and how to behave:

```
# Continuation from previous session

This is a context handoff from a previous conversation. Read it to understand where we left off. **Do NOT take any action** — just confirm you understood with a brief summary (2-3 sentences max) and wait for my next instruction.
```

After the framing header, include:

- **Branch state** (clean/dirty, ahead/behind)
- **What was completed** (from commits AND conversation — both matter)
- **What's pending** (uncommitted changes, next steps, deferred requests)
- **Conversation context** — decisions, preferences, anything the next session needs to know

**Example structure:**
```
# Continuation from previous session

This is a context handoff from a previous conversation. Read it to understand where we left off. **Do NOT take any action** — just confirm you understood with a brief summary (2-3 sentences max) and wait for my next instruction.

---

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

- **Length gate.** If the prompt exceeds ~40 lines, summarize further before presenting. Point to files and issues instead of inlining detail.

## Anti-patterns

These are specific failure modes for continuation prompts — each one has caused real issues in handoffs:

- **Too long.** A continuation prompt over ~40 lines overwhelms the next session's context. Summarize ruthlessly — if the next agent needs detail, point to a file or issue, don't paste it inline.
- **Including full diffs or code blocks.** The next session can read files and run `git diff` itself. Embed references (`see src/auth.ts:45`), not content. Pasting code wastes tokens and goes stale immediately.
- **Imperative language that forces actions.** "Run the tests", "commit the changes", "fix the bug in auth.ts" — these cause the next session to act without confirming. Describe the state ("tests are failing on auth.ts:52") and let the next session decide.
- **Forgetting conversation decisions.** Code state is recoverable from git. What's NOT recoverable: why the user chose approach A over B, preferences expressed during the conversation, deferred ideas they want to revisit. These are the highest-value items to capture.
- **Omitting branch/issue context.** Without the branch name and issue number, the next session starts blind. Always include these — they're the fastest way to reconstruct full context.
