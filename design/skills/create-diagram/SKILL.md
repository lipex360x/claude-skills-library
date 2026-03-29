---
name: create-diagram
description: >-
  Create professional diagrams using a spec-driven workflow with HTML preview
  and Excalidraw export. Use when creating visual diagrams, drawings, figures,
  schematics, charts, system architecture diagrams, network diagrams, flowcharts,
  UML, ER diagrams, sequence diagrams, state machines, org charts, mind maps,
  cloud infrastructure diagrams, research workflows, or any visual representation.
  Also use when the user sends a reference image to replicate as a diagram, says
  "create a diagram", "draw this", "make a flowchart", "diagram this architecture",
  or wants any kind of visual diagram — even if they don't explicitly say "diagram."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Agent
  - AskUserQuestion
argument-hint: "[diagram-description-or-reference-image]"
---

# Create Diagram

Generate professional diagrams through a spec-driven workflow: define the structure in a JSON spec, preview as HTML, then convert to editable Excalidraw — ensuring visual fidelity across formats.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `diagram-description` | $ARGUMENTS or conversation | yes | Non-empty text or reference image | AUQ: "Describe the diagram you want or send a reference image." |
| `route` | Inferred from input | no | `create`, `replicate`, or `excalidraw-only` | Default to `create` for text, `replicate` for images |

**Route detection:**

| Route | Trigger | Flow |
|-------|---------|------|
| `create` | Text description of a diagram | Spec → HTML → User validates → Excalidraw |
| `replicate` | User sends a reference image | Analyze image → Spec → HTML → User validates → Excalidraw |
| `excalidraw-only` | User explicitly asks for Excalidraw without HTML | Spec → Excalidraw directly |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Diagram spec | `diagram/<name>-spec.json` | yes | JSON per `templates/diagram-spec.md` |
| HTML preview | `diagram/<name>.html` | yes | Self-contained HTML |
| Excalidraw file | `diagram/<name>.excalidraw` | yes | Excalidraw JSON |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Spec template | `templates/diagram-spec.md` | R | Markdown |
| Excalidraw format ref | `references/excalidraw-format.md` | R | Markdown |
| Output directory | `diagram/` | W | Created if missing |

</external_state>

## Pre-flight

<pre_flight>

1. Input is present → if empty: AUQ for diagram description — stop.
2. `diagram/` directory exists → if not: create it.
3. Read `templates/diagram-spec.md` for the spec format.

</pre_flight>

## Steps

### 1. Design consultation

Parse `$ARGUMENTS` for the diagram description. Identify the diagram type (flowchart, architecture, mind map, ER, sequence, etc.) and key elements.

For ambiguous requests, ask with `AskUserQuestion`:
- Diagram type (if unclear)
- Visual tone: dark/moody, light/clean, colorful/vibrant, minimal/monochrome
- Layout preference: horizontal, vertical, radial, grid

Skip consultation when the request is specific enough to proceed directly. Simple requests (under 12 nodes, clear type) go straight to spec generation.

**Replicate route:** Analyze the reference image first — extract structure, nodes, labels, connections, layout direction, grouping, colors, hierarchy, annotation styles, and visual accents (border-lefts, backgrounds, icons).

### 2. Generate spec

Write `diagram/<name>-spec.json` with every element explicitly defined:
- Groups with background colors and labels
- Nodes with titles, icons, items, bullet styles
- Annotations with background, border-left accent color, positioning
- Connections with direction and style
- Panels (checklists, legends) if applicable
- Typography and color palette

Every visual detail must be in the spec. If it's not in the spec, it won't be in the Excalidraw. The spec is the contract — no guessing allowed.

### 3. Generate HTML preview

Generate a single self-contained HTML file (`diagram/<name>.html`) from the spec. Every element in the spec must appear in the HTML. Design principles:

