---
name: system-design
description: Analyze a design image and create a full design system project with separated artboards (foundations, components, sections) via MCP tools. Use this skill whenever the user provides a reference image, screenshot, or mockup and wants to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns from an existing design — even if they don't explicitly say "design system."
user-invocable: true
---

# System Design — Hub-Centric Builder

Extract a design system from a reference image and create a complete project with separated artboards. The user stays on the **project hub** throughout — thumbnails appear progressively as each agent completes its artboard.

## Usage

The user places reference images in the `design/` folder. If an argument is provided (e.g. `/system-design invena`), use it as the project slug. Otherwise, infer from the image filename or ask.

## Steps

### 1. Discover and analyze the reference image

```
Glob: design/**/*.{png,jpg,jpeg,webp}
```

Read all images. Analyze as a **design reference** — the goal is to reverse-engineer the visual language (colors, typography, spacing, component patterns), not to clone the page content.

Extract: color palette (exact hex), typography (families, weight scale, size hierarchy), spacing rhythm, components (buttons, cards, badges, nav, forms), sections, and a one-sentence visual direction.

Write a **Design Brief** with:
- All extracted design tokens
- The **artboard plan** — table with artboard name, file, content, and agent count per artboard
- A **total agent count** summary (e.g. "5 artboards, 5 agents in parallel")

Show it to the user and **wait for approval** before proceeding.

### 2. Build the Design Spec

After approval, compile a **Design Spec** — a structured, self-contained reference for subagents. Read `templates/design-spec.md` for the template structure. The spec is passed verbatim to every agent prompt so they can start writing HTML immediately without re-analyzing the image.

### 3. Launch agents + setup in ONE single response

Subagents take several seconds to initialize. They MUST be launched **at the same time** as the setup tools, NOT after.

**CRITICAL**: Your response must contain ALL of the following tool calls in a **single message** — agents AND setup tools together. Do NOT wait for setup to finish before launching agents. Do NOT send agents in a separate follow-up response.

The single response must include these tool calls (order in the message doesn't matter — they run in parallel):

- **N × Agent** (`run_in_background: true`) — one per artboard. Each receives the Design Spec and calls `mcp__design-canvas__write_artboard`. Read `references/agent-prompt.md` for prompt requirements and quality standards.
- **1 × `create_project`** — create the project
- **1 × Write** — write `tokens.css` (read template first in step 2)
- **1 × `navigate`** — open the project hub
- **1 × `create_artboards`** — batch create with skeleton HTML (shimmer cards)

This ensures agents start initializing (which takes seconds) while the project setup happens. By the time setup is done and shimmer cards appear, agents are already generating HTML. The robot indicator blinks throughout the process and stops only when all agents finish.

### 4. Plan the artboards

Read `references/artboard-guidelines.md` for the standard artboard structure and per-artboard content guidelines. Typical split: Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA. Aim for 3-6 artboards depending on the reference complexity.

### 5. Final verification

After all agents complete:
1. All thumbnails should be visible on the hub
2. Take a screenshot via `get_screenshot()` and present to the user

## Guidelines

These exist because AI-generated designs tend to fall into specific traps. Understanding *why* helps you make better judgment calls.

- **Lorem ipsum for all text.** The goal is extracting the design system, not the content. Real language distracts reviewers from evaluating visual patterns. Use Latin words only — repeat this in every agent prompt because agents don't inherit parent context.

- **Stay on the hub** during the build. The user watches thumbnails appear progressively — navigating to the editor would break the visual feedback loop.

- **Agents use `write_artboard` MCP**, which writes the file and notifies the browser in one call. `write_html` requires an open editor (wrong context), and `Write` doesn't notify the browser (no thumbnail update).

- **Batch creation** via `create_artboards` — one MCP call, not one per artboard. This shows all shimmer cards at once, giving the user immediate visual feedback of what's coming.

- **Tasks (TaskCreate)** — one per artboard minimum. The user needs to see progress as agents work independently.

- **tokens.css** — define CSS variables from the extracted palette, then reference `var()` in artboard HTML. This ensures consistency across artboards built by different agents.

- **No emojis** in designs unless the reference uses them. SVG or Unicode symbols for icons.
