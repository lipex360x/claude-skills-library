# create-readme

Generate or review README.md files that are appealing, informative, and easy to read — automatically switching between creation and review mode based on whether a README already exists.

## Trigger phrases

- "create a readme" / "generate readme"
- "review the readme" / "improve the readme" / "update the readme"
- Also activates when the user wants documentation for a repository — even without explicitly saying "readme"

## How it works

1. **Detect mode** — Checks if `README.md` exists in the project root. If missing, enters create mode; if found, enters review mode
2. **Create mode** — Scans the project (package.json, source structure, config files, CI/CD, tests), fetches reference READMEs for tone inspiration, drafts the README, and presents it for approval before writing
3. **Review mode** — Analyzes the existing README against formatting standards and reference patterns, then presents a numbered list of specific improvements without rewriting — the user chooses what to apply

> [!TIP]
> In review mode, the skill preserves all domain-specific content. It focuses on formatting, structure, and content gaps — never removes what you built intentionally.

## Formatting standards

The skill enforces these rules in both modes:

| Rule | Detail |
|------|--------|
| GFM | GitHub Flavored Markdown for all formatting |
| Admonitions | `[!NOTE]`, `[!TIP]`, `[!WARNING]` etc. where they add clarity — not decoration |
| Emoji restraint | One or two in the title at most; no emoji-heavy headers |
| Navigation | Content index and back-to-top links for READMEs over 100 lines |
| Scannable layout | Tables over prose, code blocks with syntax highlighting, short paragraphs |
| No boilerplate sections | LICENSE, CONTRIBUTING, CHANGELOG belong in dedicated files |

## Usage

```
/create-readme
```

Run from any project root. The skill detects whether a README exists and picks the right mode automatically.

## Directory structure

```
create-readme/
├── SKILL.md                          # Core instructions and formatting rules
└── references/
    └── readme-references.md          # Curated list of reference READMEs for inspiration
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-readme
```
