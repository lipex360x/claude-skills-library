# inspire-me

> Guided exploration session to unblock thinking on any topic — career, relationships, creativity, business, health, or any life area.

Structured facilitation session that combines deep questioning across 5-7 exploration branches, optional document analysis, and web research to surface actionable insights. Adapts intensity to the user's energy level, tracks sessions in a persistent history file for cross-session pattern detection, and produces a comprehensive output document with the core breakthrough, action items, and references. Facilitates insight rather than giving advice.

## Usage

```text
/inspire-me [brief description of what's blocking you]
```

> [!TIP]
> Also activates when you say "inspire me", "me inspira", "estou travado", "mental block", "can't decide", "preciso clarear a mente", "help me think through this", or "I'm stuck".

### Examples

```text
/inspire-me                                  # start an interactive session from scratch
/inspire-me can't decide between two jobs    # jump straight into the block description
/inspire-me creative block on my side project # domain auto-classified as Creative
```

## How it works

1. **Check session history** — Reviews previous sessions for pending actions and recurring patterns (3+ appearances trigger a pattern alert)
2. **Choose session language** — Lets the user pick between English, Portugues (BR), or another language
3. **Capture the block** — Collects the block description, classifies the domain (career, creative, business, relationships, health, learning), and checks energy level to adapt session intensity
4. **Estimate and negotiate question count** — Presents estimated scope with branch names and duration, lets the user adjust depth
5. **Check for auxiliary materials** — Optionally accepts documents for analysis, triggers web research, or both
6. **Conduct the exploration** — Structured questioning across applicable branches with contextual options, max 2 questions per turn, cross-referencing with any provided materials
7. **Synthesis checkpoint** — Surfaces patterns, contradictions, and connections across all answers before generating output
8. **Generate the output document** — Creates `inspire-output.md` with the block, insights, patterns, action items, and all references
9. **Update session history** — Appends session summary to `inspire-history.md`; after 3+ entries, synthesizes a Patterns section
10. **Report** — Summarizes session domain, artifacts created, materials used, and any errors

[↑ Back to top](#inspire-me)

## Directory structure

```text
inspire-me/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── exploration-branches.md  # Full branch tree with domain-specific question patterns
└── templates/
    ├── inspire-output.md        # Session output document template (insights, actions, refs)
    └── inspire-history-entry.md # History entry format for cross-session pattern tracking
```

[↑ Back to top](#inspire-me)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill inspire-me
```
