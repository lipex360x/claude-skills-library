# grill-me

Deep structured interview that extracts decisions, constraints, and context to generate PRD input. Works for both greenfield projects and features in existing codebases. Multilingual — the user chooses the interview language.

## Triggers

- `/grill-me` or `/grill-me <idea description>`
- "grill me", "me entrevista", "let's flesh this out", "quero detalhar", "stress-test this idea"

## How it works

1. **Choose language** — user picks interview language (PT-BR, English, Spanish)
2. **Detect context** — identifies whether there's an existing codebase or it's greenfield
3. **Interview by branches** — covers 7 axes (problem, audience, behaviors, technical constraints, integrations, scope, priorities) using navigable `AskUserQuestion` options
4. **Alignment checkpoint** — presents executive summary for validation
5. **Generate structured document** — output at `.claude/grill-output.md` ready to feed `/write-a-prd`

## Usage

```
/grill-me
/grill-me I want to build a delivery management app
```

All questions are presented with keyboard-navigable options. The user can always type free text if no option fits.

## Directory structure

```
grill-me/
├── SKILL.md                          # Main instructions
├── README.md                         # This file
├── references/
│   └── interview-branches.md         # Full branch tree and sample questions
└── templates/
    └── grill-output.md               # Output document template
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill grill-me
```
