---
name: create-excalidraw
description: 'Generate Excalidraw diagrams from natural language descriptions. Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", "generate an Excalidraw file", "draw this", "diagram this", or wants any kind of visual diagram — even if they don''t explicitly say "Excalidraw." Supports flowcharts, relationship diagrams, mind maps, architecture, data flow, swimlane, class, sequence, and ER diagrams. Outputs .excalidraw JSON files.'
user-invocable: true
argument-hint: '<diagram description>'
---

# Create Excalidraw

Generate visually polished Excalidraw diagrams from natural language descriptions. Every diagram should look intentionally designed — not like default AI output.

## 1. Design-First Approach

Before generating any diagram, read `references/design-aesthetics.md` for color palettes, spatial composition principles, and anti-patterns to avoid. Choose a palette and layout strategy that fits the diagram's purpose and audience.

Never default to light-blue-on-white with a perfect grid — that's the hallmark of generic AI diagrams.

## 2. Understand the Request

If `$ARGUMENTS` is provided, use it as the diagram description. If empty or too vague to determine diagram type and elements, use `AskUserQuestion` to clarify what diagram the user wants.

Analyze the user's description to determine:
1. **Diagram type** — match against the table below
2. **Key elements** — entities, steps, concepts
3. **Relationships** — flow, connections, hierarchy
4. **Complexity** — element count drives layout decisions

### Diagram Type Selection

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

## 3. Extract Structured Information

Read `references/element-types.md` for detailed extraction guides per diagram type. Key points:

- **Flowcharts**: Sequential steps, decision points, start/end
- **Relationships**: Entities (name + description), connections (from → to + label)
- **Mind Maps**: Central topic, 3-6 main branches, optional sub-topics
- **DFD**: Sources, processes, data stores, flows (left-to-right). Represent data flow, not process order
- **Swimlane**: Actors as header columns, process boxes in lanes, cross-lane handoffs
- **Class**: Classes with attributes/methods, visibility markers (+/-/#), relationship types (inheritance, composition, aggregation)
- **Sequence**: Objects at top, lifelines down, messages between lifelines, activation boxes
- **ER**: Entities with attributes, PK/FK markers, cardinality (1:1, 1:N, N:M), junction entities

## 4. Generate the Excalidraw JSON

### Available Elements

| Element | Use |
|---------|-----|
| `rectangle` | Boxes for entities, steps, concepts |
| `ellipse` | Emphasis, alternative shapes |
| `diamond` | Decision points |
| `arrow` | Directional connections |
| `text` | Labels and annotations |

### Required Properties

- **Position**: `x`, `y` coordinates
- **Size**: `width`, `height`
- **Style**: `strokeColor`, `backgroundColor`, `fillStyle` — use palette from step 1
- **Font**: `fontFamily: 1` (Virgil, hand-drawn) for most text. Use `2` (Helvetica) for clean labels, `3` (Cascadia) for code — Virgil keeps the sketch aesthetic that makes Excalidraw distinctive
- **Connections**: `points` array for arrows

### File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

Set `viewBackgroundColor` to match your chosen palette (dark palettes need dark backgrounds).

## 5. Layout Guidelines

### Spacing

- Horizontal gap: 200-300px between elements
- Vertical gap: 100-150px between rows
- Minimum 60px between any two elements; 100px for unrelated elements

### Visual Hierarchy

- Important/central nodes: 20-30% larger than peripheral ones
- Title: 28-32px font size
- Node labels: 18-22px
- Edge labels: 14-16px, lighter color
- Annotations: 12-14px, muted color

### Layout Algorithms

**Grid** (relationship diagrams):
```javascript
const columns = Math.ceil(Math.sqrt(entityCount));
const x = startX + (index % columns) * horizontalGap;
const y = startY + Math.floor(index / columns) * verticalGap;
```

**Radial** (mind maps):
```javascript
const angle = (2 * Math.PI * index) / branchCount;
const x = centerX + radius * Math.cos(angle);
const y = centerY + radius * Math.sin(angle);
```

### Element Count Limits

| Diagram Type | Recommended | Maximum |
|--------------|-------------|---------|
| Flowchart steps | 3-10 | 15 |
| Relationship entities | 3-8 | 12 |
| Mind map branches | 4-6 | 8 |
| Sub-topics per branch | 2-4 | 6 |

If the request exceeds limits, suggest splitting into multiple diagrams (high-level overview + detailed sub-diagrams).

## 6. Icon Libraries

For architecture diagrams with professional icons (AWS/GCP/Azure), read `references/icon-libraries.md` for the Python script workflow. The scripts add icons without consuming context tokens.

If no libraries are set up, use basic shapes with color coding — functional and clear, just less polished.

## 7. Validate

Before delivering, verify:
- All elements have unique IDs (use `Date.now().toString(36) + Math.random().toString(36).substr(2)`)
- No overlapping coordinates
- Text uses consistent `fontFamily` (1 for hand-drawn, 2 for clean, 3 for code)
- Colors follow a consistent palette from `references/design-aesthetics.md`
- Arrows connect logically
- Valid JSON structure
- Element count under 20 for clarity

If any check fails, fix the issue before proceeding. For overlapping coordinates, recalculate positions using the spacing rules from step 5. For invalid JSON, re-parse and correct syntax errors. For palette drift, replace off-palette colors with the nearest palette match.

## 8. Save, Deliver, and Refine

1. Save as `<descriptive-name>.excalidraw`
2. Provide a summary:

```
Created: user-workflow.excalidraw
Type: Flowchart
Elements: 7 rectangles, 6 arrows, 1 title
Total: 14 elements

To view: visit https://excalidraw.com and drag-and-drop the file,
or use the Excalidraw VS Code extension.
```

3. Ask: "Want any adjustments — layout, colors, labels, or additional elements?"
4. If the user requests changes, apply them and re-run the validation checklist (step 7) before re-delivering

## References

- `references/design-aesthetics.md` — Color palettes, spatial composition, anti-patterns
- `references/icon-libraries.md` — Icon library setup and Python script workflow
- `references/excalidraw-schema.md` — Complete Excalidraw JSON schema
- `references/element-types.md` — Detailed element type specifications and extraction guides
- `scripts/split-excalidraw-library.py` — Split `.excalidrawlib` into individual icons
- `scripts/add-icon-to-diagram.py` — Add icons to diagrams programmatically
- `scripts/add-arrow.py` — Add arrows between elements
