# Diagram Spec JSON Format

The spec is the single source of truth for the diagram. Both HTML and Excalidraw are generated from it. Every visual detail must be explicitly declared — the Excalidraw agent cannot "guess" what you intended.

## Top-level structure

```json
{
  "meta": {
    "title": "Diagram Title",
    "subtitle": "Optional subtitle",
    "type": "flowchart",
    "layout": "vertical",
    "theme": "light",
    "backgroundColor": "#f0f4f0",
    "palette": {
      "text": "#263238",
      "textMuted": "#607d8b",
      "border": "#cfd8dc",
      "arrow": "#78909c",
      "surface": "#ffffff"
    }
  },
  "typography": {
    "title": { "family": "JetBrains Mono", "size": 28, "weight": 600 },
    "phaseLabel": { "family": "JetBrains Mono", "size": 13, "weight": 600, "transform": "uppercase", "letterSpacing": "1.5px" },
    "cardTitle": { "family": "JetBrains Mono", "size": 12, "weight": 600 },
    "cardBody": { "family": "DM Sans", "size": 11.5, "weight": 400 },
    "annotation": { "family": "DM Sans", "size": 11, "weight": 400, "style": "italic" }
  },
  "groups": [],
  "connections": [],
  "panels": []
}
```

## Groups

Groups are visual containers (phases, sections, swimlanes). Each contains nodes.

```json
{
  "id": "phase1",
  "label": "Phase 1 — Project Setup",
  "labelColor": "#43a047",
  "background": {
    "color": "#e8f5e9",
    "borderRadius": 20
  },
  "nodes": [],
  "annotations": []
}
```

## Nodes

Nodes are the content cards within a group.

```json
{
  "id": "scaffold",
  "title": "Scaffold",
  "icon": "⚙",
  "iconBackground": "#e8f5e9",
  "iconColor": "#43a047",
  "background": "#ffffff",
  "borderColor": "#cfd8dc",
  "borderRadius": 16,
  "width": 220,
  "shadow": true,
  "items": [
    { "text": "Next.js com Bun", "bullet": { "type": "dot", "color": "#c8e6c9" } },
    { "text": "Configurar Vitest", "bullet": { "type": "dot", "color": "#c8e6c9" } },
    { "text": "Configurar Playwright", "bullet": { "type": "dot", "color": "#c8e6c9" } }
  ]
}
```

### Node fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier, used by connections |
| `title` | Yes | Card title text |
| `icon` | No | Emoji or icon character displayed in header |
| `iconBackground` | No | Background color of the icon container |
| `iconColor` | No | Color of the icon character |
| `background` | No | Card background color (default: surface color) |
| `borderColor` | No | Card border color |
| `borderRadius` | No | Corner radius in px |
| `width` | No | Card width in px |
| `shadow` | No | Whether to apply box shadow |
| `items` | Yes | Array of content items |

### Item fields

| Field | Required | Description |
|-------|----------|-------------|
| `text` | Yes | The text content |
| `bullet` | No | Bullet style: `{ "type": "dot"|"dash"|"number"|"none", "color": "#hex" }` |

## Annotations

Annotations are callout notes positioned relative to their group. They have a distinctive visual style — background, border-left accent, italic text.

```json
{
  "id": "ann_phase1",
  "text": "Validar que o setup funciona end-to-end antes de avançar. Deploy \"hello world\" na Vercel.",
  "position": "right",
  "style": {
    "background": "rgba(255,255,255,0.7)",
    "borderLeftColor": "#43a047",
    "borderLeftWidth": 3,
    "borderRadius": 10,
    "maxWidth": 180
  }
}
```

### Annotation fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `text` | Yes | Annotation content |
| `position` | Yes | Relative to group: `"right"`, `"left"`, `"top"`, `"bottom"` |
| `style.background` | Yes | Background color (can include alpha) |
| `style.borderLeftColor` | Yes | Accent border color — matches the group's theme |
| `style.borderLeftWidth` | No | Border width in px (default: 3) |
| `style.borderRadius` | No | Corner radius in px |
| `style.maxWidth` | No | Max width in px |

**Critical for Excalidraw fidelity:** Annotations must be rendered as a rectangle (background) + thin accent rectangle (border-left) + text element, all grouped together. Standalone text loses the visual context.

## Connections

Connections define arrows between elements.

```json
{
  "id": "e_scaffold_to_integrations",
  "from": "scaffold",
  "to": "integrations",
  "direction": "horizontal",
  "style": {
    "strokeColor": "#78909c",
    "strokeWidth": 2,
    "arrowhead": "arrow"
  }
}
```

### Connection types

| `direction` | Description |
|-------------|-------------|
| `horizontal` | Left-to-right arrow between nodes in same group |
| `vertical` | Top-to-bottom arrow between groups |
| `elbow` | L-shaped connector (horizontal then vertical or vice-versa) |

