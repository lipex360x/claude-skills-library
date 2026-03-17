# create-diagram

Create professional diagrams using an HTML-first design workflow with Excalidraw export.

## Trigger phrases

- `/create-diagram system architecture for my app`
- "draw a flowchart of the login process"
- "make a diagram of this" (with a reference image)
- Also activates when the user asks for any visual representation, diagram, chart, or schematic — even without explicitly saying "diagram"

## How it works

1. **HTML Design** — Generates a high-quality, self-contained HTML file using production-grade aesthetics (bold typography, atmospheric colors, intentional layout). This is where the design happens — Claude excels at HTML/CSS.
2. **User Screenshot** — The user opens the HTML in a browser and sends back a screenshot, giving Claude a visual reference of the rendered result.
3. **Excalidraw Export** — Converts the visual structure into a portable `.excalidraw` JSON file, preserving the information architecture (nodes, connections, labels, grouping) in an editable format.

When a reference image is provided, the skill analyzes it first and recreates it as HTML with improved aesthetics before converting to Excalidraw.

## Usage

```
/create-diagram [description or reference image]
```

Example: `/create-diagram microservices architecture with API gateway, auth service, and three backend services connected to a shared database`

## Directory structure

```
create-diagram/
├── SKILL.md              # Core instructions — HTML-first workflow + Excalidraw export
├── README.md             # This file
└── references/
    └── excalidraw-format.md  # Complete Excalidraw JSON specification
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-diagram
```
