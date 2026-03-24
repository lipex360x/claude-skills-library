# update-skill

> Scoped edits to existing Claude Code skills — reads skill-meta.json for instant context, modifies only affected sections, runs scoped content audit, and verifies skeleton compliance after every edit.

Surgical edits to existing skills with minimal blast radius. Loads instant context via `skill-meta.json`, applies changes only to affected sections, and runs scoped review (not full audit) to keep the feedback loop fast. The counterpart to `/create-skill` for editing rather than creating.

## Usage

```text
/update-skill <skill-name> [change description]
```

> [!TIP]
> Also activates when you say "update skill", "edit skill", "fix skill", "modify skill", "change this skill", "improve skill", "ajusta a skill", or want to modify an existing skill.

## How it works

1. **Load context** — Reads `skill-meta.json` for instant context (line count, section states, references); falls back to manual SKILL.md discovery if missing
2. **Parse change request** — Identifies which skeleton sections are affected by the requested change
3. **Capture before-state** — Records section metrics (line count, item count) for diff-based reporting
4. **Apply scoped changes** — Modifies only affected sections, leaving everything else untouched
5. **Verify skeleton compliance** — Confirms all 13 sections remain present with canonical names in correct order
6. **Run scoped content audit** — Audits only modified sections plus always-check categories (skeleton compliance, progressive disclosure)
7. **Run scoped review checklist** — Validates affected categories and presents results as a markdown table
8. **Update skill-meta.json** — Refreshes metadata fields (lastModified, lineCount, skeleton, references) or generates from scratch
9. **Report** — Shows before/after metrics, scoped review results, and any issues

## Directory structure

```text
update-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── review-checklist.md       # Validation checklist (self-contained copy)
    ├── scoped-audit-mapping.md   # Section → checklist category mapping
    ├── skeleton-template.md      # Canonical 13-section skeleton (self-contained copy)
    └── skill-meta-spec.md        # skill-meta.json schema specification
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill update-skill
```
