---
name: update-script
description: >-
  Audit and upgrade existing bash scripts to follow operational patterns —
  add missing flags, dry-run, validation, idempotency, and colored output.
  Use when the user says "update script", "upgrade script", "improve script",
  "fix this script", "ajusta esse script", "melhora o script", "add --check
  to this script", or wants to bring an existing script up to standard — even
  if they don't explicitly say "update."
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
argument-hint: "[script-path]"
---

# Update Script

Audit an existing bash script against the operational template standard and upgrade it — adding missing features, fixing safety issues, and preserving existing logic.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| Script path | $ARGUMENTS or AUQ | yes | File exists, is `.sh` | AUQ: list scripts in .brain/scripts/ |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Updated script | Same path as input | yes | Bash |
| Audit report | stdout | no | Markdown table |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Operational template | `~/.brain/templates/operational-script.sh` | Read | Bash skeleton |
| Reference implementation | `~/.brain/scripts/setup.sh` | Read | Bash |

</external_state>

## Pre-flight

<pre_flight>

1. Read `~/.brain/templates/operational-script.sh` to have the skeleton in context.
2. Script file exists and is readable.
3. Script is bash (has `#!/usr/bin/env bash` or `#!/bin/bash` shebang).
4. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Read and classify

Read the target script completely. Classify it:

- **Operational** — manages state, runs periodically, benefits from full template
- **Utility** — one-off, simple wrapper, doesn't need template

Present the classification with reasoning. If the script is a utility and the user wants to upgrade it, AUQ: `["Aplicar template operacional mesmo assim", "Manter como utility, só corrigir problemas"]`.

### 2. Audit against checklist

Run the script through the full checklist. Present results as a table:

**Safety checks (all scripts):**

| Check | Status | Detail |
|-------|--------|--------|
| `set -euo pipefail` | PASS/FAIL | — |
| No `$VAR && cmd` with `set -e` | PASS/FAIL | Lines X, Y |
| Paths quoted for spaces | PASS/FAIL | Lines X, Y |
| Bash 3.x compatible | PASS/FAIL | Specific issue |
| No hardcoded absolute paths | PASS/FAIL | Lines X, Y |
| Shebang present | PASS/FAIL | — |
| Executable permission | PASS/FAIL | — |

**Operational checks (operational scripts only):**

| Check | Status | Detail |
|-------|--------|--------|
| `--help` flag | PASS/FAIL/MISSING | — |
| `--check` dry-run | PASS/FAIL/MISSING | — |
| `--verbose` flag | PASS/FAIL/MISSING | — |
| Colored output helpers | PASS/FAIL/MISSING | — |
| Counters + summary | PASS/FAIL/MISSING | — |
| Validation section | PASS/FAIL/MISSING | — |
| Idempotent operations | PASS/FAIL/MISSING | — |
| Unknown flag rejection | PASS/FAIL/MISSING | — |

### 3. Propose changes

Based on the audit, present a prioritized list of changes:

**Priority 1 — Safety** (always fix):
- `set -e` issues, unquoted paths, bash compatibility

**Priority 2 — Structure** (operational scripts):
- Missing flags, helpers, counters, summary, validation

**Priority 3 — Polish** (nice to have):
- Color auto-detection for pipes, verbose-only output helpers, header cleanup

AUQ: `["Aplicar tudo", "Só Priority 1", "Só Priority 1 e 2", "Deixa eu escolher"]`

If "Deixa eu escolher" → present multiSelect with individual items.

### 4. Apply changes

Apply the approved changes. Key principles:

- **Preserve existing logic.** Never rewrite working code just for style — wrap it in the new structure.
- **Add, don't replace.** Insert flag parsing, helpers, and summary around the existing logic.
- **Test after each major change.** Don't batch all changes and hope it works.

For operational upgrades, follow this order:
1. Add `set -euo pipefail` if missing
2. Fix `$VAR && cmd` patterns → `if/then`
3. Add flag parsing block (--check, --verbose, --help)
4. Add output helpers (info/ok/warn/error/dim)
5. Add counters
6. Wrap mutations in `$CHECK_MODE` guards
7. Add validation section
8. Add summary block

### 5. Test

1. Run with `--help` — verify usage output.
2. Run with `--check` — verify dry-run reports correctly.
3. Run normally — verify original behavior preserved.
4. Run a second time — verify idempotency (operational only).
5. Compare output before/after — no regressions in core logic.

### 6. Report

<report>

- **Script** — `<path>` classified as `<type>`
- **Audit results** — X/Y checks passed before, X/Y after
- **Changes applied** — bullet list of what was added/fixed
- **Tests** — pass/fail summary
- **Regressions** — any behavior changes (or "none")

</report>

## Next action

Run the script in production to verify, or add `--self-test` for automated regression testing (see `setup.sh --self-test` for reference).

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Original behavior preserved?** — core logic unchanged, only structure added
2. **All approved changes applied?** — nothing skipped from the approved list
3. **Tests passed?** — script runs correctly in all modes
4. **No regressions?** — output matches pre-upgrade behavior for normal operations
5. **Audit improved?** — more checks pass after upgrade than before

</self_audit>

## Content audit

<content_audit>

Before finalizing, verify:

1. **`set -e` safe?** — no `$VAR && cmd` patterns remain
2. **Flag parsing complete?** — all flags work, unknown flags rejected
3. **Counters accurate?** — summary reflects actual operations
4. **`--check` truly read-only?** — no mutations in dry-run mode

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Script not found | AUQ: list available scripts |
| Script is not bash | Report: "Not a bash script — this skill handles bash only" |
| Template missing | Error: "Run setup.sh first" |
| Test fails after upgrade | Revert the last change, report the issue |
| Script has syntax errors pre-upgrade | Report: fix syntax first, then re-run upgrade |

## Anti-patterns

- **Rewriting working code for style.** The goal is to add structure, not reformat — because rewriting risks introducing bugs in tested logic.
- **Applying operational template to utilities.** A 15-line wrapper doesn't need counters and a summary — because the overhead obscures the actual logic. Classify first, then decide.
- **Batching all changes.** Applying 8 changes at once and testing at the end — because when something breaks, you don't know which change caused it. Apply and test incrementally.
- **Removing existing features.** The script may have custom flags or behaviors that aren't in the template — because the template is a minimum standard, not a maximum. Preserve what works.
- **Skipping the second run test.** Idempotency bugs only show on repeated execution — because the first run always "works" since it starts from a known state.

## Guidelines

- **Audit before touching.** Present the full checklist results before proposing changes — because the user needs to understand the current state to make good decisions about what to fix.
- **Preserve, then enhance.** Wrap existing logic in new structure rather than replacing it — because the existing code has been tested in production, and new code hasn't.
- **Incremental application.** Apply changes one priority level at a time, testing between levels — because this catches regressions early and keeps the user informed.
- **The template is a floor, not a ceiling.** Scripts may have features beyond the template (custom flags, integrations, self-test) — because the template covers the minimum, and real scripts evolve beyond it.
