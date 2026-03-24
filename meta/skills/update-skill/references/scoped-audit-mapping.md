# Scoped Audit Mapping

Maps each skeleton section to the review checklist categories that must re-run when that section is modified. Use this to avoid full-checklist overhead on scoped edits.

## Section → checklist categories

| Modified section | Re-check categories |
|---|---|
| Frontmatter | Description, Metadata, Compliance |
| Title + Intro | Description |
| Input contract | SKILL.md body |
| Output contract | SKILL.md body |
| External state | SKILL.md body |
| Pre-flight | Quality, Skeleton compliance |
| Steps | SKILL.md body, Quality |
| Next action | _(no category — minimal impact)_ |
| Self-audit | Quality |
| Content audit | Content audit |
| Error handling | Quality |
| Anti-patterns | Quality, SKILL.md body |
| Guidelines | Quality |

## Always re-check

These categories run on **every** edit regardless of which section changed:

- **Skeleton compliance** — sections still present, names canonical, order correct, never-skip sections populated
- **Progressive disclosure** — SKILL.md under 500 lines, no section exceeds ~15 lines, no duplication between SKILL.md and references

## How to use

1. Identify which sections were modified (compare before-state capture)
2. Collect the union of re-check categories from the table above
3. Add the two "always re-check" categories
4. Run only those checklist categories from `references/review-checklist.md`

This scoping reduces audit overhead from 11 categories to typically 3-5, proportional to the change size.
