---
name: create-webview
description: >
  Create beautiful data-driven HTML presentations from structured data sources.
  Full pipeline: data extraction → SQLite → JSON → dynamic HTML slides → PDF export.
  Use when the user says "create a presentation", "make slides from this data",
  "build a webview", "data to slides", "generate a report", wants to turn
  spreadsheets or databases into visual presentations, or needs a dynamic
  HTML slide deck — even if they don't explicitly say "webview."
metadata:
  category: visual-design
  tags:
    - presentation
    - slides
    - data-visualization
    - html
    - pdf
    - webview
argument-hint: "[data-sources-or-description]"
user-invocable: true
---

# Create Webview

Transform structured data from any source (Excel, PowerPoint, CSV, JSON, SQLite, images) into polished HTML slide presentations with optional PDF export. Each presentation follows a four-phase pipeline: extract data → generate JSON → render HTML slides → export PDF. The pipeline produces self-contained HTML that works offline with dynamic JavaScript rendering.

## Phase 0 — Discovery & Setup

1. **Understand the project.** Parse `$ARGUMENTS` for the presentation description. If insufficient, ask with `AskUserQuestion`:
   - Data sources (xlsx, pptx, csv, json, sqlite, images)
   - Presentation topic, audience, purpose
   - Brand identity: primary color, font preference, logo
   - Slide dimensions (default: 1440×810 / 16:9)

   **No data files found?** If there are no source files (xlsx, pptx, csv, etc.) in the working directory and the user didn't point to any, suggest: "Não encontrei arquivos de dados aqui. Quer rodar `/inspire-me` pra gente explorar o que você precisa antes?" via `AskUserQuestion` with options `["Sim, rodar /inspire-me", "Não, vou te passar as infos agora"]`. Regardless of the answer, proceed with whatever the user provides — a text description, pasted data, or even just a topic is enough to build a presentation from scratch. The pipeline adapts: skip Phase 1 (no extraction needed), build the JSON manually in Phase 2, and continue normally from Phase 3.

2. **Check dependencies.** Run `scripts/check-deps.py` to detect file types and install required Python libraries. The script inspects source files and ensures `openpyxl`, `python-pptx`, `Pillow`, or other parsers are available before extraction begins.

3. **Create the project structure.** Set up the working directories:
   ```
   <project>/
   ├── data/           # extraction scripts, SQLite DB, validation JSON
   ├── output/         # final deliverables
   │   ├── css/        # stylesheets
   │   ├── js/         # renderer and helpers
   │   └── img/        # extracted and processed images
   ```

4. **Extract image assets immediately.** If source files contain images (logos, photos, charts), extract them to `output/img/` during setup — not later. CSS `filter` properties (`brightness()`, `grayscale()`, etc.) fail silently in Chrome print mode. If you need a dark version of an image, create it with Python (Pillow) during extraction. Never rely on CSS filters to process images at render time.

## Phase 1 — Data Extraction

Read `references/data-extraction.md` for source-type handling, dependency map, and validation format.

1. **Analyze source files.** Understand the structure: sheets, tables, relationships, field types, data ranges. Map out how the data connects before writing a single line of extraction code. Sloppy analysis here cascades into broken slides downstream.

2. **Design a SQLite schema.** Tailor the schema to serve the presentation. Normalize where it aids querying, denormalize where it simplifies JSON generation. The schema serves the slides, not academic purity — a join-heavy schema that makes JSON generation painful is a bad schema.

3. **Write the extraction script.** Create `data/extract.py` to parse source files and populate the SQLite database. The script must handle edge cases: empty cells, merged rows, inconsistent date formats, encoding issues.

4. **Generate the validation dataset.** Write `data/validation.json` — a document-centric cross-reference that catches mismatches before they reach slides:
   - `_meta`: generation info (timestamp, source files, filter parameters)
   - `primary_items`: main entities with cross-references to related data
   - `excluded_items`: items filtered out, each with an explicit reason
   - `invalidated_items`: items that failed validation, each with a business reason
   - `reference_index`: inverse index by key reference for fast lookup
   - `summary_stats`: aggregated totals by category

5. **Present the validation summary to the user.** Show discrepancies, totals, and filtered items explicitly. **Gate: the user must approve the data before Phase 2.** This is non-negotiable. Wrong data in a client presentation destroys credibility faster than any design flaw.

## Phase 2 — JSON Generation

Read `references/json-contract.md` for schema rules and null handling.

1. **Write the generator script.** Create `data/generate.py` that queries the SQLite database and produces `output/data.json`. The script transforms relational data into the flat structure the renderer expects.

2. **Enforce the fixed schema contract.** ALL sections must always be present in the JSON structure. When a section has no data, use `null` for objects or `[]` for arrays. The JSON structure never changes — only content does. This is the single most important architectural decision in the pipeline. Violating it causes cascading renderer failures that are painful to debug.

3. **Support filter parameters.** Accept command-line arguments (`--cutoff`, `--category`, custom flags) that control which data appears. Filters change content, not structure. Running the generator with different filters must produce JSON with identical keys — only the values change.

4. **Validate the output.** Before proceeding, verify that every section the renderer expects exists in the generated JSON. A missing key here means a broken slide later.

## Phase 3 — HTML Renderer

Read `references/html-renderer.md` for component patterns, CSS naming, and typography.

1. **Build the HTML shell.** Read `templates/shell.html` and adapt for the project: title, meta tags, Google Fonts link, viewport settings. The shell is the container — it loads CSS, JS, and the data file, then calls the renderer.

