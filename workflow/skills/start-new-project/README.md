# start-new-project

> Plan and scaffold a new project from a prompt.

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates keep the user in control: once after clarifying questions, once after the proposed structure.

## Usage

```text
/start-new-project <project description>
```

> [!TIP]
> Also activates when the user says "new project", "let's build X", "I want to build", "plan a project", "create an issue for X", or provides a project idea wanting structured planning.

## How it works

1. **Parse the prompt** — extracts project name, tech stack hints, scope, and domain
2. **Ask clarifying questions** — 3-5 targeted questions to fill gaps (first approval gate)
3. **Propose the phase structure** — decomposes into Phases and Steps with TDD-ordered checkboxes, file paths, and verification. Splits into multiple issues if 8+ steps (second approval gate)
4. **Repo scaffolding** — creates priority labels (P0-P3), project milestone, and a permanent Backlog milestone
5. **Create GitHub issues** — creates approved issues with labels and milestone assignment
6. **Project board** — creates a GitHub Projects board with 7 status columns (Backlog → Ready → In progress → In review → Ready to PR → Done → Cancelled), Priority, and Size fields
7. **Create feature branch** — `feature/<slug>` from main
8. **Summary** — presents issue URLs, milestone, branch name, and step/checkbox counts

> [!NOTE]
> Supports **Agent Teams** parallel execution plans when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is enabled — analyzes step dependencies and groups independent steps into teammate assignments.

## Directory structure

```text
start-new-project/
├── SKILL.md              # Core instructions
├── references/           # Phase planning guide, CDP best practices
└── templates/            # Issue template, ARCHITECTURE.md, CDP scripts, Chrome launcher
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-new-project
```
