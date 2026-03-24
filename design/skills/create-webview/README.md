# create-webview

> Create beautiful data-driven HTML presentations from structured data sources.

Full data-to-slides pipeline: ingests any source (Excel, PowerPoint, CSV, JSON, SQLite, images), normalizes into SQLite, generates fixed-schema JSON, renders dynamic HTML slides with branded CSS custom properties, and exports to PDF via Chrome CDP in headed mode. The fixed JSON schema contract ensures renderer stability across filter variations. Includes a mandatory data validation gate before rendering, Python dependency auto-installer, and 3 starter templates (HTML shell, CSS brand system, JS renderer core).

## Usage

```text
/create-webview [data-sources-or-description]
```

> [!TIP]
> Also activates when you say "create a presentation", "make slides from this data", "build a webview", "data to slides", "generate a report", or want to turn spreadsheets or databases into visual presentations — even without explicitly saying "webview."

### Examples

```text
/create-webview sales-report.xlsx              # extract data from Excel and build slides
/create-webview                                # interactive: asks for data sources, topic, brand identity
/create-webview quarterly-review.pptx logo.png # multiple sources with brand logo
```

## How it works

1. **Discovery and setup** — Detect source files, gather brand identity (primary color, font, logo) and slide dimensions (default: 1440x810 / 16:9), create project structure with `data/` and `output/` directories. Pre-process image assets with Python Pillow
2. **Data extraction** — Parse sources into SQLite with a tailored schema, generate a document-centric validation dataset (`validation.json`), and gate on user approval before proceeding. Wrong data in slides is worse than no slides
3. **JSON generation** — Query SQLite to produce `output/data.json` with fixed-schema contract. All sections always present; filters change content, not structure. Command-line arguments support custom filter parameters
4. **HTML rendering** — Build dynamic slide deck from templates: HTML shell, CSS custom properties for branding, JS function-array renderer pipeline. Start with 5-7 core slide types. Opens in browser with iterative "polish, don't add" refinement loop
5. **PDF export** — Chrome CDP export with headed browser (not headless), `@page` injection for proper dimensions, font loading workarounds, and page count verification against slide count
6. **Report** — Summary of pipeline phases, data validation results, slide count and types, PDF export status, and audit results

[↑ Back to top](#create-webview)

## Directory structure

```text
create-webview/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── data-extraction.md     # Source type handling, SQLite patterns, validation format
│   ├── html-renderer.md       # Slide architecture, component patterns, CSS naming, typography
│   ├── json-contract.md       # Fixed schema rules, null handling, filter parameters
│   ├── known-pitfalls.md      # Cross-phase gotchas with tested solutions
│   └── pdf-export.md          # CDP setup, Chrome flags, font and image workarounds
├── scripts/
│   ├── check-deps.py          # Detect source types and auto-install required Python libs
│   └── export-pdf.py          # Generic CDP export with --url, --output, --width, --height
└── templates/
    ├── base-styles.css        # CSS with brand variables, slide base styles, typography scale
    ├── renderer-base.js       # JS core: el(), slide(), header(), fetch+render pipeline
    └── shell.html             # Minimal HTML shell with head, #slides container, and script tag
```

[↑ Back to top](#create-webview)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-webview
```
