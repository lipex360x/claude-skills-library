# Audit Report: create-diagram

Plugin: design
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Extensive trigger list: "create a diagram", "draw this", "make a flowchart", "diagram this architecture", covers reference image replication. Includes "even if they don't explicitly say 'diagram'" |
| 2 | WHAT + WHEN? | ✅ | Describes spec-driven workflow with HTML preview + Excalidraw export AND when it activates (visual diagrams, reference images, explicit requests) |
| 3 | "Even if" pattern? | ✅ | Present: "even if they don't explicitly say 'diagram'" (line 3) |
| 4 | Under 500 lines? | ✅ | 192 lines — well under limit |
| 5 | Imperative form? | ✅ | "Understand the diagram", "Design consultation", "Generate the spec", "Open the HTML" — consistently imperative |
| 6 | Constraints reasoned? | ✅ | Excellent reasoning throughout: "the spec is the contract — no guessing allowed" (line 51), "A beautiful HTML followed by a broken Excalidraw feels like a bait-and-switch" (line 102), "the briefing turns a negative surprise into an informed decision" (line 102) |
| 7 | Numbered steps? | ✅ | All phases use numbered steps (Phase 1: 3 steps, Phase 2: 4 steps, Phase 3: agent structure) |
| 8 | Output formats defined? | ✅ | Three output files: `<name>-spec.json`, `<name>.html`, `<name>.excalidraw` — formats described in detail |
| 9 | Input contract? | ✅ | `$ARGUMENTS` for description, reference image for replicate route, task routing table (lines 22-26) defines required vs optional inputs |
| 10 | Quality repeated at key points? | ✅ | Quality reinforced in spec generation ("every visual detail must be in the spec"), HTML generation ("typography", "color", "atmosphere"), validation ("bounding-box overlap", "text fits container", "arrow sanity"), and guidelines section |
| 11 | Anti-patterns named? | ✅ | 8 anti-patterns explicitly listed (lines 185-192): generating HTML without spec, standalone text annotations, generic fonts, sending HTML source to agent, missing icons, random IDs, skipping validation, modifying HTML without updating spec |
| 12 | Refinement step? | ✅ | Validation loop in Phase 2 (lines 83-89): "If the user requests changes: update spec → regenerate HTML → re-open → repeat until approved" |
| 13 | Error handling patterns? | ✅ | Post-generation validation checks (lines 150-158): bounding-box overlap, text overflow, arrow sanity with specific fix instructions |
| 14 | Activation tested? | N/A | Audit scope — not tested live |
| 15 | Failure modes checked? | N/A | Audit scope — not tested live |
| 16 | Agent context complete? | ✅ | Agent prompt template (lines 122-142) includes: spec path, format reference path, HTML path, conversion rules with 6 specific mappings |
| 17 | Tool access explicit? | ⚠️ | Agent is launched with `run_in_background: true` (line 144) but doesn't explicitly list which tools the agent needs (Read, Write, Bash). Implied but not stated |
| 18 | Two-phase build? | ✅ | Clear two-phase: Phase 2 (HTML preview + validation) → Phase 3 (Excalidraw export). Fidelity briefing (Phase 2.5) gates the transition |
| 19 | Race conditions mitigated? | ✅ | Sequential flow prevents races: spec → HTML → user approval → layout update → agent launch. No parallel writes to same files |
| 20 | Standard layout? | ✅ | SKILL.md + references/excalidraw-format.md + templates/diagram-spec.md + README.md |
| 21 | References one level deep? | ✅ | Single `references/` directory with one file |
| 22 | Large refs have TOC? | ✅ | excalidraw-format.md (460 lines) has TOC at top (lines 5-19) |
| 23 | Self-contained? | ✅ | No cross-skill dependencies. All Excalidraw format info is in its own reference |
| 24 | README generated? | ✅ | Complete README with triggers, how it works, usage, directory structure, output, installation |
| 25 | CLAUDE.md compliance? | ✅ | Under 500 lines, self-contained, no cross-skill deps, no local paths in public content |

## Score: 23/23 (N/A excluded)

## Priority fixes (ordered by impact)

1. **Agent tool access** — Add explicit tool list to agent prompt (Read, Write, Bash are needed). Minor gap — behavior is correct, just not documented in the prompt template.
