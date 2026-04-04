# /start-issue Decomposition Spec

Consolidated analysis from 3 planner agents (Workflow Architect, Quality System Designer, Context Strategist).

**Goal:** Break the monolithic /start-issue (420 lines, ~15 decision points) into smaller, focused skills and agents with clear responsibilities.

**Constraint:** Everything must be project-agnostic. Projects provide their own `.docs/quality.md`, quality-audit.config.json, docker-compose, etc. The skills are the ENGINE, not the rules.

---

## 1. The New Workflow Pipeline

```
/start-issue #N
    │
    ├─ Select issue (args or board)
    ├─ Analyze (fetch metadata, .docs/architecture.md, .docs/project.md)
    ├─ Plan (simplified tags, Plan Mode approval)
    ├─ Setup (rewrite issue, branch, board, tasks)
    └─ Report
    
/continue-issue (or manual dev)
    │
    └─ Per step: TDD development (RED → GREEN → INFRA → WIRE → E2E)
         └─ /push after each step

/review
    │
    ├─ 3 sub-agents in parallel:
    │   ├─ static-review  (quality-audit.py --changed, lint, type-check)
    │   ├─ semantic-review (.docs/quality.md rules, LLM judgment)
    │   └─ runtime-review  (docker, tests, logs, browser console)
    ├─ Merge into checklist-based quality report (issue comment)
    └─ Up to 3 cycles: fix → re-review → fix → re-review

/pw (web projects only)
    │
    └─ Run E2E + screenshots, fix visual issues, re-run until clean

/validate (UI changes only)
    │
    ├─ Present testing guide to user
    ├─ Collect feedback
    └─ Fix → REVIEW-LITE → /pw → /validate (loop until approved, max 3 cycles)

/update-docs
    │
    ├─ Update .docs/architecture.md (new routes, patterns, schema, flows)
    └─ Update .docs/project.md if domain concepts changed (rare, flagged for review)

/review --final
    │
    └─ Lightweight delta pass: only files changed after first /review
    
/open-pr → /close-pr
```

### Key design decisions

1. **Each phase is a separate, user-invocable skill.** Nothing is automatic. The "Next action" section of each skill tells the user what to run next. This replaces the current model where /start-issue tries to orchestrate everything inline.

2. **SPAWN is eliminated.** Development happens directly via TDD. Quality review happens as a separate phase AFTER development, not inline during it.

3. **Process gates become phases.** The inline checkbox tags [REVIEW], [PW], [HUMAN], [DOCS], [LOG], [AUDIT] are removed from issue steps and become separate skills invoked after development.

---

## 2. Skill Decomposition

### Skills (user-invocable, /command)

| Skill | Responsibility | Model | Effort | Estimated size |
|-------|---------------|-------|--------|----------------|
| `/start-issue` (refactored) | Select, analyze, plan, setup. Pure planning — no execution, no spawning. | **opus** | high | ~250-280 lines |
| `/review` | Quality gate: spawn 3 sub-agents, merge report, manage fix cycles. | **opus** | high | ~200 lines |
| `/pw` | Playwright visual validation: run E2E, screenshots, fix, re-run. | **opus** | medium | ~120 lines |
| `/validate` | Human validation: testing guide, feedback collection, iteration loop. | **sonnet** | medium | ~100 lines |
| `/update-docs` | Documentation update: .docs/architecture.md + .docs/project.md scoped to git diff. | **sonnet** | medium | ~120 lines |

### Sub-agents (spawned by /review, not user-invocable)

| Agent | Role | Scope | Model | Effort | Tokens | Parallel |
|-------|------|-------|-------|--------|--------|----------|
| `QA-static` | QA Engineer (static) | quality-audit.py --changed, lint, type-check | **sonnet** | medium | ~10k | Yes |
| `QA-semantic` | QA Engineer (semantic) | LLM judgment: semantic_rules + .docs/quality.md DON'Ts | **opus** | high | ~30k | Yes |
| `QA-runtime` | QA Engineer (runtime) | Docker up, tests, logs, browser console | **sonnet** | medium | ~20k | Yes |

### Model selection rationale (see `spec/reference-model-selection.md`)

**Context: Max 5x plan — no monetary cost per token. Cost = context window consumption + quality.**

- **Opus** for /start-issue, /review coordinator, QA-semantic, /pw: deep reasoning needed (plan quality, merging reports, code quality judgment, screenshot diagnosis)
- **Sonnet** for /validate, /update-docs, QA-static, QA-runtime: good execution, sufficient for interactive tasks, content generation, and operational checks
- **Haiku** not used: 200k context is too tight for agents reading multiple files + briefing. No monetary savings on Max plan. Reserve for future micro-tasks (structured parsing, file listing)
- **Development** (TDD phase): inherits session model (Opus on Max plan). No override — the user controls this

