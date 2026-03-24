---
name: create-excalidraw
description: >-
  Generate Excalidraw diagrams from natural language descriptions. Use when asked
  to "create a diagram", "make a flowchart", "visualize a process", "draw a system
  architecture", "create a mind map", "generate an Excalidraw file", "draw this",
  "diagram this", or wants any kind of visual diagram — even if they don't
  explicitly say "Excalidraw." Supports flowcharts, relationship diagrams, mind
  maps, architecture, data flow, swimlane, class, sequence, and ER diagrams.
  Outputs .excalidraw JSON files.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
argument-hint: "<diagram description>"
---

# Create Excalidraw

Generate visually polished Excalidraw diagrams from natural language descriptions. Every diagram should look intentionally designed — not like default AI output.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `diagram-description` | $ARGUMENTS or conversation | yes | Non-empty text describing the diagram | AUQ: "What diagram do you want to create?" |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Excalidraw file | `<descriptive-name>.excalidraw` | yes | Excalidraw JSON v2 |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Design aesthetics ref | `references/design-aesthetics.md` | R | Markdown |
| Element types ref | `references/element-types.md` | R | Markdown |
| Excalidraw schema ref | `references/excalidraw-schema.md` | R | Markdown |
| Icon libraries ref | `references/icon-libraries.md` | R | Markdown |
| Diagram templates | `templates/*.excalidraw` | R | Excalidraw JSON |
| Icon scripts | `scripts/*.py` | R/X | Python |

</external_state>

## Pre-flight

<pre_flight>

1. Input is present → if `$ARGUMENTS` is empty or too vague: AUQ to clarify — stop.
2. Read `references/design-aesthetics.md` for color palettes, spatial composition principles, and anti-patterns to avoid.
3. Choose a palette and layout strategy that fits the diagram's purpose and audience.

</pre_flight>

## Steps

### 1. Understand the request

Analyze the user's description to determine:
1. **Diagram type** — match against the type table below
2. **Key elements** — entities, steps, concepts
3. **Relationships** — flow, connections, hierarchy
4. **Complexity** — element count drives layout decisions

| Type | Keywords | Template |
|------|----------|----------|
| Flowchart | "workflow", "process", "steps" | `templates/flowchart-template.excalidraw` |
| Relationship | "connections", "dependencies" | `templates/relationship-template.excalidraw` |
| Mind Map | "mind map", "concepts", "ideas" | `templates/mindmap-template.excalidraw` |
| Architecture | "architecture", "system", "components" | — |
| Data Flow (DFD) | "data flow", "data processing" | `templates/data-flow-diagram-template.excalidraw` |
| Swimlane | "business process", "actors" | `templates/business-flow-swimlane-template.excalidraw` |
| Class Diagram | "class", "inheritance", "OOP" | `templates/class-diagram-template.excalidraw` |
| Sequence | "sequence", "interaction", "messages" | `templates/sequence-diagram-template.excalidraw` |
| ER Diagram | "database", "entity", "data model" | `templates/er-diagram-template.excalidraw` |

### 2. Extract structured information

Read `references/element-types.md` for detailed extraction guides per diagram type. Key points:

