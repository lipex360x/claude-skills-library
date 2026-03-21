---
name: deploy-vercel
description: Deploy, manage, and develop projects on Vercel from the command line. Use when deploying to Vercel, configuring domains, setting up environment variables, managing CI/CD pipelines, running local dev with `vercel dev`, or troubleshooting deployment issues — even if they don't explicitly say "Vercel."
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# Vercel CLI Skill

Deploy, manage, and develop projects on the Vercel platform using the `vercel` (or `vc`) CLI. Run `vercel <command> -h` for full flag details on any command.

## Input contract

| Input | Required | Description |
|-------|----------|-------------|
| Task type | Yes | What to do: deploy, configure env vars, set up domain, debug, local dev, CI/CD |
| Project directory | Yes | Directory containing the project (must have `.vercel/` or be linkable) |
| Environment | No | `preview` (default) or `production` — only for deploy tasks |
| Team/scope | No | Vercel team — defaults to current (`vercel whoami`) |
| Flags | No | Additional CLI flags (e.g., `--yes`, `--prebuilt`, `--env`) |

## Steps

### 1. Identify task and verify linking

Determine the task type from the user's request and verify the project is linked:

1. Check `.vercel/` exists in the project directory
2. If missing, run `vercel link` (single project) or `vercel link --repo` (monorepo)
3. Confirm the correct team with `vercel whoami`
4. Route to the correct reference file using the Decision Tree below

**Before proceeding, verify the link type matches the project structure** — `project.json` for single projects, `repo.json` for monorepos with multiple projects. A mismatch causes silent deployment failures because commands target the wrong project.

### 2. Read the relevant reference and execute

Read the reference file for the identified task type, then execute the commands:

- **Deploy** → Read `references/deployment.md`
- **Local development** → Read `references/local-development.md`
- **Environment variables** → Read `references/environment-variables.md`
- **CI/CD automation** → Read `references/ci-automation.md`
- **Domains or DNS** → Read `references/domains-and-dns.md`
- **Projects or teams** → Read `references/projects-and-teams.md`
- **Logs, debugging, or accessing preview deploys** → Read `references/monitoring-and-debugging.md`
- **Blob storage** → Read `references/storage.md`
- **Integrations (databases, storage, etc.)** → Read `references/integrations.md`
- **Access a preview deployment** → Use `vercel curl` (see `references/monitoring-and-debugging.md`)
- **CLI doesn't have a command for it** → Use `vercel api` as a fallback (see `references/advanced.md`)
- **Node.js backends (Express, Hono, etc.)** → Read `references/node-backends.md`
- **Monorepos (Turborepo, Nx, workspaces)** → Read `references/monorepos.md`
- **Bun runtime** → Read `references/bun.md`
- **Feature flags** → Read `references/flags.md`
- **Advanced (API, webhooks)** → Read `references/advanced.md`
- **Global flags** → Read `references/global-options.md`
- **First-time setup** → Read `references/getting-started.md`

**Quality gate:** before deploying to production, verify a preview deployment works first. Never skip preview → production because a failed production deploy affects real users.

### 3. Verify the result

After execution, confirm success based on the task type:

| Task | Verification |
|------|-------------|
| Deploy (preview) | Confirm deployment URL is accessible, check build logs for warnings |
| Deploy (production) | Verify production URL responds, confirm environment variables loaded |
| Environment variables | Run `vercel env ls` to confirm the variable exists in the target environment |
| Domain | Run `vercel domains ls` and confirm DNS status shows `Valid Configuration` |
| Local dev | Confirm `vercel dev` serves the app at `localhost:3000` (or configured port) |
| CI/CD | Confirm pipeline config includes `--yes` flag and uses `VERCEL_TOKEN` env var |

**If something fails, check linking first** — inspect `.vercel/` contents and verify the team with `vercel whoami`. Linking issues cause most Vercel CLI failures.

## Output format

Report the result in this structure:

```
**Vercel: [task type]**

- **Status:** [success / failed — reason]
- **URL:** [deployment or domain URL, if applicable]
- **Environment:** [preview / production]
- **Team:** [team name from `vercel whoami`]
- **Notes:** [warnings from build logs, DNS propagation time, etc.]
```

## Project linking

Commands must run from the directory containing `.vercel/` (or a subdirectory). How `.vercel/` gets set up depends on the project structure:

- **`.vercel/project.json`**: Created by `vercel link`. Links a single project. Fine for single-project repos.
- **`.vercel/repo.json`**: Created by `vercel link --repo`. Links a repo with multiple projects. Always use this when any project has a non-root directory (e.g., `apps/web`).

Running from a project subdirectory (e.g., `apps/web/`) skips the "which project?" prompt since it's unambiguous.

## Anti-patterns

- **Wrong link type in monorepos with multiple projects**: `vercel link` creates `project.json`, which only tracks one project. Use `vercel link --repo` instead — `project.json` causes silent deployment failures when commands target the wrong project.
- **Letting commands auto-link in monorepos**: Many commands implicitly run `vercel link` if `.vercel/` doesn't exist. This creates `project.json`, which may be wrong. Run `vercel link` (or `--repo`) explicitly first.
- **Linking while on the wrong team**: Use `vercel whoami` to check, `vercel teams switch` to change.
- **Forgetting `--yes` in CI**: Required to skip interactive prompts — without it the pipeline hangs.
- **Using `vercel deploy` after `vercel build` without `--prebuilt`**: The build output is ignored because the CLI rebuilds from source.
- **Hardcoding tokens in flags**: Use `VERCEL_TOKEN` env var instead of `--token` — tokens in flags leak into shell history and CI logs.
- **Disabling deployment protection**: Use `vercel curl` instead to access preview deploys — disabling protection exposes previews to the public.
- **Skipping preview before production**: Always verify a preview deployment works before promoting to production — production failures affect real users and rollback takes time.
