# capture-analysis

> Capture skill gaps, workflow frictions, and pattern improvements as structured entries in an analysis file.

Feedback buffer between skill users and skill maintainers. Each entry follows a 4-part structure (problem, gap, proposed solution, impact) tied to a specific skill and section. Supports both adding and removing entries, auto-manages `.gitignore`, deduplicates against existing entries, and renumbers sequentially on removal.

## Usage

```text
/capture-analysis <description>
```

> [!TIP]
> Also activates when you say "analisa isso", "estuda isso", "documenta essa melhoria", "adiciona no analysis", "lessons learned", or want to record a finding for future skill updates.

### Examples

```text
/capture-analysis the push skill doesn't update issue checkboxes   # add a new entry
/capture-analysis remove 3                                          # remove entry #3 and renumber
/capture-analysis                                                   # prompted for description
```

## How it works

1. **Load or create** — Checks for existing `analysis.md` at the project root; creates it with header if missing and adds to `.gitignore`
2. **Parse the input** — Extracts what happened, what's missing, and what should change. Asks at most one clarifying question if description is too vague. Scans existing entries to update duplicates instead of creating new ones
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
