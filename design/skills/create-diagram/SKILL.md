---
name: create-diagram
description: "Create professional diagrams using an HTML-first design workflow with Excalidraw export. Use when creating visual diagrams, drawings, figures, schematics, charts, system architecture diagrams, network diagrams, flowcharts, UML, ER diagrams, sequence diagrams, state machines, org charts, mind maps, cloud infrastructure diagrams, research workflows, or any visual representation. Also use when the user sends a reference image to replicate as a diagram, says 'create a diagram', 'draw this', 'make a flowchart', 'diagram this architecture', or wants any kind of visual diagram — even if they don't explicitly say 'diagram.'"
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

Generate professional diagrams through a two-phase workflow: first build a high-quality HTML visualization, then convert to portable Excalidraw format. The HTML phase is where the design happens — Claude excels at producing visually striking HTML. The Excalidraw phase makes it editable and portable.

## Task Routing

| Route | Trigger | Flow |
|-------|---------|------|
| `create` | Text description of a diagram | Design HTML → User screenshots → Generate Excalidraw |
| `replicate` | User sends a reference image | Analyze image → Recreate as HTML → User screenshots → Generate Excalidraw |
| `excalidraw-only` | User explicitly asks for Excalidraw without HTML | Generate Excalidraw JSON directly (skip HTML phase) |

## Phase 1: HTML Diagram

The HTML output is the design artifact — a self-contained `.html` file that looks production-grade. Apply the same design thinking as `/frontend-design`: bold aesthetic choices, intentional typography, atmospheric details.

### Create route

1. **Understand the diagram.** Parse `$ARGUMENTS` for the diagram description. Identify the diagram type (flowchart, architecture, mind map, ER, sequence, etc.) and the key elements.

2. **Design consultation (if needed).** For ambiguous requests, ask with `AskUserQuestion`:
   - Diagram type (if unclear)
   - Visual tone: dark/moody, light/clean, colorful/vibrant, minimal/monochrome
   - Layout preference: horizontal, vertical, radial, grid

   Skip consultation when the request is specific enough to proceed directly. Simple requests (under 12 nodes, clear type) go straight to generation.

3. **Generate the HTML diagram.** Write a single self-contained HTML file with embedded CSS and no external dependencies (except Google Fonts). Apply these design principles:

   - **Typography**: distinctive font choices — never Arial, Inter, or Roboto. Use Google Fonts (JetBrains Mono for labels, DM Sans or similar for descriptions). Pair a display font with a body font.
   - **Color**: commit to a cohesive palette. Use CSS variables. Dominant color with sharp accents. Dark backgrounds work exceptionally well for technical diagrams.
   - **Layout**: CSS Grid or Flexbox for positioning. Generous spacing between nodes. Asymmetry and intentional whitespace over rigid grids.
   - **Atmosphere**: gradients, subtle glows, border effects, shadows. Not flat and lifeless — not overdone either.
   - **Connections**: SVG lines or CSS borders for arrows and connectors. Use proper arrowheads via SVG markers.
   - **Animation**: subtle fade-in animations on load. Hover effects on nodes for interactivity.

   Write the file to the project directory (e.g., `diagram/<name>.html`).

4. **Ask the user to screenshot.** Tell the user: "Open the HTML file in your browser and send me a screenshot of the result."

5. **Wait for the screenshot.** The user sends back a screenshot of the rendered HTML. This becomes the visual reference for the Excalidraw conversion.

### Replicate route

1. **Analyze the reference image.** Extract the structure: nodes, labels, connections, layout direction, grouping, colors, and hierarchy.

2. **Recreate as HTML.** Build an HTML diagram that faithfully reproduces the reference image's structure and intent, but with elevated design quality. Don't copy ugly diagrams pixel-for-pixel — improve the aesthetics while preserving the information architecture.

3. **Follow steps 4-5 from the create route.** Ask for screenshot, wait for it.

## Phase 2: Excalidraw Export

After receiving the screenshot of the rendered HTML, generate the Excalidraw JSON file.

Read `references/excalidraw-format.md` for the complete JSON specification, element types, and styling conventions.

### Conversion process

1. **Map the visual structure.** From the screenshot and the HTML source (which you wrote), identify every element: rectangles, text labels, arrows, groups, colors.

2. **Build the Excalidraw JSON.** For each visual element:
   - Create the appropriate Excalidraw element (rectangle, ellipse, diamond, text, arrow)
   - Match position and sizing from the HTML layout
   - Apply colors from the HTML CSS variables
   - Connect arrows using proper `startBinding`/`endBinding`
   - Group related elements with `groupIds`

3. **Apply layout rules:**
   - 200-300px horizontal spacing between elements
   - 100-150px vertical spacing between rows
   - Font size 16-24px for readability
   - All text elements use `fontFamily: 5` (Excalifont)
   - Unique IDs for every element (use descriptive IDs, not random strings)
   - Elements must not overlap

4. **Write the `.excalidraw` file** next to the HTML file (e.g., `diagram/<name>.excalidraw`).

5. **Present the result.** Tell the user:
   - File location for both HTML and Excalidraw versions
   - How to open (Excalidraw.com, VS Code extension, or Obsidian)
   - Element count and diagram type summary

### Excalidraw-only route

When the user explicitly asks for Excalidraw without HTML (or the diagram is simple enough that HTML is overkill):

1. Generate the Excalidraw JSON directly from the text description.
2. Follow the same layout rules and element conventions.
3. Skip the HTML phase entirely — but still produce a high-quality result with proper spacing, colors, and typography.

## Guidelines

- **HTML is the design tool, Excalidraw is the deliverable.** The HTML phase exists because Claude produces far better visual designs in HTML/CSS than in raw JSON coordinates. The screenshot bridges the gap — it gives you a visual reference to translate into Excalidraw elements with correct positioning.

- **Self-contained HTML.** Every HTML file must work standalone — inline CSS, no external dependencies except Google Fonts CDN. The user should be able to open it in any browser.

- **Dark themes for technical diagrams.** Unless the user specifies otherwise, default to dark backgrounds for architecture, system, and technical diagrams. They look more professional and are easier on the eyes. Use light themes for business flows, org charts, and documentation diagrams.

- **Excalidraw fidelity.** The Excalidraw version won't be pixel-perfect against the HTML — Excalidraw has a hand-drawn aesthetic. Focus on preserving the information architecture (nodes, connections, labels, grouping) rather than visual effects (gradients, shadows, glows). Those are HTML-only features.

- **No Draw.io.** This skill does not use Draw.io, MCP servers, or XML formats. The only outputs are HTML files and Excalidraw JSON files.

- **Supported diagram types:** flowcharts, architecture diagrams, mind maps, ER diagrams, sequence diagrams, state machines, class diagrams, network topologies, data flow diagrams, org charts, swimlane/business flows, cloud infrastructure, research workflows, Kanban boards, timelines, and any custom visual representation.

- **Avoid these anti-patterns:**
  - Generic fonts (Arial, Inter, Roboto, system fonts) in the HTML phase
  - White/plain backgrounds for technical diagrams — add atmosphere
  - Overlapping elements in the Excalidraw output
  - Missing connections (every arrow must have start and end bindings)
  - Text smaller than 16px in Excalidraw (unreadable when zoomed out)
  - Random/UUID-style IDs in Excalidraw — use descriptive names (e.g., `"api_gateway"`, `"db_primary"`)