## Panels

Panels are standalone structured elements (checklists, legends, info boxes).

```json
{
  "id": "checklist",
  "type": "checklist",
  "title": "Development Checklist",
  "subtitle": "Progresso do desenvolvimento — atualizar conforme avança",
  "background": "#ffffff",
  "borderColor": "#cfd8dc",
  "borderRadius": 16,
  "maxWidth": 480,
  "position": "bottom-center",
  "items": [
    {
      "label": "Phase 1: Project Setup",
      "checked": false,
      "subItems": [
        "Next.js + Bun scaffold",
        "Vitest, Playwright, Husky config"
      ]
    }
  ]
}
```

## Excalidraw mapping rules

These rules ensure the agent converts spec elements to Excalidraw faithfully:

| Spec element | Excalidraw representation |
|-------------|---------------------------|
| Group background | Large rectangle with `fillStyle: "solid"`, `roundness: {"type": 3}`, `strokeWidth: 1`, low-contrast `strokeColor` |
| Group label | Standalone text with `fontFamily: 3` (monospace), uppercase |
| Node card | Rectangle with `fillStyle: "solid"`, `backgroundColor: surface`, `roundness: {"type": 3}` |
| Node title + items | Single bound text element with `\n`-separated lines. First line = title (bold via caps or emphasis). Following lines = items with text bullets (`• ` prefix) |
| Node icon | Prepend emoji to the title line: `"⚙ Scaffold\n• Item 1\n• Item 2"` |
| Annotation background | Rectangle with `fillStyle: "solid"`, matching `style.background` |
| Annotation border-left | Thin rectangle (width 3-4px) aligned to left edge of annotation bg, colored with `style.borderLeftColor` |
| Annotation text | Text element positioned inside the annotation bg rectangle |
| Annotation group | All three elements (bg rect + accent rect + text) share a `groupId` |
| Horizontal connection | Arrow with `points: [[0,0], [width, 0]]` |
| Vertical connection | Arrow with `points: [[0,0], [0, height]]` |
| Checklist panel | Rectangle container + text elements for title, items, sub-items. Checkbox = small rectangle (checked: filled green, unchecked: border only) |
| Shadow | Not available in Excalidraw — skip silently |
| Gradients | Not available in Excalidraw — use solid closest color |

## Layout

The layout section provides spatial positioning data so the Excalidraw agent can place elements precisely without guessing. Without this, CSS Grid/Flexbox handles positioning in HTML but Excalidraw needs explicit coordinates.

### Grid definition

```json
{
  "layout": {
    "grid": {
      "columns": [
        { "id": "col1", "width": 260 },
        { "id": "col2", "width": 260 }
      ],
      "rows": [
        { "id": "row1", "height": 320 },
        { "id": "row2", "height": 280 }
      ],
      "columnGap": 200,
      "rowGap": 120,
      "originX": 60,
      "originY": 100
    }
  }
}
```

### Slot assignments

Each group and node gets a slot assignment that maps to the grid:

```json
{
  "id": "phase1",
  "label": "Phase 1",
  "slot": { "column": "col1", "row": "row1" },
  "nodes": [
    {
      "id": "scaffold",
      "slot": { "index": 0, "direction": "horizontal" }
    }
  ]
}
```

- **Groups** get `slot.column` + `slot.row` to place them in the grid
- **Nodes** within a group get `slot.index` + `slot.direction` (`"horizontal"` or `"vertical"`) — the agent computes x/y from the group origin, node width, and inter-node gap
- **Annotations** keep their `position` field (`"right"`, `"left"`) — the agent offsets from the parent group

### Arrow routing hints

Connections can include routing hints to prevent arrow overlap:

```json
{
  "id": "e_scaffold_to_db",
  "from": "scaffold",
  "to": "database",
  "routeOffset": 40
}
```

- `routeOffset` — vertical or horizontal pixel offset to separate arrows that share a similar path. Positive values push right/down, negative values push left/up.

### When to populate layout

- **Phase 1 (spec generation):** define the grid and slot assignments based on the diagram structure. Use element count and widths to estimate column widths and gaps.
- **Phase 2 (after HTML validation):** if the user approved the HTML, refine the layout values to match the approved visual. Update column widths, gaps, and row heights to reflect what the CSS produced.

## Validation

Before the spec is considered complete:

- [ ] Every node `id` is unique across the entire spec
- [ ] Every connection references valid `from` and `to` ids
- [ ] Every annotation has a `style.background` and `style.borderLeftColor`
- [ ] Every group has at least one node
- [ ] Typography section covers all element types used
- [ ] Colors are valid hex values (or rgba for transparency)
- [ ] Layout grid is defined with columns, rows, gaps, and origin
- [ ] Every group has a `slot` assignment (column + row)
- [ ] Every node has a `slot` assignment (index + direction)
