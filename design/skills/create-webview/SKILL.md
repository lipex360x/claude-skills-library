---
name: create-webview
description: >-
  Create beautiful data-driven HTML presentations from structured data sources.
  Full pipeline: data extraction → SQLite → JSON → dynamic HTML slides → PDF export.
  Use when the user says "create a presentation", "make slides from this data",
  "build a webview", "data to slides", "generate a report", wants to turn
  spreadsheets or databases into visual presentations, or needs a dynamic
  HTML slide deck — even if they don't explicitly say "webview."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Agent
  - AskUserQuestion
argument-hint: "[data-sources-or-description]"
---

# Create Webview

Transform structured data from any source (Excel, PowerPoint, CSV, JSON, SQLite, images) into polished HTML slide presentations with optional PDF export.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `data-sources-or-description` | $ARGUMENTS | no | Non-empty string or data files in working directory | AUQ: ask for data sources, topic, audience, purpose |
| Brand identity | Conversation | no | Primary color, font preference, logo | Use defaults: dark theme, DM Sans |
| Slide dimensions | Conversation | no | Width × Height in pixels | Default: 1440×810 (16:9) |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| HTML presentation | `<project>/output/index.html` | yes | Self-contained HTML with JS/CSS |
| Stylesheets | `<project>/output/css/styles.css` | yes | CSS with custom properties |
| Renderer | `<project>/output/js/renderer.js` | yes | JavaScript function array pipeline |
| Data JSON | `<project>/output/data.json` | yes | JSON with fixed schema |
| SQLite database | `<project>/data/*.db` | yes | SQLite |
| Extraction script | `<project>/data/extract.py` | yes | Python |
| Generator script | `<project>/data/generate.py` | yes | Python |
| Validation dataset | `<project>/data/validation.json` | yes | JSON cross-reference |
| PDF export | `<project>/output/presentation.pdf` | yes | PDF via Chrome CDP |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Source data files | Working directory | R | xlsx, pptx, csv, json, sqlite, images |
| Chrome browser | System | R/W | CDP protocol for PDF export |
| Local HTTP server | `localhost:8080` | R | Python http.server (temporary, for PDF export) |

</external_state>

## Pre-flight

<pre_flight>

1. `python3 --version` → if missing: "Python 3 required for data extraction and PDF export." — stop.
2. Run `scripts/check-deps.py` → if dependencies missing: install required Python libraries (`openpyxl`, `python-pptx`, `Pillow`) — continue after install.
3. Source data available → if no data files and no description in $ARGUMENTS: AUQ with options `["Sim, rodar /inspire-me", "Não, vou te passar as infos agora"]` — proceed with whatever the user provides.
4. Brand identity clarified → if not provided: ask for primary color, font preference, logo via AUQ — use defaults if user skips.

</pre_flight>

## Steps

### 1. Discovery and setup

Parse `$ARGUMENTS` for the presentation description. If insufficient, ask with `AskUserQuestion`:
- Data sources (xlsx, pptx, csv, json, sqlite, images)
- Presentation topic, audience, purpose
- Brand identity: primary color, font preference, logo
- Slide dimensions (default: 1440×810 / 16:9)

Create the project structure:
```
<project>/
├── data/           # extraction scripts, SQLite DB, validation JSON
├── output/         # final deliverables
│   ├── css/        # stylesheets
│   ├── js/         # renderer and helpers
│   └── img/        # extracted and processed images
```

Extract image assets immediately if source files contain images — CSS `filter` properties fail silently in Chrome print mode. Create processed versions with Python (Pillow) during extraction, not at render time.

### 2. Data extraction

Read `references/data-extraction.md` for source-type handling, dependency map, and validation format.

1. Analyze source file structure: sheets, tables, relationships, field types, data ranges.
2. Design a SQLite schema tailored to serve the presentation — normalize for querying, denormalize for simpler JSON generation.
3. Write `data/extract.py` to parse source files and populate SQLite. Handle edge cases: empty cells, merged rows, inconsistent dates, encoding issues.
4. Generate `data/validation.json` — document-centric cross-reference with `_meta`, `primary_items`, `excluded_items`, `invalidated_items`, `reference_index`, `summary_stats`.
5. **Gate: present validation summary to user.** Show discrepancies, totals, filtered items. User must approve data before proceeding — wrong data in a client presentation destroys credibility faster than any design flaw.

If no data files exist (user provided only a description), skip this step — build the JSON manually in Step 3.

### 3. JSON generation

Read `references/json-contract.md` for schema rules and null handling.

1. Write `data/generate.py` that queries SQLite and produces `output/data.json`.
2. Enforce fixed schema contract — ALL sections always present. Use `null` for objects or `[]` for arrays when empty. Structure never changes, only content.
3. Support filter parameters via command-line arguments (`--cutoff`, `--category`, custom flags). Filters change content, not structure.
4. Validate: every section the renderer expects must exist in the generated JSON.

### 4. HTML rendering

Read `references/html-renderer.md` for component patterns, CSS naming, and typography.

1. Build HTML shell from `templates/shell.html`: title, meta tags, Google Fonts, viewport.
2. Define brand identity via CSS custom properties from `templates/base-styles.css`: `--primary`, `--primary-light`, `--primary-muted`, typography, surface colors. Write to `output/css/styles.css`.
3. Build slide renderer from `templates/renderer-base.js`: function array pipeline, spread support, null guards, helper functions (`el`, `slide`, `header`, `nextSlide`). Write to `output/js/renderer.js`.
4. Build each slide type with meticulous visual hierarchy: cover, summary/metrics, data slides, detail slides, closing slide. Start with 5–7 core types — add more only if data demands it.
5. Open in browser: `open output/index.html`.
6. **Refinement loop.** Ask: "How can I make what's here more polished?" — not "What else can I add?" Iterate until approved.

