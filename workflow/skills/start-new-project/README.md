# start-new-project

> Plan and scaffold a new project from a prompt.

Turns a project idea into a well-structured GitHub issue with phased checkboxes, creates the project board, and sets up the feature branch. Two approval gates keep the user in control: once after clarifying questions, once after the proposed structure.

## Usage

```text
/start-new-project [project description]
```

> [!TIP]
> Also activates when you say "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", or provide a project idea wanting structured planning.

## How it works

1. **Check for grill-me output** — Look for existing `.claude/grill-output.md` from a prior `/grill-me` session
2. **Parse the prompt** — Extract project name, tech stack hints, scope, and domain
3. **Ask clarifying questions** — 3-5 targeted questions to fill gaps (first approval gate)
4. **Propose the phase structure** — Decompose into Phases and Steps with checkboxes (second approval gate)
5. **Repo scaffolding (labels + milestone)** — Create priority labels, project milestone, and Backlog milestone
6. **Create the GitHub issues** — Create approved issues with labels and milestone assignment
7. **Create project board** — Set up a GitHub Projects board with 7 status columns and custom fields
8. **Create the feature branch** — Create `feature/<slug>` from main
9. **Report** — Summary with issue URLs, milestone, branch name, and step counts

## Directory structure

```text
start-new-project/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   ├── anti-patterns.md          # Common mistakes to avoid
│   ├── cdp-best-practices.md     # Chrome DevTools Protocol practices
│   ├── guidelines.md             # Skill-specific guidelines
│   ├── phase-planning-guide.md   # Phase decomposition guide
│   ├── project-board-setup.md    # Board column definitions
│   └── tdd-methodology.md        # Test-driven development methodology
└── templates/
    ├── architecture.md           # ARCHITECTURE.md template
    ├── cdp-run-all.ts            # CDP test runner template
    ├── cdp-test-example.ts       # CDP test example
    ├── issue-template.md         # Issue body template
    ├── project-settings.json     # Project settings template
    └── start-chrome.sh           # Chrome launcher script
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-new-project
```
