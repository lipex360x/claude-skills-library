---
name: create-skill
description: Guide the user through creating, reviewing, or improving Claude Code skills — from structuring SKILL.md files to writing effective descriptions, designing progressive disclosure, and launching subagents. Use this skill whenever the user mentions "create a skill", "improve a skill", "update a skill", "skill quality", "skill best practices", "how to write a skill", or wants to build or update a /command — even if they don't explicitly say "skill."
user-invocable: true
---

# Create Skill

Step-by-step guide for building high-quality Claude Code skills. Distilled from Anthropic's official skill repository and hands-on experience shipping production skills.

## Create or update

This skill handles both **new skills** and **updates to existing skills**. When the user references existing skills, read them first and apply changes following the same quality standards. Decide whether to edit in place or recreate based on the scope of changes. The user often mixes multiple requests (new + edits) in a single prompt — handle all of them.

**Updates follow the same process as creation.** Even for small changes, every step applies — description check (Step 3), quality techniques (Step 5), review checklist (Step 7), READMEs (Step 9), STRUCTURE.md (Step 10), and push (Step 11). The temptation is to skip steps for "just a small edit" — this is how skills drift from quality standards. Steps that are genuinely not applicable (e.g., subagents for a skill without them) can be marked N/A in the review, but they must still be evaluated, not silently skipped.

## Process

### 1. Understand the intent

#### 1.0 Spec detection (automatic)

Before asking intent questions, check if a `/plan-skill` spec is available:

