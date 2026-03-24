# Execution Strategy — Decision Matrix

When Agent Teams is enabled, the skill must choose the right execution pattern based on the plan's characteristics. There are three strategies: **Agent**, **Teammate**, and **Sequential**.

## Decision flow

After building the plan (Step 3) and before presenting it to the user, evaluate:

```
1. Are parallelizable steps present? (multiple steps that don't depend on each other)
   → NO: SEQUENTIAL — lead executes all steps in order, no parallelism needed.

2. Do parallel steps share state? (editing the same files, same API resource, same DB table)
   → YES: TEAMMATE — workers need coordination via SendMessage to avoid conflicts.

3. Do parallel steps need mid-execution feedback? (lead reviews output before worker continues)
   → YES: TEAMMATE — iterative loop requires long-lived workers.

4. Is the work templated? (same pattern repeated N times on independent targets)
   → YES: AGENT — fire-and-forget with background agents, no coordination overhead.

5. Default for parallelizable steps without the above signals:
   → AGENT — simpler, cheaper, less overhead.
```

## Signal table

| Signal | Agent | Teammate | Sequential |
|--------|-------|----------|------------|
| Same pattern, N independent targets | **yes** | no | no |
| Steps touch different files/areas | **yes** | no | no |
| No output dependency between steps | **yes** | no | no |
| Workers must exchange information | no | **yes** | no |
| Lead needs to review between iterations | no | **yes** | no |
| Steps share mutable state (same files, DB) | no | **yes** | no |
| Frontend/backend must change in sync | no | **yes** | no |
| Issue has ≤ 3 simple steps | no | no | **yes** |
| All steps are strictly sequential | no | no | **yes** |

## Strategy templates

### Agent strategy

```markdown
## Execution strategy

> **Agent pattern** — steps are independent and follow the same template. Workers run in background and return results. Lead validates and marks checkboxes.

After completing Step [N] (last sequential step), spawn background agents:
- Agent 1: Step [X] — [scope] ([count] items)
- Agent 2: Step [Y] — [scope] ([count] items)
...

**Agent prompt pattern:** "[Context]. For each item in your batch: [read input], [produce output]. Report completion when done."
```

Key properties:
- Use `Agent` tool with `run_in_background: true`
- **Steps must be self-contained.** Agents cannot invoke skills (`Skill` tool is not available). The issue step IS the skill, distilled — include the format specification, golden example, or quality criteria inline in the step or agent prompt. Never write "use /skill-name" in a step assigned to an agent; instead, extract what the skill does and put the actionable instructions directly in the step
- Each agent receives full instructions in prompt (no issue reading needed, but can reference it)
- Agent returns result and dies — no shutdown protocol
- Lead collects results, validates, marks issue checkboxes, pushes
- No `TeamCreate`, no `TaskCreate` for agents — lead tracks via agent completion notifications
- GitHub issue checkboxes are the only tracker (no local task board duplication)

### Teammate strategy

```markdown
## Execution strategy

> **Teammate pattern** — steps have dependencies or shared state requiring coordination. Workers stay alive for feedback loops.

After completing Step [N] (last sequential step):
- `[name]`: Steps [X-Y] — [what this teammate owns]
- `[name]`: Steps [W-Z] — [what this teammate owns]

**Teammate prompt pattern:** "Read issue #<number> Step X via `gh issue view`. Create one internal task per sub-section. Execute, mark tasks completed. Do NOT edit the issue body."

**Teammate task pattern:** One task per sub-section. Task names match sub-section headers.
```

Key properties:
- Use `TeamCreate` + `Agent` with `team_name`
- Teammates stay alive, receive `SendMessage` for coordination
- Internal tasks (`TaskCreate`/`TaskUpdate`) track progress
- Lead monitors via `TaskList`, verifies, marks issue checkboxes
- Shutdown protocol required when done
- Use when workers need to: exchange data, wait for each other, or receive revised instructions

### Sequential strategy

```markdown
## Execution strategy

> **Sequential** — steps are simple or strictly dependent. Lead executes directly.
```

No parallelism section in the issue body. Lead works through steps in order.

## Examples

### Agent: "Update all 38 skill READMEs"
- 38 independent targets, same pattern (read SKILL.md → rewrite README)
- No shared state, no feedback needed
- **→ Agent** (8 background agents, one per plugin)

### Teammate: "Refactor auth — new token format affects frontend + backend"
- Step 1 (sequential): Define new token schema
- Step 2 (parallel): Backend middleware update — depends on Step 1
- Step 3 (parallel): Frontend token handler — depends on Step 1
- Steps 2-3 share the token format and must coordinate if interface changes mid-work
- **→ Teammate** (backend-teammate, frontend-teammate, lead coordinates)

### Sequential: "Fix typo in config file"
- 2 steps, trivially sequential
- **→ Sequential** (no parallelism needed)

### Agent: "Add license headers to all source files"
- 200 files, same pattern, zero interdependence
- **→ Agent** (batch by directory)

### Teammate: "Build feature with shared database migration"
- Step 1: Migration (sequential)
- Step 2: API endpoints (parallel, needs migration)
- Step 3: UI components (parallel, needs API types from Step 2)
- Step 2 exports types that Step 3 imports — coordination needed
- **→ Teammate** (api-teammate, ui-teammate after Step 1)
