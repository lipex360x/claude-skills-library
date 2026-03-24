# capture-analysis

> Capture skill gaps, workflow frictions, and pattern improvements as structured entries in an analysis file.

Records learnings during work sessions as project-agnostic, actionable entries in `analysis.md`. Acts as a feedback buffer between skill users and skill maintainers — each entry identifies the affected skill, the gap, and a concrete proposal for improvement.

## Usage

```text
/capture-analysis <description of what to capture>
/capture-analysis remove <N>
```

> [!TIP]
> Also activates when you say "analisa isso", "estuda isso", "documenta essa melhoria", "adiciona no analysis", "lessons learned", or want to record a finding for future skill updates.

## How it works

1. **Load or create** — Checks for existing `analysis.md` at the project root; creates it with header if missing and adds to `.gitignore`
2. **Parse the input** — Extracts what happened, what's missing, and what should change. Scans existing entries for duplicates before writing
3. **Write entry** — Appends a structured entry with title, affected skill, problem, gap, proposed solution, and impact
4. **Update timestamp** — Updates the session timestamp in the file header
5. **Confirm** — Reports entry number, title, and total count
6. **Remove entry** — (conditional) Removes an entry by number, renumbers remaining entries, deletes file if empty
7. **Report** — Summarizes action taken, entry details, and total count

## Directory structure

```text
capture-analysis/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
└── skill-meta.json       # Skill metadata
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill capture-analysis
```
