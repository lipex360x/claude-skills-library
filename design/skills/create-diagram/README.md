# create-diagram

> Create professional diagrams using a spec-driven workflow with HTML preview and Excalidraw export.

Three-stage pipeline (JSON spec, HTML preview, Excalidraw export) that keeps the spec as the single source of truth across formats. Supports 3 routes: `create` from text descriptions, `replicate` from reference images, and `excalidraw-only` for direct generation. The HTML stage uses CSS Grid, SVG arrows, and distinctive typography (JetBrains Mono, DM Sans) with a user approval gate before the more expensive Excalidraw conversion. Post-generation validation catches bounding-box overlaps, text overflow, and broken arrow bindings automatically.

## Usage

```text
/create-diagram [diagram-description-or-reference-image]
```

> [!TIP]
> Also activates when you say "create a diagram", "draw this", "make a flowchart", "diagram this architecture", or want any kind of visual representation — even without explicitly saying "diagram."

### Examples

```text
/create-diagram microservices architecture with API gateway   # create from text description
/create-diagram                                               # interactive: asks for description, type, visual tone
```

## How it works

1. **Design consultation** — Identify diagram type, visual tone (dark/moody, light/clean, colorful, minimal), and layout preference from the description or reference image. Simple requests skip consultation
2. **Generate spec** — Write a detailed JSON spec capturing every visual element: groups, nodes, annotations, connections, palette, and typography
3. **Generate HTML preview** — Render a self-contained HTML file from the spec with CSS Grid layout, SVG arrows, Google Fonts, and subtle animations. Opens in browser automatically
4. **Validation loop** — User reviews the HTML preview and requests changes; spec is updated first, then HTML regenerated. Repeats until approved
5. **Fidelity briefing** — Set expectations on what transfers well to Excalidraw (structure, colors, text, grouping) vs. what degrades (precise spacing, gradients, hover effects). User can choose HTML-only
6. **Generate Excalidraw** — Background agent converts the approved spec to `.excalidraw` with proper element mapping (annotations get bg rect + accent rect + text, grouped)
7. **Post-generation validation** — Check for bounding-box overlaps, text overflow, and arrow binding integrity. Fixes coordinates inline before presenting
8. **Report** — Summary of diagram type, artifacts created, route followed, and audit results

[↑ Back to top](#create-diagram)

## Directory structure

```text
create-diagram/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── excalidraw-format.md   # Complete Excalidraw JSON specification for element mapping
└── templates/
    └── diagram-spec.md        # Diagram spec JSON format with element type definitions
```

[↑ Back to top](#create-diagram)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-diagram
```
