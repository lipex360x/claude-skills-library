# create-skill

> Guide the user through creating high-quality Claude Code skills — from structuring SKILL.md files to writing effective descriptions, designing progressive disclosure, and launching subagents.

Step-by-step factory for building structurally consistent Claude Code skills. Every output follows the 13-section canonical skeleton, with quality enforced via a review checklist and skeleton compliance gate. Ships with 12 reference documents covering prompt engineering patterns, trigger descriptions, progressive disclosure, subagent coordination, and more.

## Usage

```text
/create-skill [spec-file]
```

> [!TIP]
> Also activates when you say "create a skill", "new skill", "skill quality", "skill best practices", "how to write a skill", or want to build a /command.

### Examples

```text
/create-skill                              # interactive — asks what the skill does
/create-skill downloads/deploy-spec.md     # reads a /plan-skill spec file directly
```

## How it works

1. **Understand the intent** — Detects `/plan-skill` spec files automatically; falls back to interactive questions about what the skill does and when it activates
2. **Design the structure** — Plans the directory layout (SKILL.md, references/, templates/) using progressive disclosure
3. **Write the description** — Crafts trigger descriptions using the "pushy" technique for reliable activation
4. **Write the SKILL.md body** — Follows the 13-section canonical skeleton with imperative form, numbered steps, and explicit output formats
5. **Apply quality techniques** — Craftsmanship repetition, anti-patterns lists, and refinement-over-addition steps
6. **Handle subagents** — If applicable, designs blank-context prompts and coordination with two-phase builds
7. **Verify skeleton compliance and review** — Validates all 13 sections present, then runs the full review checklist
8. **Register and generate metadata** — Creates symlinks (global) and generates skill-meta.json
9. **Test the skill** — Functional test, activation test (3+ trigger phrases), and edge case verification
10. **Update READMEs** — Generates skill README and updates skills-library root README
11. **Update STRUCTURE.md** — Adds the skill entry to the directory index (global only)
12. **Push to GitHub** — Commits and pushes via `/push`
13. **Report** — Shows creation status, audit results, and any errors

[↑ Back to top](#create-skill)

## Directory structure

```text
create-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── anthropic-patterns.md       # Prompt engineering patterns from Anthropic research
│   ├── content-audit-patterns.md   # Content audit criteria and verification guidance
│   ├── description-patterns.md     # Trigger description examples and "pushy" technique
│   ├── error-handling-patterns.md  # Error handling patterns for skills
│   ├── progressive-disclosure.md   # Three-tier architecture for token efficiency
│   ├── quality-techniques.md       # Craftsmanship repetition, anti-patterns, refinement
│   ├── review-checklist.md         # Validation checklist for finalizing skills
│   ├── skeleton-template.md        # Canonical 13-section skeleton template
│   ├── skill-meta-spec.md          # skill-meta.json schema specification
│   ├── spec-contract.md            # Spec-to-step mapping for /plan-skill specs
│   ├── subagent-patterns.md        # Blank-context coordination and two-phase builds
│   └── xml-tag-patterns.md         # XML tag usage patterns for contracts/audits
└── templates/
    └── skill-template.md           # Starter SKILL.md with frontmatter and section stubs
```

[↑ Back to top](#create-skill)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-skill
```
