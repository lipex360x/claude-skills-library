# Audit Report: start-issue

Plugin: workflow
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy enough? | ✅ | 5 trigger phrases: "start issue", "work on issue #N", "pull from backlog", "start #N" |
| 2 | Description: WHAT + WHEN? | ✅ | "Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks" + triggers |
| 3 | Description: "even if" pattern? | ✅ | "even if they don't explicitly say 'issue'" |
| 4 | Body: under 500 lines? | ✅ | 293 lines |
| 5 | Body: imperative form? | ✅ | "Parse", "Fetch", "Extract", "Transform", "Present" |
| 6 | Body: constraints reasoned? | ✅ | Extensive reasoning throughout. TDD explained (line 233), no workarounds explained (line 276), codebase-aware plans explained (line 249), ARCHITECTURE.md explained (line 274), test isolation explained (lines 235-239) |
| 7 | Body: numbered steps? | ✅ | 7 numbered steps with sub-steps (2b, 2c, 5b) |
| 8 | Body: output formats defined? | ✅ | Step 3 references templates/step-template.md. Issue body format with What/Why/Acceptance criteria/Steps fully defined. Task preview format defined |
| 9 | Body: input contract? | ✅ | Line 15: "Parse $ARGUMENTS for an issue number. Accept both direct numbers (2) and index references (#2)" |
| 10 | Quality: repeated at key points? | ✅ | TDD repeated in Steps 2c and Guidelines. "No workarounds" repeated in 2c and Guidelines. Agent Teams check repeated with "MUST" emphasis in Step 3 |
| 11 | Quality: anti-patterns named? | ✅ | Lines 282-293: 11 explicit anti-patterns including "Checkboxes without TDD order", "Generic checkboxes without file paths", "Steps that mix concerns", "Missing verification checkboxes", "Local/absolute paths" |
| 12 | Quality: refinement step? | ✅ | Step 3: "Before presenting, review the plan with a critical eye: tighten vague checkboxes, remove redundancy, ensure TDD order, verify file paths are concrete" + approval gate with "I want to adjust" loop |
| 13 | Quality: error handling? | ✅ | Step 1 handles missing argument (query board), missing board (offer to create), empty board (inform and stop). Step 5b handles missing board and blockers |
| 14 | Testing: invoked with realistic input? | N/A | Audit-only |
| 15 | Testing: activation tested (3+ phrases)? | N/A | Audit-only |
| 16 | Testing: failure modes checked? | N/A | Audit-only |
| 17 | Subagents: agent context? | ✅ | Step 7 defines teammate spawning with TeamCreate, model inheritance, Execution mode section |
| 18 | Subagents: tool access explicit? | ⚠️ | No explicit tool list for teammates. TeamCreate invocations should specify what tools teammates need |
| 19 | Subagents: two-phase build? | N/A | Not a two-phase build pattern — teammates work on assigned Steps |
| 20 | Subagents: race conditions mitigated? | ✅ | Sequential prefix identified before parallelism. "Mark blocked teammates" explicitly required (line 131) |
| 21 | Structure: standard layout? | ✅ | SKILL.md, references/, templates/, README.md — full standard layout |
| 22 | Structure: references one level deep? | ✅ | 4 reference files, all one level deep |
| 23 | Structure: large refs have TOC? | ✅ | tdd-methodology.md (192 lines) has TOC. cdp-best-practices.md (245 lines) has numbered sections. project-board-setup.md (179 lines) has numbered sections |
| 24 | Structure: self-contained? | ✅ | All references are local copies. No cross-skill imports. References to /add-backlog in Step 4 describe behavior, not import |
| 25 | Structure: README generated? | ✅ | README.md exists |
| 26 | Compliance: CLAUDE.md? | ✅ | English, no local paths, project-agnostic |

## Score: 20/22

## Priority fixes (ordered by impact)

1. **Subagent tool access** — When spawning teammates via TeamCreate in Step 7, specify which tools each teammate needs (Bash, Read, Write, Edit, Grep, Glob at minimum). Without this, teammates may lack access to essential tools.
2. **Minor: Guidelines section length** — The guidelines section (lines 230-293) is 63 lines. While each guideline is well-reasoned, the density may cause agents to skip later entries. Consider extracting the longest guidelines (test isolation, CDP, DDD) to a reference file with Read tool instructions.
