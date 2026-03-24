# audit-skill

> Evaluate existing skills against the quality review checklist and produce structured audit reports.

Read-only quality assessment that scores skills against the `/create-skill` review checklist at runtime (never hardcoded), producing machine-consumable reports with pass/fail/partial grades per category. Supports 3 audit scopes (single skill, full plugin, entire library) and groups fix recommendations by type across all audited skills for batch remediation. Always excludes `create-skill`, `plan-skill`, and `audit-skill` themselves from audit scope.

## Usage

```text
/audit-skill <target>
```

> [!TIP]
> Also activates when you say "audit this skill", "review skill quality", "check skill health", "audita a skill X", "como está a skill Y", or want to assess skill compliance.

### Examples

```text
/audit-skill push          # audit a single skill by name
/audit-skill workflow      # audit all skills in a plugin
/audit-skill all           # audit entire library (parallel agents per plugin)
/audit-skill               # interactive selection via prompt
```

## How it works

1. **Resolve target** — Parses the argument as a skill name, plugin name, or `"all"`. Validates against known skills/plugins with fuzzy matching on typos. Presents AUQ with plugin-level options to avoid overloading the prompt with 30+ individual skills
2. **Load review checklist** — Reads the current checklist from `/create-skill` at runtime, ensuring audits always use the latest standards
3. **Evaluate skill** — Reads SKILL.md, references/, templates/, and README.md. Evaluates against 7 checklist categories (Description, SKILL.md body, Quality, Testing, Subagents, Structure, Compliance) with pass/fail/partial/N/A status
4. **Produce per-skill report** — Generates a structured report with scores, findings citing line numbers, and priority fixes. Saves to `<plugin>/skills/<name>/audit-report.md`
5. **Batch mode** — For plugin or library-wide audits, evaluates multiple skills (parallel agents for `all` mode) and collects results
6. **Produce consolidated report** — Groups fix batches by type across all audited skills. Saves to `skills-library/audit-report-<date>.md`
7. **Report** — Presents scores, top fixes, fix batches, and next steps

## Directory structure

```text
audit-skill/
├── SKILL.md                          # Core skill instructions
├── README.md                         # This file
├── skill-meta.json                   # Skill metadata
├── references/                       # (reserved for future use)
└── templates/
    ├── per-skill-report.md           # Report template for individual skill audits
    └── consolidated-report.md        # Summary template for batch/library-wide audits
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill audit-skill
```
