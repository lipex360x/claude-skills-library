---
name: create-command
description: Guide the user through creating or improving Claude Code slash commands — from frontmatter fields to instruction writing. Use this skill when the user mentions "create a command", "new command", "add a slash command", "improve a command", or wants to build a new /command — even if they don't explicitly say "command."
user-invocable: true
---

# Create Command

Step-by-step guide for building Claude Code slash commands. Commands are single `.md` files with YAML frontmatter — simple by design.

## Process

### 1. Understand the intent

Ask the user:
- What should the command do?
- Does it take arguments? (e.g., `/cmd <issue-number>`)
- Should only the user invoke it, or can Claude invoke it too?

Use `AskUserQuestion` with concrete options when clarifying ambiguous decisions.

### 2. Choose the frontmatter fields

Read `templates/command.md` in `~/www/claude/.brain/templates/` for the full field reference. Key fields:

```yaml
---
description: What the command does (shows in /help autocomplete)
argument-hint: <arg1> [optional-arg]     # shown during autocomplete
disable-model-invocation: true            # only user can invoke
allowed-tools: Bash, Read, Grep           # tools auto-allowed without prompts
---
```

**Decide each field:**
- `description` — always include. Concise, starts with verb
- `argument-hint` — include if the command takes arguments
- `disable-model-invocation` — set `true` for commands the user explicitly triggers (most cases)
- `allowed-tools` — list only the tools the command actually needs
- `context: fork` — only if the command should run in a subagent (rare)

### 3. Write the body

Commands are short — typically 5-20 lines. Follow these principles:

- **Imperative form.** "Run the tests", "Read the file", not "You should run..."
- **Be specific.** Include exact paths, exact tool names, exact formats
- **Reference `$ARGUMENTS`** when the command takes input
- **One job.** A command does one thing well. If it needs 50+ lines, it should probably be a skill instead

### 4. Determine location

Use `AskUserQuestion` with options `["Local (this project)", "Global (.brain/)"]`.

- **Local:** Write to `.claude/commands/<name>.md` in the project
- **Global:** Write to `~/www/claude/.brain/commands/<name>.md` and update `~/www/claude/.brain/STRUCTURE.md` (add entry to `commands/` section)

### 5. Review

Validate before finalizing:

- [ ] Description is concise and starts with a verb?
- [ ] `allowed-tools` lists only what's needed (principle of least privilege)?
- [ ] Body uses imperative form?
- [ ] Body is under 30 lines? (if longer, consider making it a skill)
- [ ] `$ARGUMENTS` used correctly if command takes input?
- [ ] No hardcoded paths that should be relative?

Present the review to the user before writing the file.

## Command vs Skill — when to use which

| Use a **command** when... | Use a **skill** when... |
|---|---|
| Single, focused action | Multi-step workflow |
| <30 lines of instructions | Needs references, templates, scripts |
| Always user-invoked (`/name`) | Should auto-trigger by description |
| No subagents needed | Coordinates subagents |

## Anti-patterns

- **Overloaded commands.** If you're adding flags and branching logic, it's a skill
- **Missing `allowed-tools`.** Forces the user to approve every tool call manually
- **Vague descriptions.** "Does stuff with git" → "Show compact git status with branch and stash info"
- **Hardcoded absolute paths.** Use `~/.brain/` or relative paths, not `/Users/someone/`
