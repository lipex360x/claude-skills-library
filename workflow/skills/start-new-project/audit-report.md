# Audit Report: start-new-project

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 7 trigger phrases: "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build" |
| 2 | Description: WHAT + WHEN? | ✅ | "Plan and scaffold a new project from a prompt. Asks clarifying questions, proposes a phased GitHub issue structure" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'new project'" |
| 4 | Body: under 500 lines? | ✅ | 267 lines |
| 5 | Body: imperative form? | ✅ | "Check for grill-me output", "Parse the prompt", "Ask clarifying questions", "Propose the phase structure" |
| 6 | Body: constraints reasoned? | ✅ | Extensive reasoning: TDD explained (line 197), test isolation explained (lines 199-203), E2E through UI explained (line 205), docker-compose explained (line 199), ARCHITECTURE.md explained (line 250), no workarounds explained (line 252), mandatory split explained (line 73) |
| 7 | Body: numbered steps? | ✅ | 9 numbered steps |
| 8 | Body: output formats defined? | ✅ | Step 4 references templates/issue-template.md. Summary in Step 9 defines 8 report items. Phase structure format fully defined |
| 9 | Body: input contract? | ✅ | Step 1 checks for grill-output. Step 2 parses user prompt for name/stack/scope/domain. Handles bare invocation (line 38) |
| 10 | Quality: repeated at key points? | ✅ | TDD repeated in Step 4 and Guidelines. "Don't over-plan" in guidelines. Mandatory split rule in Step 4 and guidelines. CDP emphasized in Steps 4 and guidelines |
| 11 | Quality: anti-patterns named? | ✅ | Lines 258-267: 8 explicit anti-patterns including "Checkboxes without TDD order", "Generic checkboxes", "Mixed concerns", "Missing verification", "Monolithic issues", "Front-loading detail", "Local paths", "Workarounds" |
| 12 | Quality: refinement step? | ✅ | Step 4: "Before presenting, review the plan with a critical eye" + two approval gates (Step 3 answers + Step 4 structure) |
| 13 | Quality: error handling? | ⚠️ | Step 1 handles missing grill-output. Step 2 handles missing argument. No handling for: existing repo with conflicting branch names, gh CLI failures during issue/board creation, milestone creation failures |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: agent context? | ✅ | Execution mode section (lines 75-98) defines teammate structure with dependency graph |
| 18 | Subagents: tool access explicit? | ⚠️ | No explicit tool list for teammates. Same gap as start-issue |
| 19 | Subagents: two-phase build? | N/A | Not applicable |
| 20 | Subagents: race conditions mitigated? | ✅ | Sequential prefix + blocked teammates + explicit dependency tracking (lines 93-97) |
| 21 | Structure: standard layout? | ✅ | SKILL.md, references/, templates/, README.md — full layout with 4 references and 6 templates |
| 22 | Structure: references one level deep? | ✅ | All 4 references at one level |
| 23 | Structure: large refs have TOC? | ✅ | phase-planning-guide.md (210 lines) has TOC. cdp-best-practices.md (245 lines) has numbered sections. tdd-methodology.md (192 lines) has TOC |
| 24 | Structure: self-contained? | ✅ | All references are local copies. No cross-skill imports. Mentions /grill-me as a workflow suggestion (line 25), not a dependency |
| 25 | Structure: README generated? | ✅ | README.md exists |
| 26 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 20/22

## Priority fixes (ordered by impact)

1. **Subagent tool access** — Same gap as start-issue: TeamCreate invocations should specify tool access for teammates.
2. **Error handling for gh CLI** — Add graceful degradation if issue creation fails mid-flow (e.g., after creating 2 of 4 issues). Should report what was created and suggest manual completion.
3. **Minor: Guidelines density** — Guidelines section (lines 197-267) is 70 lines. The longest guidelines (test isolation, CDP, DDD) could be extracted to references with Read tool instructions to reduce cognitive load.
