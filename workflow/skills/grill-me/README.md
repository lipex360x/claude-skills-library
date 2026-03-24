# grill-me

> Deep structured interview about a plan, feature, or project — extracts decisions, constraints, and context to generate PRD input.

Conducts a relentless, structured interview that extracts every decision, constraint, and context needed to generate a complete PRD. Works for both greenfield projects (no codebase) and features in existing codebases.

## Usage

```text
/grill-me
```

> [!TIP]
> Also activates when you say "grill me", "me entrevista", "quero detalhar isso", "vamos aprofundar", "let's flesh this out", "stress-test this idea", or want to think through a plan deeply.

## How it works

1. **Choose interview language** — Detect or ask which language to conduct the interview in
2. **Capture the starting point** — Collect the initial idea or description
3. **Detect context — existing codebase or greenfield** — Scan for project files to adapt questions
4. **Conduct the interview by branches** — Walk through structured question branches covering goals, audience, constraints, and more
5. **Alignment checkpoint** — Summarize findings and confirm understanding
6. **Generate the input document** — Produce the structured PRD input file at `.claude/grill-output.md`
7. **Report** — Summary with output file path and key decisions captured

## Directory structure

```text
grill-me/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── interview-branches.md  # Question branches for the interview
└── templates/
    └── grill-output.md        # Output document template
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill grill-me
```
