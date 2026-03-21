---
name: {{skill-name}}
description: {{Pushy description — include WHAT it does, WHEN to activate, and "even if they don't explicitly say X" where appropriate}}
user-invocable: true
---

# {{Skill Title}}

{{One-line summary of what this skill does and why it exists.}}

## Usage

{{How the user invokes it, what arguments it accepts, what input it expects.}}

## Input contract

### Required inputs

| Name | Source | Validation |
|------|--------|------------|
| `{{name}}` | `args` | {{validation rule, e.g., "non-empty, kebab-case"}} |
| `{{context}}` | environment | {{e.g., "must be inside a git repo"}} |

### Optional inputs

| Name | Default | Description |
|------|---------|-------------|
| `{{flag}}` | `{{default}}` | {{what it controls}} |

**With arguments:** `/my-skill some-name --verbose` → skill reads `some-name` from args, `--verbose` as flag.
**From context:** `/my-skill` → skill reads current branch, directory, or git state as implicit input.

Validate all required inputs in Step 1 before doing any work. See `references/error-handling-patterns.md`.

## Steps

### 1. {{First phase}}

{{Instructions in imperative form. Explain the why behind constraints.}}

### 2. {{Second phase}}

{{Continue with numbered steps. Reference files when detailed content is needed:}}

Read `references/detailed-guide.md` for the full guidelines.

### 3. {{Final phase}}

{{Verification, output, presentation to user.}}

## Guidelines

{{Reasoned constraints — explain why each one matters. Name specific anti-patterns.}}
