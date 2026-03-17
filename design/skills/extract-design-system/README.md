# extract-design-system

> Analyze a design image and create a full design system project with separated artboards (foundations, components, sections) via MCP tools.

Reverse-engineers the visual language from reference images — extracting colors, typography, spacing, and component patterns — then builds a complete project with parallel subagents, each writing an artboard. The user stays on the project hub watching thumbnails appear progressively.

## Usage

```text
/extract-design-system [project-slug]
```

> [!TIP]
> Also activates when providing a reference image, screenshot, or mockup and asking to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns — even without explicitly saying "design system."

## How it works

1. **Discover** — finds reference images in `design/` and extracts the full visual language (hex colors, typography, spacing rhythm, component patterns)
2. **Plan** — splits the design system into 3-6 artboards (Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA)
3. **Design Brief** — presents extracted tokens and artboard plan for user approval
4. **Design Spec** — compiles a self-contained reference document passed to every subagent
5. **Phase A: Setup** — creates the project, writes `tokens.css`, opens the hub, and batch-creates artboard skeletons (shimmer cards appear immediately)
6. **Phase B: Agents** — spawns one agent per artboard in parallel; each writes HTML via `curl` to the HTTP API, and thumbnails appear progressively on the hub

## Directory structure

```text
extract-design-system/
├── SKILL.md                        # Core instructions and hub-centric build process
├── references/
│   ├── agent-prompt.md             # Prompt template and curl instructions for subagents
│   └── artboard-guidelines.md      # Standard artboard structure and content guidelines
└── templates/
    └── design-spec.md              # Design spec template passed to every agent
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill extract-design-system
```
