# update-skill

> Scoped edits to existing Claude Code skills with skeleton compliance verification.

Surgical edits to existing skills — reads `skill-meta.json` for instant context, modifies only affected sections, runs scoped content audit on changes, and verifies skeleton compliance after every edit. The counterpart to `/create-skill` for editing rather than creating.

## Usage

```text
/update-skill push add an anti-pattern about force-pushing
```

> [!TIP]
> Also activates when you say "edit skill", "fix skill", "modify skill", "change this skill", "improve skill", or want to modify an existing skill.

## How it works

1. **Load context** — Reads `skill-meta.json` for instant context (line count, section states, references). Falls back to manual SKILL.md discovery if meta is missing
2. **Parse change request** — Identifies which skeleton sections are affected by the requested change
3. **Capture before-state** — Records section metrics (line count, item count) for diff-based reporting
4. **Apply scoped changes** — Modifies only affected sections, leaving everything else untouched
5. **Verify skeleton compliance** — Confirms all 13 sections remain present with canonical names
6. **Run scoped audit** — Content audit and review checklist run only on affected categories
7. **Update skill-meta.json** — Refreshes metadata (or generates from scratch if missing)
8. **Report** — Shows before/after diff, review results, and any issues

## Directory structure

```text
update-skill/
├── SKILL.md                          # Core instructions for the update process
├── skill-meta.json                   # Skill metadata for instant context
└── references/
    ├── review-checklist.md           # Validation checklist (self-contained copy)
    ├── scoped-audit-mapping.md       # Section → checklist category mapping
    ├── skeleton-template.md          # Canonical 13-section skeleton (self-contained copy)
    └── skill-meta-spec.md            # skill-meta.json schema (self-contained copy)
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill update-skill
```
