---
name: review
description: >-
  Quality gate: 3 QA sub-agents in parallel (static, semantic, runtime), merge
  into checklist report, manage fix cycles. Use when the user says "review",
  "quality check", "run review", "check quality" — even if they don't
  explicitly say "review."
model: opus
effort: high
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - Write
  - Edit
---

# /review

Spawn 3 QA sub-agents in parallel to perform static, semantic, and runtime quality checks on all files changed since the base branch. Merge results into a single quality report, post as a GitHub issue comment, and manage up to 3 fix-and-re-review cycles.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise.

## Pre-flight

1. `which gh` — if missing: "GitHub CLI required. Install: https://cli.github.com/" — stop.
2. `gh auth status` — if not authenticated: "Run `gh auth login` first." — stop.
3. Current directory is a git repo — if not: "Must run inside a git repo." — stop.
4. **Non-empty diff.** Detect the base branch (`main` or `master` — check which exists). `git diff <base-branch>..HEAD --name-only` must return at least one file. If empty: "No changes to review — nothing to do." — stop.
5. **Detect issue number.** Parse current branch name (`feat/<N>-*`). If not on a feature branch, ask the user with `AskUserQuestion`.
6. **Parse flags.**
   - `--final` — delta-only review: scope to files changed since `last_review_commit_sha` in `.claude/review-state.json`. Only static + semantic (no runtime). Single cycle, no iteration. If no state file or no prior review SHA: "No prior review found — run `/review` without `--final` first." — stop.
   - `--step N` — scope review to files touched by a specific step (cross-reference with `.docs/issues/<N>.md` checkboxes).
   - `--rerun static|semantic|runtime` — re-run a single failed sub-agent from the previous cycle.
7. **Read review state.** If `.claude/review-state.json` exists, read it. Validate `schema_version` is `1`. If corrupt or schema mismatch, warn and start fresh (cycle 1). Extract current `cycle` number. If cycle >= 3 and not `--final`, warn: "Max cycles reached — remaining items become warnings."
8. **Detect quality gate tier.** Read `references/tiered-degradation.md` for the full contract. Probe the project for available resources:
   - **Minimum** (always): git repo with branch — enables changed file scoping.
   - **Basic**: `.docs/quality.md` exists — enables semantic review.
   - **Standard**: `quality-audit.config.json` + `quality-audit.py` exist (search `.claude/scripts/` and project root) — enables static analysis.
   - **Full**: docker-compose + `scripts/dev-start.sh` (or equivalent) + test runner + Playwright config — enables runtime validation.
   - **Custom**: `.claude/review-config.json` exists — overrides default paths, commands, thresholds, cycle limits.
9. **Read context documents.** Read whichever exist (do NOT fail if missing):
   - `.docs/quality.md` — quality rules for semantic review.
   - `.docs/architecture.md` — architecture context for runtime review.
   - `.docs/project.md` — domain context for semantic review.
   - `.claude/review-config.json` — custom config overrides.
10. **Collect changed files.** Detect the base branch (`main` or `master`). `git diff <base-branch>..HEAD --name-only` (or `git diff <last_review_sha>..HEAD --name-only` for `--final`). For `--step N`: cross-reference with `.docs/issues/<N>.md` checkboxes to identify which files belong to that step — only those files are in scope. Store as the file scope for all sub-agents.
11. **Read prior cycle report.** If `.docs/reviews/<issue>-cycle-<N-1>.md` exists, read it. Extract open items to scope re-review. On cycle 2+, sub-agents only re-check: (a) items still `open` from prior cycle, (b) newly changed files since last review SHA.

**Inputs:** `$ARGUMENTS` for flags (`--final`, `--step N`, `--rerun <agent>`). Issue number from branch name.

**Reads:** `.docs/quality.md`, `.docs/architecture.md`, `.docs/project.md`, `.claude/review-state.json`, `.claude/review-config.json`, `.docs/reviews/`, `.docs/issues/<N>.md`.

**Writes:** `.docs/reviews/<issue>-cycle-<N>.md`, `.claude/review-state.json`, GitHub issue comment.

## Steps

### 1. Prepare sub-agent briefings

Read `references/sub-agent-prompts.md` for the full prompt templates.

Build 3 role-based briefing packets. Each sub-agent receives ONLY the context it needs — never send all docs to all agents.

