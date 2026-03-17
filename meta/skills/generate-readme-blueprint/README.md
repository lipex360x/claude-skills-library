# generate-readme-blueprint

> Generate a README.md by analyzing project documentation in `.github/copilot`.

Scans `.github/copilot` directory files and `copilot-instructions.md` to extract project information, then generates a comprehensive README with proper formatting, cross-references, and developer-focused content.

## Usage

```text
/generate-readme-blueprint
```

> [!TIP]
> Also activates when you want to generate a README based on existing Copilot documentation files in `.github/copilot/`.

## How it works

1. **Scan documentation** — Reads all files in `.github/copilot/` (Architecture, Coding Standards, Technology Stack, Unit Tests, Workflow Analysis, etc.) and `copilot-instructions.md`
2. **Extract project info** — Identifies project name, purpose, tech stack, architecture, folder structure, and development workflow
3. **Generate README** — Produces a structured README.md with sections for tech stack, architecture, getting started, project structure, key features, coding standards, testing, and more

> [!NOTE]
> The generated README focuses on what new developers or users need to know. It includes proper Markdown formatting with clear headings, code blocks, lists, and badges when information is available.

## Directory structure

```text
generate-readme-blueprint/
└── SKILL.md              # Core prompt with generation instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill generate-readme-blueprint
```
