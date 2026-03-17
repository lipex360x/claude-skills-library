# create-readme

> Create or review a README.md for the project.

Generate or review README.md files that are appealing, informative, and easy to read. Automatically detects whether a README already exists and switches between creation and review mode.

## Usage

```text
/create-readme
```

> [!TIP]
> Also activates when you say "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or want documentation for a repository.

## How it works

1. **Detect mode** — Checks if `README.md` exists. If missing, enters create mode; if found, enters review mode
2. **Create mode** — Scans the project (package.json, source structure, config files, CI/CD, tests), fetches reference READMEs for tone inspiration, and presents a draft for approval
3. **Review mode** — Analyzes the existing README against formatting standards and reference patterns, then presents a numbered list of specific improvements — the user chooses what to apply

> [!TIP]
> In review mode, the skill preserves all domain-specific content. It focuses on formatting, structure, and content gaps — never removes what you built intentionally.

## Directory structure

```text
create-readme/
├── SKILL.md                          # Core instructions and formatting rules
└── references/
    └── readme-references.md          # Curated list of reference READMEs for inspiration
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-readme
```
