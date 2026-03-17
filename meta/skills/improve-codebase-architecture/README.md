# /improve-codebase-architecture

Explore a codebase for architectural friction and propose deep-module refactors as GitHub issue RFCs.

## Triggers

- `/improve-codebase-architecture`
- "improve architecture", "refactor modules", "make code agent-friendly"
- "deep modules", "module boundaries", "codebase review"

## How it works

1. **Explore** — navigates the codebase organically, surfacing friction (shallow modules, file scatter, tight coupling)
2. **Present candidates** — numbered list of deepening opportunities with effort estimates
3. **Frame the problem** — constraints and illustrative sketch for the chosen candidate
4. **Design interfaces** — spawns 3 parallel agents with different design constraints (minimalist, flexible, ergonomic)
5. **Compare and recommend** — presents designs with trade-offs, gives an opinionated recommendation
6. **Create RFC issue** — GitHub issue with interface, migration plan, and verification criteria

## Usage

```bash
/improve-codebase-architecture
```

Run weekly or after development surges to consolidate accidental complexity.

## Directory structure

```
improve-codebase-architecture/
├── SKILL.md
├── README.md
└── references/
    ├── dependency-categories.md    # Four dependency types and refactoring strategies
    └── rfc-template.md             # GitHub issue format for refactor RFCs
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill improve-codebase-architecture
```
