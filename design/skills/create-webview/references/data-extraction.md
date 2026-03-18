# Data Extraction Reference

Detailed guide for Phase 1 — extracting data from source files into SQLite.

## Source Type Handling

### Excel (.xlsx, .xls)

Use `openpyxl` for .xlsx files. Key patterns:

- **Read worksheets by name**, not index — sheet order is unreliable
- **Skip header rows** intelligently: detect where data starts by checking for empty rows or known header patterns
- **Handle merged cells**: `openpyxl` reads the value only from the top-left cell of a merge range. Check `cell.value` for `None` in merged regions
- **Date cells**: Excel stores dates as serial numbers. Use `cell.is_date` or check `cell.number_format` to detect date columns. Convert to ISO format (YYYY-MM-DD) immediately
- **Numeric precision**: Float values from Excel may have floating-point artifacts (e.g., 3.0000000001). Round to appropriate precision based on the data domain

```python
from openpyxl import load_workbook

wb = load_workbook('source.xlsx', data_only=True)  # data_only=True reads computed values
ws = wb['Sheet1']

for row in ws.iter_rows(min_row=2, values_only=True):  # skip header
    # row is a tuple of cell values
    pass
```

### PowerPoint (.pptx)

Use `python-pptx`. PowerPoint files contain both text and images:

- **Text extraction**: iterate `slide.shapes` → check `shape.has_text_frame` → read `shape.text_frame.paragraphs`
- **Table extraction**: check `shape.has_table` → read `shape.table.rows` and `shape.table.cell(row, col).text`
- **Image extraction**: check `shape.shape_type == MSO_SHAPE_TYPE.PICTURE` → `shape.image.blob` gives raw bytes. Save to `output/img/` immediately
- **Slide notes**: `slide.notes_slide.notes_text_frame.text` — often contains metadata or commentary
- **Layout detection**: `slide.slide_layout.name` tells you the intended slide type

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = Presentation('source.pptx')
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_table:
            table = shape.table
            for row in table.rows:
                cells = [cell.text for cell in row.cells]
        elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            img_bytes = shape.image.blob
            ext = shape.image.content_type.split('/')[-1]
            # Save to output/img/
```

### CSV (.csv)

Use Python's built-in `csv` module. Key considerations:

- **Encoding**: try UTF-8 first, fall back to `latin-1` or `cp1252` for Brazilian Portuguese content
- **Delimiter detection**: use `csv.Sniffer().sniff(sample)` to auto-detect delimiter
- **Large files**: use `csv.reader` with streaming, don't load all into memory

### JSON (.json)

Direct loading with `json.load()`. Validate structure before importing:

- Check for expected top-level keys
- Handle nested objects by flattening for SQLite or using JSON columns

### Images (.png, .jpg, .webp)

Use `Pillow` for processing:

- **Copy to output/img/** preserving original quality
- **Generate dark variants** if needed: use `ImageEnhance.Brightness(img).enhance(0.7)` — NOT CSS filters
- **Optimize for web**: resize if over 2000px wide, convert to WebP if appropriate
- **Extract metadata**: EXIF data may contain dates, GPS, camera info

```python
from PIL import Image, ImageEnhance

img = Image.open('photo.jpg')
# Create darkened version for dark theme backgrounds
dark = ImageEnhance.Brightness(img).enhance(0.6)
dark.save('output/img/photo-dark.jpg', quality=85)
```

## Dependency Map

| Extension | Package | Import | Purpose |
|-----------|---------|--------|---------|
| .xlsx, .xls | openpyxl | openpyxl | Excel spreadsheet reading |
| .pptx, .ppt | python-pptx | pptx | PowerPoint reading + image extraction |
| .png, .jpg, .webp | Pillow | PIL | Image processing and dark variants |
| .csv | (built-in) | csv | CSV parsing |
| .json | (built-in) | json | JSON loading |
| .sqlite, .db | (built-in) | sqlite3 | Database operations |
| (PDF export) | websocket-client | websocket | Chrome CDP communication |

## SQLite Schema Design

Principles for presentation-oriented schemas:

1. **One table per entity type.** If the presentation shows projects, create a `projects` table. If it shows people, create a `people` table. The schema mirrors the presentation structure.

2. **Denormalize for query simplicity.** Joins are cheap in SQLite, but complex joins make the JSON generation script harder to maintain. Store the project name directly in the task table rather than forcing a join.

3. **Use TEXT for dates.** Store as ISO format (YYYY-MM-DD). SQLite date functions work on text columns.

4. **Add computed columns.** If the presentation needs "days since start", compute it during extraction and store it. Don't recompute during JSON generation.

5. **Create indexes for filter columns.** If the presentation supports `--cutoff` by date, index the date column.

```sql
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    value REAL,
    source_file TEXT  -- track which file this came from
);

CREATE INDEX IF NOT EXISTS idx_projects_category ON projects(category);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
```

## Validation Dataset Format

The validation dataset (`data/validation.json`) is a cross-reference tool that catches data mismatches before they reach slides. Structure:

```json
{
  "_meta": {
    "generated_at": "2024-01-15T10:30:00",
    "source_files": ["data.xlsx", "images.pptx"],
    "filter_params": {"cutoff": "2024-01-01"},
    "total_records": 150,
    "filtered_records": 120
  },
  "primary_items": [
    {
      "id": "PROJ-001",
      "name": "Project Alpha",
      "category": "Infrastructure",
      "cross_refs": {
        "tasks": 12,
        "team_members": 5,
        "images": ["alpha-site.jpg"]
      }
    }
  ],
  "excluded_items": [
    {
      "id": "PROJ-099",
      "name": "Project Omega",
      "reason": "end_date before cutoff (2023-06-15 < 2024-01-01)"
    }
  ],
  "invalidated_items": [
    {
      "id": "PROJ-050",
      "name": "Project Delta",
      "reason": "Referenced 3 team members but team table has 0 records for this project"
    }
  ],
  "reference_index": {
    "Infrastructure": ["PROJ-001", "PROJ-005", "PROJ-012"],
    "Software": ["PROJ-002", "PROJ-008"]
  },
  "summary_stats": {
    "by_category": {
      "Infrastructure": {"count": 45, "total_value": 1250000},
      "Software": {"count": 30, "total_value": 890000}
    },
    "by_status": {
      "active": 80,
      "completed": 35,
      "on_hold": 5
    }
  }
}
```

### Why validation matters

The original use case caught a critical mismatch: one data source showed 331 items while another showed 488 items for the same category. Without the validation dataset, this discrepancy would have produced incorrect totals on a client presentation — destroying credibility. The validation gate in Phase 1 exists because of this exact scenario.
