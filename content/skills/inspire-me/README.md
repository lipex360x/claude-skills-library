# inspire-me

> Guided exploration session to unblock thinking on any topic — career, relationships, creativity, business, health, or any life area.

Helps clarify mental blocks through structured questioning, optional document analysis, and web research. Combines deep exploration across multiple branches with cross-session pattern detection to surface insights and actionable next steps.

## Usage

```text
/inspire-me [brief description of what's blocking you]
```

> [!TIP]
> Also activates when you say "inspire me", "me inspira", "estou travado", "mental block", "can't decide", "preciso clarear a mente", "help me think through this", or "I'm stuck".

## How it works

1. **Check session history** — Reviews previous sessions for pending actions and recurring patterns
2. **Choose session language** — Lets the user pick between English, Português (BR), or another language
3. **Capture the block** — Collects the block description, classifies the domain, and checks energy level
4. **Estimate and negotiate question count** — Presents estimated scope and lets the user adjust depth
5. **Check for auxiliary materials** — Optionally accepts documents for analysis or triggers web research
6. **Conduct the exploration** — Structured questioning across 5-7 branches adapted to the domain and energy level
7. **Synthesis checkpoint** — Surfaces patterns, contradictions, and connections across all answers
8. **Generate the output document** — Creates `inspire-output.md` with insights, action plan, and references
9. **Update session history** — Appends session summary to `inspire-history.md` for cross-session pattern detection
10. **Report** — Summarizes session domain, artifacts created, materials used, and any errors

## Directory structure

```text
inspire-me/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── exploration-branches.md  # Full branch tree with question patterns
└── templates/
    ├── inspire-output.md        # Session output document template
    └── inspire-history-entry.md # History entry format for cross-session memory
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill inspire-me
```
