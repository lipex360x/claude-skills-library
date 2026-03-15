# Agent Prompt Requirements

## What each subagent prompt should include

1. The full Design Spec (tokens, typography, patterns)
2. Which specific artboard + sections to write (e.g., "Foundations: Color Palette, Typography, Spacing")
3. The complete HTML template structure (doctype, head with tokens.css + fonts, artboard container)
4. The lorem ipsum rule (agents don't inherit parent context, so repeat it explicitly)
5. Instruction to call `mcp__design-canvas__write_artboard` with slug, file, and the complete HTML string
6. Instruction to use only `write_artboard` — no other tools
7. The quality standards below

## Why only `write_artboard`

- `write_html` injects into a live editor DOM via WebSocket — requires an open editor, which doesn't exist during hub-centric builds
- `write_artboard` writes the file to disk AND broadcasts `artboard-ready` to the hub in one call
- `Write` (filesystem) works but doesn't notify the browser, so thumbnails won't update

## Quality standards

Include these in every agent prompt. Repetition is intentional — it's a prompt engineering technique that combats the tendency to produce generic output.

**Craftsmanship**: Every artboard should look like it was designed by a senior designer with painstaking attention to alignment, consistent spacing, and visual rhythm. Master-level execution of shadows, borders, color application, and typography sizing. This matters because AI-generated designs tend toward "good enough" — push past that.

**Containment**: Nothing falls off the artboard. Nothing overlaps unintentionally. Every element has breathing room and clear separation from its neighbors. This is the most common failure mode in AI-generated compositions — elements bleed off edges or stack on top of each other.

**Anti-patterns to avoid** (these are the specific traps AI designs fall into):
- Generic gradients (especially purple-to-blue on white)
- Uniform spacing everywhere — vary rhythm intentionally
- Oversized elements that waste space
- Tiny text that's unreadable at thumbnail scale
- Inconsistent border-radius across similar elements
- Colors that don't match the design spec tokens
- Placeholder images as plain gray boxes — use colored rectangles with subtle gradients from the palette

**Refinement over addition**: If the artboard feels incomplete, refine what's already there rather than adding more elements. Fewer components executed beautifully beats many done generically. The guiding question: "How can I make what's here more polished?"
