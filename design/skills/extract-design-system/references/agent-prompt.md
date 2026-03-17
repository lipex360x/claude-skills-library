# Agent Prompt Requirements

## What each subagent prompt should include

1. The full Design Spec (tokens, typography, patterns)
2. Which specific artboard + sections to write (e.g., "Foundations: Color Palette, Typography, Spacing")
3. The complete HTML template structure (doctype, head with tokens.css + fonts, artboard container)
4. The lorem ipsum rule (agents don't inherit parent context, so repeat it explicitly)
5. Instruction to write via HTTP API using Bash + curl (see below)
6. The quality standards below

## How agents write artboards

Subagents MUST write artboards via the HTTP API using Bash + curl. They do NOT have access to MCP tools and MUST NOT use the `Write` tool to touch artboard files directly.

**Why:**
- `curl` → HTTP API → writes file + emits `artboard-ready` via WebSocket → hub updates thumbnail + robot stops blinking
- `Write` tool → writes file but does NOT notify the browser → no thumbnail update, robot blinks forever

**Include this exact block in every agent prompt:**

```
## How to write your artboard

Use Bash with curl to write the artboard. Do NOT use the Write tool or any MCP tool.

Write your HTML to a shell variable, then POST it:

```bash
HTML='your complete HTML string here'
curl -s -X POST http://localhost:3001/api/write-artboard \
  -H 'Content-Type: application/json' \
  -d "$(jq -n --arg slug "PROJECT_SLUG" --arg file "FILENAME" --arg html "$HTML" '{slug:$slug,file:$file,html:$html}')"
```

IMPORTANT:
- Use jq to safely escape the HTML into JSON (handles quotes, newlines, special chars)
- Do NOT use the Write tool to write artboard files — it breaks the notification flow
- Do NOT use MCP tools — they are not available to subagents
- If curl fails, report the error. Do NOT fall back to Write.
```

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
