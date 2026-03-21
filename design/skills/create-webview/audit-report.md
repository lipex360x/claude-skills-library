# Audit Report: create-webview

Plugin: design
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Covers "create a presentation", "make slides from this data", "build a webview", "data to slides", "generate a report", spreadsheet/database conversions. Includes "even if they don't explicitly say 'webview'" |
| 2 | WHAT + WHEN? | ✅ | WHAT: full pipeline data → SQLite → JSON → HTML slides → PDF. WHEN: presentation requests, data visualization, report generation |
| 3 | "Even if" pattern? | ✅ | Present: "even if they don't explicitly say 'webview'" (line 9) |
| 4 | Under 500 lines? | ✅ | 172 lines — well under limit |
| 5 | Imperative form? | ✅ | "Understand the project", "Check dependencies", "Create the project structure", "Analyze source files", "Write the extraction script" — consistently imperative |
| 6 | Constraints reasoned? | ✅ | Excellent reasoning throughout: "The schema serves the slides, not academic purity" (referenced in data-extraction.md), "This is non-negotiable. Wrong data in a client presentation destroys credibility" (line 69), "Refinement over addition" (line 120), "Transparency builds trust" (line 144), "CSS filter properties fail silently in Chrome print mode" (line 49) |
| 7 | Numbered steps? | ✅ | All 4 phases use numbered steps. Phase 0: 4 steps, Phase 1: 5 steps, Phase 2: 4 steps, Phase 3: 6 steps, Phase 4: 5 steps |
| 8 | Output formats defined? | ✅ | Complete output listing: extract.py, generate.py, validation.json, index.html, styles.css, renderer.js, data.json, presentation.pdf. README mirrors this (lines 55-62) |
| 9 | Input contract? | ✅ | `$ARGUMENTS` for description, `argument-hint` in frontmatter, `AskUserQuestion` for missing info (lines 30-34), graceful handling of "no data files found" scenario (line 35) |
| 10 | Quality repeated at key points? | ✅ | Quality emphasized in guidelines ("meticulous craftsmanship — not 'good enough'", line 150), at Phase 1 validation gate (line 69), Phase 3 refinement loop (line 120), Phase 4 PDF verification (line 145-146) |
| 11 | Anti-patterns named? | ✅ | 10 anti-patterns explicitly listed (lines 162-173): generic fonts, CSS filters for print, hardcoded paths, changing JSON structure, skipping validation, white-space on badges, headless Chrome, over-engineering slides, HTML without understanding data, base64 images |
| 12 | Refinement step? | ✅ | Phase 3 step 6 (lines 120-121): "Ask the user for feedback. At each iteration, ask: 'How can I make what's here more polished?' — not 'What else can I add?' Refinement over addition. Iterate until approved." |
| 13 | Error handling patterns? | ✅ | Validation gate in Phase 1 (line 69), dependency check in Phase 0 (line 37), PDF verification in Phase 4 (line 145-146), known-pitfalls.md covers 8 specific failure modes with root causes and fixes |
| 14 | Activation tested? | N/A | Audit scope |
| 15 | Failure modes checked? | N/A | Audit scope |
| 16 | Subagents? | N/A | No subagents used |
| 17 | Standard layout? | ✅ | SKILL.md + references/ (5 files) + templates/ (3 files) + scripts/ (2 files) + README.md |
| 18 | References one level deep? | ✅ | Single `references/` directory |
| 19 | Large refs have TOC? | ⚠️ | html-renderer.md (455 lines) has no TOC — uses section headers but no table of contents at top. known-pitfalls.md has a quick reference table at the end (good) but no TOC |
| 20 | Self-contained? | ✅ | All references are local. No cross-skill dependencies. Only external suggestion is `/inspire-me` in the "no data files" flow, but it's a user-facing suggestion, not a dependency |
| 21 | README generated? | ✅ | Complete README with trigger phrases, how it works, usage examples, directory structure, output listing, installation |
| 22 | CLAUDE.md compliance? | ✅ | Under 500 lines, self-contained, no local paths in public content |
| 23 | templates referenced exist? | ✅ | shell.html exists and matches description. base-styles.css and renderer-base.js referenced in SKILL.md are present in templates/ |
| 24 | scripts referenced exist? | ✅ | check-deps.py and export-pdf.py both present in scripts/ |

## Score: 21/22 (N/A excluded)

## Priority fixes (ordered by impact)

1. **Large refs missing TOC** — Add table of contents to html-renderer.md (455 lines). It's the most navigated reference in this skill and currently has no index.