| Sub-agent | Model | Context packet | Approximate tokens |
|-----------|-------|---------------|-------------------|
| **QA-static** | sonnet* | quality-audit config path + lint/type-check commands + changed file list | ~400 |
| **QA-semantic** | opus* | `.docs/project.md` content + `.docs/quality.md` content + changed file contents | ~900 + file contents |
| **QA-runtime** | sonnet* | `.docs/architecture.md` scripts/config section + test commands + port info | ~600 |

*Model column is aspirational — pass `model: "sonnet"` or `model: "opus"` in the Agent tool call, but sub-agents may inherit the session model if override is not supported. Design briefings assuming the target model's capabilities regardless.

For `--final`: skip QA-runtime entirely (only static + semantic).
For `--rerun <agent>`: build only the specified agent's briefing.

Each briefing includes:
- The role preamble ("You are a senior QA Engineer specializing in...")
- Inline context (NOT "go read file X" — inline the content)
- The list of changed files to review
- On cycle 2+: the open items from the prior report that this agent owns
- Output format instruction: wrap results in `<review-result>...</review-result>` XML tags with structured items

**Read-only enforcement:**
- QA-static: use `--check` flags only (lint --check, format --check, type-check). No auto-fix.
- QA-semantic: allowed tools are Read, Grep, Glob only. No Bash, no Write.
- QA-runtime: "Do NOT modify files, restart services beyond what's needed for testing, or run git write operations."

### 2. Spawn sub-agents

Spawn all applicable sub-agents in a **single message** using the `Agent` tool with `run_in_background: true`. This runs them in parallel.

```
Agent(prompt=QA_STATIC_BRIEFING, run_in_background=true)
Agent(prompt=QA_SEMANTIC_BRIEFING, run_in_background=true)
Agent(prompt=QA_RUNTIME_BRIEFING, run_in_background=true)
```

**Before spawning:** set `"skill-active": false` in `.claude/project-setup.json` to prevent the stop-hook from blocking during the background wait. Re-enable when merging results.

**Port conflict handling (QA-runtime only):** The runtime briefing must include: "Before starting the stack, check if ports are in use (`lsof -i :<port>`). If the app is already running, reuse it — do not restart. If `.claude/review-config.json` has `dev_already_running: true`, skip stack startup entirely."

**Timeout expectations:** static ~2 min, semantic ~3 min, runtime ~5 min. If a sub-agent does not return, proceed with partial results.

### 3. Merge reports

Re-enable `"skill-active": true` in `.claude/project-setup.json`.

As each sub-agent completes, parse its `<review-result>` XML output. Extract structured items with: `id`, `rule`, `file`, `line`, `status` (FAIL/WARN/PASS), `detail`, `reasoning` (semantic only).

**Intermediate state writes.** After parsing each sub-agent's results, immediately append them to `.claude/review-state.json` (update the `items` array and `skipped_agents`). This protects against context compaction — if the session compacts mid-review, the coordinator can recover from the state file instead of losing completed sub-agent results.

Read `references/quality-report-format.md` for the report template.

**Merge logic:**
1. Group items by section: Static analysis, Semantic review, Runtime validation.
2. Assign sequential IDs: `S1, S2...` (static), `Q1, Q2...` (semantic), `R1, R2...` (runtime).
3. Generate **Action items** checklist: one checkbox per FAIL item, warnings listed separately.
4. If a sub-agent failed or timed out: add a `SKIPPED` section with the agent name and reason. Do NOT block the report.
5. Count totals: errors, warnings, suppressed (justified items from prior cycles).

**Partial results handling:** If only 1 or 2 sub-agents return, post the report with available data. The SKIPPED section tells the developer what's missing and how to re-run (`/review --rerun <agent>`).

### 4. Write report and update state

**Write the report file first (local-first):** `.docs/reviews/<issue>-cycle-<N>.md` using the format from `references/quality-report-format.md`. The local file is the source of truth — git history is the backup.

**Then post as GitHub issue comment.** Always create a NEW comment — never edit a previous one (immutable audit trail). Post from the local file:

```bash
gh issue comment <number> --body "$(cat .docs/reviews/<issue>-cycle-<N>.md)"
```

If the post fails, the local report still exists — warn the user to post manually or let `/push` sync it later.

**Update `.claude/review-state.json`:**

Read `references/review-state-schema.md` for the full schema.

