# audit-skill

> Evaluate existing skills against the quality review checklist and produce structured audit reports.

Read-only skill that assesses one or more skills against the review checklist from `/create-skill`, producing machine-consumable reports with pass/fail scores, specific findings, and prioritized fix batches. Never modifies audited skills — reports feed into `/update-skill` for remediation.

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

1. **Resolve target** — Parses the argument as a skill name, plugin name, or `"all"`. Validates against known skills/plugins with fuzzy matching on typos
2. **Load review checklist** — Reads the current checklist from `/create-skill` at runtime (never hardcoded), ensuring audits always use the latest standards
3. **Evaluate skill** — Reads SKILL.md, references/, templates/, and README.md. Evaluates against every checklist category with pass/fail/partial/N/A status
4. **Produce per-skill report** — Generates a structured report with scores, findings citing line numbers, and priority fixes. Saves to `<plugin>/skills/<name>/audit-report.md`
5. **Batch mode** — For plugin or library-wide audits, evaluates multiple skills (parallel agents for `all` mode) and collects results
6. **Produce consolidated report** — Groups fix batches by type across all audited skills. Saves to `skills-library/audit-report-<date>.md`
7. **Report** — Presents scores, top fixes, fix batches, and next steps

## Directory structure

```text
audit-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/           # (reserved)
└── templates/
    ├── per-skill-report.md       # Report template for individual skills
    └── consolidated-report.md    # Summary template for batch audits
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill audit-skill
```
