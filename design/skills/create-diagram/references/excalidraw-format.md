# Excalidraw JSON Format Reference

Complete specification for generating valid Excalidraw `.excalidraw` files programmatically.

## Table of contents

- [File structure](#file-structure)
- [Element types](#element-types)
- [Common properties](#common-properties)
- [Rectangles](#rectangles)
- [Ellipses](#ellipses)
- [Diamonds](#diamonds)
- [Text elements](#text-elements)
- [Arrows](#arrows)
- [Lines](#lines)
- [Groups](#groups)
- [Layout guidelines](#layout-guidelines)
- [Color palettes](#color-palettes)
- [Validation checklist](#validation-checklist)

## File structure

Every `.excalidraw` file is a JSON object with this top-level structure:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "theme": "dark",
    "viewBackgroundColor": "#0B0F1A",
    "gridSize": 20,
    "gridColor": {
      "bold": "#1e293b",
      "regular": "#131825"
    }
  },
  "files": {}
}
```

- `elements`: array of all diagram elements (shapes, text, arrows)
- `appState.theme`: `"dark"` or `"light"`
- `appState.viewBackgroundColor`: canvas background color
- `appState.gridSize`: snap grid in pixels (use 20 for most diagrams)
- `files`: empty object (used for embedded images, rarely needed)

## Element types

| Type | Excalidraw `type` | Use for |
|------|-------------------|---------|
| Rectangle | `rectangle` | Nodes, cards, containers, services |
| Ellipse | `ellipse` | Start/end terminals, circular nodes |
| Diamond | `diamond` | Decision points, conditions |
| Text | `text` | Labels, annotations, standalone text |
| Arrow | `arrow` | Connections with direction |
| Line | `line` | Connections without direction, separators |

## Common properties

Every element shares these properties:

```json
{
  "id": "unique_descriptive_id",
  "type": "rectangle",
  "x": 310,
  "y": 490,
  "width": 280,
  "height": 96,
  "strokeColor": "#3b82f6",
  "backgroundColor": "#131825",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "angle": 0,
  "seed": 1001,
  "version": 1,
  "versionNonce": 1001,
  "isDeleted": false,
  "groupIds": [],
  "boundElements": [],
  "frameId": null,
  "link": null,
  "locked": false
}
```

### Property notes

- **`id`**: unique string. Use descriptive names: `"api_gateway"`, `"db_primary"`, `"e_api_to_db"` (prefix arrows with `e_`), `"lbl_ready"` (prefix standalone labels with `lbl_`).
- **`seed`** and **`versionNonce`**: use any integer. These control the hand-drawn randomization. Use the same value for both. Assign incrementally (1001, 1002, 1003...).
- **`roughness`**: `0` = clean lines (recommended for technical diagrams), `1` = slight roughness, `2` = full hand-drawn sketch.
- **`fillStyle`**: `"solid"`, `"hachure"`, `"cross-hatch"`, or `"dots"`.
- **`strokeStyle`**: `"solid"`, `"dashed"`, or `"dotted"`.
- **`groupIds`**: array of group ID strings. Elements sharing a group ID move together.
- **`boundElements`**: array of `{"type": "text"|"arrow", "id": "element_id"}` — references to text labels contained inside this shape, or arrows connected to it.

### Container-text binding

To place text inside a shape, the shape's `boundElements` must reference the text, and the text's `containerId` must reference the shape:

```json
// Shape
{
  "id": "my_node",
  "type": "rectangle",
  "boundElements": [{"type": "text", "id": "my_node_text"}],
  ...
}

// Text inside shape
{
  "id": "my_node_text",
  "type": "text",
  "containerId": "my_node",
  "verticalAlign": "middle",
  "textAlign": "center",
  ...
}
```

## Rectangles

Standard shape for nodes, cards, services, containers.

```json
{
  "id": "service_auth",
  "type": "rectangle",
  "x": 310,
  "y": 200,
  "width": 280,
  "height": 72,
  "strokeColor": "#3b82f6",
  "backgroundColor": "#131825",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "roundness": {"type": 3},
  "boundElements": [
    {"type": "text", "id": "service_auth_text"},
    {"type": "arrow", "id": "e_auth_to_db"}
  ]
}
```

- **`roundness`**: `{"type": 3}` for rounded corners (recommended), `null` for sharp corners.
- **Accent border**: use `strokeColor` on the left side by making the shape's left border thicker — or create a thin rectangle (width 3-4px) aligned to the left edge as a visual accent. Alternatively, use `strokeWidth: 2` with a colored `strokeColor`.

## Ellipses

Circular or oval shapes for terminals, events, states.

```json
{
  "id": "start",
  "type": "ellipse",
  "x": 420,
  "y": 50,
  "width": 60,
  "height": 60,
  "strokeColor": "#10b981",
  "backgroundColor": "#064e3b",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 0
}
```

## Diamonds

Decision points, conditions, branching logic.

```json
{
  "id": "decision_auth",
  "type": "diamond",
  "x": 390,
  "y": 400,
  "width": 120,
  "height": 80,
  "strokeColor": "#334155",
  "backgroundColor": "#131825",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "roughness": 0,
  "roundness": null,
  "boundElements": [
    {"type": "text", "id": "decision_auth_text"},
    {"type": "arrow", "id": "e_yes"},
    {"type": "arrow", "id": "e_no"}
  ]
}
```

## Text elements

### Standalone text (labels, annotations, phase headers)

```json
{
  "id": "lbl_phase1",
  "type": "text",
  "x": 80,
  "y": 100,
  "width": 160,
  "height": 16,
  "text": "● DISCOVERY",
  "fontSize": 12,
  "fontFamily": 3,
  "textAlign": "left",
  "verticalAlign": "top",
  "strokeColor": "#475569",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "containerId": null,
  "originalText": "● DISCOVERY",
  "lineHeight": 1.25
}
```

### Contained text (inside shapes)

```json
{
  "id": "service_auth_text",
  "type": "text",
  "x": 330,
  "y": 210,
  "width": 240,
  "height": 48,
  "text": "Auth Service\nHandles login and session\nmanagement",
  "fontSize": 13,
  "fontFamily": 2,
  "textAlign": "left",
  "verticalAlign": "middle",
  "strokeColor": "#e2e8f0",
  "backgroundColor": "transparent",
  "containerId": "service_auth",
  "originalText": "Auth Service\nHandles login and session\nmanagement",
  "lineHeight": 1.25
}
```

### Font families

| Value | Font | Use for |
|-------|------|---------|
| 1 | Virgil (hand-drawn) | Sketchy/informal diagrams |
| 2 | Helvetica | Body text, descriptions |
| 3 | Cascadia (monospace) | Labels, code, technical annotations |
| 5 | Excalifont | Default Excalidraw font |

**Recommendation**: Use `fontFamily: 3` (monospace) for node titles and labels, `fontFamily: 2` for descriptions. Use `fontFamily: 5` only if you want the hand-drawn Excalidraw aesthetic.

### Font sizes

| Context | Size |
|---------|------|
| Phase/section headers | 12px (monospace, uppercase) |
| Node titles (first line) | 14px (monospace, bold weight 600) |
| Node descriptions | 12-13px |
| Arrow labels | 10-12px |
| Small annotations | 10-11px |
| Minimum readable | 10px |

## Arrows

Arrows connect elements with direction and optional labels.

```json
{
  "id": "e_auth_to_db",
  "type": "arrow",
  "x": 450,
  "y": 272,
  "width": 0,
  "height": 40,
  "points": [[0, 0], [0, 40]],
  "strokeColor": "#3b82f6",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 1.5,
  "strokeStyle": "solid",
  "roughness": 0,
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "startBinding": {"elementId": "service_auth", "focus": 0, "gap": 1},
  "endBinding": {"elementId": "db_primary", "focus": 0, "gap": 1}
}
```

### Arrow properties

- **`points`**: array of `[x, y]` offsets from the arrow's position. First point is always `[0, 0]`. Multi-segment arrows have intermediate points.
- **`startArrowhead`** / **`endArrowhead`**: `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`.
- **`startBinding`** / **`endBinding`**: connects the arrow to shapes.
  - `elementId`: the shape's ID
  - `focus`: position on the shape's edge (-1 to 1, 0 = center)
  - `gap`: distance from the shape's edge (use 1)
- **Important**: when an arrow binds to a shape, the shape's `boundElements` must include a reference back to the arrow: `{"type": "arrow", "id": "e_auth_to_db"}`.

### Multi-segment arrows (elbows, loops)

```json
{
  "id": "e_loop",
  "type": "arrow",
  "x": 590,
  "y": 662,
  "width": 56,
  "height": 124,
  "points": [[0, 0], [56, 0], [56, -124], [0, -124]],
  "strokeStyle": "dashed",
  "opacity": 40,
  "startBinding": {"elementId": "push", "focus": -0.8, "gap": 1},
  "endBinding": {"elementId": "startbacklog", "focus": -0.8, "gap": 1}
}
```

### Arrow labels

Place a standalone text element near the arrow midpoint. Don't use `containerId` binding — position it manually near the arrow's visual center.

## Lines

Non-directional connections, dividers, separators.

```json
{
  "id": "separator_1",
  "type": "line",
  "x": 250,
  "y": 400,
  "width": 560,
  "height": 0,
  "points": [[0, 0], [560, 0]],
  "strokeColor": "#1e293b",
  "strokeWidth": 1,
  "startArrowhead": null,
  "endArrowhead": null,
  "startBinding": null,
  "endBinding": null
}
```

## Groups

Group elements by adding the same group ID string to their `groupIds` arrays:

```json
// Element 1
{"id": "card1", "groupIds": ["group_board"], ...}
// Element 2
{"id": "card2", "groupIds": ["group_board"], ...}
```

Grouped elements move, resize, and rotate together in Excalidraw.

## Layout guidelines

### Spacing

| Aspect | Recommended |
|--------|-------------|
| Horizontal gap between nodes | 200-300px |
| Vertical gap between rows | 100-150px |
| Arrow length (short) | 40px |
| Arrow length (medium) | 60-80px |
| Padding inside containers | 16-20px |
| Margin between sections | 40-56px |

### Positioning strategy

1. **Start at a consistent origin**: first element at approximately `x: 300, y: 100`.
2. **Flow direction**: top-to-bottom for most diagrams, left-to-right for timelines/pipelines.
3. **Align centers**: for vertical flows, keep `x` consistent. For horizontal flows, keep `y` consistent.
4. **Grid snap**: position elements on multiples of 20 (matching `gridSize: 20`).

### Coordinate calculation for arrows

Vertical arrow (top to bottom):
- `x`: center of the connected nodes (`node.x + node.width / 2`)
- `y`: bottom of source node (`source.y + source.height`)
- `height`: gap between source bottom and target top
- `points`: `[[0, 0], [0, height]]`

Horizontal arrow (left to right):
- `x`: right edge of source (`source.x + source.width`)
- `y`: vertical center of source (`source.y + source.height / 2`)
- `width`: gap between source right and target left
- `points`: `[[0, 0], [width, 0]]`

## Color palettes

### Dark theme (default for technical diagrams)

```
Background:     #0B0F1A
Surface:        #131825
Surface raised: #1A2035
Border:         #252D44
Text primary:   #E2E8F0
Text muted:     #64748B
Text dim:       #475569
Blue:           #3B82F6
Blue light:     #60A5FA
Cyan:           #06B6D4
Emerald:        #10B981
Amber:          #F59E0B
Violet:         #8B5CF6
Rose:           #F43F5E
```

### Light theme

```
Background:     #FFFFFF
Surface:        #F8FAFC
Border:         #E2E8F0
Text primary:   #1E293B
Text muted:     #64748B
Blue:           #3B82F6
Emerald:        #059669
Amber:          #D97706
Rose:           #E11D48
```

### Pastel theme

```
Background:     #FEFCE8
Surface:        #FFF7ED
Primary:        #A5D8FF (light blue)
Secondary:      #B2F2BB (light green)
Central:        #FFD43B (yellow)
Alert:          #FFC9C9 (light red)
```

## Validation checklist

Before saving the `.excalidraw` file, verify:

- [ ] All element IDs are unique
- [ ] No elements overlap (check x, y, width, height)
- [ ] Every arrow has valid `startBinding` and `endBinding` (or explicit `null`)
- [ ] Every shape referenced by an arrow has that arrow in its `boundElements`
- [ ] Every text with `containerId` has its container shape reference it in `boundElements`
- [ ] Text is readable (minimum 10px, prefer 12-16px)
- [ ] `seed` and `versionNonce` are unique per element
- [ ] JSON is valid and parseable
- [ ] Element count is reasonable (under 100 for readability, under 200 for complex diagrams)
- [ ] `appState.viewBackgroundColor` matches the intended theme
