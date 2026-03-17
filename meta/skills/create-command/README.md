# create-command

> Guide the user through creating or improving Claude Code slash commands.

Step-by-step guide for building Claude Code slash commands — from frontmatter fields to instruction writing. Commands are single `.md` files with YAML frontmatter, simple by design.

## Usage

```text
/create-command
```

> [!TIP]
> Also activates when you say "create a command", "new command", "add a slash command", "improve a command", or want to build a new `/command`.

## How it works

1. **Understand the intent** — Asks what the command should do, whether it takes arguments, and who can invoke it
2. **Choose frontmatter fields** — Walks through `description`, `argument-hint`, `disable-model-invocation`, `allowed-tools`, and `context`
3. **Write the body** — Drafts concise, imperative instructions (typically 5-20 lines)
4. **Determine location** — Asks whether the command should be local (project) or global (`.brain/`)
5. **Review** — Validates against a checklist before writing the file

> [!TIP]
> If your command needs more than 30 lines of instructions, it probably should be a **skill** instead. The skill includes a comparison table to help you decide.

## Directory structure

```text
create-command/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-command
```
