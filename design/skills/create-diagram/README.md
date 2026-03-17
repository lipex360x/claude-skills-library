# create-diagram

> AI-powered Draw.io diagram creation, editing, and replication with a YAML design system supporting 6 themes.

Create, edit, validate, and export professional Draw.io diagrams through a YAML-first workflow. Supports semantic shapes, typed connectors, academic/IEEE-style figures, cloud architecture stencils, and 3-layer validation. Accepts Mermaid, CSV, and YAML input with `.drawio` and `.svg` output.

## Usage

```text
/create-diagram [diagram-description-or-instruction]
```

> [!TIP]
> Also activates when creating visual diagrams, flowcharts, system architecture diagrams, network diagrams, UML, ER diagrams, sequence diagrams, state machines, org charts, mind maps, cloud infrastructure diagrams, or IEEE-style paper figures.

## How it works

1. **Route** — matches the request to create, edit, replicate, academic-paper, stencil-heavy, or edge-audit workflow
2. **Fast path vs full path** — simple diagrams (up to ~12 nodes, clear type/theme/layout) render directly; complex or academic diagrams go through consultation with ASCII draft confirmation
3. **Normalize** — converts Mermaid or CSV input into canonical YAML spec
4. **Render** — generates `.drawio` XML or `.svg` output using the CLI toolchain
5. **Validate** — runs 3-layer checks (structure, layout, quality) with optional `--strict` mode

## Directory structure

```text
create-diagram/
├── SKILL.md                 # Core instructions and routing rules
├── assets/
│   ├── examples/            # Sample .drawio files
│   ├── schemas/             # JSON Schema for YAML spec
│   └── themes/              # Theme JSON definitions
├── references/
│   ├── docs/                # Design system docs, format guides
│   ├── examples/            # Reusable YAML spec templates
│   └── workflows/           # Step-by-step workflow guides
├── scripts/
│   ├── cli.js               # Main CLI tool
│   ├── dsl/                 # YAML/Mermaid/CSV converters
│   ├── adapters/            # Input format adapters
│   ├── math/                # LaTeX/MathJax support
│   └── svg/                 # SVG export module
└── evals/                   # Evaluation prompts and assertions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-diagram
```
