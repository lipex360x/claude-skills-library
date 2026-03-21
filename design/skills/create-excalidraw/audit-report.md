# Audit Report: create-excalidraw

Plugin: design
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Covers "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "generate an Excalidraw file", "draw this", "diagram this". Includes "even if they don't explicitly say 'Excalidraw'" |
| 2 | WHAT + WHEN? | ✅ | WHAT: generates Excalidraw JSON from natural language. WHEN: diagram/visual requests with extensive keyword list |
| 3 | "Even if" pattern? | ✅ | Present: "even if they don't explicitly say 'Excalidraw'" (line 3) |
| 4 | Under 500 lines? | ✅ | 172 lines — well under limit |
| 5 | Imperative form? | ✅ | "Analyze the user's description", "Read references/design-aesthetics.md", "Save as", "Verify" — consistently imperative |
| 6 | Constraints reasoned? | ⚠️ | Some reasoning: "Never default to light-blue-on-white — that's the hallmark of generic AI diagrams" (line 13). But many rules are stated without reasoning: "fontFamily: 5 — required for ALL text" (line 68) contradicts the excalidraw-format.md reference which recommends fontFamily 3 for labels and 2 for descriptions. The design-aesthetics.md reference also says "All text uses fontFamily: 5" (line 72) which conflicts with the format reference |
| 7 | Numbered steps? | ✅ | 8 numbered top-level steps with sub-steps |
| 8 | Output formats defined? | ✅ | Output is `.excalidraw` JSON file. Summary template at lines 143-151 shows expected delivery format |
| 9 | Input contract? | ⚠️ | Accepts "user's description" as input but doesn't define required vs optional. No `$ARGUMENTS` reference. No `argument-hint` in frontmatter. No `user-invocable` field in frontmatter |
| 10 | Quality repeated at key points? | ✅ | Design-first approach (step 1), palette selection, anti-patterns in design-aesthetics.md, validation checklist (step 8) |
| 11 | Anti-patterns named? | ✅ | 8 anti-patterns in design-aesthetics.md (lines 82-92): same-size-same-color nodes, perfect grid, straight arrows everywhere, no visual hierarchy, default white bg, rainbow colors, cramped text, arrows crossing elements |
| 12 | Refinement step? | ❌ | No refinement/validation loop. No user feedback step. Generates and delivers — no "ask user to approve" or iteration cycle. Contrast with create-diagram which has a full validation loop |
| 13 | Error handling patterns? | ⚠️ | Validation checklist at step 8 (lines 155-162) verifies structure, but no guidance on what to do when checks fail. No fallback behavior defined |
| 14 | Activation tested? | N/A | Audit scope |
| 15 | Failure modes checked? | N/A | Audit scope |
| 16 | Subagents? | N/A | No subagents used |
| 17 | Standard layout? | ✅ | SKILL.md + references/ (4 files) + scripts/ (3 files) + templates/ (8 templates) + README.md |
| 18 | References one level deep? | ✅ | Single `references/` directory |
| 19 | Large refs have TOC? | ⚠️ | element-types.md (497 lines) has no TOC — uses `---` dividers but no TOC header. excalidraw-schema.md (351 lines) has no TOC either |
| 20 | Self-contained? | ✅ | All references are local. No cross-skill dependencies |
| 21 | README generated? | ✅ | Complete README with triggers, how it works, supported types, structure, install |
| 22 | CLAUDE.md compliance? | ✅ | Under 500 lines, self-contained, no local paths |
| 23 | fontFamily contradiction | ❌ | SKILL.md line 68 says "fontFamily: 5 (Excalifont) — required for ALL text elements". But the same skill's excalidraw-format.md reference (line 260) recommends fontFamily 3 for labels and 2 for descriptions. Also the excalidraw-schema.md reference uses fontFamily 1 and 2 in examples. This is a conflicting instruction that will confuse execution |

## Score: 16/21 (N/A excluded)

## Priority fixes (ordered by impact)

1. **fontFamily contradiction** — Resolve the conflict between SKILL.md ("fontFamily: 5 required for ALL") and excalidraw-format.md ("fontFamily 3 for labels, 2 for descriptions"). Pick one convention and align all files.
2. **No refinement step** — Add a validation/feedback loop. Currently generates and delivers with no user approval gate. At minimum, add "present to user and ask for adjustments."
3. **Input contract missing** — Add `user-invocable: true` and `argument-hint` to frontmatter. Define what `$ARGUMENTS` provides vs what needs to be asked via `AskUserQuestion`.
4. **Large refs missing TOC** — Add table of contents to element-types.md (497 lines) and excalidraw-schema.md (351 lines).
5. **Error handling gaps** — Add "what to do when validation fails" guidance after the validation checklist.
