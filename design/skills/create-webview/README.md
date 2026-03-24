# create-webview

> Create beautiful data-driven HTML presentations from structured data sources.

Transforms data from any source (Excel, PowerPoint, CSV, JSON, SQLite, images) into polished HTML slide presentations with optional PDF export. Full pipeline: data extraction into SQLite, fixed-schema JSON generation, dynamic HTML rendering with branded CSS, and Chrome CDP export.

## Usage

```text
/create-webview [data-sources-or-description]
```

> [!TIP]
> Also activates when you say "create a presentation", "make slides from this data", "build a webview", "data to slides", "generate a report", or want to turn spreadsheets or databases into visual presentations — even without explicitly saying "webview."

## How it works

1. **Discovery and setup** — Detect source files, gather brand identity and slide dimensions, create project structure with data and output directories
2. **Data extraction** — Parse sources into SQLite, generate validation dataset, and gate on user approval before proceeding
3. **JSON generation** — Query SQLite to produce fixed-schema JSON with filter support; structure never changes, only content
4. **HTML rendering** — Build dynamic slide deck with function-array pipeline, CSS custom properties for branding, and iterative refinement loop
5. **PDF export** — Chrome CDP export with headed browser, temp user-data-dir, @page injection, and font loading workarounds
6. **Report** — Summary of pipeline phases, data validation results, slide count, and PDF export status

## Directory structure

```text
create-webview/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── data-extraction.md     # Source type handling, SQLite patterns, validation format
│   ├── html-renderer.md       # Slide architecture, CSS patterns, JS renderer
│   ├── json-contract.md       # Fixed schema rules, null handling, filter params
│   ├── known-pitfalls.md      # Cross-phase gotchas with solutions
│   └── pdf-export.md          # CDP setup, Chrome flags, all workarounds
├── scripts/
│   ├── check-deps.py          # Detect source types and install required Python libs
│   └── export-pdf.py          # Generic CDP export (--url, --output, --width, --height)
└── templates/
    ├── base-styles.css        # CSS with brand variables, slide base, typography
    ├── renderer-base.js       # JS core: el(), slide(), header(), fetch+render loop
    └── shell.html             # Minimal HTML shell (head + #slides + script)
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-webview
```
