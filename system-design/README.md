# system-design

Extract a design system from a reference image and create a complete project with separated artboards — foundations, components, and sections — built in parallel by subagents.

## Trigger phrases

- "extract a design system"
- "create artboards from this design"
- "build a component library"
- Also activates when the user provides a reference image, screenshot, or mockup and wants to reverse-engineer visual patterns — even without explicitly saying "design system"

## How it works

1. **Discover and analyze** — Finds reference images in the `design/` folder and reverse-engineers the visual language: color palette (hex), typography, spacing rhythm, and component patterns
2. **Plan the artboards** — Splits the design system into 3-6 artboards (typically: Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA)
3. **Present the Design Brief** — Shows extracted design tokens and artboard plan for user approval
4. **Build the Design Spec** — Compiles a self-contained reference document passed to every subagent
5. **Phase A: Setup** — Creates the project, writes `tokens.css` with CSS variables, opens the project hub, and batch-creates artboard skeletons (shimmer cards appear immediately)
6. **Phase B: Launch agents** — Spawns one agent per artboard in parallel, each writing HTML via `curl` to the HTTP API. Thumbnails appear progressively on the hub as agents complete

The user stays on the **project hub** throughout — watching thumbnails appear in real-time as each agent finishes its artboard.

## Usage

```
/system-design my-project
```

Place reference images in the `design/` folder before running. The skill will analyze all images found there. If no project slug is provided, it infers one from the image filename or asks.

## Directory structure

```
system-design/
├── SKILL.md                            # Core instructions and hub-centric build process
├── references/
│   ├── agent-prompt.md                 # Prompt template and curl instructions for subagents
│   └── artboard-guidelines.md          # Standard artboard structure and content guidelines
└── templates/
    └── design-spec.md                  # Design spec template passed to every agent
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill system-design
```
