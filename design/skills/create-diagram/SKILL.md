---
name: create-diagram
description: "Create professional diagrams using a spec-driven workflow with HTML preview and Excalidraw export. Use when creating visual diagrams, drawings, figures, schematics, charts, system architecture diagrams, network diagrams, flowcharts, UML, ER diagrams, sequence diagrams, state machines, org charts, mind maps, cloud infrastructure diagrams, research workflows, or any visual representation. Also use when the user sends a reference image to replicate as a diagram, says 'create a diagram', 'draw this', 'make a flowchart', 'diagram this architecture', or wants any kind of visual diagram — even if they don't explicitly say 'diagram.'"
metadata:
  category: visual-design
  tags:
    - diagram
    - excalidraw
    - architecture
    - flowchart
    - visual
argument-hint: "[diagram-description-or-reference-image]"
user-invocable: true
---

# Create Diagram

Generate professional diagrams through a three-phase spec-driven workflow: define the structure in a JSON spec, preview as HTML, then convert to editable Excalidraw. The spec is the single source of truth — both HTML and Excalidraw are derived from it, ensuring visual fidelity across formats.

## Task Routing

| Route | Trigger | Flow |
|-------|---------|------|
| `create` | Text description of a diagram | Spec → HTML → User validates → Excalidraw |
| `replicate` | User sends a reference image | Analyze image → Spec → HTML → User validates → Excalidraw |
| `excalidraw-only` | User explicitly asks for Excalidraw without HTML | Spec → Excalidraw directly |

## Phase 1: Diagram Spec

The spec captures every visual detail needed to reproduce the diagram in any format. Read `templates/diagram-spec.md` for the complete format.

### Create route

1. **Understand the diagram.** Parse `$ARGUMENTS` for the diagram description. Identify the diagram type (flowchart, architecture, mind map, ER, sequence, etc.) and the key elements.

2. **Design consultation (if needed).** For ambiguous requests, ask with `AskUserQuestion`:
   - Diagram type (if unclear)
   - Visual tone: dark/moody, light/clean, colorful/vibrant, minimal/monochrome
   - Layout preference: horizontal, vertical, radial, grid

   Skip consultation when the request is specific enough to proceed directly. Simple requests (under 12 nodes, clear type) go straight to spec generation.

3. **Generate the spec.** Write `diagram/<name>-spec.json` with every element explicitly defined:
   - Groups with background colors and labels
   - Nodes with titles, icons, items, bullet styles
   - Annotations with background, border-left accent color, positioning
   - Connections with direction and style
   - Panels (checklists, legends) if applicable
   - Typography and color palette

   Every visual detail must be in the spec. If it's not in the spec, it won't be in the Excalidraw. The spec is the contract — no guessing allowed.

### Replicate route

1. **Analyze the reference image.** Extract the structure: nodes, labels, connections, layout direction, grouping, colors, hierarchy, annotation styles, and any visual accents (border-lefts, backgrounds, icons).

2. **Generate the spec.** Capture the reference image's visual language in the spec, improving aesthetics while preserving the information architecture.

3. **Continue to Phase 2.**

## Phase 2: HTML Preview

The HTML is the visual validation artifact. Generate it from the spec — every element in the spec must appear in the HTML.

1. **Generate the HTML.** Write a single self-contained HTML file (`diagram/<name>.html`) with embedded CSS and no external dependencies (except Google Fonts). Design principles:

   - **Typography**: use the fonts defined in the spec's `typography` section. Never Arial, Inter, or Roboto. Prefer JetBrains Mono for labels, DM Sans for descriptions.
   - **Color**: use the spec's `palette`. CSS variables for consistency.
   - **Layout**: CSS Grid or Flexbox. Generous spacing between nodes.
   - **Atmosphere**: gradients, subtle glows, shadows. Not flat — not overdone.
   - **Connections**: SVG arrows with proper arrowheads.
   - **Animation**: subtle fade-in on load. Hover effects for interactivity.
   - **Annotations**: render with background, border-left accent, and italic text exactly as specified.

2. **Open the HTML in the browser.**

   ```bash
   open <path-to-html-file>
   ```

3. **Ask for validation.** Tell the user: "Me manda um screenshot do resultado. Se estiver aprovado, gero o Excalidraw. Se tiver ajustes, me fala."

