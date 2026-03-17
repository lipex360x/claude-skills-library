# create-diagram

Create professional diagrams using a spec-driven workflow with HTML preview and Excalidraw export.

## Triggers

- `/create-diagram <description>` — create from text
- `/create-diagram` with a reference image — replicate
- "draw this", "make a flowchart", "diagram this architecture"
- Activates for any visual representation request — even without explicitly saying "diagram"

## How it works

1. **Spec** — generates a `diagram-spec.json` capturing every visual detail (nodes, connections, annotations with backgrounds, icons, colors)
2. **HTML Preview** — renders a production-grade HTML from the spec, opens in browser for validation
3. **Validation loop** — user approves or requests changes (spec is updated first, then HTML regenerated)
4. **Excalidraw Export** — background agent converts the approved spec to `.excalidraw` with high fidelity

The spec is the single source of truth. Both HTML and Excalidraw are derived from it, ensuring visual consistency across formats.

## Usage

```
/create-diagram system architecture for a payment management app
/create-diagram [attach reference image] replicate this flow diagram
```

## Directory structure

```
create-diagram/
├── SKILL.md                          # Skill instructions — spec-driven workflow
├── README.md                         # This file
├── references/
│   └── excalidraw-format.md          # Complete Excalidraw JSON specification
└── templates/
    └── diagram-spec.md               # Diagram spec JSON format documentation
```

## Output

Each diagram generates 3 files in the project's `diagram/` directory:

- `<name>-spec.json` — semantic structure (source of truth)
- `<name>.html` — visual preview (self-contained, no dependencies)
- `<name>.excalidraw` — editable portable format

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-diagram
```
