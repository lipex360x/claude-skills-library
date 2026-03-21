# Completeness Checklist

Agnostic checklist for analyzing skill design input. Each category contains concrete questions to ask against the raw input. The answers feed into the hybrid decision model — each item is classified as `[inferred]`, `[gap]`, or `[ask]`.

## How to use

For each category, iterate through the questions. For each question:

1. **Search the input** for explicit answers, implicit signals, or related context
2. **Classify** using the rules in `decision-model.md`:
   - Clear answer with high confidence → `[inferred]`
   - No answer but non-blocking → `[gap]`
   - Ambiguous or architectural → `[ask]`
3. **Record** the classification and rationale in the Decisions Log

## Categories

### 1. External Dependencies

What tools, APIs, CLIs, or services does this skill need beyond Claude Code's built-in tools?

| # | Question | What to look for |
|---|----------|-----------------|
| 1.1 | Does the skill call external CLIs? | References to `gh`, `git`, `npm`, `docker`, specific binaries |
| 1.2 | Does it need network access? | API calls, web fetches, URL references |
| 1.3 | Does it read/write files outside the project? | Paths outside the working directory, `~/`, absolute paths |
| 1.4 | Does it depend on specific environment variables? | `process.env`, `$VAR`, env file references |
| 1.5 | What happens if a dependency is unavailable? | Should it fail hard, degrade gracefully, or offer alternatives? |

### 2. Cross-Skill State

Does this skill read from or write to state that other skills depend on?

| # | Question | What to look for |
|---|----------|-----------------|
| 2.1 | Does it consume output from another skill? | References to other skills' artifacts, file paths they produce |
| 2.2 | Does it produce output another skill consumes? | Output files with known consumers, shared config updates |
| 2.3 | Does it modify shared resources? | STRUCTURE.md, CLAUDE.md, project-settings.json, package.json |
| 2.4 | Is the read/write contract documented? | Format expectations, version compatibility, what-if-missing behavior |
| 2.5 | Can concurrent access cause conflicts? | Two skills writing the same file, race conditions |

### 3. Input Ambiguity

Is the skill's input clear enough to implement without guessing?

| # | Question | What to look for |
|---|----------|-----------------|
| 3.1 | Are all input sources defined? | Where data comes from — args, files, environment, conversation |
| 3.2 | Is the priority order clear when multiple sources exist? | Which source wins when both args and file provide the same data |
| 3.3 | Are validation rules specified? | Required vs optional, format constraints, type expectations |
| 3.4 | What happens with malformed input? | Error messages, fallback behavior, partial acceptance |
| 3.5 | Are concrete examples provided? | Real invocation examples, not just abstract descriptions |

### 4. Resource Cost

How expensive is this skill to run in terms of tokens, time, and side effects?

| # | Question | What to look for |
|---|----------|-----------------|
| 4.1 | Does it load large files into context? | Reading entire codebases, large documents, multiple references |
| 4.2 | Does it spawn subagents? | Agent tool usage, parallel work, context duplication |
| 4.3 | Does it make external API calls? | Network requests, rate limits, cost per call |
| 4.4 | Is there a token budget strategy? | Progressive disclosure, on-demand loading, summarization |
| 4.5 | What's the expected execution time? | Quick (<30s), moderate (1-3min), long (>3min) |

### 5. Idempotency

What happens when the skill runs twice with the same input?

| # | Question | What to look for |
|---|----------|-----------------|
| 5.1 | Does it overwrite, append, or skip existing output? | File write behavior — create vs update vs upsert |
| 5.2 | Are side effects repeatable? | Git operations, API calls, file mutations |
| 5.3 | Does it detect previous runs? | Checking for existing files, state markers |
| 5.4 | Is the behavior documented? | Explicit statement of idempotency contract |

### 6. Error Surface

What can go wrong and how does the skill handle it?

| # | Question | What to look for |
|---|----------|-----------------|
| 6.1 | What are the failure modes per step? | Each workflow step should have a failure path |
| 6.2 | Are errors user-facing or silent? | Error messages, recovery suggestions, silent swallowing |
| 6.3 | Does it validate preconditions before doing work? | Dependency checks, input validation, environment verification |
| 6.4 | Can partial execution leave dirty state? | Half-written files, uncommitted changes, orphaned processes |
| 6.5 | Is there a rollback strategy? | Undo partial work, restore previous state |

### 7. Guardrails

What should the skill never do, and what must it always do?

| # | Question | What to look for |
|---|----------|-----------------|
| 7.1 | Are there destructive operations? | File deletion, git force-push, overwriting without backup |
| 7.2 | Does it touch user-facing systems? | GitHub issues, PRs, external services, shared config |
| 7.3 | Are there security boundaries? | Secrets in output, credential handling, path traversal |
| 7.4 | Is there a confirmation gate before irreversible actions? | AUQ before destructive steps |
| 7.5 | Are "must do" and "must NOT do" rules explicit? | Clear positive and negative constraints with reasons |

### 8. VCS Impact

Does this skill interact with version control?

| # | Question | What to look for |
|---|----------|-----------------|
| 8.1 | Does it create/modify files that should be committed? | Source files, config, templates |
| 8.2 | Does it create files that should be gitignored? | Temporary files, build artifacts, local config |
| 8.3 | Does it create branches, commits, or PRs? | Git workflow operations |
| 8.4 | Does it modify .gitignore or other VCS config? | Adding ignore patterns, hooks |
| 8.5 | Should output be committed automatically or left for user? | Auto-commit vs manual staging |

## Scoring summary

After completing all categories, produce a summary table:

```markdown
| Category | Items | Inferred | Gaps | Asks |
|----------|-------|----------|------|------|
| External deps | 5 | 3 | 1 | 1 |
| Cross-skill state | 5 | 2 | 2 | 1 |
| ... | | | | |
| **Total** | **40** | **X** | **Y** | **Z** |
```

A high gap count (>10) signals the input needs more detail before proceeding to `/create-skill`. A high ask count (>5) means the skill involves many architectural decisions — consider whether `/grill-me` should run first.
