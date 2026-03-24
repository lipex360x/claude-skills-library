---
name: create-continuation
description: >-
  Generate a continuation prompt to paste into a new Claude Code conversation.
  Use this skill when the user wants to switch sessions, is hitting context
  limits, needs to hand off work to a fresh window, says "let's continue later",
  "save context", "continuation prompt", or asks to prepare a handoff for a new
  conversation — even if they don't explicitly say "continuation" or "handoff."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Create Continuation

Generate a continuation prompt the user can paste into a new Claude Code conversation to resume work seamlessly. Captures branch state, conversation decisions, and pending work — the things a fresh session cannot recover from git alone.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| Active conversation | Session context | yes | At least 3 substantive messages or git history on branch | Generate lightweight prompt with branch/issue state only, note limited context |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Continuation prompt | clipboard (pbcopy/xclip) | no | Markdown code block |
| Prompt display | stdout | no | Fenced markdown |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Git repo | `.git/` | R | git CLI |
| GitHub issue | GitHub API | R | Markdown |
| Conversation context | Session | R | In-memory |

</external_state>

## Pre-flight

<pre_flight>

1. Current directory is a git repo → if not: generate prompt from conversation context only, skip git steps, note this in output.
2. Git has at least one commit → if fresh repo with no commits: note "fresh repo, no commit history" in prompt.
3. Current branch has a related issue → if no issue identifiable: skip issue section in prompt.

</pre_flight>

## Steps

### 1. Analyze conversation

This is the most important source. Extract from the full conversation:
- What was discussed, decisions made, what the user asked for next
- Pending requests or deferred ideas
- Preferences expressed during the session

Focus on context and situational awareness, not action items — the goal is to inform the next session, not command it.

### 2. Gather git state

Run these in parallel:
- `git status -u` for uncommitted changes
- `git log --oneline -5` for recent work
- `git diff --stat` for modified files
- Check the current branch name

If not a git repo, skip and note this in the prompt.

### 3. Read related issue

Check the current branch for a related issue number. If identifiable, read the GitHub issue to find pending checkboxes and overall progress.

### 4. Generate prompt

The prompt **must start** with this framing header:

```
# Continuation from previous session

This is a context handoff from a previous conversation. Read it to understand where we left off. **Do NOT take any action** — just confirm you understood with a brief summary (2-3 sentences max) and wait for my next instruction.
```

After the framing header, include:
- **Branch state** (clean/dirty, ahead/behind)
- **What was completed** (from commits AND conversation)
- **What's pending** (uncommitted changes, next steps, deferred requests)
- **Conversation context** — decisions, preferences, anything the next session needs to know

Write the prompt in whatever language the user has been communicating in.

### 5. Review and trim

Check the generated prompt against quality gates:
- Under ~40 lines? If not, summarize further — point to files and issues instead of inlining detail.
- No code blocks or diffs pasted inline? Remove any — the next session can read files itself.
- No imperative language? Replace "run the tests" with "tests are failing on auth.ts:52".
- Includes branch/issue context? Verify branch name and issue number are present.
- Captures conversation decisions? Verify the highest-value items (why approach A over B, deferred ideas).

### 6. Copy to clipboard

Copy to clipboard using `pbcopy` on macOS, `xclip` on Linux. If neither is available, inform the user. Show the prompt in a fenced code block for review.

### 7. Report

<report>

Present concisely:
- **Prompt length:** line count
- **Sources used:** conversation, git, issue (list which were available)
- **Clipboard:** copied / not available
- **Audit results:** self-audit summary
- **Errors:** issues encountered (or "none")

</report>

## Next action

Paste the prompt into a new Claude Code conversation to resume work.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — git state checked, issue identified if available
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — prompt generated and displayed in fenced code block
4. **Length gate?** — prompt is under ~40 lines
5. **Anti-patterns clean?** — no diffs, no imperative language, no missing branch context
6. **Conversation decisions captured?** — highest-value items (why A over B, deferred ideas) present

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Self-contained?** — a fresh session can understand the prompt without prior context
2. **No stale content?** — no inlined code or diffs that will go stale immediately
3. **Branch/issue present?** — fastest path to full context reconstruction is included
4. **Language match?** — prompt is in the user's communication language

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Not a git repo | Generate from conversation context only, note limitation |
| No commits on branch | Note "fresh branch" in prompt, proceed |
| No issue identifiable | Skip issue section, proceed |
| Clipboard tool unavailable | Show prompt in code block, inform user to copy manually |
| Minimal conversation | Generate lightweight prompt with branch/issue state only |

## Anti-patterns

- **Too long.** A continuation prompt over ~40 lines overwhelms the next session's context — because token-heavy prompts crowd out the new conversation's working memory. Summarize ruthlessly; point to files and issues, don't paste them.
- **Including full diffs or code blocks.** The next session can read files and run `git diff` itself — because embedded code wastes tokens and goes stale immediately.
- **Imperative language that forces actions.** "Run the tests", "commit the changes" — because these cause the next session to act without confirming. Describe state, let the next session decide.
- **Forgetting conversation decisions.** Code state is recoverable from git. What's NOT recoverable: why approach A over B, preferences expressed, deferred ideas — because these are the highest-value items to capture.
- **Omitting branch/issue context.** Without branch name and issue number, the next session starts blind — because these are the fastest way to reconstruct full context.

## Guidelines

- **Context, not instructions.** The prompt gives situational awareness so the next session can continue naturally. Avoid imperative language — because imperative prompts cause the next session to act without confirming, which surprises the user.

- **Match the user's language.** Write the continuation prompt in whatever language the user has been communicating in — because language mismatch creates friction and feels impersonal.

- **Decisions over diffs.** Prioritize capturing why decisions were made, not what code changed — because code changes are recoverable from git, but reasoning is lost when the session ends.

- **Length gate is non-negotiable.** If the prompt exceeds ~40 lines, summarize further before presenting — because verbose handoffs hurt more than they help.