```json
{
  "schema_version": 1,
  "session_id": "<current-session-id>",
  "issue": <number>,
  "cycle": <N>,
  "last_review_commit_sha": "<HEAD SHA at review completion>",
  "items": [
    { "id": "S1", "rule": "...", "file": "...", "status": "open", "agent": "static" },
    { "id": "Q1", "rule": "...", "file": "...", "status": "open", "agent": "semantic" }
  ],
  "skipped_agents": []
}
```

Store the HEAD commit SHA (not timestamp) for future delta scoping.

### 5. Present results and determine next action

Present a summary table to the user:

| Section | Errors | Warnings | Skipped |
|---------|--------|----------|---------|
| Static  | N      | N        | -       |
| Semantic| N      | N        | -       |
| Runtime | N      | N        | -       |

**If all pass (zero errors):**
- Report: "Quality review passed. No blocking issues found."
- Next action: suggest `/pw` (if web project with E2E tests) or `/update-docs` (if no UI).

**If errors exist and cycle < 3:**
- Present the action items checklist.
- Instruct: "Fix the items above, then run `/review` again. Cycle <N+1> will only re-check open items and newly changed files."
- **Justification flow:** explain that the developer can justify items via:
  - Reply on the GitHub comment: `justify S3: reason here`
  - Or add to `.claude/review-justifications.json`: `{ "S3": "reason here" }`
  - On re-review, justified items are evaluated. If reasonable: status becomes `justified`. If weak: counter-proposal provided.

**If cycle = 3 with remaining errors:**
- Convert remaining FAIL items to WARN in the report.
- Report: "Max review cycles reached. Remaining items converted to warnings."
- Next action: suggest `/pw` or `/update-docs` with a note about the warnings.

## Error handling

| Failure | Strategy |
|---------|----------|
| `gh` auth expired | AUQ: "Run `gh auth login`" — stop |
| No changes vs main | "No changes to review" — stop |
| `.claude/review-state.json` corrupt | Warn, start fresh cycle 1 |
| Sub-agent timeout (static) | SKIPPED in report, suggest `--rerun static` |
| Sub-agent timeout (semantic) | SKIPPED in report, suggest `--rerun semantic` |
| Sub-agent timeout (runtime) | SKIPPED in report, suggest `--rerun runtime` |
| Docker won't start | QA-runtime posts SKIPPED with error detail |
| Ports in use | QA-runtime reuses running app or reports conflict |
| No `.docs/quality.md` | Semantic review runs with general best-practices fallback (clean code, error handling, no magic numbers, single responsibility). Tier degrades to Minimum but QA-semantic still spawns — see `references/sub-agent-prompts.md` for the fallback prompt |
| No quality-audit scripts | Static review limited to lint + type-check |
| No test runner found | Runtime review skips test execution, checks logs only |
| GitHub comment post fails | Write report to local file, warn user to post manually |
| `--final` without prior review | "No prior review found — run `/review` first" — stop |

## Anti-patterns

- **Sending all docs to all sub-agents** — because QA-static needs ~400 tokens of config, not 2800 tokens of project context. Role-based briefing saves ~4700 tokens/cycle and focuses each agent on its specialty.
- **Editing previous review comments** — because last-write-wins conflicts with developer justification edits. Always post a NEW comment per cycle for an immutable audit trail.
- **Auto-fixing in sub-agents** — because sub-agents are READ-ONLY reviewers. QA-static uses `--check` flags, QA-semantic has no Bash/Write access. The developer fixes; the reviewer reviews.
- **Spawning sub-agents for REVIEW-LITE** — because 2-3 changed files after HUMAN feedback cost ~31k tokens with sub-agents vs ~10k inline. REVIEW-LITE is internal to `/validate`, not part of `/review`.
- **Using timestamps for delta scoping** — because git timestamps are unreliable (amends, rebases, cherry-picks). Use commit SHA from `review-state.json` for deterministic scoping.
- **Failing when a tier is missing** — because projects provide different infrastructure levels. Degrade gracefully: report "static analysis skipped: quality-audit.py not found" instead of erroring.
- **Running runtime review in --final mode** — because `--final` is a lightweight delta pass. Only static + semantic, single cycle. Runtime validation was already done in the full review.

## Next action

- **All pass:** Run `/pw` (web projects with UI changes) or `/update-docs` (backend/infra only), then `/review --final`, then `/open-pr`.
- **Errors found (cycle < 3):** Fix issues, add justifications if needed, then run `/review` again.
- **Max cycles reached:** Proceed to `/pw` or `/update-docs` — remaining items are warnings, not blockers.
