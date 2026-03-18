# create-webview

Create beautiful data-driven HTML presentations from structured data sources — full pipeline from extraction to PDF.

## Trigger phrases

- `/create-webview <data-sources-or-description>` — start a new presentation
- "create a presentation", "make slides from this data", "generate a report"
- "data to slides", "build a webview", "turn this spreadsheet into slides"
- Also activates when the user wants to turn spreadsheets, databases, or structured data into visual presentations — even without explicitly saying "webview"

## How it works

1. **Discovery & Setup** — detect source files, install dependencies, create project structure
2. **Data Extraction** — parse sources (Excel, PowerPoint, CSV, JSON, images) into SQLite, generate validation dataset
3. **JSON Generation** — query SQLite → produce fixed-schema JSON (structure never changes, only content)
4. **HTML Renderer** — build dynamic slide deck with function-array pipeline, CSS custom properties for branding
5. **PDF Export** — Chrome CDP export with all workarounds (temp user-data-dir, @page injection, font loading)

Key design decisions: validation gate after extraction (user must approve data), fixed JSON schema contract (prevents renderer breakage), pre-processed images (CSS filters fail in Chrome print), headed Chrome for export (user sees what's happening).

## Usage

```
/create-webview data from report.xlsx and images from presentation.pptx
/create-webview create a quarterly report from the sales database
/create-webview build slides from the CSV files in data/
```

## Directory structure

```
create-webview/
├── SKILL.md                      # Core instructions — 4-phase pipeline
├── README.md                     # This file
├── references/
│   ├── data-extraction.md        # Source type handling, SQLite patterns, validation format
│   ├── json-contract.md          # Fixed schema rules, null handling, filter params
│   ├── html-renderer.md          # Slide architecture, CSS patterns, JS renderer
│   ├── pdf-export.md             # CDP setup, Chrome flags, all workarounds
│   └── known-pitfalls.md         # Cross-phase gotchas with solutions
├── templates/
│   ├── shell.html                # Minimal HTML shell (head + #slides + script)
│   ├── base-styles.css           # CSS with brand variables, slide base, typography
│   └── renderer-base.js          # JS core: el(), slide(), header(), fetch+render loop
└── scripts/
    ├── check-deps.py             # Detect source types → install required Python libs
    └── export-pdf.py             # Generic CDP export (--url, --output, --width, --height)
```

## Output

Each presentation generates a self-contained project:

- `data/extract.py` — source-to-SQLite extraction
- `data/generate.py` — SQLite-to-JSON with fixed schema
- `data/validation.json` — cross-reference dataset for data verification
- `output/index.html` — presentation shell
- `output/css/styles.css` — branded stylesheet
- `output/js/renderer.js` — dynamic slide renderer
- `output/data.json` — presentation data
- `output/presentation.pdf` — exported PDF (optional)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-webview
```
