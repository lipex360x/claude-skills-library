# JSON Contract Reference

The fixed schema contract is the architectural backbone of the create-webview pipeline. This document defines the rules that govern how `data/generate.py` produces `output/data.json`.

## The Fixed Schema Principle

Once the JSON schema is defined in Phase 2, it never changes. Every key, every section, every array — always present in the output. Filters change content, not structure.

### Why this matters

The HTML renderer (`output/js/renderer.js`) is built against a specific JSON shape. If a filter removes a section entirely, the renderer crashes with `Cannot read property 'length' of undefined`. The fixed schema prevents this by guaranteeing every section exists.

### Bad example (structure changes with filters)

```json
// Without --cutoff flag:
{
  "summary": { "total": 100 },
  "projects": [...],
  "timeline": [...]
}

// With --cutoff=2024-01-01 (timeline removed!):
{
  "summary": { "total": 45 },
  "projects": [...]
  // timeline is GONE — renderer breaks
}
```

### Good example (structure fixed, content changes)

```json
// Without --cutoff flag:
{
  "summary": { "total": 100 },
  "projects": [...],
  "timeline": [...]
}

// With --cutoff=2024-01-01 (timeline empty but present):
{
  "summary": { "total": 45 },
  "projects": [...],
  "timeline": []  // empty array, renderer handles gracefully
}
```

## Section Types and Null Handling

### Always-present sections

These sections exist in every generated JSON, regardless of filters:

| Section type | Empty value | Example |
|-------------|-------------|---------|
| Meta object | Always populated | `"meta": { "title": "...", "generated": "..." }` |
| Summary object | Always populated | `"summary": { "total": 0, "categories": {} }` |
| Arrays | Empty array `[]` | `"projects": []` |
| Optional objects | `null` | `"highlights": null` |
| Strings | Empty string `""` | `"notes": ""` |
| Numbers | `0` | `"count": 0` |

### Meta section (always first)

```json
{
  "meta": {
    "title": "Presentation Title",
    "subtitle": "Optional subtitle",
    "date": "2024-01-15",
    "generated_at": "2024-01-15T10:30:00",
    "filter_params": {
      "cutoff": "2024-01-01"
    },
    "brand": {
      "primary_color": "#2563eb",
      "logo": "img/logo.png",
      "company": "Company Name"
    }
  }
}
```

### Summary section (always second)

```json
{
  "summary": {
    "total_items": 120,
    "total_value": 5400000,
    "by_category": {
      "Infrastructure": { "count": 45, "value": 1250000 },
      "Software": { "count": 30, "value": 890000 }
    },
    "by_status": {
      "active": 80,
      "completed": 35,
      "on_hold": 5
    },
    "highlights": [
      { "label": "Largest project", "value": "Project Alpha", "detail": "$450,000" }
    ]
  }
}
```

### Data arrays (variable content)

```json
{
  "projects": [
    {
      "id": "PROJ-001",
      "name": "Project Alpha",
      "category": "Infrastructure",
      "status": "active",
      "value": 450000,
      "start_date": "2023-06-01",
      "end_date": "2024-12-31",
      "progress": 0.65,
      "details": {
        "team_size": 5,
        "location": "Site A",
        "notes": "On track"
      }
    }
  ]
}
```

## Filter Parameter Pattern

Filters are command-line arguments to `generate.py`:

```bash
python3 data/generate.py --cutoff 2024-01-01 --category Infrastructure
```

### Implementation rules

1. **Default = all data.** Running without flags produces the complete dataset
2. **Filters are additive.** `--cutoff` AND `--category` both apply (AND logic)
3. **Record filter params in meta.** The JSON meta section must include which filters were applied
4. **Empty results are valid.** A filter that matches nothing produces empty arrays, not errors
5. **Never skip sections.** Even if a filter eliminates all items from a category, the category key exists with count 0 in summary

### Example generate.py pattern

```python
import argparse
import json
import sqlite3

def generate(db_path, cutoff=None, category=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Build query with optional filters
    where = []
    params = []
    if cutoff:
        where.append("start_date >= ?")
        params.append(cutoff)
    if category:
        where.append("category = ?")
        params.append(category)

    where_clause = " AND ".join(where) if where else "1=1"

    projects = conn.execute(
        f"SELECT * FROM projects WHERE {where_clause} ORDER BY name",
        params
    ).fetchall()

    # Build fixed-schema output
    data = {
        "meta": {
            "title": "...",
            "generated_at": "...",
            "filter_params": {"cutoff": cutoff, "category": category}
        },
        "summary": build_summary(projects),  # always present
        "projects": [dict(row) for row in projects],  # may be empty []
        "timeline": build_timeline(projects),  # may be empty []
        "highlights": build_highlights(projects) if projects else None  # null when N/A
    }

    return data
```

## Schema Documentation

Document the schema in a comment block at the top of `generate.py`:

```python
"""
JSON Schema Contract
====================
{
  "meta": { ... },          // ALWAYS present, always populated
  "summary": { ... },       // ALWAYS present, always populated
  "projects": [ ... ],      // ALWAYS present, [] when filtered empty
  "timeline": [ ... ],      // ALWAYS present, [] when filtered empty
  "categories": [ ... ],    // ALWAYS present, [] when no categories
  "highlights": { ... },    // ALWAYS present, null when N/A
}

Structure NEVER changes. Filters change content, not keys.
"""
```
