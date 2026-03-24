# extract-design-system

> Analyze a design image and create a full design system project with separated artboards via MCP tools.

Reverse-engineers the visual language from reference images — extracting colors, typography, spacing, and component patterns — then builds a complete project with parallel subagents, each writing an artboard. The user stays on the project hub watching thumbnails appear progressively as agents complete their work.

## Usage

```text
/extract-design-system [project-slug]
```

> [!TIP]
> Also activates when you provide a reference image, screenshot, or mockup and want to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns — even without explicitly saying "design system."

## How it works

1. **Discover and analyze reference image** — Read images from `design/` and extract the full visual language: hex colors, typography, spacing rhythm, and component patterns
2. **Plan artboards** — Split the design system into 3–6 artboards (Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA)
3. **Present Design Brief** — Show extracted design tokens and artboard plan for user approval before proceeding
4. **Build Design Spec** — Compile a self-contained reference document passed verbatim to every subagent
5. **Setup and launch agents** — Phase A: create project, write tokens.css, open hub, batch-create artboard skeletons. Phase B: spawn one agent per artboard in parallel
6. **Final verification** — Verify all thumbnails are visible on the hub and present screenshot to user
7. **Refinement** — User reviews artboards and requests adjustments; only affected agents are re-launched
8. **Report** — Summary of project slug, artboard count, design tokens, completion status, and audit results

## Directory structure

```text
extract-design-system/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── agent-prompt.md        # Prompt template and curl instructions for subagents
│   └── artboard-guidelines.md # Standard artboard structure and content guidelines
└── templates/
    └── design-spec.md         # Design spec template passed to every agent
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill extract-design-system
```
