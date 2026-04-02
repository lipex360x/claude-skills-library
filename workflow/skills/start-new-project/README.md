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

## Issue validator rules

The `validate-issue.sh` template is copied to `.claude/scripts/` during Phase 1 scaffolding. It validates issue bodies written by `/start-issue` against structural, sizing, and semantic rules. The `/start-issue` skill runs it automatically after rewriting the issue body.

### Structure (errors)

| Rule | Validation |
|------|------------|
| `## What` section | Required |
| `## Why` section | Required |
| `## Acceptance criteria` | Required, ≥1 checkbox |
| Step count | 2-8 per issue |
| Step numbering | Sequential, no gaps or duplicates |
| Step title format | Must use em dash (`—`), not hyphen |

### Sizing

| Rule | Level | Validation |
|------|-------|------------|
| Checkboxes per step | error | Max 8 (hard limit) |
| Checkboxes per step | warning | Recommended ≤6 |
| Checkbox text length | warning | Max 200 chars — break into multiple, never shorten |
| Empty step | error | Must have ≥1 checkbox |

### Checkbox tags

Every checkbox must have a tag: `` `[TAG]` ``. Valid tags and ordering:

```
RED → GREEN → INFRA → WIRE → E2E → PW → HUMAN → DOCS → AUDIT
```

| Rule | Level | Validation |
|------|-------|------------|
| `[GREEN]` requires `[RED]` | error | No GREEN without RED in same step |
| `[E2E]` requires `[PW]` | error | E2E tests need visual verification |
| `[PW]` requires `[HUMAN]` | error | Visual verification needs human approval |
| `[HUMAN]` requires `[PW]` | error | Human approval needs visual verification |
| `[AUDIT]` mandatory | error | Every step must end with AUDIT |
| `[AUDIT]` must be last | error | No tags after AUDIT |
| Frontend UI → full chain | error | UI work requires E2E + PW + HUMAN |
| Tag ordering | warning | Must follow the sequence above |
| `[DOCS]` recommended | warning | Suggested when step has GREEN or WIRE |
| `[E2E]` without `[RED]` | warning | E2E without unit tests is fragile |

### Semantic rules per tag

| Tag | Level | Validation |
|-----|-------|------------|
| `[RED]` | error | Must mention "test" or "spec" |
| `[RED]` after `[RED]` | error | No consecutive RED without GREEN (horizontal TDD) |
| `[GREEN]` before `[RED]` | error | GREEN can't appear before RED |
| `[GREEN]` writes tests | warning | Shouldn't mention writing tests |
| `[E2E]` | error | Must mention test/spec/playwright |
| `[PW]` | warning | Should mention screenshots/verification |
| `[HUMAN]` | warning | Should mention presenting to user/approval |
| `[AUDIT]` | warning | Should mention quality.md |
| `[DOCS]` | warning | Should mention ARCHITECTURE.md |
| `[INFRA]` writes tests | warning | Shouldn't mention writing tests |
| `[WIRE]` | warning | Should mention integration/connection |

### Other

| Rule | Level | Validation |
|------|-------|------------|
| Duplicate checkboxes | error | No duplicate text in same step |
| Empty checkbox text | error | Must have description after tag |
| Last AUDIT mentions quality.md | warning | Final audit should reference quality.md |

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
    ├── start-chrome.sh           # Chrome launcher script for CDP testing
    └── validate-issue.sh         # Issue structure validator (copied to .claude/scripts/)
```

[↑ Back to top](#start-new-project)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-new-project
```
