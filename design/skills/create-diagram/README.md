# create-diagram

> Create professional diagrams using a spec-driven workflow with HTML preview and Excalidraw export.

Generates diagrams through a three-stage pipeline: define the structure in a JSON spec, preview as production-grade HTML, then convert to editable Excalidraw — ensuring visual fidelity across formats. Supports creating from text descriptions, replicating from reference images, or generating Excalidraw directly.

## Usage

```text
/create-diagram [diagram-description-or-reference-image]
```

> [!TIP]
> Also activates when you say "create a diagram", "draw this", "make a flowchart", "diagram this architecture", or want any kind of visual representation — even without explicitly saying "diagram."

## How it works

1. **Design consultation** — Identify diagram type, visual tone, and layout preference from the description or reference image
2. **Generate spec** — Write a detailed JSON spec capturing every visual element: groups, nodes, annotations, connections, and palette
3. **Generate HTML preview** — Render a self-contained HTML file from the spec with CSS Grid layout, SVG arrows, and subtle animations
4. **Validation loop** — User reviews the HTML preview and requests changes; spec is updated first, then HTML regenerated
5. **Fidelity briefing** — Set expectations on what transfers well to Excalidraw vs. what degrades (gradients, precise spacing)
6. **Generate Excalidraw** — Background agent converts the approved spec to `.excalidraw` with proper element mapping
7. **Post-generation validation** — Check for bounding-box overlaps, text overflow, and arrow binding integrity
8. **Report** — Summary of diagram type, artifacts created, route followed, and audit results

## Directory structure

```text
create-diagram/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── excalidraw-format.md   # Complete Excalidraw JSON specification
└── templates/
    └── diagram-spec.md        # Diagram spec JSON format documentation
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-diagram
```
