# Claude Code Skills — Documentation Summary

Reference document summarizing Anthropic's official skills documentation for evaluating the /start-issue decomposition spec.

---

## What Are Skills?

Skills are custom commands that extend Claude Code with reusable, prompt-based instructions. They follow the open [Agent Skills](https://agentskills.io) standard.

A skill is a directory containing:
- **SKILL.md** (required): YAML frontmatter + markdown instructions
- **Supporting files** (optional): templates/, references/, scripts/, assets/

## SKILL.md Frontmatter Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | directory name | Becomes the `/slash-command`. Max 64 chars. |
| `description` | string | first paragraph | What it does + when to trigger. **Under 250 chars.** |
| `argument-hint` | string | — | Autocomplete hint (e.g., `[issue-number]`) |
| `disable-model-invocation` | boolean | `false` | Prevents Claude from auto-loading |
| `user-invocable` | boolean | `true` | Set `false` to hide from `/` menu |
| `allowed-tools` | string/list | — | Restrict tools during skill execution |
| `model` | string | — | Override model (`sonnet` for operational, omit for analytical) |
| `effort` | string | inherit | `low`/`medium`/`high`/`max` (Opus 4.6 only) |
| `context` | string | — | `fork` to run in isolated subagent |
| `agent` | string | `general-purpose` | Subagent type when `context: fork` |
| `hooks` | object | — | Hooks scoped to skill lifecycle |
| `paths` | list/string | — | Glob patterns for auto-activation scope |

## String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed |
| `$ARGUMENTS[N]` / `$N` | Positional argument (0-based) |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Skill directory path |

## Skill Scopes & Priority

1. Enterprise (highest)
2. Personal (`~/.claude/skills/`)
3. Project (`.claude/skills/`)
4. Plugin (lowest, namespaced `plugin:skill`)

## Invocation Model

| Frontmatter | User | Claude | When loaded |
|---|---|---|---|
| (default) | Yes | Yes | Description always, full on invoke |
| `disable-model-invocation: true` | Yes | No | Not in context |
| `user-invocable: false` | No | Yes | Description always |

## Progressive Disclosure

- **SKILL.md < 500 lines** — always in context on invoke
- **references/** — loaded on demand when Claude needs detail
- **templates/, scripts/** — executed, not loaded into context

## Best Practices

1. **Description as trigger** — Include "even if they don't explicitly say X" for intent matching
2. **Craftsmanship repetition** — Repeat quality expectations at key decision points
3. **Anti-patterns list** — Name specific failure modes explicitly
4. **Output format examples** — Show concrete expected shapes
5. **Input/Output contracts** — Define what skill expects and produces
6. **Pre-flight checklists** — Validate inputs before executing
7. **Self-audit section** — Verify before presenting results
8. **Error handling table** — Define recovery strategies

## Limitations

- Skills cannot directly invoke other `/commands` or tool calls
- Hook timeout: 10 min default
- Description truncation at 250 chars in listings
- `allowed-tools` creates permission boundaries, not capabilities
- Enterprise deny rules always take precedence

## Lifecycle Events

| Event | What happens |
|-------|---|
| SessionStart | Descriptions loaded |
| UserPromptSubmit | Claude evaluates skill match |
| PreToolUse | Hooks may modify/block |
| PostToolUse | Hooks run after execution |
| PreCompact | Skills re-summarized |

## Model Selection

- **`model: sonnet`** — Operational skills (scripts, CLIs, structured data)
- **Omit (opus)** — Analytical/creative (reasoning, architecture, judgment)
