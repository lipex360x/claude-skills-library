# Audit Report: extract-design-system

Plugin: design
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Covers reference images, screenshots, mockups. Triggers: "extract a design system", "create artboards", "build a component library", "reverse-engineer visual patterns". Includes "even if they don't explicitly say 'design system'" |
| 2 | WHAT + WHEN? | ✅ | WHAT: analyze image → extract design system → create artboards via parallel subagents. WHEN: user provides visual reference and wants design system extraction |
| 3 | "Even if" pattern? | ✅ | Present: "even if they don't explicitly say 'design system'" (line 3) |
| 4 | Under 500 lines? | ✅ | 87 lines — very concise |
| 5 | Imperative form? | ✅ | "Read all images", "Analyze as a design reference", "Extract:", "Write a Design Brief", "Show it to the user" — consistently imperative |
| 6 | Constraints reasoned? | ✅ | Two-phase rationale explained in detail (lines 61-63): "If agents run before setup, they race against create_artboards and produce an empty manifest." Curl vs MCP explained (line 64): "Subagents don't reliably inherit MCP tools." Lorem ipsum rule explained (line 76): "Real language distracts reviewers from evaluating visual patterns." |
| 7 | Numbered steps? | ✅ | 6 numbered steps with Phase A/B sub-structure in step 5 |
| 8 | Output formats defined? | ⚠️ | Output is artboard HTML files but the exact file format isn't explicitly listed. The artboard-guidelines.md reference defines the standard filenames (foundations.html, components.html, etc.) but SKILL.md doesn't summarize the deliverables |
| 9 | Input contract? | ⚠️ | Accepts images from `design/` folder and optional project slug argument. But no `argument-hint` in frontmatter. No explicit validation of what happens when no images are found (just Glob pattern, no error handling for empty results) |
| 10 | Quality repeated at key points? | ✅ | Quality in agent-prompt.md (craftsmanship, containment, anti-patterns), artboard-guidelines.md (containment rules as "non-negotiable"), SKILL.md guidelines (lorem ipsum, no emojis) |
| 11 | Anti-patterns named? | ✅ | Agent-prompt.md lists 7 specific anti-patterns: generic gradients, uniform spacing, oversized elements, tiny text, inconsistent border-radius, wrong colors, gray placeholder boxes |
| 12 | Refinement step? | ⚠️ | Step 3 has user approval gate via `AskUserQuestion` for the Design Brief. But no refinement loop after artboards are generated — step 6 only verifies thumbnails and takes a screenshot. No "iterate on individual artboards" guidance |
| 13 | Error handling patterns? | ❌ | No error handling defined. What if an agent fails? What if curl returns an error? What if create_artboards fails? What if no images are found in design/? The agent-prompt.md mentions "If curl fails, report the error. Do NOT fall back to Write" but SKILL.md has no orchestration-level error handling |
| 14 | Activation tested? | N/A | Audit scope |
| 15 | Failure modes checked? | N/A | Audit scope |
| 16 | Agent context complete? | ✅ | agent-prompt.md defines 6 requirements for agent prompts: Design Spec, artboard assignment, HTML template, lorem ipsum rule, curl instructions, quality standards. Curl template is complete with jq escaping |
| 17 | Tool access explicit? | ✅ | Explicitly states agents use Bash + curl, NOT Write tool, NOT MCP tools. Clear rationale for each restriction |
| 18 | Two-phase build? | ✅ | Phase A (setup: create_project, tokens.css, navigate, create_artboards) → wait → Phase B (agents). Clearly documented why (lines 47-48, 61-63) |
| 19 | Race conditions mitigated? | ✅ | Phase A must complete before Phase B: "Wait for all setup calls to complete before proceeding" (line 55). Explains the manifest race condition explicitly |
| 20 | Standard layout? | ✅ | SKILL.md + references/ (2 files) + templates/ (1 file) + README.md |
| 21 | References one level deep? | ✅ | Single `references/` directory with 2 files |
| 22 | Large refs have TOC? | N/A | No reference exceeds 100 lines |
| 23 | Self-contained? | ⚠️ | Depends on external MCP tools: `create_project`, `navigate`, `create_artboards`, `get_screenshot()`. These are expected to be available via MCP server but the skill doesn't document which MCP server provides them or how to verify availability. If the MCP server isn't configured, the skill silently fails |
| 24 | README generated? | ✅ | Complete README with usage, how it works (6-step summary), directory structure, installation |
| 25 | CLAUDE.md compliance? | ✅ | Under 500 lines, no local paths in public content |

## Score: 17/23 (N/A excluded)

## Priority fixes (ordered by impact)

1. **No error handling** — Add orchestration-level error handling: what if agent fails, what if no images found, what if MCP tools unavailable. At minimum, check MCP tool availability before starting Phase A.
2. **MCP dependency not documented** — The skill depends on `create_project`, `navigate`, `create_artboards`, `get_screenshot()` from an external MCP server. Document which MCP server provides these and add a pre-flight check.
3. **No post-build refinement** — Add guidance for iterating on individual artboards after initial generation. Currently ends at "take a screenshot" with no adjustment loop.
4. **Input contract gaps** — Add `argument-hint` to frontmatter. Add error handling for empty `design/` folder (no images found).
5. **Output format not summarized** — Add a deliverables summary to SKILL.md listing the expected output files (tokens.css, artboard HTML files, project manifest).
