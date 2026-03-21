# Error Handling Patterns

Three categories of defensive patterns every skill should consider. Each prevents a class of failures that produce confusing or silent errors.

## 1. Dependency check

**When to use:** The skill relies on an external tool, CLI command, or MCP server that may not be installed.

**Pattern:**

```markdown
### 1. Verify dependencies

Before proceeding, check that the required tools are available:

- Run `which gh` to verify GitHub CLI is installed
- If missing, use `AskUserQuestion` with the message:
  "GitHub CLI (`gh`) is required but not found. Install it: https://cli.github.com/"
  Options: `["I've installed it, retry", "Cancel"]`
- Do NOT proceed until the dependency is confirmed
```

**Anti-pattern it prevents:** Skill runs multiple steps, then fails mid-execution with a cryptic "command not found" error — wasting time and leaving partial state.

## 2. Input validation

**When to use:** The skill requires user-provided arguments, context from the environment (branch name, file path), or data from a previous step.

**Pattern:**

```markdown
### 1. Validate inputs

Check required inputs before doing any work:

- `args` must contain a skill name in kebab-case (e.g., `my-skill`). If missing or malformed:
  "Expected a skill name in kebab-case (e.g., `my-skill`). Got: `{{actual}}`"
- Current directory must be a git repository. If not:
  "This skill must run inside a git repository."

Do NOT silently default missing required inputs — fail with a clear message.
```

**Anti-pattern it prevents:** Skill proceeds with empty or malformed input, produces garbage output, and the user has to trace back to figure out what went wrong.

## 3. Tool/API failure

**When to use:** The skill calls tools (Bash, Read, API endpoints, MCP tools) that can fail due to network issues, permissions, or unexpected state.

**Pattern:**

```markdown
### 3. Create the branch

Run `git checkout -b feat/{{name}}`.

If this fails:
- **Branch already exists** → ask the user: "Branch `feat/{{name}}` already exists."
  Options: `["Switch to it", "Delete and recreate", "Cancel"]`
- **Dirty working tree** → show the status and ask:
  "You have uncommitted changes. Stash or commit before proceeding."
  Options: `["Stash and continue", "Cancel"]`
- **Other error** → surface the full error message and stop

Do NOT retry non-idempotent operations (commits, pushes, issue creation) automatically.
Only retry idempotent reads (file reads, API GETs) up to once.
```

**Anti-pattern it prevents:** Skill silently swallows errors or retries destructive operations, creating duplicate issues, double commits, or corrupted state the user discovers later.
