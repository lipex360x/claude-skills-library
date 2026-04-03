---
name: deploy-vercel
description: >-
  Deploy, manage, and develop projects on Vercel from the command line. Use when
  deploying to Vercel, configuring domains, setting up environment variables,
  managing CI/CD pipelines, running local dev with `vercel dev`, or
  troubleshooting deployment issues — even if they don't explicitly say "Vercel."
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# Vercel CLI Skill

Deploy, manage, and develop projects on the Vercel platform using the `vercel` (or `vc`) CLI. Run `vercel <command> -h` for full flag details on any command.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| Task type | Conversation | yes | One of: deploy, env vars, domain, local dev, CI/CD, debug | AUQ: "What Vercel task do you need?" |
| Project directory | Filesystem | yes | Directory exists and contains `.vercel/` or is linkable | Run `vercel link` to set up |
| Environment | Conversation | no | `preview` or `production` | Default to `preview` |
| Team/scope | Conversation | no | Valid Vercel team | Default to current (`vercel whoami`) |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Deployment | Vercel platform | yes | URL |
| CLI output | stdout | no | Text with status, URL, environment |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Vercel project link | `.vercel/project.json` or `.vercel/repo.json` | R/W | JSON |
| Vercel CLI | `vercel` binary | R | CLI |
| Reference files | `references/*.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which vercel` → if missing: "Vercel CLI required. Install: `npm i -g vercel`" — stop.
2. `.vercel/` exists in project directory → if missing: run `vercel link` (single project) or `vercel link --repo` (monorepo).
3. Correct team confirmed via `vercel whoami` → if wrong team: run `vercel teams switch`.
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Identify task and verify linking

Determine the task type from the user's request and verify the project is linked:

1. Check `.vercel/` exists in the project directory
2. If missing, run `vercel link` (single project) or `vercel link --repo` (monorepo)
3. Confirm the correct team with `vercel whoami`
4. Route to the correct reference file using the decision tree below

**Before proceeding, verify the link type matches the project structure** — `project.json` for single projects, `repo.json` for monorepos with multiple projects. A mismatch causes silent deployment failures because commands target the wrong project.

### 2. Read the relevant reference and execute

Read the reference file for the identified task type, then execute the commands:

- **Deploy** → Read `references/deployment.md`
- **Local development** → Read `references/local-development.md`
- **Environment variables** → Read `references/environment-variables.md`
- **CI/CD automation** → Read `references/ci-automation.md`
- **Domains or DNS** → Read `references/domains-and-dns.md`
- **Projects or teams** → Read `references/projects-and-teams.md`
- **Logs, debugging, or preview deploys** → Read `references/monitoring-and-debugging.md`
- **Blob storage** → Read `references/storage.md`
- **Integrations** → Read `references/integrations.md`
- **Node.js backends** → Read `references/node-backends.md`
- **Monorepos** → Read `references/monorepos.md`
- **Bun runtime** → Read `references/bun.md`
- **Feature flags** → Read `references/flags.md`
- **Advanced (API, webhooks)** → Read `references/advanced.md`
- **Global flags** → Read `references/global-options.md`
- **First-time setup** → Read `references/getting-started.md`

**Quality gate:** before deploying to production, verify a preview deployment works first — a failed production deploy affects real users.

### 3. Verify the result

After execution, confirm success based on the task type:

| Task | Verification |
|------|-------------|
| Deploy (preview) | Deployment URL is accessible, build logs have no warnings |
| Deploy (production) | Production URL responds, env vars loaded |
| Environment variables | `vercel env ls` confirms variable exists |
| Domain | `vercel domains ls` shows `Valid Configuration` |
| Local dev | `vercel dev` serves the app at `localhost:3000` |
| CI/CD | Pipeline config includes `--yes` and uses `VERCEL_TOKEN` |

**If something fails, check linking first** — inspect `.vercel/` contents and verify the team with `vercel whoami`. Linking issues cause most Vercel CLI failures.

### 4. Report

<report>

Present concisely:
- **Task:** what was executed (deploy, env var, domain, etc.)
- **Status:** success or failed with reason
- **URL:** deployment or domain URL, if applicable
- **Environment:** preview or production
- **Team:** team name from `vercel whoami`
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

</report>

## Next action

> _Skipped: "Task-dependent — user decides next steps based on deployment result."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — Vercel CLI installed, project linked, correct team
2. **Link type correct?** — `project.json` for single projects, `repo.json` for monorepos
3. **Preview before production?** — if deploying to production, preview was verified first
4. **Result verified?** — verification step from Step 3 was executed for the task type
5. **Anti-patterns clean?** — no force-deployed to production, no hardcoded tokens

</self_audit>

## Content audit

<content_audit>

> _Skipped: "N/A — skill executes CLI commands, does not generate verifiable content."_

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| `vercel` not installed | Report install command → stop |
| Auth expired | AUQ: "Run `vercel login`" → stop |
| Project not linked | Run `vercel link` or `vercel link --repo` → retry |
| Wrong team | Run `vercel teams switch` → retry |
| Build failure | Show build logs, suggest fix → stop |
| DNS not propagated | Report status, note propagation may take up to 48h |

## Anti-patterns

- **Wrong link type in monorepos.** `vercel link` creates `project.json`, which only tracks one project — because `project.json` causes silent deployment failures when commands target the wrong project in multi-project repos. Use `vercel link --repo` instead.
- **Letting commands auto-link in monorepos.** Many commands implicitly run `vercel link` if `.vercel/` doesn't exist — because this creates `project.json`, which may link to the wrong project.
- **Linking while on the wrong team.** Verify with `vercel whoami` before linking — because the link is scoped to the team and changing teams later doesn't update existing links.
- **Forgetting `--yes` in CI.** Required to skip interactive prompts — because without it the pipeline hangs waiting for input.
- **Using `vercel deploy` after `vercel build` without `--prebuilt`.** The build output is ignored — because the CLI rebuilds from source, wasting the prior build step.
- **Hardcoding tokens in flags.** Use `VERCEL_TOKEN` env var instead of `--token` — because tokens in flags leak into shell history and CI logs.
- **Disabling deployment protection.** Use `vercel curl` to access preview deploys — because disabling protection exposes previews to the public.
- **Skipping preview before production.** Always verify a preview deployment works first — because production failures affect real users and rollback takes time.

## Guidelines

- **Check linking first.** When something fails, inspect `.vercel/` contents and verify the team — because linking issues cause most Vercel CLI failures and are the cheapest thing to check.
- **Preview before production.** Never deploy directly to production without a verified preview — because a failed production deploy affects real users and the rollback window is not instant.
- **Reference-driven execution.** Route to the correct reference file for each task type rather than working from memory — because reference files contain the exact flags, options, and edge cases for each operation.
- **Monorepo awareness.** Always check if the project is part of a monorepo before linking — because the wrong link type is the single most common source of silent Vercel CLI failures.
