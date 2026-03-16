# start-new-project

Turn a project idea into a well-structured GitHub issue with phased checkboxes, then create the feature branch. Two approval gates keep the user in control throughout the planning process.

## Trigger phrases

- "start a new project" / "new project"
- "let's build X" / "I want to build"
- "plan a project" / "create an issue for X"
- Also activates when the user provides a project idea wanting structured planning — even without explicitly saying "new project"

## How it works

1. **Parse the prompt** — Extracts project name, tech stack hints, scope, and domain from the user's input
2. **Ask clarifying questions** — Generates 3-5 targeted questions to fill gaps (platform, stack, scope, key features, deployment). First approval gate
3. **Propose the phase structure** — Decomposes the project into Parts (grouped by theme) and Steps (concrete milestones) with verifiable checkboxes. Second approval gate
4. **Repo scaffolding** — Creates labels (P0-P3, type labels) and milestones as needed, plus a permanent "Backlog" milestone for future ideas
5. **Create GitHub issue** — Creates the issue with the approved structure, applies labels and milestone
6. **Project board** — For 3+ issues, offers to create a GitHub Projects board for visual tracking
7. **Create feature branch** — Checks out from main, creates and pushes `feature/<slug>`
8. **Summary** — Presents issue URLs, milestone, branch name, and total steps/checkboxes count

Supports **Agent Teams** parallel execution plans when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is enabled — analyzes step dependencies and groups independent steps into teammate assignments.

## Usage

```
/start-new-project
```

Provide a project description as context (e.g., "I want to build a CLI tool that converts markdown to PDF") or run bare to be prompted for details.

## Directory structure

```
start-new-project/
├── SKILL.md              # Core instructions
├── references/           # Phase planning and decomposition heuristics
└── templates/            # GitHub issue template
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-new-project
```
