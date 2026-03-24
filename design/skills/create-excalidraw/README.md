# create-excalidraw

> Generate Excalidraw diagrams from natural language descriptions.

Produces polished `.excalidraw` JSON files from plain-text descriptions with design-first aesthetics. Supports 9 diagram types (flowcharts, mind maps, architecture, ER, sequence, class, swimlane, DFD, relationship) with curated color palettes, grid and radial layout algorithms, and optional icon library integration for AWS/GCP/Azure via Python scripts that run outside the context window. Includes 8 starter templates and a 6-step validation pass covering overlapping coordinates, color consistency, readable text, valid JSON, and element count limits.

## Usage

```text
/create-excalidraw <diagram description>
```

> [!TIP]
> Also activates when you say "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "draw this", "diagram this" — even without explicitly saying "Excalidraw."

### Examples

```text
/create-excalidraw user authentication flow with OAuth2      # flowchart with specific domain
/create-excalidraw mind map of our product strategy           # radial layout mind map
/create-excalidraw ER diagram for the e-commerce database     # entity-relationship with tables
```

## How it works

1. **Understand the request** — Determine diagram type, key elements, relationships, and complexity from the description
2. **Extract structured information** — Parse entities, attributes, connections, and flow using type-specific extraction guides from the element-types reference
3. **Generate the Excalidraw JSON** — Build valid `.excalidraw` file with proper element IDs, coordinates, and styling using the full schema spec
4. **Apply layout** — Position elements with consistent spacing, visual hierarchy, and grid/radial composition rules from the design-aesthetics reference
5. **Add icons (if applicable)** — Integrate professional icons (AWS/GCP/Azure) via Python scripts without consuming context tokens
6. **Validate** — Check for overlapping coordinates, consistent colors, readable text, valid JSON, and element count limits
7. **Deliver and refine** — Save the file and iterate on user feedback with re-validation after each change
8. **Report** — Summary of diagram type, element count, file path, and audit results

[↑ Back to top](#create-excalidraw)

## Directory structure

```text
create-excalidraw/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── design-aesthetics.md       # Color palettes, spatial composition rules, anti-patterns
│   ├── element-types.md           # Per-type element specs and structured extraction guides
│   ├── excalidraw-schema.md       # Complete Excalidraw JSON schema with field definitions
│   └── icon-libraries.md          # Icon library setup and Python script integration workflow
├── scripts/
│   ├── add-arrow.py               # Programmatically add arrows between existing elements
│   ├── add-icon-to-diagram.py     # Insert icons from .excalidrawlib into diagrams
│   ├── README.md                  # Scripts usage documentation and examples
│   └── split-excalidraw-library.py  # Split .excalidrawlib bundles into individual icon files
└── templates/
    ├── business-flow-swimlane-template.excalidraw  # Swimlane layout for business processes
    ├── class-diagram-template.excalidraw            # UML class diagram starter
    ├── data-flow-diagram-template.excalidraw        # DFD with processes, stores, and flows
    ├── er-diagram-template.excalidraw               # Entity-relationship with table notation
    ├── flowchart-template.excalidraw                # Standard flowchart with decision nodes
    ├── mindmap-template.excalidraw                  # Radial mind map layout
    ├── relationship-template.excalidraw             # Generic relationship/connection diagram
    └── sequence-diagram-template.excalidraw         # Sequence diagram with lifelines and messages
```

[↑ Back to top](#create-excalidraw)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-excalidraw
```
