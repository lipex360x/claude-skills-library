# inspire-me

Guided exploration session to unblock thinking on any topic — career, relationships, creativity, business, health, or any life area.

## Trigger phrases

- `/inspire-me`
- "inspire me", "me inspira"
- "estou travado", "I'm stuck", "mental block"
- "preciso clarear a mente", "help me think through this"
- Also activates when the user wants to work through a block — even without explicit keywords

## How it works

1. **Session history** — If previous sessions exist, check on pending actions and detect recurring patterns
2. **Language & context** — Choose session language, describe the block, classify the domain, check energy level
3. **Negotiate scope** — See estimated question count and adjust depth before starting
4. **Gather materials** — Optionally provide documents for analysis or request web research
5. **Deep exploration** — Structured questioning across 5-7 branches adapted to the domain
6. **Synthesis** — Surface patterns, contradictions, and connections across all answers
7. **Output** — Generate `inspire-output.md` with insights, action plan, and all references
8. **History** — Append session summary to `inspire-history.md` for cross-session pattern detection

Every invocation is self-contained — history enhances but never blocks standalone use.

## Usage

```
/inspire-me
/inspire-me I can't decide whether to change careers
/inspire-me estou travado no meu projeto criativo
```

## Directory structure

```
inspire-me/
├── SKILL.md                              # Core instructions
├── README.md                             # This file
├── references/
│   └── exploration-branches.md           # Full branch tree with question patterns
└── templates/
    ├── inspire-output.md                 # Session output document template
    └── inspire-history-entry.md          # History entry format for cross-session memory
```

## Installation

```bash
npx skills add https://github.com/felipebarcelospro/skills-library --skill inspire-me
```
