# create-command

Step-by-step guide for building Claude Code slash commands -- from frontmatter fields to instruction writing.

## Trigger phrases

- "create a command"
- "new command"
- "add a slash command"
- "improve a command"
- Also activates when the user wants to build a new `/command` -- even without explicitly saying "command"

## How it works

1. **Understand the intent** -- Asks what the command should do, whether it takes arguments, and who can invoke it (user-only or Claude too)
2. **Choose frontmatter fields** -- Walks through `description`, `argument-hint`, `disable-model-invocation`, `allowed-tools`, and `context` based on the command's needs
3. **Write the body** -- Drafts concise, imperative instructions (typically 5-20 lines) following best practices
4. **Determine location** -- Asks whether the command should be local (project) or global (`.brain/`)
5. **Review** -- Validates the command against a checklist before writing the file

> [!TIP]
> If your command needs more than 30 lines of instructions, it probably should be a **skill** instead. The skill includes a comparison table to help you decide.

## Usage

```
/create-command
```

Tell Claude what you want the command to do, and it will guide you through each decision -- frontmatter fields, body content, and file placement.

**Example:** "I want a command that runs my test suite and shows only failures" will produce a focused `.md` file with the right frontmatter and imperative instructions, placed in the location you choose.

## Command vs Skill

| Use a **command** when... | Use a **skill** when... |
|---|---|
| Single, focused action | Multi-step workflow |
| < 30 lines of instructions | Needs references, templates, scripts |
| Always user-invoked (`/name`) | Should auto-trigger by description |
| No subagents needed | Coordinates subagents |

## Directory structure

```
create-command/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill create-command
```
