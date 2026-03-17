# readme-blueprint-generator

Intelligent README.md generation prompt that analyzes project documentation structure — scanning `.github/copilot` directory files and `copilot-instructions.md` — to create comprehensive repository documentation.

## Trigger phrases

- `generate readme from copilot docs`
- `create readme from .github/copilot`
- Also activates when the user wants to generate a README based on existing Copilot documentation files

## How it works

1. **Scan documentation** — Reads all files in `.github/copilot/` (Architecture, Coding Standards, Technology Stack, Unit Tests, Workflow Analysis, etc.) and `.github/copilot-instructions.md`
2. **Extract project info** — Identifies project name, purpose, tech stack, architecture, folder structure, and development workflow from the scanned files
3. **Generate README** — Produces a well-structured README.md with proper formatting, cross-references, and developer-focused content

## Generated sections

| Section | Source |
|---------|--------|
| Project Name & Description | Extracted from documentation context |
| Technology Stack | `Technology_Stack` file |
| Project Architecture | `Architecture` file |
| Getting Started | Inferred from tech stack |
| Project Structure | `Project_Folder_Structure` file |
| Key Features | Aggregated from all docs |
| Development Workflow | `Workflow_Analysis` file |
| Coding Standards | `Coding_Standards` file |
| Testing | `Unit_Tests` file |

> [!NOTE]
> The generated README focuses on what new developers or users need to know. It includes proper Markdown formatting with clear headings, code blocks, lists, links to other docs, and badges when information is available.

## Usage

```
/readme-blueprint-generator
```

Point it at a repository that has `.github/copilot/` documentation files and it will generate a comprehensive README.md from the existing content.

## Directory structure

```
readme-blueprint-generator/
└── SKILL.md    # Core prompt with generation instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill readme-blueprint-generator
```
