# Design Aesthetics for Diagrams

Principles adapted from the frontend-design skill to elevate Excalidraw diagram quality beyond generic defaults.

## Design Thinking

Before generating any diagram, commit to an aesthetic direction:

1. **Purpose**: What is this diagram communicating? Technical architecture, business process, conceptual map?
2. **Audience**: Engineers want precision and clarity. Executives want hierarchy and simplicity. Designers want visual polish.
3. **Tone**: Choose one and commit — clean/corporate, playful/sketch, bold/technical, minimal/elegant, rich/detailed.

## Color Palettes

Avoid the default light-blue-on-white that screams "AI-generated diagram."

### Curated Palettes

**Dark Professional** (for technical audiences):
- Background: `#1e1e2e` or `#0f172a`
- Primary elements: `#cdd6f4` stroke, `#313244` fill
- Accent: `#89b4fa` (blue), `#a6e3a1` (green), `#f38ba8` (red)
- Text: `#cdd6f4`

**Warm Earth** (for business/strategy):
- Background: `#faf6f1`
- Primary elements: `#5c4b3a` stroke, `#f0e6d8` fill
- Accent: `#c47f3c` (amber), `#6a8f6b` (sage), `#b85c4c` (terracotta)
- Text: `#3d3024`

**Ocean Depth** (for data flow):
- Background: `#f8fafc`
- Primary elements: `#1e3a5f` stroke, `#e8f4f8` fill
- Accent: `#0ea5e9` (sky), `#06b6d4` (cyan), `#8b5cf6` (violet)
- Text: `#0f172a`

**Neon Minimal** (for modern/startup):
- Background: `#09090b`
- Primary elements: `#a1a1aa` stroke, `#18181b` fill
- Accent: `#22d3ee` (cyan), `#a78bfa` (purple), `#34d399` (emerald)
- Text: `#fafafa`

**Pastel Soft** (for conceptual/educational):
- Background: `#fffbf0`
- Primary elements: `#6b7280` stroke
- Node fills: `#fde68a` (yellow), `#bbf7d0` (green), `#bfdbfe` (blue), `#fecaca` (red), `#e9d5ff` (purple)
- Text: `#374151`

### Palette Rules

- **Dominant + accent**: One dominant color for most elements, 1-2 accent colors for emphasis. Never distribute colors evenly.
- **Semantic consistency**: Same color = same category throughout the diagram. Don't reuse colors for unrelated concepts.
- **Contrast hierarchy**: Important elements get higher contrast (darker stroke, saturated fill). Supporting elements fade back.

## Spatial Composition

### Layout Principles

- **Asymmetry over symmetry**: Perfectly centered grids look mechanical. Offset clusters, varied spacing, and intentional grouping create visual interest.
- **Whitespace as design element**: Dense diagrams lose clarity. Use generous padding (200-300px between groups, 150px between related elements).
- **Visual hierarchy through size**: Central/important nodes should be 20-30% larger than peripheral ones. Not everything needs to be the same size.
- **Flow direction**: Left-to-right or top-to-bottom for processes. Radial for relationships. Hierarchical for org structures.

### Advanced Layout Techniques

- **Cluster grouping**: Related elements close together with shared background rectangle at low opacity
- **Floating labels**: Place descriptive text near groups, not crammed inside boxes
- **Staggered grids**: Offset every other row by half a column width for organic feel
- **Breathing room**: Minimum 60px between any two elements; 100px for unrelated elements

## Typography in Excalidraw

Default to `fontFamily: 1` (Virgil) for the hand-drawn sketch feel that defines Excalidraw. Use `2` (Helvetica) when clean readability matters, `3` (Cascadia) for code or monospace contexts. Control hierarchy through:

- **Title**: 28-32px, bold weight simulation through element emphasis
- **Node labels**: 18-22px, centered in elements
- **Edge labels**: 14-16px, lighter color than node text
- **Annotations**: 12-14px, muted color, positioned as floating notes

## Anti-Patterns

These make diagrams look like generic AI output — avoid them:

- All nodes the same size and color (`#a5d8ff` everywhere)
- Perfect grid layout with equal spacing
- Every connection as a straight arrow
- No visual hierarchy — everything at the same importance level
- Default white background with no atmosphere
- Rainbow colors with no semantic meaning
- Text crammed inside tiny boxes
- Arrows crossing over elements instead of routing around them
