---
name: update-docs
description: >-
  Update .docs/architecture.md and .docs/project.md to reflect code changes.
  Use when the user says "update docs", "update architecture", "sync
  documentation", "document changes", or wants docs current — even if they
  don't explicitly say "docs."
disable-model-invocation: true
model: sonnet
effort: medium
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---

# Update Docs

Update `.docs/architecture.md` and `.docs/project.md` with changes from the current branch. Scoped to `git diff main..HEAD` — only documents what changed, never rewrites entire files.

## Pre-flight

<pre_flight>

1. Current directory is a git repo → if not: "Must run inside a git repo." — stop.
2. `.docs/architecture.md` exists → if not: "No `.docs/architecture.md` found. Run `/start-new-project` to scaffold `.docs/`." — stop.
3. `.docs/project.md` exists → if not: warn "`.docs/project.md` not found — will only update architecture.md."
4. Branch is not `main` → if on main: "Nothing to document — you're on main." — stop.
5. Diff is not empty → `git diff main..HEAD --stat` → if empty: "No changes to document." — stop.
6. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present pre-flight results as a markdown table: **Check** | **Status** | **Detail**.

</pre_flight>

## Steps

### 1. Collect the diff

Read the full diff and changed file list:

```bash
git diff main..HEAD --stat
git diff main..HEAD --name-only
```

Read the current `.docs/architecture.md`. If `.docs/project.md` exists, read it too.

### 2. Run the update checklist

Read `references/update-checklist.md`. For each changed file, evaluate every checklist item. Produce a summary table:

| Category | Changes found | Target doc | Section to update |
|----------|--------------|------------|-------------------|

If no checklist items match (pure refactor, formatting, test-only changes), report "No documentation updates needed" and skip to Step 5.

### 3. Update architecture.md

For each matched category, apply **surgical edits** to `.docs/architecture.md`:

- **Add** new sections or entries for new routes, patterns, schemas, scripts, config vars, or directory changes.
- **Modify** existing sections where behavior or structure changed.
- **Never delete** sections not touched by the diff.
- **Never rewrite** the entire document — use the Edit tool for targeted changes.

If the architecture.md structure doesn't have a section for the change (e.g., no "Config" section but new env vars were added), create the section following the document's existing style.

### 4. Evaluate project.md changes

`.docs/project.md` covers domain concepts, business rules, user roles, and boundaries. It changes **rarely**.

Scan the diff for:
- New domain terms or redefined existing ones
- New or modified business rules
- New user roles or permission changes
- Scope boundary changes

**If no domain-level changes found:** skip — report "project.md: no changes needed."

**If domain-level changes found:** draft the edits, then present them via `AskUserQuestion` with the message: "project.md change detected — review carefully before applying." Options: `["Apply changes", "Skip project.md update"]`. Only apply if approved.

### 5. Update drift detector

Compute a hash of the directory structure and update the footer of `.docs/architecture.md`:

```bash
find . -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './.docs/*' | sort | sha256sum | cut -c1-12
```

Update or add at the bottom of architecture.md:

```
<!-- arch-hash: <hash> -->
<!-- last-updated: YYYY-MM-DD -->
```

Use today's date. If the hash comment already exists, replace it. If not, append it.

### 6. Report

Present concisely:
- **architecture.md** — sections added/modified (list them) or "no changes"
- **project.md** — changes applied, skipped, or "no changes needed"
- **Drift detector** — hash value and date updated

## Error handling

| Failure | Strategy |
|---------|----------|
| No `.docs/` directory | "Run `/start-new-project` to scaffold `.docs/`." — stop |
| No diff against main | "No changes to document." — stop |
| On main branch | "Switch to a feature branch first." — stop |
| architecture.md parse error | Warn user, apply changes best-effort, flag for manual review |
| project.md AUQ declined | Skip project.md, continue with architecture.md and drift detector |

## Anti-patterns

- **Rewriting architecture.md from scratch instead of surgical edits.** The document has accumulated context from many merges. A full rewrite destroys that history and introduces drift in sections unrelated to the current change.
- **Updating project.md for code-level changes.** project.md is for domain concepts (business rules, user roles, boundaries). A new API route or refactored module does NOT belong in project.md — it belongs in architecture.md.
- **Adding implementation details that will be stale next commit.** Document patterns and structure, not specific line numbers, variable names, or temporary states. "Auth uses JWT middleware" is good. "Token validation is on line 47 of auth.ts" is bad.
- **Skipping the drift detector hash update.** The hash is how other skills detect staleness. Without it, `/start-issue` cannot know if architecture.md is current, leading to unnecessary codebase exploration (~50k tokens wasted).
- **Deleting sections not touched by the diff.** A section might look outdated, but if the diff didn't change it, leave it. The next `/update-docs` run for the relevant branch will handle it.

## Next action

> Run `/review --final` to validate the documentation changes and any remaining code.
