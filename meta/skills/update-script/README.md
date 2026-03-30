# update-script

Audit and upgrade existing bash scripts to follow operational patterns — add missing flags, dry-run, validation, idempotency, and colored output.

## Usage

```
/update-script path/to/script.sh
/update-script
```

If no path is provided, lists scripts in `.brain/scripts/` for selection.

## When to use

- An existing script lacks `--check`, `--verbose`, or `--help`
- A script has safety issues (`$VAR && cmd` with `set -e`, unquoted paths)
- You want to bring a script up to the operational template standard
- A script works but feels fragile or hard to debug

## How it works

1. **Reads** the target script completely
2. **Classifies** as operational or utility
3. **Audits** against a comprehensive checklist (safety + structure)
4. **Proposes** prioritized changes (safety first, then structure, then polish)
5. **Applies** approved changes incrementally with testing between steps
6. **Reports** before/after audit comparison

## Key principles

- **Preserve first.** Existing logic is wrapped in new structure, never rewritten
- **Incremental changes.** Each priority level is applied and tested separately
- **Template is a floor.** Custom features beyond the template are preserved
- **Classify before acting.** Utilities get safety fixes only, not full template

## Install

```bash
npx skills add lipex360x/claude-skills-library --skill update-script
```