1. **Check args** — If the user passed a file path as an argument, try to read it as a spec.
2. **Check downloads/** — If no args, glob for `downloads/*-spec.md`. If multiple matches, present them via `AskUserQuestion` and let the user pick (or choose "none — start fresh").
3. **Validate** — A valid spec must contain these headers: `## Meta`, `## Purpose`, `## Trigger`, `## Workflow`, `## Guardrails`, `## Decisions Log`. If any is missing, warn and fall back to normal flow.

When a valid spec is found, present a summary table to the user:

```
| Field       | Value from spec       |
|-------------|-----------------------|
| Name        | (from Meta)           |
| Plugin      | (from Meta)           |
| Invocable   | (from Meta)           |
| Purpose     | (first line of Purpose > What it does) |
| Scope       | (first line of Purpose > What it does NOT do) |
```

Use `AskUserQuestion` with options `["Confirm — use this spec", "Reject — start fresh"]`. If confirmed, load all spec decisions as defaults and skip to Step 1.1 (scope classification is usually N/A with a spec unless the user adds extra requests). If rejected, proceed with normal flow below.

Read `references/spec-contract.md` for the full mapping of spec sections to create-skill steps and which steps can be accelerated vs. which are never skippable.

#### 1.0a Normal flow (no spec)

Ask the user:
- What should the skill do? (the core action)
- When should it activate? (trigger contexts)
- Is it user-invocable (`/skill-name`) or auto-triggered by description matching?

Use `AskUserQuestion` with concrete options when clarifying ambiguous decisions — it's faster than freeform conversation and keeps the flow moving.

#### 1.1 Classify scope (mandatory vs optional)

When the user's request contains **multiple actions** (e.g., "rename X, add Y, update Z"), break it into discrete steps and classify each one. This prevents silently skipping steps the user considers mandatory.

**Process:**

1. Parse the request into a numbered list of discrete actions
2. For each action, suggest whether it seems **mandatory** or **optional** based on the request wording — direct instructions ("rename", "add", "change") are likely mandatory; vague mentions ("maybe also", "if possible", "could also") are likely optional
3. Present via `AskUserQuestion` with `multiSelect: true` so the user selects which are mandatory. Pre-label suggestions in the option descriptions:

```
question: "Which of these steps are mandatory? (unselected = optional, can be skipped if not applicable)"
options:
  - label: "1. Rename skill to create-excalidraw"
    description: "Suggested: Mandatory — direct instruction"
  - label: "2. Add design aesthetics reference"
    description: "Suggested: Mandatory — direct instruction"
  - label: "3. Trim SKILL.md to under 500 lines"
    description: "Suggested: Optional — quality improvement, not explicitly requested"
```

4. After the user responds, mark each step internally:
   - **Mandatory** steps: execute unconditionally, never skip or simplify
   - **Optional** steps: execute if applicable, can be deprioritized if they conflict with mandatory steps

**When to skip this gate:** If the request is a single, unambiguous action (e.g., "create a skill that does X"), there's nothing to classify — proceed directly to step 2.

### 2. Design the structure

```
skill-name/
├── SKILL.md              # Required. YAML frontmatter + lean instructions (<500 lines)
├── templates/            # Optional. Starter structures, output formats
├── references/           # Optional. Detailed docs loaded on demand via Read tool
├── scripts/              # Optional. Executable code for deterministic tasks
└── assets/               # Optional. Static resources (fonts, images, data files)
```

Only `SKILL.md` is required. Everything else is loaded on demand. Read `references/progressive-disclosure.md` for the three-tier architecture that keeps token costs low.

### 3. Write the description

The description is the single most important design decision — Claude decides whether to activate a skill based solely on `name` + `description`.

Read `references/description-patterns.md` for examples and the "pushy" technique that prevents undertriggering.

### 4. Write the SKILL.md body

Keep it under 500 lines. These principles produce measurably better results:

- **Imperative form.** "Parse the config", "Read the template", "Launch the agents". Not "You should parse..." or "The skill will...".
- **Explain the why.** Reasoning beats rigid rules. Instead of "NEVER do X", write "Avoid X because Y — this causes Z". LLMs handle edge cases better when they understand the reasoning behind a constraint.
- **Numbered steps.** Give the model a clear execution path. Headers for major phases, numbers for sequential steps within each phase.
- **Explicit output formats.** When the skill produces structured output (a brief, a spec, a report), show the expected format with an example — the model follows concrete shapes better than abstract descriptions.
- **Error handling.** Skills that call external tools, APIs, or check dependencies should handle failures explicitly. Read `references/error-handling-patterns.md` for patterns: dependency checks via AUQ, input validation with clear messages, and tool failure recovery.

If approaching 500 lines, move detailed content to `references/` with a pointer:

```markdown
Read `references/quality-standards.md` for the full guidelines.
```

This is NOT an `@` import — it's an instruction for the agent to use the Read tool. `@` imports only work in CLAUDE.md, not in SKILL.md.

### 5. Apply quality techniques

Read `references/quality-techniques.md` for the full set. The key ones:

- **Craftsmanship repetition.** Repeat quality expectations at multiple points in the instructions. Each repetition reinforces the quality bar — this is intentional prompt engineering, not redundancy.
- **Anti-patterns list.** Name the specific failure modes to avoid. Generic instructions ("make it look good") produce generic output.
- **Refinement over addition.** Build in an explicit "polish, don't add" step. AI tends to add more elements when the answer is refining what exists.

### 6. Handle subagents (if applicable)

Subagents start with a blank context — they don't inherit the parent conversation. This has significant implications for how you structure prompts and coordinate work.

Read `references/subagent-patterns.md` for practical patterns, race conditions to avoid, and the two-phase build approach learned from production experience.

### 7. Review against checklist

Read `references/review-checklist.md` and validate every item. Present the results to the user before finalizing.

### 8. Register the skill

If the skill was created inside `skills-library/`, run `setup.sh` to create the symlink in `~/.claude/skills/` so Claude Code discovers it:

```bash
bash ~/.brain/scripts/setup.sh
```

Without this step, the skill won't appear in `/` autocomplete in new sessions.

### 8b. Test the skill

Invoke the skill with realistic input before moving on. A skill that passes review but fails on real input is worse than no skill — it erodes trust in the entire library.

1. **Functional test** — Run the skill with a realistic scenario that exercises its main workflow. Verify it activates, follows the expected steps, and produces the expected output format.
2. **Activation test** — Test with at least 3 natural phrases that should trigger the skill. Vary the wording: use the exact `/command` name, a natural description of the action, and a partial or indirect reference. All three must activate the skill. If any fails, revise the description (Step 3) and retest.
3. **Edge case** — Try one input that's just outside the skill's intended scope. Verify it either handles it gracefully or doesn't activate (no silent failures, no crashes).

If any test fails, fix the issue before proceeding. Do not defer fixes to a follow-up — the skill is not done until it works.

### 9. Update READMEs

After the skill passes review, update two READMEs using the `/create-readme` skill:

1. **Skill README** — Run `/create-readme` targeting the skill's own directory. This creates or updates the skill's `README.md` with what it does, how to trigger it, and how to install it.
2. **skills-library README** — Run `/create-readme` targeting the `skills-library/` root directory. This keeps the master catalog of all skills up to date with any new or changed skills.

Both READMEs must be updated on every create or update — never skip this step.

### 10. Update STRUCTURE.md files

Check if the changes require updates to structure files — this applies when skills were created, moved, renamed, or deleted:

1. **`skills-library/STRUCTURE.md`** — Read it and check if the skill is listed. If not (new skill) or if its location changed, update the entry. If a skill was removed, delete the entry.
2. **`.brain/STRUCTURE.md`** — Only update if the change affects `.brain/` structure (rare for skill-only changes, but check).

Skip this step if the changes are purely content edits to existing skills (no structural changes).

### 11. Push to GitHub

After all updates are complete (skill, READMEs, STRUCTURE.md), push both repos automatically using `/push -y`:

1. **`skills-library/`** — Stage all files touched in this session, commit with a conventional message, and push.
2. **`.brain/`** — If any `.brain/` files were modified (STRUCTURE.md, CLAUDE.md, etc.), stage, commit, and push. If `.brain/` has no changes, skip.

This is the final step — the skill creation/update is not done until changes are pushed to GitHub.

## Naming convention

Skill names follow the **verb-subject** pattern: the verb describes the action, the subject describes what it acts on. This makes names scannable and consistent across the library.

- `download-video` (not `video-download`)
- `create-skill` (not `skill-creator`)
- `review-postgres` (not `postgres-review`)
- `check-gmail` (not `gmail-checker`)

Format: lowercase, hyphens, verb first. The name must match the directory name.

## Frontmatter reference

```yaml
---
name: verb-subject        # Required. Lowercase + hyphens, verb-subject pattern, matches directory name
description: ...          # Required. The trigger mechanism — be pushy and specific
user-invocable: true      # Set true if the user can call it directly via /skill-name
compatibility: ...        # Optional. Environment requirements (rarely needed)
---
```

## What doesn't work in skills

These are hard-won lessons — each one caused real debugging time:

- **`@` imports** — Only resolved in CLAUDE.md files, not in SKILL.md. Use Read tool instructions instead.
- **Cross-skill dependencies** — Each skill must be fully self-contained. You can't call one skill from another.
- **Shared state without contracts** — When a skill reads or writes shared state (filesystem paths, config files like `project-settings.json`, manifests like `STRUCTURE.md`), it must document the contract: what it reads, what it writes, and the expected format. Without this, one skill's update silently breaks another because neither declared the dependency. Add an `## External state` section to the SKILL.md listing each shared resource, its path, and whether the skill reads or writes it.
- **Overly specific instructions** — Skills may be used across many inputs. Avoid rules tied to one test case. Generalize the principle, not the specific fix.
- **Long SKILL.md without hierarchy** — Walls of text get lost in context. Use headers, numbered steps, and extract detail to references.
