# audit-skill

> Evaluate existing skills against the quality review checklist and produce structured audit reports.

Read-only skill that assesses one or more skills against the review checklist from `/create-skill`, producing machine-consumable reports with scores, findings, and prioritized fixes. Never modifies audited skills — reports are the input artifact for `/create-skill` to apply fixes.

## Usage

```text
/audit-skill push          # audit a single skill
/audit-skill workflow      # audit all skills in a plugin
/audit-skill all           # audit entire library (parallel agents)
/audit-skill               # interactive selection via prompt
```

> [!TIP]
> Also activates when you say "audit this skill", "review skill quality", "check skill health", "audita a skill X", "como está a skill Y", or want to assess skill compliance.

## How it works

1. **Resolve target** — Parses the argument as a skill name, plugin name, or `"all"`. Validates against known skills and plugins. If no argument, presents an interactive selection
2. **Load review checklist** — Reads the current checklist from `/create-skill` at runtime (never hardcoded), ensuring audits always use the latest standards
3. **Evaluate** — For each skill, reads SKILL.md, references/, templates/, and README.md. Evaluates against every checklist category (Description, SKILL.md body, Quality, Testing, Subagents, Structure, Compliance)
4. **Produce report** — Generates a structured per-skill report with pass/fail table, score, priority fixes, and recommended action. Saves to `<plugin>/skills/<name>/audit-report.md`
5. **Consolidated report** — (batch mode only) Produces a summary table with fix batches grouped by type. Saves to `skills-library/audit-report-<date>.md`

## Directory structure

```text
audit-skill/
├── SKILL.md                          # Core instructions for the audit process
├── README.md                         # This file
├── references/                       # (reserved for future detailed guides)
└── templates/
    ├── per-skill-report.md           # Structured report template for individual skills
    └── consolidated-report.md        # Summary template for batch audits
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill audit-skill
```
