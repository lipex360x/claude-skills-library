# create-excalidraw

> Generate Excalidraw diagrams from natural language descriptions.

Produces polished `.excalidraw` JSON files from plain-text descriptions with design-first aesthetics. Supports 9 diagram types (flowcharts, mind maps, architecture, ER, sequence, class, swimlane, DFD, relationship) with curated color palettes, layout algorithms, and optional icon library integration.

## Usage

```text
/create-excalidraw <diagram description>
```

> [!TIP]
> Also activates when you say "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "draw this", "diagram this" — even without explicitly saying "Excalidraw."

## How it works

1. **Understand the request** — Determine diagram type, key elements, relationships, and complexity from the description
2. **Extract structured information** — Parse entities, attributes, connections, and flow using type-specific extraction guides
3. **Generate the Excalidraw JSON** — Build valid `.excalidraw` file with proper element IDs, coordinates, and styling
4. **Apply layout** — Position elements with consistent spacing, visual hierarchy, and grid/radial composition rules
5. **Add icons (if applicable)** — Integrate professional icons (AWS/GCP/Azure) via Python scripts without consuming context tokens
6. **Validate** — Check for overlapping coordinates, consistent colors, readable text, valid JSON, and element count limits
7. **Deliver and refine** — Save the file and iterate on user feedback with re-validation after each change
8. **Report** — Summary of diagram type, element count, file path, and audit results

## Directory structure

```text
create-excalidraw/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── design-aesthetics.md       # Color palettes, spatial composition, anti-patterns
│   ├── element-types.md           # Element type specs and extraction guides
│   ├── excalidraw-schema.md       # Complete Excalidraw JSON schema
│   └── icon-libraries.md          # Icon library setup and Python script workflow
├── scripts/
│   ├── add-arrow.py               # Add arrows between elements
│   ├── add-icon-to-diagram.py     # Add icons programmatically
│   ├── README.md                  # Scripts documentation
│   └── split-excalidraw-library.py  # Split .excalidrawlib into individual icons
└── templates/
    ├── business-flow-swimlane-template.excalidraw
    ├── class-diagram-template.excalidraw
    ├── data-flow-diagram-template.excalidraw
    ├── er-diagram-template.excalidraw
    ├── flowchart-template.excalidraw
    ├── mindmap-template.excalidraw
    ├── relationship-template.excalidraw
    └── sequence-diagram-template.excalidraw
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-excalidraw
```
