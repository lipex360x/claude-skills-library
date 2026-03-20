# Icon Libraries

For specialized diagrams (AWS/GCP/Azure architecture), use pre-made icon libraries from Excalidraw for professional, standardized icons.

## Setup

1. Visit https://libraries.excalidraw.com/
2. Download the `.excalidrawlib` file (e.g., "AWS Architecture Icons")
3. Create directory: `libraries/<icon-set-name>/`
4. Place the file and run the splitter:

```bash
python scripts/split-excalidraw-library.py libraries/<icon-set-name>/
```

Expected output structure:
```
libraries/<icon-set-name>/
  <name>.excalidrawlib     # Original
  reference.md             # Generated icon lookup table
  icons/                   # Individual icon JSON files
    EC2.json
    S3.json
    Lambda.json
    ...
```

## Using Icons (Recommended: Python Scripts)

The Python scripts handle icon integration without consuming context tokens:

### Add icons

```bash
python scripts/add-icon-to-diagram.py <diagram> <icon-name> <x> <y> [--label "Text"] [--library-path PATH]
```

Edit via `.excalidraw.edit` is enabled by default; pass `--no-use-edit-suffix` to disable.

### Add arrows

```bash
python scripts/add-arrow.py <diagram> <from-x> <from-y> <to-x> <to-y> [--label "Text"] [--style solid|dashed|dotted] [--color HEX]
```

### Example workflow

```bash
# 1. Create base .excalidraw with title and structure
# 2. Add icons
python scripts/add-icon-to-diagram.py diagram.excalidraw "Internet-gateway" 150 100 --label "Internet Gateway"
python scripts/add-icon-to-diagram.py diagram.excalidraw VPC 200 200
python scripts/add-icon-to-diagram.py diagram.excalidraw ELB 350 250 --label "Load Balancer"
python scripts/add-icon-to-diagram.py diagram.excalidraw EC2 500 300 --label "Web Server"
python scripts/add-icon-to-diagram.py diagram.excalidraw RDS 650 350 --label "Database"

# 3. Connect with arrows
python scripts/add-arrow.py diagram.excalidraw 200 150 250 200
python scripts/add-arrow.py diagram.excalidraw 265 230 350 250
python scripts/add-arrow.py diagram.excalidraw 415 280 500 300
python scripts/add-arrow.py diagram.excalidraw 565 330 650 350 --label "SQL" --style dashed
```

Benefits:
- No token consumption — icon JSON (200-1000 lines each) never enters context
- Deterministic coordinate transforms and UUID generation
- Fast, reliable, reusable with any Excalidraw library

## Manual Integration (Fallback)

Only if Python scripts are unavailable:

1. Read `libraries/<name>/reference.md` for the icon index
2. Load only needed icon JSON files (200-1000 lines each — high token cost)
3. Extract elements array, calculate bounding box, apply coordinate offsets
4. Generate new unique IDs, update groupIds references
5. Merge transformed elements into your diagram

This approach consumes 2000-5000+ tokens per diagram and risks coordinate/ID errors.

## No Icons Available

If no libraries are set up:
- Use basic shapes (rectangles, ellipses, arrows) with color coding
- Inform user they can set up libraries later for professional icons
- The diagram remains functional — just less visually polished