4. **Validation loop.** If the user requests changes:
   - Update the spec JSON first (the spec is the source of truth)
   - Regenerate the HTML from the updated spec
   - Re-open in browser
   - Repeat until approved

   If the user approves (sends screenshot without change requests, or says it's good): proceed to Phase 3.

## Phase 2.5: Fidelity Briefing

Before generating Excalidraw, set expectations. Tell the user:

> **O que transfere bem:** estrutura, cores, texto, agrupamento, anotações com borda de destaque.
> **O que degrada:** espaçamento preciso (CSS layout → coordenadas manuais), sombras, gradientes, efeitos de hover, setas curvas customizadas.
>
> Posso gerar o Excalidraw (com essas limitações) ou manter o HTML como entregável final. O que prefere?

Use `AskUserQuestion` with options `["Gerar Excalidraw", "Manter só o HTML"]`. If the user chooses HTML-only, skip Phase 3 and end.

This briefing exists because the HTML uses CSS Grid/Flexbox which auto-resolves layout, while Excalidraw needs manual coordinates. A beautiful HTML followed by a broken Excalidraw feels like a bait-and-switch — the briefing turns a negative surprise into an informed decision.

### Update layout coordinates

Before launching the Excalidraw agent, update the spec's `layout` section to match the approved HTML. Refine grid column widths, row heights, gaps, and slot assignments so the agent has precise positioning data. The layout section format is defined in `templates/diagram-spec.md`.

## Phase 3: Excalidraw Export

Once the HTML is approved and the fidelity briefing is acknowledged, launch a background agent to generate the Excalidraw file from the spec.

Read `references/excalidraw-format.md` for the complete JSON specification.

### Agent prompt structure

The agent receives a lean prompt with:
- Path to the spec JSON (the source of truth)
- Path to the excalidraw format reference
- Path to the approved HTML (for visual cross-reference)
- Key Excalidraw mapping rules (from the spec template's "Excalidraw mapping rules" table)

```
Agent prompt template:

Generate an Excalidraw file from the diagram spec.

1. Read the spec: `diagram/<name>-spec.json`
2. Read the format reference: `<skill-dir>/references/excalidraw-format.md`
3. Read the HTML for visual reference: `diagram/<name>.html`

Conversion rules:
- Group backgrounds → large rounded rectangles with solid fill
- Node cards → white rectangles with bound text (title + bullet items as \n-separated lines)
- Node icons → prepend emoji to the title line
- Annotations → THREE grouped elements: bg rectangle + thin accent rectangle (left border) + text
- Connections → arrows with proper startBinding/endBinding
- Checklist panels → rectangle container + checkbox rectangles + text elements

Critical: Annotations must NOT be standalone text. They must have a visible background rectangle and a colored left-border accent rectangle, grouped together. This is the most common fidelity loss.

Write to: `diagram/<name>.excalidraw`
```

Launch the agent with `run_in_background: true` so the conversation continues while the Excalidraw is generated.

### Post-generation validation

After the agent completes, validate the output before presenting to the user. Read the `.excalidraw` JSON and check:

1. **Bounding-box overlap.** For elements in the same row, verify `x + width + 20` of one element doesn't exceed `x` of the next. If elements overlap, adjust x positions using the spec's layout grid.

2. **Text fits container.** For bound text elements, verify `fontSize × 1.35 × lineCount ≤ containerHeight - 20`. If text overflows, increase the container height.

3. **Arrow sanity.** For arrows with `startBinding`/`endBinding`, verify the referenced element IDs exist. Remove bindings that reference non-existent elements.

If any check fails, fix the coordinates inline — the spec's layout section provides the intended positions. After fixes, write the corrected file.

Only tell the user the file is ready after validation passes. This prevents the user from seeing broken layout on first open, which destroys trust in the workflow.

### Excalidraw-only route

When the user explicitly asks for Excalidraw without HTML:

1. Generate the spec JSON (same as Phase 1)
2. Generate the Excalidraw directly from the spec (no HTML, no agent — do it inline)
3. Present the result

## Guidelines

- **The spec is the contract.** If a visual detail isn't in the spec, it won't survive the HTML → Excalidraw conversion. Every annotation background, every icon, every border accent must be explicitly declared. This is the single most important principle of this skill.

- **Self-contained HTML.** Every HTML file must work standalone — inline CSS, no external dependencies except Google Fonts CDN.

- **Always open after generating.** After writing the HTML file, always run `open <path>` to open it in the user's default browser.

- **Dark themes for technical diagrams.** Unless the user specifies otherwise, default to dark backgrounds for architecture, system, and technical diagrams. Use light themes for business flows, org charts, and documentation diagrams.

- **Excalidraw fidelity through the spec.** The Excalidraw version won't have gradients, shadows, or hover effects — those are HTML-only features. But structural elements (annotation backgrounds, border accents, icons, grouping) must be faithfully reproduced because the spec explicitly defines how to map them.

- **No Draw.io.** This skill does not use Draw.io, MCP servers, or XML formats. The only outputs are spec JSON, HTML, and Excalidraw JSON files.

- **Supported diagram types:** flowcharts, architecture diagrams, mind maps, ER diagrams, sequence diagrams, state machines, class diagrams, network topologies, data flow diagrams, org charts, swimlane/business flows, cloud infrastructure, research workflows, Kanban boards, timelines, and any custom visual representation.

- **Avoid these anti-patterns:**
  - Generating HTML without a spec first (the spec must always exist)
  - Annotations as standalone text in Excalidraw (they need bg rect + accent rect + text, grouped)
  - Generic fonts (Arial, Inter, Roboto) in the HTML phase
  - Sending the entire HTML source in the agent prompt (send the spec path instead)
  - Missing icon emojis in Excalidraw card titles
  - Random/UUID-style IDs in Excalidraw — use descriptive names from the spec
  - Skipping the validation loop — always wait for user approval before Excalidraw
  - Modifying the HTML without updating the spec first
