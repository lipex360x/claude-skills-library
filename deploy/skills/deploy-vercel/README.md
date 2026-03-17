# deploy-vercel

> Deploy, manage, and develop projects on Vercel from the command line.

A comprehensive Vercel CLI skill that routes tasks through a decision tree to specialized reference files — covering deployment, local development, environment variables, domains, CI/CD, monorepos, storage, integrations, and more.

## Usage

```text
/deploy-vercel
```

> [!TIP]
> Also activates when saying "deploy to production", "set up environment variables", "configure a domain", "start local development", "add a database", or anything related to Vercel infrastructure management.

## How it works

1. **Route** — matches the user's intent to the correct `references/<topic>.md` file via the decision tree
2. **Verify linking** — checks `.vercel/` directory exists and uses the right link type (`project.json` for single projects, `repo.json` for monorepos)
3. **Execute** — runs the appropriate Vercel CLI commands with best-practice flags
4. **Summarize** — reports what was done in a structured summary

## Topics covered

| Reference | Covers |
|-----------|--------|
| `deployment.md` | Preview and production deploys, `--prebuilt`, promote |
| `local-development.md` | `vercel dev`, local server, framework detection |
| `environment-variables.md` | `vercel env` add/pull/rm, `.env` management |
| `ci-automation.md` | CI/CD pipelines, `--yes`, `VERCEL_TOKEN` |
| `domains-and-dns.md` | Custom domains, DNS records, redirects |
| `projects-and-teams.md` | Project settings, team switching |
| `monitoring-and-debugging.md` | Logs, `vercel inspect`, `vercel curl` for previews |
| `storage.md` | Vercel Blob storage |
| `integrations.md` | Databases, third-party services |
| `monorepos.md` | Turborepo, Nx, workspaces, `--repo` linking |
| `node-backends.md` | Express, Hono, and other Node.js backends |
| `bun.md` | Bun runtime configuration |
| `flags.md` | Feature flags |
| `advanced.md` | `vercel api`, webhooks, escape hatches |

## Directory structure

```text
deploy-vercel/
├── SKILL.md              # Core instructions and decision tree
├── command/
│   └── vercel.md         # Slash command entry point
└── references/           # 16 topic-specific reference files
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill deploy-vercel
```
