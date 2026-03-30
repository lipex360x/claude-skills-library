---
name: create-script
description: >-
  Create bash scripts with the right level of structure — operational template
  for stateful/periodic scripts, direct for one-off utilities. Use when the user
  says "create a script", "novo script", "new script", "make a bash script",
  "cria um script", or wants to write a shell script in .brain/scripts/ — even
  if they don't explicitly say "script."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Create Script

Build bash scripts that are safe, idempotent, and structured — applying the operational template when the script manages state or runs periodically, and writing directly when it's a one-off utility.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| Script purpose | Conversation | yes | Clear description of what the script does | AUQ: "O que o script deve fazer?" |
| `--name` | $ARGUMENTS | no | Lowercase, hyphens, `.sh` suffix | Suggest correction |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Script file | `.brain/scripts/<name>.sh` (or user-specified) | yes | Bash with `set -euo pipefail` |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Operational template | `~/.brain/templates/operational-script.sh` | Read | Bash skeleton |
| Reference implementation | `~/.brain/scripts/setup.sh` | Read | Bash (for patterns) |
| STRUCTURE.md | `.brain/STRUCTURE.md` | Write | Markdown (if script goes in .brain/) |

</external_state>

## Pre-flight

<pre_flight>

1. Read `~/.brain/templates/operational-script.sh` to have the skeleton in context.
2. Target directory exists → if `.brain/scripts/`, confirm we're in the `.brain/` working directory (per CLAUDE.md rule). If not, alert.
3. Script name doesn't conflict with existing files → if it does: AUQ with options `["Sobrescrever", "Escolher outro nome"]`.

</pre_flight>

## Steps

### 1. Classify the script

Evaluate the request against these criteria:

| Criterion | Yes → Operational | No → Utility |
|-----------|-------------------|--------------|
| Manages state that can drift? (files, links, configs) | Template | Direct |
| Will be run again tomorrow? | Template | Direct |
| Needs dry-run? (errors break something) | Template | Direct |
| Is a wrapper or one-shot transform? | Direct | Direct |

Present the classification and reasoning to the user in a short table:

```
Script: <name>
Type: Operational / Utility
Reason: <1 sentence>
```

If the classification is ambiguous, AUQ: `["Operational (com template)", "Utility (direto)"]`.

### 2. Scaffold the script

**If Operational:**

1. Read `~/.brain/templates/operational-script.sh`.
2. Copy the skeleton, replacing:
   - `SCRIPT_NAME` → actual name and description in the header
   - `Usage:` block → relevant flags for this script
   - `Constants` → paths and values for this use case
3. Remove template sections that don't apply (e.g., `link_item` example).
4. Add custom flags to the `case` block if needed beyond `--check`/`--verbose`/`--help`.

**If Utility:**

Write the script directly. Minimal structure:
- `set -euo pipefail`
- Brief header comment (what + usage)
- Pre-flight checks for dependencies
- Logic
- No counters, no summary, no flags unless explicitly needed

### 3. Implement the logic

Fill in the script sections:

1. **Pre-flight checks** — verify dependencies, paths, permissions.
2. **Main logic** — the actual work. For operational scripts, use `$CHECK_MODE` guards on mutations.
3. **Validation** (operational only) — verify the result is correct after execution.

Read `~/.brain/scripts/setup.sh` for reference patterns when implementing:
- Idempotent operations (check before act)
- Colored output helpers
- Counter-based summaries
- `set -e` safe patterns (`if $VAR; then ...` not `$VAR && ...`)

### 4. Review

Verify the script against the checklist:

| Check | Operational | Utility |
|-------|-------------|---------|
| `set -euo pipefail` | Required | Required |
| Header with usage | Required | Required |
| `--help` flag | Required | Optional |
| `--check` dry-run | Required | N/A |
| `--verbose` flag | Required | N/A |
| Colored output helpers | Required | Optional |
| Counters + summary | Required | N/A |
| Post-execution validation | Required | N/A |
| Bash 3.x compatible (no associative arrays) | Required | Required |
| `if/then` instead of `$VAR && cmd` | Required | Required |
| Quoted paths with spaces | Required | Required |
| No hardcoded absolute paths (use variables) | Required | Required |

Fix any gaps before proceeding.

### 5. Test

1. Run the script with `--help` (operational) or no args to verify it doesn't crash.
2. Run with `--check` (operational) to verify dry-run output.
3. Run normally and verify the result.
4. Run a second time to verify idempotency (operational only).

### 6. Register

If the script was created in `.brain/scripts/`:
- Update `.brain/STRUCTURE.md` with the new script entry under `### scripts/`.

Make the script executable: `chmod +x <path>`.

### 7. Report

<report>

- **Script created** — `<path>` (`<type>`: operational/utility)
- **Features** — flags supported, key behaviors
- **Tests** — pass/fail summary
- **Registration** — STRUCTURE.md updated (or N/A)

</report>

## Next action

Test the script in a real scenario, or run `setup.sh --self-test` as a reference for adding self-tests to operational scripts.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Classification correct?** — operational vs utility matches the criteria table
2. **Template applied?** — operational scripts use the full skeleton, utilities don't
3. **All checks pass?** — review checklist has no gaps
4. **Tests ran?** — script executed successfully at least once
5. **Idempotent?** — operational scripts produce same result on second run
6. **Registered?** — STRUCTURE.md updated if script is in .brain/

</self_audit>

## Content audit

<content_audit>

Before finalizing, verify the generated script:

1. **Skeleton structure valid?** — operational scripts have all template sections (flags, helpers, counters, summary)
2. **`set -e` safe?** — no `$VAR && cmd` patterns that would exit on false
3. **Paths quoted?** — all file paths handle spaces correctly
4. **Bash 3.x compatible?** — no associative arrays, no `${var,,}` lowercasing, no `|&` pipe

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Template file missing | Error: "Template not found at ~/.brain/templates/operational-script.sh — run setup.sh" |
| Target directory doesn't exist | Create it after AUQ confirmation |
| Script already exists | AUQ: overwrite or rename |
| Script fails on test run | Show error output, fix, re-test |

## Anti-patterns

- **Applying the template to utilities.** A 10-line wrapper doesn't need flags, counters, and a summary — because over-engineering simple scripts makes them harder to read and maintain.
- **Skipping the template for operational scripts.** A stateful script without `--check` or validation will silently drift — because the whole point of the template is catching problems before they happen.
- **Using `$VAR && cmd` with `set -e`.** When `$VAR` is false, bash exits the entire script — because `&&` returns the exit code of the left side, and `set -e` treats non-zero as fatal. Always use `if $VAR; then cmd; fi`.
- **Hardcoding absolute paths.** `/Users/lipex360/...` breaks on other machines — because the script should work anywhere via variables like `$HOME`, `$SCRIPT_DIR`, or env overrides.
- **Forgetting `chmod +x`.** The script won't run without execute permission — because bash requires it unless explicitly called via `bash script.sh`.

## Guidelines

- **Classification drives structure.** The first decision (operational vs utility) determines everything else — because applying the wrong template wastes effort in both directions.
- **Reference implementation over documentation.** When in doubt about a pattern, read `setup.sh` — because it's a working example with all patterns applied and tested, more reliable than abstract rules.
- **Idempotency is non-negotiable for operational scripts.** Running twice must produce the same result — because these scripts will be run on new machines, after git pulls, and by cron jobs where "run again" is the recovery strategy.
- **Bash 3.x compatibility.** macOS ships bash 3.x by default — because requiring bash 5 means the user needs to install it first, and the script should work out of the box.
