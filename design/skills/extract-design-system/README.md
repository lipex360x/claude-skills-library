# extract-design-system

> Analyze a design image and create a full design system project with separated artboards via MCP tools.

Reverse-engineers the visual language from reference images — extracting exact hex colors, typography hierarchy, spacing rhythm, and component patterns — then builds a complete project with parallel subagents, each writing one artboard via HTTP API (`curl`). Uses a two-phase build sequence: Phase A sets up the project, writes `tokens.css`, and batch-creates artboard skeletons with shimmer cards; Phase B launches one agent per artboard in parallel. The user stays on the project hub throughout, watching thumbnails appear progressively as agents complete.

## Usage

```text
/extract-design-system [project-slug]
```

> [!TIP]
> Also activates when you provide a reference image, screenshot, or mockup and want to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns — even without explicitly saying "design system."

### Examples

```text
/extract-design-system landing-page      # use "landing-page" as project slug
/extract-design-system                   # infer slug from image filename or ask interactively
```

## How it works

1. **Discover and analyze reference image** — Read images from `design/` and extract the full visual language: exact hex colors, typography families and weight scale, spacing rhythm, component patterns (buttons, cards, badges, nav, forms), and a one-sentence visual direction
2. **Plan artboards** — Split the design system into 3-6 artboards (typically Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA) following the artboard guidelines
3. **Present Design Brief** — Show all extracted design tokens and artboard plan in a table with agent count. Gate on user approval before any project creation
4. **Build Design Spec** — Compile a self-contained reference document from the approved brief, passed verbatim to every subagent so they can write HTML without re-analyzing the image
5. **Setup and launch agents** — Phase A: `create_project`, write `tokens.css`, `navigate` to hub, `create_artboards` batch (shimmer cards appear). Phase B: spawn one agent per artboard in parallel, each writing via `curl` to the HTTP API
6. **Final verification** — Verify all thumbnails are visible on the hub and present a screenshot to the user
7. **Refinement** — User reviews artboards and requests adjustments; only affected agents are re-launched
8. **Report** — Summary of project slug, artboard count, design token palette, completion status per artboard, and audit results

[↑ Back to top](#extract-design-system)

## Directory structure

```text
extract-design-system/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── agent-prompt.md        # Prompt template, curl command format, and quality standards for subagents
│   └── artboard-guidelines.md # Standard artboard structure, naming, and per-artboard content rules
└── templates/
    └── design-spec.md         # Design spec template compiled from the brief and passed to every agent
```

[↑ Back to top](#extract-design-system)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill extract-design-system
```