2. **Define the brand identity via CSS custom properties.** Read `templates/base-styles.css` and set:
   - `--primary`, `--primary-light`, `--primary-muted` from the brand color
   - Typography: heading font, body font, monospace font
   - Surface colors, accent colors, border radii
   - Slide dimensions if non-default (adjust `--slide-width`, `--slide-height`)

   Write the adapted stylesheet to `output/css/styles.css`.

3. **Build the slide renderer.** Read `templates/renderer-base.js` and construct the rendering engine:
   - **Function array pipeline:** each slide type is an independent function `(data) → HTMLElement | null`
   - **Spread support:** functions may return arrays for multi-slide sections (e.g., paginated detail cards)
   - **Null guard on every renderer:** `if (!data.section || !data.section.length) return null` — missing data produces no slide, not a broken slide
   - **Helper functions:** `el(tag, attrs, children)`, `slide(opts)`, `header(tag, title, subtitle)`, `nextSlide()`

   Write the renderer to `output/js/renderer.js`.

4. **Build each slide type with meticulous attention to visual hierarchy:**
   - **Cover slide:** title, subtitle, date, branding — sets the visual tone for everything that follows
   - **Summary/metrics slides:** KPI cards with large numbers, trend indicators, category breakdowns
   - **Data slides:** tables with zebra striping, bar charts via CSS, timelines with milestones
   - **Detail slides:** cards with rich content, tags, status badges, cross-references
   - **Closing slide:** contact information, next steps, call to action

   Start with 5–7 core slide types. Add more only if the data demands it — over-engineering slide types creates maintenance burden without visual payoff.

5. **Open in the browser for validation.**

   ```bash
   open output/index.html
   ```

6. **Refinement loop.** Ask the user for feedback. At each iteration, ask: "How can I make what's here more polished?" — not "What else can I add?" Refinement over addition. Iterate until approved.

## Phase 4 — PDF Export

Read `references/pdf-export.md` for CDP setup and all workarounds.

1. **Start a local server if needed.** Chrome requires HTTP for proper font loading and asset resolution:
   ```bash
   python3 -m http.server 8080 --directory output/
   ```

2. **Run the export script:**
   ```bash
   python3 <skill-dir>/scripts/export-pdf.py --url <server-url> --output output/presentation.pdf --width 1440 --height 810
   ```

3. **The script handles all CDP complexity:**
   - Temporary `--user-data-dir` (works even with Chrome already open)
   - `--remote-allow-origins=*` (required since Chrome 113+)
   - `@page { size: WxH }` injection via `Runtime.evaluate`
   - Font loading wait before capture
   - Retry loop with 30-second timeout
   - Automatic cleanup of temp directories

4. **Chrome runs headed, not headless.** The user sees exactly what's being exported. Transparency builds trust. Headless mode hides rendering issues that only surface in the final PDF.

5. **Verify the PDF output.** Page count must match slide count. Images must render correctly. No blank pages, no clipped content, no missing fonts. If verification fails, diagnose and re-export — do not deliver a broken PDF.

## Guidelines

- **Quality at every phase.** Each phase produces a deliverable that must stand on its own. The extraction script should be clean and documented. The JSON should be human-readable. The HTML should be beautiful. The PDF should be pixel-perfect. Meticulous craftsmanship — not "good enough."

- **Self-contained HTML.** Every presentation must work standalone. Inline CSS or local files in `output/css/`. Only Google Fonts as external dependency. No CDN libraries, no remote images, no API calls.

- **Dark themes for technical/data presentations.** Default to dark backgrounds (#0a0a0a to #1a1a1a) for engineering reports, technical data, analytics dashboards. Light themes for business, educational, or client-facing corporate decks. Ask if ambiguous.

- **Pre-process image assets.** Extract images from source files (PPTX, XLSX) early in Phase 0. Store in `output/img/` as actual files. Never rely on CSS `filter: brightness()`, `filter: grayscale()`, or any CSS filter for print — Chrome's print engine ignores them silently. If you need a processed version of an image, create it with Python (Pillow) during extraction.

- **Fixed JSON schema.** The JSON structure is a contract between generator and renderer. Once defined in Phase 2, it never changes. Filters change content, not structure. This prevents the renderer from breaking when different filter combinations exclude data.

- **Validation before rendering.** The validation dataset in Phase 1 exists to catch data mismatches — wrong date ranges, missing cross-references, inconsistent totals — before they reach slides. Present discrepancies to the user explicitly. They must confirm the data is correct.

- **Avoid these anti-patterns:**
  - Generic fonts (Arial, Inter, Roboto) — use distinctive typography (DM Sans, JetBrains Mono, Space Grotesk, etc.)
  - CSS filters for print output — they fail silently in Chrome print mode
  - Hardcoded absolute paths in scripts — use relative paths from project root
  - Changing JSON structure per filter — filters change content, structure stays fixed
  - Skipping the validation gate — wrong data in slides is worse than no slides
  - `white-space: normal` on badges/tags — use `nowrap` to prevent line breaks in small elements
  - Headless Chrome for export — use headed mode so the user sees what's happening
  - Over-engineering slide types — start with 5–7 core types, add only if data demands it
  - Generating HTML without understanding the data first — Phase 1 must complete before Phase 3
  - Embedding base64 images in HTML — use file references in `output/img/` for maintainability