### 5. PDF export

Read `references/pdf-export.md` for CDP setup and all workarounds.

1. Start local server: `python3 -m http.server 8080 --directory output/`.
2. Run `scripts/export-pdf.py` with slide dimensions.
3. Chrome runs headed (not headless) — the user sees exactly what's being exported.
4. Verify PDF: page count matches slide count, images render correctly, no blank pages, no clipped content, no missing fonts. Re-export if verification fails.

### 6. Report

<report>

Present concisely:
- **Pipeline completed:** phases executed, artifacts created (list file paths)
- **Data validation:** summary of extraction results and user-approved data
- **Slide count:** number and types of slides rendered
- **PDF status:** exported successfully or skipped (with reason)
- **Audit results:** self-audit + content audit summary
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Share the presentation with stakeholders. Run `/push` if working inside a git repo.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — Python available, dependencies installed, data source confirmed
2. **Steps completed?** — list any skipped phases with reason (e.g., "no data files — JSON built manually")
3. **Output exists?** — `output/index.html` renders in browser, `output/data.json` has valid structure, `output/css/` and `output/js/` populated
4. **Fixed schema intact?** — JSON structure has all expected keys, no missing sections
5. **Anti-patterns clean?** — no CSS filters for print, no generic fonts, no hardcoded paths, no base64 embedded images
6. **Approval gates honored?** — data validation approved by user before rendering

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Data accuracy?** — cross-reference rendered slide content against `data/validation.json` totals and categories. Numbers on slides must match source data exactly.
2. **Visual hierarchy correct?** — cover slide sets tone, metrics use large numbers with trend indicators, data slides have proper zebra striping and alignment.
3. **Self-contained HTML?** — presentation works offline. Only Google Fonts as external dependency. No CDN libraries, no remote images, no API calls.
4. **PDF fidelity?** — if exported, PDF page count matches slide count. No blank pages, no clipped content, no missing fonts. Images render correctly (no CSS filter reliance).
5. **Brand consistency?** — CSS custom properties match the agreed brand identity. Typography is distinctive (not Arial/Inter/Roboto). Color palette applied consistently across all slide types.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Python not installed | Report: "Python 3 required" — stop |
| Missing Python libraries | Auto-install via `pip install` — continue |
| Source file parse error | Report file and error details, suggest format fix — stop |
| SQLite schema mismatch | Report column/type mismatch, suggest schema correction — stop |
| Chrome not available for PDF | Skip PDF export, report: "Chrome required for PDF" — deliver HTML only |
| CDP connection failure | Retry once with fresh `--user-data-dir`, report if still failing — stop |
| Partial completion | Report what succeeded, suggest manual fix for remainder |

## Anti-patterns

- **Generic fonts (Arial, Inter, Roboto).** Use distinctive typography (DM Sans, JetBrains Mono, Space Grotesk) — because generic fonts make presentations look templated and unmemorable.
- **CSS filters for print output.** `brightness()`, `grayscale()`, etc. fail silently in Chrome print mode — because the PDF will look different from the browser preview with no error.
- **Hardcoded absolute paths in scripts.** Use relative paths from project root — because scripts break when the project moves or another user runs them.
- **Changing JSON structure per filter.** Filters change content, structure stays fixed — because the renderer depends on consistent keys and will break on missing sections.
- **Skipping the data validation gate.** Wrong data in slides is worse than no slides — because a single wrong number in a client presentation destroys trust.
- **`white-space: normal` on badges/tags.** Use `nowrap` — because line breaks in small UI elements look broken.
- **Headless Chrome for export.** Use headed mode — because headless hides rendering issues that only surface in the final PDF.
- **Over-engineering slide types.** Start with 5–7 core types — because more types create maintenance burden without visual payoff.
- **Generating HTML without understanding data first.** Data extraction (Step 2) must complete before rendering (Step 4) — because slides built on assumed data structure will need full rewrites.
- **Embedding base64 images in HTML.** Use file references in `output/img/` — because base64 bloats the HTML file and makes debugging image issues impossible.

## Guidelines

- **Quality at every phase.** Each phase produces a deliverable that must stand on its own. Extraction scripts should be clean. JSON should be human-readable. HTML should be beautiful. PDF should be pixel-perfect — because meticulous craftsmanship at each stage prevents compounding errors.

- **Self-contained HTML.** Every presentation must work standalone. Inline CSS or local files in `output/css/`. Only Google Fonts as external dependency — because presentations are often shared offline or on restricted networks.

- **Dark themes for technical presentations.** Default to dark backgrounds (#0a0a0a to #1a1a1a) for engineering reports, analytics dashboards. Light themes for business or client-facing decks. Ask if ambiguous — because the wrong theme undermines the content's credibility with its audience.

- **Fixed JSON schema is the contract.** Once defined in Step 3, it never changes. Filters change content, not structure — because renderer stability depends on predictable keys.

- **Validation before rendering.** The validation dataset catches data mismatches before they reach slides. Present discrepancies explicitly — because the user must confirm data correctness before visual work begins.

- **Pre-process image assets.** Extract images from source files early. Store in `output/img/` as actual files. Create processed versions with Python (Pillow) — because CSS filters are unreliable in print mode.

- **Refinement over addition.** Ask "How can I make this more polished?" not "What else can I add?" — because polish compounds while feature additions create complexity.
