# Step Template

Use this structure when rewriting the issue body with a detailed plan. Adapt to the issue — not every issue needs all sections.

## Template

```markdown
## Execution mode

> **MUST use Agent Teams (`TeamCreate`).** Do NOT fall back to isolated worktree agents.

After completing Step [N] ([last sequential step]):
- `[teammate-name]`: Steps [X-Y] — [what this teammate owns]
- `[teammate-name]`: Steps [W-Z] — [what this teammate owns]

**Teammate prompt pattern:** "Read issue #<number> Step X via `gh issue view`. Create one internal task per sub-section in your Step. Execute each unit, mark internal tasks as completed. Do NOT edit the issue body — lead verifies and marks checkboxes."

**Teammate task pattern:** Create one task per sub-section in your assigned Step. Task names must match sub-section headers for lead monitoring.

_Remove this section entirely if Agent Teams is not enabled._

## What

[Keep or slightly improve the original description]

## Why

[Keep or slightly improve the original motivation]

## Acceptance criteria

- [ ] [Original criterion 1]
- [ ] [Original criterion 2]
- [ ] [Original criterion 3]

## Step 1 — [Concise title]

- [ ] [Concrete task — include file path, e.g., `Create src/templates/readme.md with standard sections`]
- [ ] [Another task — specific and verifiable]
- [ ] [Verification: how to confirm this step works]

## Step 2 — [Concise title]

- [ ] [Task with file path]
- [ ] [Task with file path]

## Step 3 — [Concise title]

- [ ] [Task]
- [ ] [Task]
- [ ] [Verification]

```

## Section notes

### What / Why
- Preserve the original author's intent — don't rewrite substantially
- Improve clarity only if the original is ambiguous

### Acceptance criteria
- Copy the original checkboxes exactly
- These are the "definition of done" — they stay at the top
- Steps below are the HOW, acceptance criteria are the WHAT

### Steps
- Each Step = a focused work session (30 min to 2 hours)
- Start title with a verb: "Define", "Add", "Update", "Configure", "Implement"
- Number Steps sequentially across the entire issue (Step 1, 2, 3... not per-section)
- Include a verification checkbox as the last item when the Step has observable output
- For changes involving databases or file I/O, include test environment setup early — create or verify `docker-compose.test.yml` (or `test` profile) to orchestrate the test stack. Configure `.env.test` pointing at local containers. This must exist before any test checkbox can run
- For web projects with UI changes, include CDP setup as the first Step if `.claude/project-settings.json` doesn't exist yet. If it does, use the `pages` map to reference routes in verification checkboxes: "Navigate to [page] via CDP and take screenshot to verify [expected state]"

### Checkboxes
- One action per checkbox — avoid "X and Y" (split into two)
- Include file paths: `Create src/templates/readme.md` not just `Create readme template`
- **TDD order:** for Steps with new behavior, place test checkboxes before implementation checkboxes. Example:
  - `Add test for user creation in src/__tests__/user.test.ts — expect valid user object returned`
  - `Implement user creation in src/services/user.ts`
- For config tasks: `Configure Y in config-file.ext`

### Parallelizable Steps (Agent Teams)
When a Step will be assigned to a teammate, make it self-contained:
- Start with a **"Before starting"** block listing references to read (repo-relative paths)
- Use **sub-sections** (`### unit-name (path/)`) for each unit of work with individual checkboxes
- The teammate reads the issue step directly — no context duplication in the TeamCreate prompt

Example:
```markdown
## Step 2 — Migrate batch A

⚠️ This step runs in parallel via Agent Teams — see Execution mode above.

**Before starting:** Read these references:
- `path/to/reference-1.md` — what it provides
- `path/to/reference-2.md` — what it provides

### component-a (`src/components/a/`)
- [ ] Task 1
- [ ] Task 2
- [ ] Verify

### component-b (`src/components/b/`)
- [ ] Task 1
- [ ] Task 2
- [ ] Verify
```

### Consolidation Step (Agent Teams)
The final step consolidates progressive audit results — the actual auditing happens in background as teammates deliver (see Step 7 in SKILL.md):
- Each checkbox names a specific consolidation action
- The lead collects audit results and presents the verification matrix
- Flag failures for remediation, document false positives

Example:
```markdown
## Step 4 — Consolidate audit results and push

- [ ] Collect progressive audit results for all [units] — present consolidated verification matrix
- [ ] Flag any audit failures for remediation
- [ ] Document false positives with reasoning
- [ ] Push all changes
```

### Sizing
- 2-8 Steps per issue (simple issues: 2-3, complex: 5-8)
- 2-6 checkboxes per Step
- If you need 9+ Steps, the issue might need to be split into multiple issues
