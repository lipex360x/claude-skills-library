# system-design

> Extract a design system from a reference image and build a complete project with separated artboards — foundations, components, and sections — all in parallel.

## Usage

```
/system-design my-project
```

> [!IMPORTANT]
> Place reference images in the `design/` folder before running. The skill analyzes all images found there. If no project slug is provided, it infers one from the image filename or asks.

## How it works

| Phase | What happens |
|-------|-------------|
| **Discover** | Finds reference images and reverse-engineers the visual language: colors (hex), typography, spacing, and component patterns |
| **Plan** | Splits the design system into 3-6 artboards (Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA) |
| **Design Brief** | Presents extracted tokens and artboard plan for user approval |
| **Design Spec** | Compiles a self-contained reference document passed to every subagent |
| **Phase A: Setup** | Creates the project, writes `tokens.css`, opens the project hub, and batch-creates artboard skeletons (shimmer cards appear immediately) |
| **Phase B: Agents** | Spawns one agent per artboard in parallel — each writes HTML via `curl` to the HTTP API. Thumbnails appear progressively on the hub |

The user stays on the **project hub** throughout, watching thumbnails appear in real-time as each agent finishes its artboard.

## Trigger phrases

- "extract a design system"
- "create artboards from this design"
- "build a component library"
- Also activates when a reference image, screenshot, or mockup is provided — even without explicitly saying "design system"

## Directory structure

```
system-design/
├── SKILL.md                        # Core instructions and hub-centric build process
├── references/
│   ├── agent-prompt.md             # Prompt template and curl instructions for subagents
│   └── artboard-guidelines.md      # Standard artboard structure and content guidelines
└── templates/
    └── design-spec.md              # Design spec template passed to every agent
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill system-design
```