- **Typography**: use the fonts defined in the spec's `typography` section. Never Arial, Inter, or Roboto. Prefer JetBrains Mono for labels, DM Sans for descriptions.
- **Color**: use the spec's `palette`. CSS variables for consistency.
- **Layout**: CSS Grid or Flexbox. Generous spacing between nodes.
- **Atmosphere**: gradients, subtle glows, shadows. Not flat — not overdone.
- **Connections**: SVG arrows with proper arrowheads.
- **Animation**: subtle fade-in on load. Hover effects for interactivity.
- **Annotations**: render with background, border-left accent, and italic text exactly as specified.

Open the HTML in the browser:

```bash
open <path-to-html-file>
```

Tell the user: "Me manda um screenshot do resultado. Se estiver aprovado, gero o Excalidraw. Se tiver ajustes, me fala."

### 4. Validation loop

If the user requests changes:
1. Update the spec JSON first (the spec is the source of truth)
2. Regenerate the HTML from the updated spec
3. Re-open in browser
4. Repeat until approved

If the user approves (sends screenshot without change requests, or says it's good): proceed to Step 5.

### 5. Fidelity briefing

Before generating Excalidraw, set expectations:

> **O que transfere bem:** estrutura, cores, texto, agrupamento, anotações com borda de destaque.
> **O que degrada:** espaçamento preciso (CSS layout → coordenadas manuais), sombras, gradientes, efeitos de hover, setas curvas customizadas.
>
> Posso gerar o Excalidraw (com essas limitações) ou manter o HTML como entregável final. O que prefere?

Use `AskUserQuestion` with options `["Gerar Excalidraw", "Manter só o HTML"]`. If the user chooses HTML-only, skip to Step 8 (Report).

This briefing exists because HTML uses CSS Grid/Flexbox which auto-resolves layout, while Excalidraw needs manual coordinates. A beautiful HTML followed by a broken Excalidraw feels like a bait-and-switch — the briefing turns a negative surprise into an informed decision.

Update the spec's `layout` section to match the approved HTML before launching the agent.

### 6. Generate Excalidraw

Read `references/excalidraw-format.md` for the complete JSON specification.

Launch a background agent to generate the Excalidraw file from the spec. The agent receives:
- Path to the spec JSON (the source of truth)
- Path to the excalidraw format reference
- Path to the approved HTML (for visual cross-reference)
- Key Excalidraw mapping rules:
  - Group backgrounds → large rounded rectangles with solid fill
  - Node cards → white rectangles with bound text
  - Node icons → prepend emoji to the title line
  - Annotations → THREE grouped elements: bg rectangle + thin accent rectangle (left border) + text
  - Connections → arrows with proper startBinding/endBinding
  - Checklist panels → rectangle container + checkbox rectangles + text elements

**Critical:** Annotations must NOT be standalone text. They must have a visible background rectangle and a colored left-border accent rectangle, grouped together.

**Excalidraw-only route:** Generate the Excalidraw directly from the spec (no HTML, no agent — do it inline).

### 7. Post-generation validation

After the agent completes, validate the output before presenting to the user. Read the `.excalidraw` JSON and check:

1. **Bounding-box overlap.** For elements in the same row, verify `x + width + 20` of one element doesn't exceed `x` of the next. If elements overlap, adjust x positions using the spec's layout grid.
2. **Text fits container.** For bound text elements, verify `fontSize × 1.35 × lineCount ≤ containerHeight - 20`. If text overflows, increase the container height.
3. **Arrow sanity.** For arrows with `startBinding`/`endBinding`, verify the referenced element IDs exist. Remove bindings that reference non-existent elements.

If any check fails, fix the coordinates inline. Only present the file after validation passes — a broken layout on first open destroys trust in the workflow.

### 8. Report

<report>

Present concisely:
- **Diagram:** name, type, element count
- **Artifacts:** list files created (spec, HTML, Excalidraw) with paths
- **Route:** which route was followed (create/replicate/excalidraw-only)
- **Audit results:** content audit + self-audit summary (or "all checks passed")
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Open the `.excalidraw` file in Excalidraw (https://excalidraw.com or VS Code extension) to make manual adjustments if needed.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — input was validated, output directory exists
2. **Spec is source of truth?** — all visual details are in the spec, not just in HTML
3. **HTML matches spec?** — every spec element appears in the HTML
4. **Excalidraw matches spec?** — structural elements faithfully reproduced (if generated)
5. **Validation passed?** — no bounding-box overlaps, text fits containers, arrow bindings valid
6. **Approval gates honored?** — user approved HTML before Excalidraw generation, fidelity briefing presented

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Spec completeness?** — every node, connection, annotation, and group from the user's description is captured in the spec JSON
2. **Visual accuracy?** — HTML renders the spec faithfully (colors, layout, typography match spec declarations)
3. **Excalidraw fidelity?** — structural elements (groups, annotations with bg+accent, icons) are present in the Excalidraw output
4. **No phantom elements?** — no elements appear in the output that aren't in the spec or user's description
5. **Label accuracy?** — all text labels, node titles, and annotation text match the user's original description exactly (no paraphrasing)

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Reference image unreadable | AUQ: "Could not analyze the image. Please send a clearer version or describe the diagram." → stop |
| HTML fails to render | Check for syntax errors, fix inline, re-open → retry once |
| Excalidraw agent fails | Report error, offer to retry or keep HTML as final deliverable |
| Spec template not found | Report path and suggest running from skills-library root → stop |
| Bounding-box validation fails | Fix coordinates inline using spec layout grid |

## Anti-patterns

- **HTML without a spec.** Generating HTML directly from the description — because without the spec as source of truth, the Excalidraw conversion has no contract to follow and visual fidelity breaks.
- **Annotations as standalone text.** In Excalidraw, annotations need bg rect + accent rect + text, grouped — because standalone text loses the visual accent that distinguishes annotations from labels.
- **Generic fonts.** Using Arial, Inter, or Roboto in the HTML phase — because they produce generic-looking output that undermines the professional quality goal.
- **Sending HTML source to the agent.** Send the spec path instead — because the HTML is too large for agent context and the spec contains all the information needed.
- **Skipping the validation loop.** Always wait for user approval before Excalidraw generation — because regenerating Excalidraw is expensive and the user should validate the structure first.
- **Modifying HTML without updating the spec.** The spec is the single source of truth — because HTML-only changes create drift that makes Excalidraw conversion inaccurate.
- **Random IDs in Excalidraw.** Use descriptive names from the spec — because meaningful IDs make debugging and manual editing possible.

## Guidelines

- **The spec is the contract.** If a visual detail isn't in the spec, it won't survive the HTML → Excalidraw conversion. Every annotation background, every icon, every border accent must be explicitly declared.

- **Self-contained HTML.** Every HTML file must work standalone — inline CSS, no external dependencies except Google Fonts CDN.

- **Always open after generating.** After writing the HTML file, always run `open <path>` to open it in the user's default browser.

- **Dark themes for technical diagrams.** Unless the user specifies otherwise, default to dark backgrounds for architecture, system, and technical diagrams. Use light themes for business flows, org charts, and documentation diagrams.

- **Excalidraw fidelity through the spec.** The Excalidraw version won't have gradients, shadows, or hover effects — those are HTML-only features. But structural elements (annotation backgrounds, border accents, icons, grouping) must be faithfully reproduced because the spec explicitly defines how to map them.

- **No Draw.io.** This skill does not use Draw.io, MCP servers, or XML formats. The only outputs are spec JSON, HTML, and Excalidraw JSON files.

- **Supported diagram types:** flowcharts, architecture diagrams, mind maps, ER diagrams, sequence diagrams, state machines, class diagrams, network topologies, data flow diagrams, org charts, swimlane/business flows, cloud infrastructure, research workflows, Kanban boards, timelines, and any custom visual representation.
