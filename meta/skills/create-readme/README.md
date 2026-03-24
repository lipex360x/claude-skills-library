# create-readme

> Create or review a README.md for the project.

Dual-mode README tool: generates from scratch in create mode or presents numbered improvement suggestions in review mode. Auto-detects which mode to use based on whether `README.md` exists. Ships with 4 curated reference READMEs covering CLI tools, small utilities, serverless apps, and recipe-style repos for tone and structure inspiration.

## Usage

```text
/create-readme [path | mode]
```

> [!TIP]
> Also activates when you say "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or want documentation for a repository.

### Examples

```text
/create-readme                 # auto-detect mode at project root
/create-readme ./packages/api  # target a specific subdirectory
/create-readme review          # force review mode even if no README exists
```

## How it works

1. **Detect mode** — Checks if `README.md` exists at the target path; enters create mode if missing, review mode if found. Handles edge cases: empty projects, monorepos, binary-only repos
2. **Create mode** — Scans the project (package.json, source structure, config, CI/CD, tests), reads at least 2 reference READMEs matching the project type for structure and tone inspiration, then presents a draft for approval
3. **Review mode** — Analyzes the existing README against formatting standards and reference patterns. Presents numbered findings with category, line number, current state, suggested change, and rationale. Does not rewrite — lets the user choose which improvements to apply
4. **Report** — Shows mode used, target path, references consulted, and action taken

## Directory structure

```text
create-readme/
├── SKILL.md                                    # Core skill instructions
├── README.md                                   # This file
├── skill-meta.json                             # Skill metadata
└── references/
    ├── readme-references.md                    # Curated index of reference READMEs by project type
    ├── run-on-output.md                        # Reference: small utility with inline navigation and admonitions
    ├── serverless-chat-langchainjs.md          # Reference: serverless app with architecture diagrams
    ├── serverless-recipes-javascript.md        # Reference: recipe-style repo with contribution guide
    └── smoke.md                                # Reference: CLI tool with badges, options table, migration guide
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-readme
```