**Why 3 sub-agents instead of 1:**
- Token efficiency (60-80k monolithic vs 10-30k each in parallel)
- Failure isolation (docker failing doesn't block regex checks)
- Zero shared state during execution

### What /start-issue loses

| Removed | Reason |
|---------|--------|
| Step 2b (execution strategy) | No more Agent/Teammate/Sequential detection |
| Step 7 (spawn workers) | SPAWN eliminated |
| SPAWN/REVIEW/PW/HUMAN/DOCS/LOG/AUDIT tag logic | Moved to phase skills |
| Progressive audit system | Replaced by explicit /review |
| execution-strategy.md reference | No longer relevant |

### What /start-issue keeps

Pre-flight (9 checks, updated to also read .docs/project.md), Step 1 (select issue), Step 2 (analyze — simplified), Step 3 (plan with 5 tags), Step 4 (update issue), Step 5 (branch), Step 5b (board), Step 6 (tasks), Step 8 (report), Post-flight.

---

## 3. Simplified Tag System

### Tags that REMAIN in issue checkboxes

| Tag | Purpose | Rules |
|-----|---------|-------|
| `[RED]` | Write a failing test | Must mention test/spec |
| `[GREEN]` | Implement to pass the test | Requires [RED] earlier. No consecutive [GREEN] without [RED] |
| `[INFRA]` | Infrastructure/config/tooling | Non-test work |
| `[WIRE]` | Connect layers (frontend ↔ backend) | Must mention integration |
| `[E2E]` | Write Playwright E2E test | Must appear after RED/GREEN pairs |

### Tags REMOVED (moved to phase skills)

| Tag | Moved to | Rationale |
|-----|----------|-----------|
| `[SPAWN]` | **DELETED** | No inline delegation. Dev happens directly. |
| `[REVIEW]` | `/review` skill | Quality review is a phase |
| `[PW]` | `/pw` skill | Visual verification is a phase |
| `[HUMAN]` | `/validate` skill | User validation is a phase |
| `[DOCS]` | `/update-docs` skill | Docs update is a phase |
| `[LOG]` | Absorbed into `/review` | Log check becomes a review item |
| `[AUDIT]` | Absorbed into `/review` | .docs/quality.md audit becomes the core of /review |

### Tag ordering (simplified)

`RED → GREEN → INFRA → WIRE → E2E`

5 tags, one ordering rule, no process gates.

---

## 4. Issue Body Format

### BEFORE (current — 13 checkboxes, 5 work + 8 process gates)

```markdown
## Step 4 — Document ingestion API

- [ ] `[SPAWN]` Delegate RED/GREEN/WIRE — mock embedding calls, use existing EmbeddingService
- [ ] `[RED]` Write test in `backend/tests/test_chunker.py` — expected count, overlap, empty
- [ ] `[GREEN]` Create Chunk value object + chunker in `services/chunker.py`
- [ ] `[RED]` Write test in `backend/tests/test_ingestion.py` — upload Ok, invalid Err, chunks stored
- [ ] `[GREEN]` Create Document entity, DocumentRepository, ChunkRepository, ingestion route
- [ ] `[WIRE]` Integrate Supabase Realtime broadcast for ingestion status updates
- [ ] `[REVIEW]` Review sub-agent output — validate code quality, fix issues
- [ ] `[PW]` Run E2E tests, read screenshots, capture console errors
- [ ] `[HUMAN]` Present screenshots and iterate on user feedback until approved
- [ ] `[DOCS]` Update .docs/architecture.md — ingestion pipeline, document routes
- [ ] `[LOG]` Verify ingestion error paths emit structured logs
- [ ] `[AUDIT]` Audit all Step 4 code against `.docs/quality.md`
```

### AFTER (new — 6 checkboxes, all work)

```markdown
## Step 4 — Document ingestion API

- [ ] `[RED]` Write test in `backend/tests/test_chunker.py` — expected count, overlap, empty
- [ ] `[GREEN]` Create Chunk value object + chunker in `services/chunker.py`
- [ ] `[RED]` Write test in `backend/tests/test_ingestion.py` — upload Ok, invalid Err, chunks stored
- [ ] `[GREEN]` Create Document entity, DocumentRepository, ChunkRepository, ingestion route
- [ ] `[WIRE]` Integrate Supabase Realtime broadcast for ingestion status updates
- [ ] `[E2E]` Write Playwright test for document upload flow
```

### New section at issue bottom

```markdown
## Post-development phases

After all steps are complete, run in order:

1. `/review` — Quality review (static + semantic + runtime)
2. Fix issues from review report, then re-run `/review` if needed
3. `/pw` — Playwright visual verification (web projects)
4. `/validate` — User tests live app, provides feedback (UI changes)
5. `/update-docs` — Update .docs/architecture.md + .docs/project.md
6. `/review --final` — Final quality gate (delta only)
7. `/open-pr` — Create pull request
```

---

## 5. Quality Review System

### The /review skill flow

```
/review triggered (manually or after step completion)
    │
    ▼
Coordinator reads:
  - git diff main..HEAD --name-only (scope)
  - .docs/quality.md (if exists)
  - quality-audit.config.json (if exists)
  - .docs/architecture.md (for context)
  - .docs/project.md (for domain context)
  - .claude/review-state.json (if exists, for prior cycle)
    │
    ├──▶ Spawn static-review (background)
    │     Run quality-audit.py --changed, lint, type-check
    │
    ├──▶ Spawn semantic-review (background)
    │     Read each changed file, evaluate against .docs/quality.md + semantic_rules
    │
    └──▶ Spawn runtime-review (background)
          Verify stack running, run tests, capture logs + browser console
    │
    ▼
Merge 3 reports into single Quality Report
    │
    ▼
Post as GitHub issue comment
```

### Quality report format

```markdown
## Quality Review — Step N (cycle M)

### Static analysis
| Rule | File | Status | Detail |
|------|------|--------|--------|
| no-magic-numbers | `src/domain/order.ts` | FAIL | Line 42: raw `0.1` |

Errors: N | Warnings: N | Suppressed: N

### Semantic review
| Rule | File | Verdict | Reasoning |
|------|------|---------|-----------|
| rich-vs-anemic | `src/domain/order.ts` | FAIL | No behavior methods |

### Runtime validation
| Check | Status | Detail |
|-------|--------|--------|
| Unit tests | PASS | 47/47 passed |
| E2E tests | FAIL | checkout.spec.ts — timeout |
| App logs | WARN | 3 deprecated API warnings |
| Browser console | FAIL | Hydration mismatch |

### Action items
- [ ] [S1] Fix magic number in `src/domain/order.ts:42`
- [ ] [S2] Add behavior to `Order` entity
- [ ] [R1] Fix E2E timeout in `checkout.spec.ts`
- [ ] [R2] Fix hydration mismatch

> Developer notes: (edit this comment to add justifications)
> - [S3] Keeping `processData` — processes multiple data types. Will add JSDoc.

---
Reviewed: 2026-04-04T14:30:00Z | Files: 12 | Scope: git diff main..HEAD
```

### State tracking

`.claude/review-state.json` (gitignored) persists across cycles:

```json
{
  "issue": 42,
  "step": 3,
  "cycle": 2,
  "items": [
    { "id": "S1", "rule": "no-magic-numbers", "file": "src/domain/order.ts", "status": "open" },
    { "id": "S3", "rule": "semantic-naming", "status": "justified", "accepted": true }
  ],
  "last_review_timestamp": "2026-04-04T14:30:00Z",
  "last_review_comment_id": "IC_kwDONnR..."
}
```

### Cycle limits

- **Max 3 review cycles.** After 3 cycles, unresolved items become warnings (not blockers).
- **Re-reviews are scoped:** only re-check open items + newly changed files.
- **Justification flow:** developer edits the GitHub comment to add justifications. On re-review, agent evaluates them. If reasonable: accepted. If weak: proposes alternative.

### Quality gate contract (tiered, graceful degradation)

| Tier | What project provides | What's enabled |
|------|----------------------|----------------|
| **Minimum** | Git repo with branch | Changed file scoping |
| **Basic** | + .docs/quality.md | Semantic review |
| **Standard** | + quality-audit.config.json + quality-audit.py | Static analysis |
| **Full** | + docker-compose + dev-start.sh + test runner + Playwright | Runtime validation |
| **Custom** | + .claude/review-config.json | Explicit paths, thresholds, cycle limits |

Missing tiers degrade gracefully — report notes "static analysis skipped: quality-audit.py not found" instead of failing.

### Optional .claude/review-config.json

```json
{
  "quality_audit_path": ".claude/scripts/quality-audit.py",
  "quality_md_path": ".docs/quality.md",
  "test_commands": {
    "unit": "pytest tests/unit -x -v",
    "integration": "pytest tests/integration -x -v",
    "e2e": "npx playwright test"
  },
  "dev_start": "scripts/dev-start.sh",
  "log_sources": ["docker compose logs --tail=200"],
  "max_review_cycles": 3,
  "max_human_cycles": null
}
```

---

## 6. The REVIEW ↔ HUMAN Conflict Resolution

### The problem

- REVIEW before HUMAN: user might request changes that undo quality fixes
- REVIEW after HUMAN: new issues from user feedback won't be caught
- Neither alone is sufficient

### The solution: REVIEW full + REVIEW-LITE after HUMAN

```
Development complete
    │
    ▼
/review (FULL) ◄── 3 sub-agents, up to 3 cycles
    │
    ▼
/pw — Playwright verification
    │
    ▼
/validate — User tests, provides feedback
    │
    ├── No changes → /update-docs → /review --final → /open-pr
    │
    └── Changes requested
         │
         ▼
        Developer applies feedback
         │
         ▼
        REVIEW-LITE (automatic, scoped):
          - ONLY files modified after HUMAN feedback
          - ONLY static + semantic (no full runtime)
          - Single cycle, no iteration
         │
         ▼
        /pw re-run (modified pages only)
         │
         ▼
        /validate re-validation
         │
         └── Loop until approved (max 3 HUMAN cycles)
              │
              ▼
             /update-docs → /review --final → /open-pr
```

**Why this works:**
1. Full REVIEW catches all quality issues BEFORE the user sees the app — no broken foundation.
2. HUMAN changes are typically small (visual: button color, spacing, wording) — REVIEW-LITE is proportional.
3. `/review --final` catches anything that slipped through: scoped to files changed AFTER the first full review (timestamp-based via `review-state.json`).
4. If HUMAN requested no changes, `/review --final` is a no-op (zero files in delta).

---

## 7. Context Strategy: .docs/project.md + Improved .docs/architecture.md

### The context triad

| Document | Answers | Tokens | Volatility |
|----------|---------|--------|------------|
| `.docs/project.md` (NEW) | What is this app? Who uses it? What are the rules? | 300-500 | Very low (monthly) |
| `.docs/architecture.md` | How is it built? Where is everything? | 800-1500 | Medium (per-merge) |
| `.docs/quality.md` | How should code be written? | 400-800 | Low (per-phase) |
| **Total briefing** | | **1500-2800** | |

Compare: codebase exploration burns 30,000-80,000 tokens. The triad costs 1,500-2,800.

### .docs/project.md template

```markdown
# Project

## Purpose
One paragraph: what the application does, who it serves, what problem it solves.

## Domain
| Term | Definition | Example |
|------|-----------|---------|
Key domain concepts as glossary. Agents must use these terms correctly.

## Users
| Role | Can do | Cannot do | Auth level |
|------|--------|-----------|------------|
User personas with capabilities and constraints.

## Business rules
1. Non-negotiable rules that code must enforce.
2. These are the rules review agents verify.

## Boundaries
What is explicitly OUT of scope. Prevents agents from suggesting features
that violate the project's purpose.

## External dependencies
| Service | Purpose | Swappable? | Notes |
|---------|---------|------------|-------|

## Constraints
Technical or organizational constraints that shape decisions.
```

**Created by:** `/start-new-project` during Phase 1 scaffolding.
**Updated by:** `/update-docs` agent (rare — only when domain concepts change).

### .docs/architecture.md improvements

Add these sections to the existing template:

1. **"At a glance"** — 2 lines at top: project type, primary framework, entry points. (~20 tokens)
2. **"Key flows"** — 2-3 numbered sequences showing how data moves through layers. Highest-value section for agents implementing new features.
3. **"Config"** — Environment variables table (Variable | Purpose | Required | Default).
4. **Drift detector** — Hash + timestamp at bottom for staleness detection:
   ```
   <!-- arch-hash: <sha256-of-directory-structure> -->
   <!-- last-updated: 2026-04-04 -->
   ```

### Agent briefing protocol

Every spawned agent receives context INLINED in the prompt (not "go read file X"):

```
Briefing cost breakdown:
1. .docs/project.md content (inline)           ~400 tokens
2. .docs/architecture.md content (inline)      ~1200 tokens
3. .docs/quality.md relevant section (inline)  ~300 tokens
4. Task-specific checkboxes              ~200 tokens
5. Files to modify (inline)              ~variable
                                         ─────────
                              Base cost: ~2100 tokens + file contents
```

Role-based packet:
- **Developer** (writes code): all 3 docs + files to modify
- **QA-static** (linter/type-check): quality-audit config path + file list only (~400 tokens)
- **QA-semantic** (code quality judgment): .docs/project.md + .docs/quality.md + changed files (~900 tokens)
- **QA-runtime** (runs app/tests/logs): .docs/architecture.md scripts/config section + test commands (~600 tokens)
- **Tech Writer** (updates docs): .docs/architecture.md + git diff
- **Explorer** (discovers structure): nothing (its job IS to build context)

### The /update-docs agent

Receives: current .docs/architecture.md + .docs/project.md + full git diff for the step. Produces surgical updates to both docs. .docs/project.md changes are flagged for human review (".docs/project.md change — review carefully").

---

## 8. validate-issue.config.json changes

The existing validator needs updating for the new 5-tag system:

### Removed rules
- All SPAWN-related rules (spawn_must_be_first, spawn_requires_review, spawn_mentions_delegation)
- All REVIEW-related rules (review_recommended, review_mentions_validation)
- PW rules (pw_requires_human, pw_mentions_visual)
- HUMAN rules (human_requires_pw, human_mentions_iteration)
- DOCS rules (docs_required, docs_mentions_architecture)
- LOG rules (log_mentions_logging)
- AUDIT rules (audit_mandatory, audit_must_be_last, audit_mentions_quality, last_audit_quality)
- UI chain rule (no longer needed — PW/HUMAN are phases, not inline)
- e2e_requires_pw (E2E is now just writing the test, PW running is a phase)

### Remaining rules
- green_requires_red ✅
- red_no_consecutive ✅
- green_no_consecutive ✅
- green_before_red ✅
- tag_ordering (simplified to RED → GREEN → INFRA → WIRE → E2E) ✅
- red_mentions_test ✅
- green_writes_tests (warn) ✅
- e2e_mentions_test ✅
- wire_mentions_integration ✅
- infra_writes_tests (warn) ✅
- no_duplicate_checkboxes ✅
- All structure rules (what/why/acceptance/step_count/numbering) ✅
- All sizing rules (empty_step/checkbox_count/checkbox_length) ✅

### count_excluded_tags update
From: `["SPAWN", "REVIEW", "PW", "HUMAN", "DOCS", "LOG", "AUDIT"]`
To: `[]` (all tags count now — no more process gates)

### Sizing limits update
Process gates are gone — every checkbox is real work now. Limits relax accordingly:

| Rule | Old | New | Reason |
|------|-----|-----|--------|
| Steps per issue | 2-8 hard | 2-8 recommended, **10 warn**, **12 hard** | Better one extra step than an artificial split into 2 issues |
| Checkboxes per step | 6 recommended, 8 hard | **8 recommended**, **10 hard** | No process gates eating slots. Each checkbox is pure work |
| Min checkboxes | 2 | **1** | A step can legitimately be 1 checkbox (e.g., `[INFRA]` configure docker) |
| Checkbox chars | 200 | **300** | More room for specificity (file paths, conditions) |

Clarity comes from TaskBoard ticks, not from cramming work into artificial limits.

---

## 9. Migration Path

### Phase 1: Create new skills (no breaking changes)

Create `/review`, `/pw`, `/validate`, `/update-docs` as new skills alongside existing /start-issue. They coexist — users can start using them manually.

- `workflow/skills/review/SKILL.md` + references/
- `workflow/skills/pw/SKILL.md` + move playwright-practices.md here
- `workflow/skills/validate/SKILL.md`
- `workflow/skills/update-docs/SKILL.md`

### Phase 2: Create .docs/project.md template

Add .docs/project.md template to `/start-new-project/templates/`. Update `/start-new-project` to scaffold it.

### Phase 3: Simplify /start-issue

Remove Steps 2b, 7. Simplify Step 3 tag table (12 → 5). Add "Post-development phases" section to issue template. Update step-template.md.

### Phase 4: Update /continue-issue

Remove inline process gate chain (SPAWN → REVIEW → PW → HUMAN → DOCS → LOG → AUDIT). Simplify tag execution to 5 entries. "Next action" says "run `/review` when the step is done".

### Phase 5: Update validator template

Update the validate-issue.config.json template in start-new-project to reflect the new 5-tag system.

### Phase 6: Update .docs/architecture.md template

Add "At a glance", "Key flows", "Config" sections. Add drift detector.

**Sequencing:** Phase 1 + 2 in parallel → Phase 3 → Phase 4 + 5 + 6 in parallel.

---

## 10. Decisions (resolved)

1. **Naming:** `/validate` (not `/human`). Clearer as an action.
2. **`/review --final`:** Explicit. Each phase is a deliberate user action.
3. **`/review` vs `/simplify`:** Coexist. `/review` = formal quality gate. `/simplify` = quick ad-hoc.
4. **Review scope:** Per-phase default, `--step N` opt-in for critical steps.
5. **Quality report location:** Local-first in `.docs/reviews/<issue>-cycle-<N>.md`. `/push` syncs to GitHub as issue comment for visibility. Same pattern as `.docs/issues/`.
6. **Next action guidance:** ALL skills must suggest the next step. `/continue-issue` suggests `/review` when all dev steps are complete.
7. **Role names in sub-agent prompts:** Yes, use real-world roles. "You are a senior QA Engineer specializing in semantic code review..." — role names shape agent behavior toward expertise.
8. **`.docs/` creation:** `/start-new-project` creates it. If the issue skill detects `.docs/` missing, it creates it with a warning ("`.docs/` not found — creating it now").
9. **Lean skeleton migration:** Incremental. Start with /start-issue decomposition. Then update /update-skill and /create-skill to understand the new dynamics. Leave inertia specs in `spec/` directory so future sessions can understand the context immediately.
10. **Flow diagram:** Markdown in spec (fast to iterate, viewable in IDE).

---

## 11. Depuration Findings (6 agents + hooks analysis)

Consolidated from 6 specialized auditors analyzing the spec against Anthropic's official docs for skills and agents. Findings organized by priority.

### CRITICAL — Must fix before implementation

#### C1. REVIEW-LITE must NOT spawn sub-agents
The spec proposes 2 sub-agents for REVIEW-LITE (post-HUMAN changes). For 2-3 changed files, this costs ~31k tokens vs ~10k inline. **REVIEW-LITE should be an internal step of /validate, not a separate skill invocation.** Skills cannot invoke other skills (`Skill` tool limitation). The /validate skill embeds lightweight review logic (static + semantic on delta files, single cycle).

#### C2. Replace timestamp-based scoping with commit SHA
`/review --final` uses `last_review_timestamp` from review-state.json. Git timestamps are unreliable (amends, rebases, cherry-picks). **Use `last_review_commit_sha` instead** — store HEAD SHA at review completion, scope delta via `git diff <sha>..HEAD`.

#### C3. Pipeline prerequisite validation missing
Each skill is independently invocable but the pipeline assumes order. If user runs `/validate` before `/review`, no quality report exists. **Each skill's pre-flight must validate prerequisites as warnings (not blocks):**
- `/review`: verify non-empty git diff
- `/pw`: verify E2E test files exist
- `/validate`: warn if no review-state.json found
- `/update-docs`: warn if step checkboxes incomplete
- `/open-pr`: warn if no review comment on issue

#### C4. Error handling for sub-agent failures undefined
What if runtime-review crashes (docker won't start) while static-review succeeds? **Add:**
- Per-agent timeout: static (2 min), semantic (3 min), runtime (5 min)
- Partial results: coordinator posts report with "SKIPPED: [agent] failed — [reason]"
- Re-run capability: `/review --rerun runtime`

#### C5. Developer justification flow is fragile
Editing a GitHub comment's markdown to add justifications is error-prone. **Two alternatives:**
- Reply-based: developer replies with `justify S3: reason here` — agent scans replies
- File-based: `.claude/review-justifications.json` — deterministic, machine-parseable
Recommendation: support both, prefer reply-based for simplicity.

### HIGH — Should fix in spec

#### H1. New skills need full 14-section canonical skeleton
The spec defines flow but not the standard sections every skill in this library has: frontmatter, input/output contracts, external state, pre-flight, steps, post-flight, next action, self-audit, content-audit, error handling, anti-patterns, guidelines. **Add at minimum skeleton headers for each new skill.**

#### H2. /review will exceed 500 lines — extract to references/
Estimated ~425 lines minimum when properly implemented. Extract:
- `references/quality-report-format.md`
- `references/sub-agent-prompts.md` (static, semantic, runtime templates)
- `references/review-lite.md`
- `references/tiered-degradation.md`

#### H3. Use XML tags for structured sub-agent output
Each review agent should return `<review-result>...</review-result>` with structured items instead of freeform prose. Enables deterministic merge by coordinator.

#### H4. Immutable review comments — new comment per cycle
Don't edit existing comments (last-write-wins conflict with developer edits). Post a NEW comment per review cycle. This creates an audit trail and avoids concurrent modification.

#### H5. Role-based briefing must be per-sub-agent, not generic "Reviewer"
Expand from 4 roles to 6:

| Role | Documents |
|------|-----------|
| Static-Reviewer | quality-audit config path + file list only (~400 tokens) |
| Semantic-Reviewer | .docs/project.md + .docs/quality.md + changed files (~900 tokens) |
| Runtime-Reviewer | .docs/architecture.md scripts/config section + test commands (~600 tokens) |

Savings: ~4,700 tokens/cycle vs current "all docs to all agents" approach.

#### H6. `context: fork` for /review and /pw
Both produce verbose output (sub-agent reports, Playwright DOM dumps) that pollutes main context. `context: fork` runs them in isolation, returning only the final result.

#### H7. Agent definitions as inline prompts with reference templates
Create `references/static-review-prompt.md`, `references/semantic-review-prompt.md`, `references/runtime-review-prompt.md` in the /review skill directory. Coordinator fills placeholders at spawn time. NOT in `.claude/agents/` (those are project-specific).

#### H8. review-state.json needs hardening
- Add `schema_version: 1` field
- Add `session_id` to detect stale state from prior sessions
- Add `.gitignore` requirement explicitly
- Fallback: if missing/corrupt, start fresh cycle 1 (never fail)

#### H9. Missing anti-patterns and error handling tables
Every existing workflow skill has both. Proposed anti-patterns documented in depuration reports — must be formalized per skill.

#### H10. Port conflict handling for runtime-review
Agent prompt must include: "Check if ports are in use before starting stack. If app already running, reuse it." Support `dev_already_running` flag in review-config.json.

### MEDIUM — Address during implementation

#### M1. Skill descriptions under 250 chars
Draft descriptions needed for all 4 new skills. Existing workflow skills also exceed limit (continue-issue: 465 chars, push: 492 chars).

#### M2. `effort: max` for /review, `effort: high` for /start-issue
Leverage Opus 4.6 effort field for reasoning-intensive skills.

#### M3. `disable-model-invocation: true` for /validate and /update-docs
Prevent auto-triggering of human-interactive or deliberate-action skills.

#### M4. Parallel sub-agents must be explicitly read-only
Static-review: `--check` only flags, no auto-fix. Semantic-review: Read/Grep/Glob only, no Bash. Runtime-review: "Do NOT modify files, restart services, or run git write operations."

#### M5. PreCompact-aware design
Write intermediate state to review-state.json after each sub-agent completes (not just at end). If context compacts mid-review, coordinator can recover from state file.

#### M6. Sub-agent model optimization (future)
static-review and runtime-review are operational (Sonnet candidates). semantic-review requires Opus. Currently Agent tool doesn't support per-agent model override — document as future optimization (~40% cost reduction for 2/3 agents).

#### M7. Billing transparency
`/review` costs ~4 sessions (coordinator + 3 background agents). Skill should report estimated cost upfront.

### Hooks evaluation

All 3 existing hooks remain necessary with the new architecture:

| Hook | Verdict | Reason |
|------|---------|--------|
| Skill Reload Enforcer | **KEEP** | Infrastructure problem (cache stale), not solved by agent specialization |
| Skill Reload Blocker | **KEEP** | Deterministic enforcement of Skill tool call, still needed |
| Skill Step Enforcer | **KEEP** (simplify) | skill-active flag still relevant but simpler with smaller skills |

New hook opportunities:
- `/review`: PostToolUse hook to validate sub-agent report format
- `/open-pr`: PreToolUse soft gate checking review completion

---

## 12. Additional Requirements (user input)

### E2E tests must navigate like a human
No `page.goto('/dashboard')`. E2E tests must navigate via UI: clicks, sidebar, menus, links. This is a fundamental rule for /pw and all E2E-related work. A human expert doesn't type URLs — the tests shouldn't either.

### Local issue body in .docs/ (committed to git)
Replace the complex issue backup system with a simple local directory:
- `/start-issue` writes the plan to `.docs/issues/<number>.md` + publishes to GitHub
- During development, agents consult the LOCAL file (not GitHub API)
- `/push` syncs checkboxes back to GitHub if changed
- `.docs/issues/` is **committed to git** (not gitignored) — any agent in any session has the plan locally without hitting GitHub. The cost is minimal (1 markdown file per issue) and checkbox updates are naturally part of work commits.
- Eliminates: issue-backup.sh, snapshot system, .bak files, GitHub API rate limit concerns during dev
- The file IS the source of truth during development. GitHub is the sync target, not the source.
- **Safety rule:** NEVER use sed/regex on the GitHub issue body directly. Always edit `.docs/issues/<N>.md` locally and publish the entire file: `gh issue edit <N> --body "$(cat .docs/issues/<N>.md)"`. Git history is the backup — `git restore` or `git show HEAD~1:.docs/issues/<N>.md` recovers any prior state. No separate backup mechanism needed.

### Tests for all scripts
Every Python/sh script generated by the skills library must have an associated test file. Scripts are deterministic — there's no excuse for not testing them. This includes:
- quality-audit.py → test_quality_audit.py
- validate-issue.py → test_validate_issue.py
- Any new scripts created by /review, /pw, etc.

### Lean skill skeleton (14 sections → 7)
The current 14-section canonical skeleton is too heavy. Each skill loads ~900 extra tokens of sections that provide little runtime value (output contract, post-flight, self-audit, content-audit, flight tables, guidelines, report). New structure:

```
---
(frontmatter)
---
# Skill Name
(1-2 lines: what it does)

## Pre-flight
(checks + inputs + external state — all compact, merged)

## Steps
### 1. ...
### 2. ...

## Error handling
| Failure | Strategy |

## Anti-patterns
- Don't X because Y

## Next action
(what to run after)
```

**What was removed and where it went:**
- Input/Output contract → absorbed into pre-flight as 1-line descriptions
- External state → absorbed into pre-flight ("Reads: .docs/quality.md")
- Post-flight → unnecessary. TaskBoard ticks show progress.
- Self-audit + Content audit → removed. Validation comes from /review agent, not self-checking. Redundant to audit yourself then have an auditor audit you again.
- Guidelines → moved to references/ if skill-specific, or already in project CLAUDE.md
- Flight tables → removed. TaskBoard is sufficient.
- Report section → removed. Model naturally reports what it did.

**Impact:** ~900 tokens saved per skill load. With 5 pipeline skills, ~4,500 tokens returned to real work per session.

**skill-active simplification:** Flag true at Step 1 start, false when last step completes. No post-flight to wait for.

**Existing skills migration:** Update incrementally. When a skill is edited for any reason, slim it down. No big-bang rewrite.

### Project docs consolidation (.docs/)
Move all project analysis/architecture/quality files from root into `.docs/`:
```
project-root/
├── CLAUDE.md              ← stays in root (Anthropic requires it)
├── .docs/
│   ├── architecture.md    ← was ARCHITECTURE.md (root, uppercase)
│   ├── project.md         ← new SOT document
│   ├── quality.md         ← was quality.md (root)
│   └── issues/
│       └── 42.md          ← local issue body (replaces backup system)
└── .claude/
    └── scripts/
```
All lowercase inside `.docs/`. CLAUDE.md stays uppercase in root (Anthropic convention).

### Checkbox character limit: 200 → 300
Increase `max_checkbox_chars` from 200 to 300 in validate-issue.config.json. 200 was too tight — forced generic checkboxes or excessive splitting. 300 allows specificity (file paths, conditions, context) without becoming a paragraph. Update in both the template (`start-new-project/templates/`) and existing projects.

### Token efficiency is a constraint, NOT the objective
Quality of delivery > token efficiency. If /review costs 60k tokens but catches a real bug, it's worth it. Never sacrifice review thoroughness to save tokens. The optimizations in section 11 are about eliminating WASTE (spawning 2 agents for 3 files), not reducing THOROUGHNESS.

---

## 13. Agent Role Nomenclature — Real-World Analogy

### The question
Should agents/skills map to real-world roles (PO, Architect, TechLead, QA, Developer)?

### Analysis

The current proposal maps to functions, not roles:

| Current name | Function | Real-world analogy |
|---|---|---|
| /start-issue | Plan the work | **PO + Architect** (scope + technical breakdown) |
| Developer (you) | Write code via TDD | **Developer** |
| /review (static) | Automated checks | **CI Pipeline / Linter** |
| /review (semantic) | Code quality judgment | **QA Engineer** (code review) |
| /review (runtime) | Run the system, check behavior | **QA Engineer** (integration testing) |
| /pw | Visual validation | **QA Engineer** (visual/E2E) |
| /validate | User acceptance | **PO** (acceptance criteria) |
| /update-docs | Documentation | **Tech Writer** |

### Recommendation: Hybrid approach

Use role-based naming for SUB-AGENTS (internal, not user-facing) and function-based naming for SKILLS (user-facing).

**Why:** The user types `/review`, not `/call-qa-team`. Skill names should be verbs (actions). But the sub-agents spawned by /review benefit from role names because it clarifies their perspective and expertise:

```
/review (skill — user types this)
  ├── QA-static (sub-agent — runs linters, type-checks)
  ├── QA-semantic (sub-agent — judges code quality)
  └── QA-runtime (sub-agent — runs app, tests, logs)
```

The role name in the sub-agent prompt shapes behavior: "You are a QA Engineer performing semantic code review" produces better output than "You are a static analysis runner."

**Full role map for future reference:**

| Role | Maps to | When active |
|------|---------|-------------|
| **Architect** | /start-issue (plan phase) | Analyzing issue, proposing plan |
| **Developer** | The user + Claude | TDD implementation |
| **QA Engineer** | /review sub-agents | Quality review phase |
| **QA Visual** | /pw | Playwright validation |
| **PO** | /validate | User acceptance |
| **Tech Writer** | /update-docs | Documentation update |

This gives Claude a mental model for each phase without forcing role-based skill names on the user.

**Decision:** Use role names. "You are a senior QA Engineer specializing in semantic code review..." — the role shapes the agent toward expertise, not generic execution.

### Future role: UI Designer (Super Agent)

A specialized agent with deep frontend-design expertise for generating high-quality, minimalist layouts (Apple-level visual quality). This agent would:

- **Absorb** the existing `/frontend-design` skill capabilities
- **Specialize** in: spacing systems, typography scales, color harmony, component composition, responsive breakpoints, micro-interactions
- **Reference style:** Apple HIG — clean, generous whitespace, purposeful hierarchy, invisible complexity
- **When invoked:** During /pw phase when layout issues are detected, or explicitly by user for design-intensive steps
- **Model:** Opus with high effort (visual design requires deep aesthetic judgment)
- **Key constraint:** Must generate Tailwind-only solutions (no inline styles, no custom CSS unless unavoidable)

This is a separate initiative — not part of the /start-issue decomposition. Tracked as a future backlog item for when the core pipeline is stable.

---

## 14. Flow Diagram

### Complete lifecycle: from issue to PR

```
=== /start-new-project ===
(once per project -- creates .docs/, quality.md, etc.)
    |
    v
=== /start-issue #N ======================================= [Architect] ===

  1. Select issue (args or board query)
  2. Analyze (fetch metadata, read .docs/architecture.md,
     .docs/project.md, detect capabilities)
  3. Plan (simplified tags: RED/GREEN/INFRA/WIRE/E2E)
     -> Present via Plan Mode -> User approves
  4. Write plan to .docs/issues/<N>.md + publish to GitHub
  5. Create branch feat/<N>-<slug>
  6. Update board -> "In Progress"
  7. Create tasks (1 per step)

  -> Next: /continue-issue or start developing

    |
    v
=== DEVELOPMENT PHASE ===================================== [Developer] ===

  Per step (reading from .docs/issues/<N>.md):

    [RED]   Write failing test
    [GREEN] Implement to pass
    [INFRA] Config/tooling
    [WIRE]  Connect layers
    [E2E]   Write Playwright E2E test

    -> /push after each step
       (syncs checkboxes to GitHub, updates .docs/issues/<N>.md)

  When all steps complete:
  -> Next: /review

    |
    v
=== /review =============================================== [QA] ==========

  Spawns 3 sub-agents in parallel (run_in_background):

    +---------------+  +---------------+  +------------------+
    | QA-static     |  | QA-semantic   |  | QA-runtime       |
    |               |  |               |  |                  |
    | quality-audit |  | quality.md    |  | docker up        |
    | lint          |  | project.md    |  | run tests        |
    | type-check    |  | LLM judgment  |  | capture logs     |
    |               |  | per file      |  | browser console  |
    +-------+-------+  +-------+-------+  +--------+---------+
            |                   |                    |
            +-------------------+--------------------+
                                |
                                v
              Coordinator merges reports
              Writes .docs/reviews/<N>-cycle-<M>.md
              /push syncs to GitHub as issue comment

  +---- All pass? ----YES----> Next: /pw (web) or /update-docs
  |         |
  |        NO
  |         v
  |  Developer fixes + adds justifications
  |         |
  |         v
  |  /review (cycle 2, scoped to open items + new changes)
  |         |
  |  (max 3 cycles, then remaining become warnings)
  +---------+

  -> Next: /pw

    |
    v
=== /pw =================================================== [QA Visual] ==

  (web projects with UI changes only)

  1. Detect Playwright config
  2. Run E2E tests (navigate like a human -- no URL typing)
  3. Capture screenshots + browser console errors
  4. Read screenshots, diagnose issues
  5. Fix -> re-run -> repeat until clean

  -> Next: /validate

    |
    v
=== /validate ============================================= [PO] =========

  (UI changes only)

  1. Present testing guide (URLs, credentials, click paths)
  2. User tests live app
  3. Collect feedback

  +---- Approved? ----YES----> Next: /update-docs
  |         |
  |        NO (changes requested)
  |         v
  |  Developer applies feedback
  |         |
  |         v
  |  REVIEW-LITE (internal, not a separate skill):
  |    - Only files changed after feedback
  |    - Static + semantic inline (no sub-agents)
  |    - Single pass, ~10k tokens
  |         |
  |         v
  |  /pw re-run (modified pages only)
  |         |
  |         v
  |  /validate re-present (until approved)
  +---------+

  -> Next: /update-docs

    |
    v
=== /update-docs ========================================== [Tech Writer] =

  1. Read current .docs/architecture.md + .docs/project.md
  2. Read git diff main..HEAD
  3. Update architecture.md (routes, patterns, schema, flows)
  4. Update project.md if domain concepts changed (flag review)
  5. Update drift detector hash

  -> Next: /review --final

    |
    v
=== /review --final ======================================= [QA] =========

  Lightweight delta pass:
  - Scope: git diff <last_review_sha>..HEAD
  - Only static + semantic (no runtime)
  - Single cycle
  - If no files changed since last review -> "Nothing to review"

  -> Next: /open-pr

    |
    v
=== /open-pr -> /close-pr =================================================

  Pre-flight: warn if no review found on issue
```

### Data flow: .docs/ during the pipeline

```
.docs/
├── architecture.md    ←── read by /start-issue, /review (QA-runtime), /update-docs
├── project.md         ←── read by /start-issue, /review (QA-semantic), /update-docs
├── quality.md         ←── read by /review (QA-semantic, QA-static)
├── issues/
│   └── 42.md          ←── written by /start-issue
│                          read by /continue-issue, /push
│                          updated by /push (checkbox sync)
└── reviews/
    ├── 42-cycle-1.md  ←── written by /review
    ├── 42-cycle-2.md      read by /review (next cycle)
    └── 42-final.md        read by developer (justifications)
                           synced to GitHub by /push
```

### Skip paths (not all phases required)

```
Backend-only (no UI):
  /start-issue → dev → /review → /update-docs → /review --final → /open-pr

Full-stack with UI:
  /start-issue → dev → /review → /pw → /validate → /update-docs → /review --final → /open-pr

Config/infra only:
  /start-issue → dev → /review → /update-docs → /open-pr
  (skip /pw, /validate, /review --final if no code changes after docs)

Hotfix (minimal):
  /start-issue → dev → /review → /open-pr
```

---

## Appendix: Planner cross-reference

| Topic | Planner A (Workflow) | Planner B (Quality) | Planner C (Context) | Consolidated |
|-------|---------------------|--------------------|--------------------|-------------|
| SPAWN removal | Eliminated | Not referenced | N/A | **Eliminated** |
| Tag simplification | 5 tags | N/A | N/A | **5 tags: RED/GREEN/INFRA/WIRE/E2E** |
| Review agents | 0 agents (all skills) | 3 sub-agents + coordinator | N/A | **1 skill (/review) spawns 3 sub-agents** |
| REVIEW/HUMAN conflict | Full + final delta | Full + REVIEW-LITE | N/A | **Full -> HUMAN -> REVIEW-LITE -> final** |
| Max cycles | 3 review + unlimited human | 3 review + unlimited human | N/A | **3 review + unlimited human** |
| SOT document | N/A | N/A | .docs/project.md | **.docs/project.md** |
| Architecture docs | N/A | N/A | Add: at-a-glance, key flows, config, drift detector | **4 new sections** |
| Token budget | N/A | N/A | 1500-2800 base | **2100 tokens base briefing** |
| Migration | 5 phases | Enhancement to continue-issue | 7 priority-ordered recs | **6 phases** |
