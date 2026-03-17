# vercel-cli

> Deploy, manage, and develop projects on Vercel from the command line.

A comprehensive Vercel CLI skill that routes tasks through a decision tree to specialized reference files — covering deployment, environment variables, domains, CI/CD, monorepos, storage, integrations, and more.

## Usage

```text
/vercel
```

Describe what you need (e.g., "deploy to production", "add a custom domain", "set up environment variables") and the skill will load the relevant reference, verify project linking, and execute the task.

> [!TIP]
> Also activates when the user says "deploy a project", "set up environment variables", "configure a domain", "start local development", "add a database", "install an integration", or anything related to Vercel infrastructure management.

## How it works

1. **Load skill** — reads the SKILL.md with the full decision tree
2. **Route to reference** — matches the user's intent to the correct `references/<topic>.md` file
3. **Verify project linking** — checks `.vercel/` directory exists and uses the right link type (`project.json` vs `repo.json`)
4. **Execute task** — runs the appropriate Vercel CLI commands with best-practice flags
5. **Summarize** — reports what was done in a structured summary

## Topics covered

| Reference file | Covers |
|----------------|--------|
| `deployment.md` | Preview and production deploys, `--prebuilt`, promote |
| `local-development.md` | `vercel dev`, local server, framework detection |
| `environment-variables.md` | `vercel env` add/pull/rm, `.env` management |
| `ci-automation.md` | CI/CD pipelines, `--yes`, `VERCEL_TOKEN` |
| `domains-and-dns.md` | Custom domains, DNS records, redirects |
| `projects-and-teams.md` | Project settings, team switching, `vercel whoami` |
| `monitoring-and-debugging.md` | Logs, `vercel inspect`, `vercel curl` for previews |
| `storage.md` | Vercel Blob storage |
| `integrations.md` | Databases, third-party services, Marketplace |
| `monorepos.md` | Turborepo, Nx, workspaces, `--repo` linking |
| `node-backends.md` | Express, Hono, and other Node.js backends on Vercel |
| `bun.md` | Bun runtime configuration |
| `flags.md` | Feature flags |
| `advanced.md` | `vercel api`, webhooks, escape hatches |
| `global-options.md` | Global CLI flags (`--token`, `--scope`, `--cwd`) |
| `getting-started.md` | First-time setup, login, linking |

## Directory structure

```text
vercel-cli/
├── SKILL.md              # Core instructions and decision tree
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
npx skills add lipex360x/claude-skills-library --skill vercel-cli
```
