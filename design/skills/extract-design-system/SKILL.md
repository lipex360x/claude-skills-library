---
name: extract-design-system
description: Analyze a design image and create a full design system project with separated artboards (foundations, components, sections) via MCP tools. Use this skill whenever the user provides a reference image, screenshot, or mockup and wants to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns from an existing design — even if they don't explicitly say "design system."
user-invocable: true
argument-hint: "[project-slug]"
---

# System Design — Hub-Centric Builder

Extract a design system from a reference image and create a complete project with separated artboards. The user stays on the **project hub** throughout — thumbnails appear progressively as each agent completes its artboard.

## Usage

The user places reference images in the `design/` folder. If an argument is provided (e.g. `/extract-design-system my-project`), use it as the project slug. Otherwise, infer from the image filename or ask.

## Prerequisites

This skill depends on MCP tools from a **web-based design system server** (e.g. a local dev server with artboard management). The following tools must be available:

| MCP Tool | Purpose |
|---|---|
| `create_project` | Create a new design system project |
| `navigate` | Open the project hub in the browser |
| `create_artboards` | Batch-create artboard files with shimmer placeholders |
| `get_screenshot()` | Capture a screenshot of the current browser view |

**Pre-flight check:** Before starting Phase A, verify these tools are available. If any tool is missing, stop and tell the user which MCP server needs to be configured.

## Deliverables

The skill produces the following output files inside the project directory:

- **`tokens.css`** — CSS custom properties extracted from the reference (colors, typography, spacing)
- **Artboard HTML files** — one per artboard (e.g. `foundations.html`, `components.html`, `hero-navigation.html`, `content-sections.html`, `footer-cta.html`). See `references/artboard-guidelines.md` for the standard filenames
- **Project manifest** — created by `create_artboards`, tracks artboard status and metadata

## Steps

### 0. Pre-flight

Verify that the required MCP tools (`create_project`, `navigate`, `create_artboards`, `get_screenshot`) are available. If any is missing, stop and tell the user which MCP server to configure — do not proceed with a partial toolset.

### 1. Discover and analyze the reference image

```
Glob: design/**/*.{png,jpg,jpeg,webp}
```

If no images are found, stop and tell the user: "No reference images found in `design/`. Place at least one image (PNG, JPG, or WebP) in the `design/` folder and try again."

Read all images. Analyze as a **design reference** — the goal is to reverse-engineer the visual language (colors, typography, spacing, component patterns), not to clone the page content.

Extract: color palette (exact hex), typography (families, weight scale, size hierarchy), spacing rhythm, components (buttons, cards, badges, nav, forms), sections, and a one-sentence visual direction.

### 2. Plan the artboards

Read `references/artboard-guidelines.md` for the standard artboard structure and per-artboard content guidelines. Typical split: Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA. Aim for 3-6 artboards depending on the reference complexity.

### 3. Present the Design Brief

Write a **Design Brief** with:
- All extracted design tokens
- The **artboard plan** — table with artboard name, file, content, and agent count per artboard
- A **total agent count** summary (e.g. "5 artboards, 5 agents in parallel")

Show it to the user and **wait for approval** before proceeding. Use `AskUserQuestion` with approve/adjust options for a cleaner flow.

### 4. Build the Design Spec

After approval, compile a **Design Spec** — a structured, self-contained reference for subagents. Read `templates/design-spec.md` for the template structure. The spec is passed verbatim to every agent prompt so they can start writing HTML immediately without re-analyzing the image.

### 5. Setup first, then launch agents

The build is a **two-phase sequence**. Setup must complete before agents start — otherwise agents race against infrastructure creation and may write to a manifest that doesn't exist yet.

#### Phase A — Setup (single response, all in parallel)

- **1 × `create_project`** — create the project
- **1 × Write** — write `tokens.css` (read template first in step 4)
- **1 × `navigate`** — open the project hub
- **1 × `create_artboards`** — batch create with skeleton HTML (shimmer cards appear)

Wait for all setup calls to complete before proceeding.

#### Phase B — Launch agents (follow-up response)

- **N × Agent** — one per artboard, all in a **single message** (foreground so the user can watch progress). Each receives the Design Spec and writes via `curl` to the HTTP API. Read `references/agent-prompt.md` for prompt requirements, the curl template, and quality standards.

**Why two phases?** `create_artboards` populates the manifest and creates shimmer files. Agents call the HTTP API (`POST /api/write-artboard`) which overwrites the shimmer HTML and emits `artboard-ready` via WebSocket. The client tracks `pendingArtboards` — the robot badge blinks the entire time and only stops when all agents finish. If agents run before setup, they race against `create_artboards` and produce an empty manifest.

**Why curl, not MCP?** Subagents don't reliably inherit MCP tools from the parent process. The HTTP API is the same endpoint the MCP tool calls internally — `curl` cuts the intermediary and works 100% of the time.

**Error handling:**
- If `create_project` or `create_artboards` fails in Phase A, stop and report the error — do not launch agents against a broken setup.
- If an agent fails in Phase B (curl error, crash, timeout), report which artboard failed. The user can re-run individual agents without restarting the whole build.

### 6. Final verification

After all agents complete:
1. All thumbnails should be visible on the hub
2. Take a screenshot via `get_screenshot()` and present to the user

### 7. Refinement

After presenting the screenshot, ask the user if any artboard needs adjustments. Use `AskUserQuestion` with options like `["Looks good — done", "Adjust an artboard"]`. If the user wants changes, re-launch only the affected agent(s) with updated instructions — no need to rebuild the entire project. Repeat until the user approves.

## Guidelines

These exist because AI-generated designs tend to fall into specific traps. Understanding *why* helps you make better judgment calls.

- **Lorem ipsum for all text.** The goal is extracting the design system, not the content. Real language distracts reviewers from evaluating visual patterns. Use Latin words only — repeat this in every agent prompt because agents don't inherit parent context.

- **Stay on the hub** during the build. The user watches thumbnails appear progressively — navigating to the editor would break the visual feedback loop.

- **Agents write via `curl` to the HTTP API** (`POST /api/write-artboard`), which writes the file and notifies the browser in one call. Using the `Write` tool directly doesn't notify the browser — no thumbnail update, robot keeps blinking. MCP tools are not available to subagents.

- **Batch creation** via `create_artboards` — one MCP call, not one per artboard. This shows all shimmer cards at once, giving the user immediate visual feedback of what's coming.

- **Tasks (TaskCreate)** — one per artboard minimum. The user needs to see progress as agents work independently.

- **tokens.css** — define CSS variables from the extracted palette, then reference `var()` in artboard HTML. This ensures consistency across artboards built by different agents.

- **No emojis** in designs unless the reference uses them. SVG or Unicode symbols for icons.
