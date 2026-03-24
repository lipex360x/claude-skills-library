# start-new-project

> Plan and scaffold a new project from a prompt.

Nine-step project scaffolding that turns an idea into a fully tracked GitHub project: asks 3-5 targeted clarifying questions, decomposes work into Phases and Steps with concrete checkboxes (2-4 phases, 3-8 steps each), creates issues with labels and milestone, sets up a project board with 7 status columns and Priority/Size custom fields, and creates the feature branch. Optionally consumes `/grill-me` output to skip clarifying questions. Two approval gates keep the user in control: once after questions, once after the proposed structure. Splits into multiple issues automatically when a phase exceeds 8 steps.

## Usage

```text
/start-new-project [project description]
```

> [!TIP]
> Also activates when you say "start a new project", "new project", "let's build X", "plan a project", "create an issue for X", "I want to build", or provide a project idea wanting structured planning.

### Examples

```text
/start-new-project a CLI tool for managing dotfiles   # start with description
/start-new-project                                     # interactive — prompts for idea
```

Also triggered by natural language:

```text
"let's build a REST API for inventory"    # same effect via model invocation
"I want to build a dashboard"             # same effect via model invocation
```

## How it works

1. **Check for grill-me output** — Look for `.claude/grill-output.md` from a prior `/grill-me` session to use as planning base
2. **Parse the prompt** — Extract project name, tech stack hints, scope, and domain
3. **Ask clarifying questions** — 3-5 targeted questions about platform, stack, scope, key features, and deployment (first approval gate)
4. **Propose the phase structure** — Decompose into Phases and Steps with checkboxes, TDD order enforced, Agent Teams execution mode if enabled (second approval gate)
5. **Repo scaffolding** — Create priority labels (P0/P1/P2), type labels, and optional milestone
6. **Create the GitHub issues** — Create approved issues sequentially with labels and cross-references
7. **Create project board** — Set up GitHub Projects board with 7 columns (Backlog through Cancelled), Priority and Size fields, blocker annotations
8. **Create the feature branch** — Create `feature/<slug>` from main and push upstream
9. **Report** — Summary with issue URLs, board link, branch name, total steps/checkboxes, and priority/size per issue

[↑ Back to top](#start-new-project)

## Directory structure

```text
start-new-project/
├── SKILL.md              # Core skill instructions (9 steps, 2 approval gates)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
├── references/
│   ├── anti-patterns.md          # 9 common mistakes to avoid during planning
│   ├── cdp-best-practices.md     # Chrome DevTools Protocol setup and verification
│   ├── guidelines.md             # 19 skill-specific guidelines and constraints
│   ├── phase-planning-guide.md   # Phase decomposition heuristics and sizing rules
│   ├── project-board-setup.md    # Board column definitions (7 columns) and custom fields
│   └── tdd-methodology.md        # Test-driven development methodology and examples
└── templates/
    ├── architecture.md           # ARCHITECTURE.md starter template for new projects
    ├── cdp-run-all.ts            # CDP test runner script template
    ├── cdp-test-example.ts       # CDP test example with page navigation
    ├── issue-template.md         # Issue body template with Phases/Steps structure
    ├── project-settings.json     # .claude/project-settings.json template with CDP config
    └── start-chrome.sh           # Chrome launcher script for CDP testing
```

[↑ Back to top](#start-new-project)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-new-project
```
