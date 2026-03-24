# create-readme

> Create or review a README.md for the project.

Generates or reviews README.md files that are appealing, informative, and easy to read. Automatically detects whether a README already exists and switches between creation and review mode — preserving domain-specific content in review mode.

## Usage

```text
/create-readme
```

> [!TIP]
> Also activates when you say "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or want documentation for a repository.

## How it works

1. **Detect mode** — Checks if `README.md` exists at the target path; enters create mode if missing, review mode if found
2. **Create mode** — Scans the project (package.json, source structure, config, CI/CD, tests), reads reference READMEs for tone inspiration, and presents a draft for approval
3. **Review mode** — Analyzes the existing README against formatting standards and reference patterns, presents numbered improvement suggestions for the user to choose
4. **Report** — Shows mode used, target path, references consulted, and action taken

## Directory structure

```text
create-readme/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── readme-references.md              # Curated list of reference READMEs
    ├── run-on-output.md                  # Reference README sample
    ├── serverless-chat-langchainjs.md    # Reference README sample
    ├── serverless-recipes-javascript.md  # Reference README sample
    └── smoke.md                          # Reference README sample
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-readme
```