- **Flowcharts**: Sequential steps, decision points, start/end
- **Relationships**: Entities (name + description), connections (from → to + label)
- **Mind Maps**: Central topic, 3-6 main branches, optional sub-topics
- **DFD**: Sources, processes, data stores, flows (left-to-right)
- **Swimlane**: Actors as header columns, process boxes in lanes, cross-lane handoffs
- **Class**: Classes with attributes/methods, visibility markers (+/-/#), relationship types
- **Sequence**: Objects at top, lifelines down, messages between lifelines, activation boxes
- **ER**: Entities with attributes, PK/FK markers, cardinality (1:1, 1:N, N:M), junction entities

### 3. Generate the Excalidraw JSON

Use the elements from the matched template (if available) or build from scratch.

**Available elements:** `rectangle` (boxes), `ellipse` (emphasis), `diamond` (decisions), `arrow` (connections), `text` (labels/annotations).

**Required properties:**
- **Position**: `x`, `y` coordinates
- **Size**: `width`, `height`
- **Style**: `strokeColor`, `backgroundColor`, `fillStyle` — use palette from pre-flight
- **Font**: `fontFamily: 1` (Virgil, hand-drawn) for most text. Use `2` (Helvetica) for clean labels, `3` (Cascadia) for code
- **Connections**: `points` array for arrows

**File structure:**
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

Set `viewBackgroundColor` to match your chosen palette (dark palettes need dark backgrounds).

### 4. Apply layout

Read `references/design-aesthetics.md` for spatial composition. Key rules:

- **Spacing**: horizontal gap 200-300px, vertical gap 100-150px, minimum 60px between any two elements
- **Visual hierarchy**: important nodes 20-30% larger; title 28-32px, node labels 18-22px, edge labels 14-16px, annotations 12-14px
- **Grid layout** (relationship diagrams): `columns = ceil(sqrt(entityCount))`
- **Radial layout** (mind maps): distribute branches evenly around center

**Element count limits:**

| Type | Recommended | Maximum |
|------|-------------|---------|
| Flowchart steps | 3-10 | 15 |
| Relationship entities | 3-8 | 12 |
| Mind map branches | 4-6 | 8 |
| Sub-topics per branch | 2-4 | 6 |

If the request exceeds limits, suggest splitting into multiple diagrams (high-level overview + detailed sub-diagrams).

### 5. Add icons (if applicable)

For architecture diagrams with professional icons (AWS/GCP/Azure), read `references/icon-libraries.md` for the Python script workflow. The scripts add icons without consuming context tokens.

If no libraries are set up, use basic shapes with color coding — functional and clear, just less polished.

### 6. Validate

Before delivering, verify:
- All elements have unique IDs
- No overlapping coordinates
- Text uses consistent `fontFamily`
- Colors follow a consistent palette from `references/design-aesthetics.md`
- Arrows connect logically
- Valid JSON structure
- Element count under 20 for clarity

If any check fails, fix the issue before proceeding. For overlapping coordinates, recalculate positions using spacing rules. For palette drift, replace off-palette colors with the nearest palette match.

### 7. Deliver and refine

Save as `<descriptive-name>.excalidraw`. Ask: "Want any adjustments — layout, colors, labels, or additional elements?"

If the user requests changes, apply them and re-run validation (Step 6) before re-delivering.

### 8. Report

<report>

Present concisely:
- **Created:** `<filename>.excalidraw`
- **Type:** diagram type
- **Elements:** element breakdown (e.g., "7 rectangles, 6 arrows, 1 title — 14 total")
- **Palette:** which palette was used
- **Audit results:** content audit + self-audit summary (or "all checks passed")
- **Errors:** issues encountered and how they were handled (or "none")
- **To view:** visit https://excalidraw.com and drag-and-drop the file, or use the Excalidraw VS Code extension.

</report>

## Next action

Open the `.excalidraw` file in Excalidraw (https://excalidraw.com or VS Code extension) to review and make manual adjustments.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — palette chosen, design aesthetics loaded
2. **Steps completed?** — diagram type identified, elements extracted, JSON generated, layout applied, validation passed
3. **Output exists?** — `.excalidraw` file written and contains valid JSON
4. **Anti-patterns clean?** — no default blue-on-white, no overlapping elements, no generic fonts
5. **Element count reasonable?** — under 20 elements for clarity, or split suggested

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **All elements present?** — every entity, step, or concept from the user's description appears in the diagram
2. **Relationships accurate?** — connections match the described flows, hierarchies, or dependencies
3. **Labels exact?** — all text labels match the user's original description (no paraphrasing or abbreviating)
4. **Layout readable?** — no overlapping elements, text is legible, arrows don't cross unnecessarily
5. **Visual quality?** — palette is intentional (not default), spacing is generous, hierarchy is clear

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Description too vague | AUQ with specific questions about diagram type and elements → retry |
| Template not found | Build from scratch using basic elements — functional, just less templated |
| Icon library not set up | Fall back to basic shapes with color coding |
| Element count exceeds limit | Suggest splitting into overview + detail diagrams → AUQ for user preference |
| JSON validation fails | Re-parse, fix syntax errors, re-validate |
| Overlapping coordinates | Recalculate positions using spacing rules from Step 4 |

## Anti-patterns

- **Default light-blue-on-white.** Using Excalidraw's default colors with a perfect grid — because that's the hallmark of generic AI diagrams and undermines the professional quality goal.
- **Exceeding element limits silently.** Generating diagrams with 20+ elements without suggesting a split — because cluttered diagrams are unreadable and defeat the purpose of visualization.
- **Skipping palette selection.** Jumping straight to generation without choosing a palette from `references/design-aesthetics.md` — because intentional color choices are what separate designed diagrams from generated ones.
- **Overlapping elements.** Not validating coordinates before delivery — because overlapping elements make the diagram unusable and destroy trust in the output.
- **Ignoring the refinement loop.** Not asking for adjustments after delivery — because first-pass diagrams rarely match the user's mental model perfectly, and one round of feedback dramatically improves quality.

## Guidelines

- **Design-first approach.** Always choose a palette and layout strategy before generating any elements — because visual decisions made upfront produce coherent output, while decisions made during generation produce inconsistent results.

- **Virgil for sketches, Helvetica for clean.** Use `fontFamily: 1` (Virgil) for the hand-drawn Excalidraw aesthetic, `2` (Helvetica) for clean professional labels, `3` (Cascadia) for code — because font choice signals intent and mixing fonts without purpose looks accidental.

- **Dark themes for technical diagrams.** Default to dark backgrounds for architecture, system, and technical diagrams. Use light themes for business flows, org charts, and documentation — because the audience and context determine the appropriate visual tone.

- **Split over clutter.** When a diagram exceeds element limits, always suggest splitting into a high-level overview plus detailed sub-diagrams — because a readable overview is more useful than a comprehensive but unreadable single diagram.

- **Supported diagram types:** flowcharts, relationship diagrams, mind maps, architecture, data flow (DFD), swimlane/business flows, class diagrams, sequence diagrams, ER diagrams, network topologies, state machines, org charts, cloud infrastructure, and any custom visual representation.
