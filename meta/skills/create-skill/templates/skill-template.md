---
name: {{skill-name}}
# Required. Lowercase + hyphens, verb-subject pattern (e.g., push, create-skill, list-issues)
description: >-
  {{Action summary}} — {{key details}}. Use when the user says "{{trigger 1}}",
  "{{trigger 2}}", "{{trigger 3}}", or wants to {{action}} — even if they don't
  explicitly say "{{keyword}}."
# Required. Pushy trigger description — include WHAT it does, WHEN to activate,
# and the "even if they don't explicitly say X" pattern.
user-invocable: true
# Required. true for /commands, false for auto-triggered skills.
allowed-tools:
  - Read
  - Edit
  - Bash
# Required. Explicit tool list — only include tools the skill genuinely needs.
# Read-only skills: Read, Glob, Grep, Bash. File writers: add Edit, Write.
# User interaction: add AskUserQuestion. Subagents: add Agent.
argument-hint: {{hint}}
# Optional. Shows in autocomplete: /skill-name <hint>. Remove if no arguments.
---

# {{Skill Title}}

{{One-line summary of what this skill does and why it exists.}}

## Input contract

<!-- What the skill receives. Use the table for skills with arguments or context inputs.
     Mark as Skipped for skills that operate purely on current state. -->

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `{{name}}` | $ARGUMENTS | yes | {{rule}} | {{action — e.g., AUQ with suggestions}} |
| `{{flag}}` | $ARGUMENTS | no | Flag presence | — |

</input_contract>

<!-- OR if no input:
> _Skipped: "No input — operates on current directory state."_
-->

## Output contract

<!-- What the skill produces. List all persistent artifacts. -->

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| {{artifact}} | {{path or API}} | yes/no | {{format}} |

</output_contract>

<!-- OR if no persistent output:
> _Skipped: "No persistent output — conversational only."_
-->

## External state

<!-- Resources the skill reads or writes outside its own directory. -->

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| {{resource}} | {{path}} | R/W | {{format}} |

</external_state>

<!-- OR if self-contained:
> _Skipped: "N/A — self-contained, no external reads or writes."_
-->

## Pre-flight

<!-- Validations before any work begins. NEVER skip this section.
     Every skill validates something: tools available? files exist? context sufficient? -->

<pre_flight>

1. {{Check 1}} → if fails: "{{message}}" — stop.
2. {{Check 2}} → if fails: "{{message}}" — stop.

</pre_flight>

## Steps

### 1. {{First step}}

{{Instructions in imperative form. Explain the why behind constraints.
Reference files when detailed content is needed:}}

Read `references/{{guide}}.md` for the full guidelines.

### 2. {{Main work}}

{{The core workflow. Continue with numbered steps.}}

### {{N}}. Report

<!-- Always the last numbered step. Standardized structure. -->

<report>

- **What was done** — {{actions taken, artifacts created/modified}}
- **Audit results** — {{self-audit + content audit summary, or "all checks passed"}}
- **Errors** — {{issues encountered, or "none"}}

</report>

## Next action

{{What the user should do after this skill completes.}}

<!-- OR if nothing to suggest:
> _Skipped: "Session complete — no follow-up needed."_
-->

## Self-audit

<!-- Process verification before the Report step. NEVER skip this section. -->

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — all validations green, or user approved override
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — verify artifacts match Output contract
4. **Anti-patterns clean?** — scan execution for violations
5. **Approval gates honored?** — all required user confirmations obtained

If any check fails, note it in the Report.

</self_audit>

## Content audit

<!-- Verification of generated output. Required for content-producing skills.
     See references/content-audit-patterns.md for audit types and examples. -->

<content_audit>

Before finalizing output, verify:

1. {{Audit criterion 1 — e.g., "Facts correct? WebSearch to confirm claims"}}
2. {{Audit criterion 2 — e.g., "Format matches declared contract?"}}
3. {{Audit criterion 3 — e.g., "References and paths cited exist?"}}

</content_audit>

<!-- OR if skill does not generate verifiable content:
> _Skipped: "N/A — skill does not generate verifiable content (read-only / state management)."_
-->

## Error handling

<!-- Declared strategy per failure type. Required for skills with external calls. -->

| Failure | Strategy |
|---------|----------|
| {{failure type}} | {{strategy — e.g., AUQ with fix suggestion, stop, degrade gracefully}} |

<!-- OR if no external calls:
> _Skipped: "No external calls — no error surface."_
-->

## Anti-patterns

<!-- Specific failure modes. NEVER skip this section. Always its own section, never inline.
     Format: **Bold name.** Description — because reason. -->

- **{{Pattern name}}.** {{What goes wrong}} — because {{why it matters}}.
- **{{Pattern name}}.** {{What goes wrong}} — because {{why it matters}}.

## Guidelines

<!-- Principles and reasoning. NEVER skip this section. Separate from Anti-patterns.
     Format: **Bold principle.** Explanation — because context. -->

- **{{Principle}}.** {{Explanation}} — because {{context}}.
- **{{Principle}}.** {{Explanation}} — because {{context}}.
