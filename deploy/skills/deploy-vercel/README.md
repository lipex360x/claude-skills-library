# deploy-vercel

> Deploy, manage, and develop projects on Vercel from the command line.

A comprehensive Vercel CLI skill that handles deployment, environment variables, domains, CI/CD pipelines, local development, and more. Routes each task through a decision tree to specialized reference files, ensuring best-practice flags and correct project linking every time.

## Usage

```text
/deploy-vercel
```

> [!TIP]
> Also activates when you say "deploy to Vercel", "configure domains", "set up environment variables", "manage CI/CD", "run local dev", or "troubleshoot deployment issues."

## How it works

1. **Identify task and verify linking** — determines the task type and checks that the project is correctly linked via `.vercel/`
2. **Read the relevant reference and execute** — routes to the correct `references/<topic>.md` file and runs the appropriate CLI commands
3. **Verify the result** — confirms success based on task type (URL accessible, env vars listed, domain valid, etc.)
4. **Report** — presents a structured summary with task, status, URL, environment, and team info

## Directory structure

```text
deploy-vercel/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── command/
│   └── vercel.md         # Slash command entry point
└── references/           # 16 topic-specific reference files
    ├── advanced.md
    ├── bun.md
    ├── ci-automation.md
    ├── deployment.md
    ├── domains-and-dns.md
    ├── environment-variables.md
    ├── flags.md
    ├── getting-started.md
    ├── global-options.md
    ├── integrations.md
    ├── local-development.md
    ├── monitoring-and-debugging.md
    ├── monorepos.md
    ├── node-backends.md
    ├── projects-and-teams.md
    └── storage.md
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill deploy-vercel
```
