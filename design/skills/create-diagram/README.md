# Draw.io Skill

AI-powered diagram creation, editing, and replication for [Draw.io](https://www.drawio.com/) — driven by a YAML-first design system with 6 themes, semantic shapes, and academic/engineering guardrails.

[Features](#features) | [Installation](#installation) | [Usage](#usage) | [Themes](#themes) | [Design System](#design-system) | [CLI Reference](#cli-reference)

---

## Features

- **YAML-first workflow** — define diagrams as structured YAML specs; Mermaid and CSV accepted as input formats
- **6 built-in themes** — Tech Blue, Academic (grayscale), Academic Color, Nature, Dark Mode, High Contrast (WCAG AA)
- **Semantic shapes** — automatic shape selection from node type (`service` → rounded rectangle, `database` → cylinder, `decision` → diamond, etc.)
- **Typed connectors** — `primary` (solid), `data` (dashed), `optional` (dotted) for visual hierarchy
- **Academic paper support** — IEEE-style figures, LaTeX/MathJax formulas, grayscale-safe export, publication-ready vector output
- **Stencil library** — AWS, Azure, GCP, and network gear icons for cloud architecture diagrams
- **3-layer validation** — structure, layout, and quality checks with optional `--strict` mode
- **Multiple output formats** — `.drawio` XML and `.svg` export

---

## Installation

### As a Claude Code skill

```bash
npx claude-skills add drawio
```

### Dependencies

Node.js is required for the CLI toolchain. Install script dependencies:

```bash
cd scripts && npm install
```

---

## Usage

The skill routes automatically based on your request:

| Route | When to use |
|-------|-------------|
| **Create** | New diagram from a text description or spec |
| **Edit** | Modify an existing `.drawio` file |
| **Replicate** | Recreate a diagram from an uploaded image or screenshot |

### Quick example

```yaml
meta:
  theme: tech-blue
  layout: horizontal

nodes:
  - id: api
    label: API Gateway
    type: service

  - id: db
    label: User Database
    type: database

edges:
  - from: api
    to: db
    type: data
    label: Query
```

### Fast path vs full path

Simple diagrams (up to ~12 nodes, clear type/theme/layout) skip consultation and render directly. Complex, dense, or academic diagrams go through a full consultation with ASCII draft confirmation before rendering.

> [!TIP]
> Academic keywords like `paper`, `IEEE`, `thesis`, or `figure` in your prompt automatically activate academic-paper mode with grayscale-safe styling and export checks.

---

## Themes

| Theme | Use case |
|-------|----------|
| `tech-blue` | Software architecture, DevOps |
| `academic` | IEEE papers, grayscale print |
| `academic-color` | Research papers, color print/digital |
| `nature` | Environmental, lifecycle diagrams |
| `dark` | Presentations, slides |
| `high-contrast` | WCAG AA accessible, maximum readability |

---

## Design System

All diagrams follow an 8px grid system with consistent spacing tokens:

| Spacing | Value | Usage |
|---------|-------|-------|
| Node margin | 32px | Minimum space between nodes |
| Container padding | 24px | Space inside modules |
| Canvas padding | 32px | Edge to content |

### Semantic shapes

| Type | Shape |
|------|-------|
| `service` | Rounded rectangle |
| `database` | Cylinder |
| `decision` | Diamond |
| `terminal` | Stadium / Pill |
| `queue` | Parallelogram |
| `user` | Ellipse |
| `document` | Document |
| `formula` | Rectangle |

### Workflow profiles

| Profile | Best for |
|---------|----------|
| `default` | Standard diagrams |
| `academic-paper` | IEEE figures, thesis diagrams, paper-ready exports |
| `engineering-review` | Dense architecture and network diagrams |

Full design system documentation: [`references/docs/design-system/`](references/docs/design-system/)

---

## CLI Reference

```
node scripts/cli.js <input> [output] [options]
```

| Option | Description |
|--------|-------------|
| `<input>` | Path to input file, or `-` for stdin |
| `[output]` | Output file (`.drawio` or `.svg`). Omit for stdout |
| `--input-format <f>` | Input format: `yaml` (default), `mermaid`, `csv` |
| `--theme <name>` | Override theme (e.g. `tech-blue`, `academic`) |
| `--strict` | Fail on complexity/quality warnings |
| `--validate` | Run XML validation and print results |

### Examples

```bash
# YAML to .drawio file
node scripts/cli.js diagram.yaml output.drawio --validate

# Mermaid to SVG with academic theme
node scripts/cli.js flow.mmd output.svg --input-format mermaid --theme academic

# Pipe from stdin
cat spec.yaml | node scripts/cli.js - output.drawio --strict
```

---

## Project Structure

```
drawio/
├── SKILL.md                 # Skill definition and routing rules
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
│   ├── dsl/                 # YAML/Mermaid/CSV → draw.io converters
│   ├── adapters/            # Input format adapters
│   ├── math/                # LaTeX/MathJax support
│   └── svg/                 # SVG export module
└── evals/                   # Evaluation prompts and assertions
```

---

## License

See the repository root for license information.

<p align="right"><a href="#drawio-skill">Back to top</a></p>
