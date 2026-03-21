# Audit Report: capture-voice

Plugin: content
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: Pushy enough? | PASS | Description includes 6 trigger contexts: `/capture-voice`, PreCompact hook, "meu estilo", "como eu falo", "aprenda meu jeito", voice profile updates (line 3) |
| 2 | Description: WHAT + WHEN? | PASS | WHAT: "Analyzes the current conversation to capture the user's writing voice for content generation." WHEN: lists explicit triggers including slash command, hook, and natural language phrases (line 3) |
| 3 | Description: "Even if" pattern? | PASS | "even if they don't explicitly say 'voice' or 'myvoice'" (line 3) |
| 4 | Body: Under 500 lines? | PASS | 81 lines total — well within limit |
| 5 | Body: Imperative form? | PASS | Uses imperatives throughout: "Read the current voice profile" (line 16), "Scan all user messages" (line 20), "Extract:" (line 22), "Compare findings" (line 39), "Merge new observations" (line 53) |
| 6 | Body: Constraints reasoned? | PASS | Constraints include reasoning: "require at least 2 messages showing the same pattern before recording. One-off phrasing is noise, not signal" (line 42), "never delete previous entries, because a run with limited context might discard patterns" (line 79), "False negatives are cheap (you'll catch it next run). False positives pollute the profile permanently" (line 80) |
| 7 | Body: Numbered steps? | PASS | 5 numbered steps: Load existing profile, Analyze conversation, Deduplicate and validate, Consolidate before appending, Write updates (lines 14-61) |
| 8 | Body: Output formats defined? | PASS | Output format specified: one-line entries in Portuguese with concrete examples in quotes (lines 54-57), changelog format `### YYYY-MM-DD HH:MM` (line 60), frontmatter `updated` field (line 61) |
| 9 | Body: Input contract? | FAIL | No explicit input contract. The skill implicitly requires the current conversation as input and an optional existing profile, but never states required vs optional inputs or validation rules (e.g., minimum conversation length, what happens with zero user messages) |
| 10 | Quality: Quality repeated at key points? | PASS | Quality gate repeated at step 5: "Se eu usar só esse perfil para escrever um post, vai soar como o usuário escreveu?" (line 63). Also at step 2: "Each observation must be specific enough that another AI could write a post" (line 30) |
| 11 | Quality: Anti-patterns named? | PASS | 7 anti-patterns explicitly named with bad/good examples (lines 65-76): generic observations, over-reading single messages, duplicate wording, capturing content vs style, capturing Claude interaction, capturing typos, empty changelogs |
| 12 | Quality: Refinement step? | PASS | Step 4 "Consolidate before appending" serves as explicit refinement — scan for overlapping entries, merge redundant ones (lines 47-49) |
| 13 | Quality: Error handling patterns? | PARTIAL | Handles missing profile (line 16: "If the file doesn't exist, create it from template"), handles no-new-patterns case (line 45: "stop here"). Does not handle: conversation too short, profile file corrupted/malformed, write failures |
| 14 | Testing: Invoked with realistic input? | FAIL | No evidence of testing documentation or test scenarios |
| 15 | Testing: Activation tested (3+ trigger phrases)? | FAIL | No testing documentation. Description lists 5+ triggers but no verification that model actually activates on them |
| 16 | Testing: Failure modes checked? | FAIL | No failure mode testing documented |
| 17 | Subagents: Agent context complete? | PARTIAL | Line 12 says "Run this as a background agent" but does not specify what context to pass to the agent (conversation history, profile path, etc.) |
| 18 | Subagents: Tool access explicit? | FAIL | No explicit tool access list. The agent needs Read, Write/Edit at minimum, but this is never stated |
| 19 | Subagents: Two-phase build? | FAIL | No two-phase build pattern (draft then review). The skill goes straight from analysis to writing |
| 20 | Subagents: Race conditions mitigated? | FAIL | No mention of race conditions. If the user triggers another capture-voice while one is running (background agent), or if the profile is being edited concurrently, no mitigation is specified |
| 21 | Structure: Standard layout? | PARTIAL | Has SKILL.md and templates/ but no references/ directory. The anti-patterns and guidelines sections are inline (acceptable at 81 lines, but could be extracted if the skill grows) |
| 22 | Structure: References one level deep? | N/A | No references/ directory |
| 23 | Structure: Large refs have TOC? | N/A | No references/ directory |
| 24 | Structure: Self-contained? | PASS | No cross-skill dependencies. Only references its own template and `~/.brain/memory/voice-profile.md` |
| 25 | Structure: README generated? | PASS | README.md exists with usage, how-it-works, directory structure, and installation sections |
| 26 | Compliance: CLAUDE.md compliance? | PARTIAL | Skill references `~/.brain/memory/voice-profile.md` — a local path that would appear in the skill file shipped to other users. Per memory rule `feedback_no_local_paths.md`, local paths should not appear in public content. The path should use a placeholder or be configurable |

## Score: 14/26

## Priority fixes (ordered by impact)

1. **Subagent tool access** — The skill says "Run this as a background agent" (line 12) but never specifies which tools the agent needs (Read, Write/Edit, Bash). Without this, the spawned agent may lack permissions to read or write the voice profile.
2. **Race condition mitigation** — No protection against concurrent runs. Since this runs as a background agent and can be triggered by PreCompact hook or manual invocation simultaneously, add file locking or a "skip if already running" guard.
3. **Input contract** — Add explicit required/optional inputs: conversation context (required, minimum N user messages), existing profile path (optional, default location). Define behavior when conversation has zero analyzable user messages.
4. **Local path in skill body** — Line 16 hardcodes `~/.brain/memory/voice-profile.md`. This is a user-specific path that won't work for other users. Use a placeholder like `(e.g., ~/.brain/memory/voice-profile.md)` or make it configurable.
5. **Subagent context** — Specify what context to pass when spawning the background agent: full conversation history, profile file path, template path. Without this, the agent may not have enough context to analyze.
6. **Two-phase build** — Add a draft-then-validate phase: the agent should draft proposed changes, validate them against the quality test (line 63), then write. Currently it goes straight from analysis to writing with no review gate.
7. **Testing documentation** — No test scenarios, trigger verification, or failure mode checks exist. Add at minimum: 3 trigger phrase tests, a test with empty conversation, a test with an existing rich profile.
