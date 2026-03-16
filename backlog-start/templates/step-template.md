# Step Template

Use this structure when rewriting the issue body with a detailed plan. Adapt to the issue — not every issue needs all sections.

## Template

```markdown
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

## Parallel execution plan (Agent Teams)

> Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. Remove this section if not using Agent Teams.

After Step [N] ([last sequential step]), spawn teammates:
- `[teammate-name]`: Steps [X-Y] — [what this teammate owns]
- `[teammate-name]`: Steps [W-Z] — [what this teammate owns]
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

### Sizing
- 2-8 Steps per issue (simple issues: 2-3, complex: 5-8)
- 2-6 checkboxes per Step
- If you need 9+ Steps, the issue might need to be split into multiple issues
