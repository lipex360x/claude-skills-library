# deploy-vercel

> Deploy, manage, and develop projects on Vercel from the command line.

Reference-driven Vercel CLI skill covering 16 task domains — deployment, environment variables, domains/DNS, CI/CD automation, local development, monorepos, storage, integrations, and more. Routes each request through a decision tree to the correct reference file, enforces preview-before-production gating, and catches the most common CLI pitfall: wrong project link type in monorepos.

## Usage

```text
/deploy-vercel
```

> [!TIP]
> Also activates when you say "deploy to Vercel", "configure domains", "set up environment variables", "manage CI/CD", "run local dev", or "troubleshoot deployment issues."

### Examples

```text
/deploy-vercel                    # describe the task and the skill routes to the right reference
```

Also triggered by natural language:

```text
"deploy this to production"       # triggers deployment flow with preview gate
"add env vars for staging"        # routes to environment variable reference
"set up a custom domain"          # routes to domains and DNS reference
```

> [!NOTE]
> Requires a Vercel account and the `vercel` CLI installed globally. Run `npm i -g vercel` and `vercel login` if not set up. The project must be linked via `vercel link` (single project) or `vercel link --repo` (monorepo).

## How it works

1. **Identify task and verify linking** — Determines the task type and checks that the project is correctly linked via `.vercel/`
2. **Read the relevant reference and execute** — Routes to the correct `references/<topic>.md` file and runs the appropriate CLI commands
3. **Verify the result** — Confirms success based on task type (URL accessible, env vars listed, domain valid, etc.)
4. **Report** — Presents a structured summary with task, status, URL, environment, and team info

[↑ Back to top](#deploy-vercel)

## Directory structure

```text
deploy-vercel/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── command/
│   └── vercel.md         # Slash command entry point for /vercel alias
└── references/           # 16 topic-specific reference files
    ├── advanced.md               # API routes, webhooks, and advanced CLI usage
    ├── bun.md                    # Bun runtime configuration and deployment
    ├── ci-automation.md          # CI/CD pipeline setup with VERCEL_TOKEN
    ├── deployment.md             # Preview and production deployment commands
    ├── domains-and-dns.md        # Custom domain and DNS configuration
    ├── environment-variables.md  # Env var scoping, pull, and management
    ├── flags.md                  # Feature flags (LaunchDarkly-style)
    ├── getting-started.md        # First-time install, login, and project setup
    ├── global-options.md         # Global CLI flags (--token, --scope, --debug)
    ├── integrations.md           # Marketplace and third-party integrations
    ├── local-development.md      # vercel dev local server setup
    ├── monitoring-and-debugging.md # Logs, inspect, and preview debugging
    ├── monorepos.md              # Multi-project repo linking and deployment
    ├── node-backends.md          # Node.js serverless and edge function config
    ├── projects-and-teams.md     # Project and team management commands
    └── storage.md                # Blob and KV storage operations
```

[↑ Back to top](#deploy-vercel)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill deploy-vercel
```
