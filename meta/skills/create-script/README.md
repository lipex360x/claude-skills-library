# create-script

Create bash scripts with the right level of structure — operational template for stateful/periodic scripts, direct for one-off utilities.

## Usage

```
/create-script
/create-script --name sync-tokens
```

## When to use

- Creating a new bash script in `.brain/scripts/`
- Building operational scripts that manage state (setup, sync, deploy, migration)
- Writing one-off utilities (the skill classifies and applies the right structure)

## How it works

1. **Classifies** the script as operational or utility based on 4 criteria
2. **Scaffolds** from `~/.brain/templates/operational-script.sh` (operational) or writes directly (utility)
3. **Implements** the logic with proper patterns (`set -e` safety, idempotency, colored output)
4. **Reviews** against a type-specific checklist
5. **Tests** the script (including idempotency for operational scripts)
6. **Registers** in STRUCTURE.md if applicable

## Key features

- Automatic classification: operational vs utility
- Template-based scaffolding with all safety patterns
- Bash 3.x compatibility (macOS default)
- `--check` dry-run, `--verbose`, `--help` flags for operational scripts
- Post-execution validation
- Idempotency verification

## Install

```bash
npx skills add lipex360x/claude-skills-library --skill create-script
```
