# capture-analysis

> Capture skill gaps, workflow frictions, and pattern improvements as structured entries in an analysis file.

Records learnings during work sessions as project-agnostic, actionable entries in `analysis.md`. This file acts as a feedback buffer between skill users and skill maintainers — consistent format in, reliable implementation out.

## Usage

```text
/capture-analysis
/capture-analysis remove <N>
```

> [!TIP]
> Also activates when you say "analisa isso", "estuda isso", "documenta essa melhoria", "adiciona no analysis", "lessons learned", or want to record a finding for future skill updates.

## How it works

1. **Load or create** — Checks for `analysis.md` at the project root. Creates it (and adds to `.gitignore`) if missing
2. **Parse the input** — Extracts what happened, what's missing, and what should change. Deduplicates against existing entries
3. **Write entry** — Appends a structured entry with problem, gap, proposed solution, and impact sections
4. **Confirm** — Reports the entry number, title, and total count

Supports removing entries with `remove <N>`, which renumbers remaining entries and deletes the file if empty.

## Directory structure

```text
capture-analysis/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-analysis
```
