---
name: skill-authoring-guide
description: Best practices for writing high-quality Claude Code skills. Use this guide when creating, reviewing, or improving skills — including structuring SKILL.md files, writing effective descriptions, designing progressive disclosure, launching subagents, and avoiding common pitfalls. Activate whenever the user mentions "create a skill", "improve a skill", "skill quality", "skill best practices", or "how to write a skill."
user-invocable: true
---

# Skill Authoring Guide

A practical guide for writing high-quality Claude Code skills, distilled from analyzing Anthropic's official skill repository (github.com/anthropics/skills) and hands-on experience building skills.

Read this guide when creating or improving skills. It captures patterns that produce measurably better results and pitfalls that waste tokens or degrade output quality.

## Directory structure

```
skill-name/
├── SKILL.md              # Required. YAML frontmatter + lean instructions (<500 lines)
├── templates/            # Optional. Starter structures, HTML scaffolds, output formats
├── references/           # Optional. Detailed docs loaded into context on demand
├── scripts/              # Optional. Executable code for deterministic tasks
└── assets/               # Optional. Static resources (fonts, images, data files)
```

Only `SKILL.md` is required. Everything else is loaded on demand by the agent using the Read tool.

## Progressive disclosure (the core architecture)

Skills load in three tiers. This design keeps token costs low and context focused.

| Level | Content | Size | When loaded |
|-------|---------|------|-------------|
| **Metadata** | `name` + `description` | ~100 tokens | Always in context (all sessions) |
| **Instructions** | SKILL.md body | <500 lines | When the skill is activated |
| **Resources** | files in templates/, references/, scripts/ | Unlimited | On demand, when the agent reads them |

The implication: the description determines whether the skill activates. The SKILL.md body guides execution. Resources provide depth without bloating the activation payload.

## The description field

This is the single most important design decision. Claude decides whether to load a skill based solely on `name` + `description`.

### Make it "pushy"

Claude tends to **undertrigger** — it won't use a skill unless the match is obvious. Counter this by including specific trigger phrases and contexts, not just a dry summary.

**Weak:**
```yaml
description: Create a design system from a reference image.
```

**Strong:**
```yaml
description: Analyze a design image and create a full design system project with separated artboards. Use this skill whenever the user provides a reference image, screenshot, or mockup and wants to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns — even if they don't explicitly say "design system."
```

The "even if they don't explicitly say X" pattern is particularly effective.

### Include both WHAT and WHEN

The description should answer: "What does this skill do?" AND "In what situations should Claude activate it?"

## SKILL.md body

### Keep it lean

Under 500 lines. If you're approaching the limit, move detailed content to `references/` files and add a pointer:

```markdown
Read `references/agent-prompt.md` for the full prompt requirements and quality standards.
```

The agent will read the file when it reaches that step. This is NOT an `@` import — it's an instruction for the agent to use the Read tool. (`@` imports only work in CLAUDE.md, not in SKILL.md.)

### Explain the why, not rigid MUSTs

If you find yourself writing ALWAYS or NEVER in all caps, reframe it. Explain the reasoning so the model understands *why* and can make better judgment calls in edge cases.

**Rigid (less effective):**
```markdown
- NEVER navigate to the editor during the build
```

**Reasoned (more effective):**
```markdown
- Stay on the hub during the build. The user watches thumbnails appear progressively —
  navigating to the editor would break the visual feedback loop.
```

LLMs respond better to reasoning than rote instructions. The reasoning also helps when the model encounters situations the rule didn't anticipate.

### Use imperative form

Write instructions as direct commands: "Extract the color palette", "Read the template", "Launch agents in parallel". Not "You should extract..." or "The skill will...".

### Structure with clear steps

Number the steps. Use headers for major phases. This gives the model a clear execution path and makes it easy to reference specific steps ("go back to step 2").

### Define output formats explicitly

When the skill produces structured output (a brief, a spec, a prompt), show the expected format:

```markdown
## Output format

**Example structure:**
Branch `feature/foo` (issue #N). Working tree dirty — N files modified.

## What was done
- ...

## Where we left off
- ...
```

## Reference files

### When to extract to references/

Move content to a reference file when:
- It's detailed guidelines that not every execution needs to read in full
- It's a template or schema that's long but stable
- It's domain-specific content that only applies to certain inputs
- The SKILL.md is approaching 500 lines

### How to reference

Use natural language instructions, not special syntax:

```markdown
Read `references/artboard-guidelines.md` for the standard artboard structure.
```

The agent reads it with the Read tool when it reaches that instruction. Keep file references one level deep — avoid chains where one reference points to another.

### Large references (>300 lines)

Include a table of contents at the top so the agent can navigate efficiently.

## Quality techniques

### Craftsmanship repetition

Repeat quality expectations at multiple points in the instructions, not just once. This is intentional prompt engineering — it combats the tendency to produce "good enough" output.

Use language like "meticulously crafted", "painstaking attention", "master-level execution" throughout. This isn't filler — each repetition reinforces the quality bar.

### Anti-patterns list

Explicitly name the specific failure modes to avoid. Generic instructions ("make it look good") don't work. Specific anti-patterns do:

```markdown
**Avoid these specific AI design traps:**
- Generic gradients (especially purple-to-blue on white)
- Uniform spacing everywhere — vary rhythm intentionally
- Placeholder images as plain gray boxes
```

### Containment rules

For visual/spatial skills, explicitly state boundary rules. AI-generated compositions commonly have elements that bleed off edges or overlap. Mark these as non-negotiable and explain why.

### Refinement over addition

Build in an explicit "polish, don't add" step. AI tends to solve "it doesn't feel complete" by adding more elements. The better answer is usually refining what exists.

## Subagent prompts

When a skill launches subagents, each agent starts with a blank context. They don't inherit the parent conversation. This means:

- Repeat critical rules in every agent prompt (e.g., lorem ipsum, containment)
- Include all necessary context inline (design specs, tokens, templates)
- Be explicit about which tools to use and which to avoid, with *why*
- Include quality standards — the agent won't know about them otherwise

### Launch strategy

Subagents take several seconds to initialize. Launch them immediately (with `run_in_background: true`) and do setup work in parallel. By the time the setup completes, agents are already generating output.

## What doesn't work in skills

- **`@` imports** — Only resolved in CLAUDE.md files, not in SKILL.md. Use Read tool instructions instead.
- **Cross-skill dependencies** — Each skill should be fully self-contained.
- **Overly specific instructions** — Skills may be used across many different inputs. Avoid fiddly rules tied to one test case. Generalize.
- **Long SKILL.md without hierarchy** — Walls of text get lost. Use headers, numbered steps, and extract detail to references.

## Frontmatter fields

```yaml
---
name: skill-name          # Required. Lowercase + hyphens, matches directory name
description: ...          # Required. The trigger mechanism — be pushy and specific
user-invocable: true      # Set true if the user can call it directly via /skill-name
compatibility: ...        # Optional. Environment requirements (rarely needed)
---
```

## Checklist for reviewing a skill

1. Is the description pushy enough? Does it include trigger contexts, not just a summary?
2. Is the SKILL.md under 500 lines? Is detail extracted to references?
3. Are instructions reasoned ("because X") rather than rigid ("ALWAYS/NEVER")?
4. Are output formats defined with examples?
5. If using subagents, do their prompts include all necessary context?
6. Are quality expectations repeated at key points, not just stated once?
7. Are specific anti-patterns named, not just generic "make it good"?
