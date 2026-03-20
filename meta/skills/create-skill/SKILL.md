---
name: create-skill
description: Guide the user through creating, reviewing, or improving Claude Code skills — from structuring SKILL.md files to writing effective descriptions, designing progressive disclosure, and launching subagents. Use this skill whenever the user mentions "create a skill", "improve a skill", "update a skill", "skill quality", "skill best practices", "how to write a skill", or wants to build or update a /command — even if they don't explicitly say "skill."
user-invocable: true
---

# Create Skill

Step-by-step guide for building high-quality Claude Code skills. Distilled from Anthropic's official skill repository and hands-on experience shipping production skills.

## Create or update

This skill handles both **new skills** and **updates to existing skills**. When the user references existing skills, read them first and apply changes following the same quality standards. Decide whether to edit in place or recreate based on the scope of changes. The user often mixes multiple requests (new + edits) in a single prompt — handle all of them.

## Process

### 1. Understand the intent

Ask the user:
- What should the skill do? (the core action)
- When should it activate? (trigger contexts)
- Is it user-invocable (`/skill-name`) or auto-triggered by description matching?

Use `AskUserQuestion` with concrete options when clarifying ambiguous decisions — it's faster than freeform conversation and keeps the flow moving.

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

### 9. Update READMEs

After the skill passes review, update two READMEs using the `/create-readme` skill:

1. **Skill README** — Run `/create-readme` targeting the skill's own directory. This creates or updates the skill's `README.md` with what it does, how to trigger it, and how to install it.
2. **skills-library README** — Run `/create-readme` targeting the `skills-library/` root directory. This keeps the master catalog of all skills up to date with any new or changed skills.

Both READMEs must be updated on every create or update — never skip this step.

## Frontmatter reference

```yaml
---
name: skill-name          # Required. Lowercase + hyphens, matches directory name
description: ...          # Required. The trigger mechanism — be pushy and specific
user-invocable: true      # Set true if the user can call it directly via /skill-name
compatibility: ...        # Optional. Environment requirements (rarely needed)
---
```

## What doesn't work in skills

These are hard-won lessons — each one caused real debugging time:

- **`@` imports** — Only resolved in CLAUDE.md files, not in SKILL.md. Use Read tool instructions instead.
- **Cross-skill dependencies** — Each skill must be fully self-contained. You can't call one skill from another.
- **Overly specific instructions** — Skills may be used across many inputs. Avoid rules tied to one test case. Generalize the principle, not the specific fix.
- **Long SKILL.md without hierarchy** — Walls of text get lost in context. Use headers, numbered steps, and extract detail to references.
