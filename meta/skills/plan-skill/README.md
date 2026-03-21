# plan-skill

> Plan and spec out a Claude Code skill from raw input — producing a structured spec file that `/create-skill` consumes directly.

Separates planning from implementation in skill creation. Analyzes raw input (document, conversation, verbal idea) against an 8-category completeness checklist, classifies decisions using a hybrid model (inferred/gap/ask), and produces a self-contained spec file with 90% of decisions pre-made.

## Usage

```text
/plan-skill                          # uses conversation context
/plan-skill my-skill-name            # skill name hint + conversation
/plan-skill path/to/input.md         # reads file as primary input
```

> [!TIP]
> Also activates when you say "plan a skill", "spec for a skill", "structure this idea into a skill", "prepare input for create-skill", or describe a skill idea you want to formalize.

## How it works

1. **Parse input** — Detects file path, conversation context, or verbal description. Validates at least one input source
2. **Run completeness checklist** — 8 categories (external deps, cross-skill state, input ambiguity, resource cost, idempotency, error surface, guardrails, VCS impact), 39 questions total
3. **Present decisions** — Inferred decisions shown for review, architectural choices via AskUserQuestion, gaps flagged as non-blocking
4. **Self-containment check** — Ensures spec is readable by a fresh session with zero prior context
5. **CLAUDE.md compliance check** — Validates naming conventions, plugin structure, and global rules
6. **Generate spec** — Writes complete spec to `downloads/<skill-name>-spec.md`

## Output

Produces a structured spec file with sections: Meta, Purpose, Trigger, Input Contract, Workflow (with failure paths), Output Contract, Dependencies, Cross-Skill State, Guardrails, and Decisions Log.

The spec is consumed by `/create-skill`, which detects it automatically and skips redundant intent questions.

## Directory structure

```text
plan-skill/
├── SKILL.md                              # Main skill instructions (210 lines)
├── README.md                             # This file
├── references/
│   ├── completeness-checklist.md         # 8-category, 39-question analysis framework
│   └── decision-model.md                 # Hybrid classification rules (inferred/gap/ask)
└── templates/
    └── spec-template.md                  # Output format with 10 sections
```

## Install

```bash
npx @anthropic-ai/claude-code-skills install lipex360x/claude-skills-library/meta/skills/plan-skill -a claude-code
```
