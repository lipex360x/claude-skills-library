# plan-skill

> Plan and spec out a Claude Code skill from raw input — a document, conversation, verbal idea, or rough notes.

Separates planning from implementation in skill creation. Analyzes raw input against an 8-category completeness checklist (39 questions), classifies every decision using a hybrid model (inferred/gap/ask), and produces a self-contained spec file that `/create-skill` consumes directly with 90% of decisions pre-made. The spec is designed so a fresh session can build the skill without any prior context.

## Usage

```text
/plan-skill [name-hint | file-path]
```

> [!TIP]
> Also activates when you say "plan a skill", "spec for a skill", "structure this idea into a skill", "prepare input for create-skill", "think through a skill before building it", or describe a skill idea you want to formalize.

### Examples

```text
/plan-skill                          # uses current conversation context as input
/plan-skill my-skill-name            # skill name hint + conversation context
/plan-skill path/to/input.md         # reads file as primary input source
```

## How it works

1. **Parse input** — Detects file path, kebab-case name hint, or conversation context as input sources. Multiple sources can combine (file + conversation)
2. **Run completeness checklist** — Evaluates 8 categories (external deps, cross-skill state, input ambiguity, resource cost, idempotency, error surface, guardrails, VCS impact) with 39 questions. Warns if gap count exceeds 10
3. **Present decisions** — Shows inferred decisions in a table for review, batches architectural questions via AUQ (max 4 per call with concrete options), lists gaps as non-blocking warnings with safe defaults
4. **Self-containment check** — Rewrites opaque references so the spec is readable by a fresh session with zero prior context
5. **CLAUDE.md compliance check** — Validates naming conventions, plugin structure, and global rules
6. **Generate spec** — Writes complete spec to `downloads/<skill-name>-spec.md` with all 10 sections filled
7. **Report** — Shows spec path, decision counts (inferred/gap/ask), and readiness for `/create-skill`

## Directory structure

```text
plan-skill/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── completeness-checklist.md   # 8-category, 39-question analysis framework
│   └── decision-model.md           # Hybrid classification rules (inferred/gap/ask)
└── templates/
    └── spec-template.md            # Output format with 10 sections for /create-skill consumption
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill plan-skill
```
