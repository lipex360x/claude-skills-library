# create-excalidraw

> Natural language to polished Excalidraw diagrams — with design-first aesthetics.

A Claude Code skill that generates `.excalidraw` JSON files from plain-text descriptions. Supports 9 diagram types with curated color palettes, layout algorithms, and optional icon library integration.

## Triggers

```
/create-excalidraw
```

Also activates automatically when you say things like:
- "create a diagram", "make a flowchart", "draw a system architecture"
- "visualize a process", "create a mind map", "diagram this"

## Supported Diagram Types

| Type | Template Included |
|------|:-:|
| Flowchart | Yes |
| Relationship Diagram | Yes |
| Mind Map | Yes |
| Architecture Diagram | — |
| Data Flow (DFD) | Yes |
| Swimlane (Business Flow) | Yes |
| Class Diagram | Yes |
| Sequence Diagram | Yes |
| ER Diagram | Yes |

## How It Works

1. **Design first** — Picks a color palette and layout strategy before generating anything
2. **Extract structure** — Parses entities, relationships, and flow from the description
3. **Generate JSON** — Produces a valid `.excalidraw` file with proper element IDs and coordinates
4. **Validate** — Checks for overlaps, consistent colors, readable text, and valid JSON

> [!TIP]
> Output files can be opened at [excalidraw.com](https://excalidraw.com) or with the Excalidraw VS Code extension.

## Icon Libraries (Optional)

For professional architecture diagrams (AWS, GCP, Azure), the skill supports pre-made icon libraries via Python scripts that add icons without consuming context tokens.

See `references/icon-libraries.md` for setup instructions.

## Structure

```
create-excalidraw/
├── SKILL.md                    # Core instructions (172 lines)
├── references/
│   ├── design-aesthetics.md    # Color palettes, spatial composition, anti-patterns
│   ├── icon-libraries.md       # Icon library setup and Python script workflow
│   ├── excalidraw-schema.md    # Complete Excalidraw JSON schema
│   └── element-types.md        # Element type specs and extraction guides
├── scripts/
│   ├── add-icon-to-diagram.py  # Add icons programmatically
│   ├── add-arrow.py            # Add arrows between elements
│   └── split-excalidraw-library.py  # Split .excalidrawlib into individual icons
└── templates/                  # 8 starter templates (.excalidraw)
```

## Install

**Global** (via skills-library):
```bash
# Already included in the design plugin
bash ~/.brain/scripts/setup.sh
```

**Local** (single project):
```bash
npx skills add lipex360/skills-library/design/skills/create-excalidraw --copy -a claude-code -y
```
