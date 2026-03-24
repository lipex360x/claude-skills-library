# improve-codebase-architecture

> Explore a codebase for architectural friction, surface shallow modules and coupling issues, and propose deep-module refactors as GitHub issue RFCs.

Organic codebase exploration that surfaces architectural friction — shallow modules, file scatter, tight coupling, and untested areas. Based on John Ousterhout's "A Philosophy of Software Design," it proposes deep-module refactors where a small interface hides large implementation complexity. Spawns 3 parallel agents with different design constraints (minimalist, flexible, ergonomic) to produce radically different interface proposals, then delivers the chosen design as a GitHub issue RFC.

## Usage

```text
/improve-codebase-architecture [focus area]
```

> [!TIP]
> Also activates when you say "improve architecture", "refactor modules", "codebase review", "make code agent-friendly", "deep modules", "module boundaries", "architectural friction", or want to restructure code for better maintainability.

### Examples

```text
/improve-codebase-architecture              # explore entire codebase
/improve-codebase-architecture src/auth     # focus on a specific module
```

> [!NOTE]
> Requires GitHub CLI (`gh`) authenticated for creating the RFC issue. Without `gh`, the RFC is saved as a local markdown file instead. Skips codebases with fewer than 5 source files.

## How it works

1. **Explore the codebase** — Uses Agent/Explore to navigate organically, surfacing friction signals (shallow modules, file scatter, tight coupling, untested areas). Reads ARCHITECTURE.md if present but verifies against actual code
2. **Present candidates** — Lists deepening opportunities with file paths, friction signals, dependency categories, test impact, and effort estimates (S/M/L). User picks via AUQ
3. **Frame the problem space** — Describes constraints and dependencies for the chosen candidate with an illustrative code sketch (not a proposal, just grounding)
4. **Design multiple interfaces** — Spawns 3 parallel agents with different constraints (minimalist: 1-3 entry points, flexible: many use cases, ergonomic: trivial default case) to produce radically different interface designs
5. **User picks an interface** — Presents designs with trade-offs and an opinionated recommendation; user selects via AUQ including a hybrid option
6. **Create GitHub issue RFC** — Creates a refactor issue with problem description, chosen design, migration plan, and verification criteria. Adds to Backlog milestone and applies `refactor` label
7. **Report** — Summarizes areas explored, candidate chosen, design selected, and issue link

## Directory structure

```text
improve-codebase-architecture/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── dependency-categories.md    # Four dependency types and refactoring strategies
    └── rfc-template.md             # GitHub issue format for refactor RFCs
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill improve-codebase-architecture
```
