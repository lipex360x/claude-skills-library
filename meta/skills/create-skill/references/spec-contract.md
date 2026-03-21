# Spec Contract — plan-skill to create-skill handoff

When `/plan-skill` produces a spec file, `/create-skill` can consume it to accelerate skill creation. The spec is a starting point — not a binding contract. The user can override any decision during execution.

## Expected file path

```
downloads/<skill-name>-spec.md
```

Glob pattern: `downloads/*-spec.md`

The user may also pass the spec path directly as an argument to `/create-skill`.

## Spec validation

A well-formed spec must contain ALL of these sections (check with header matching):

| Required section | Header to match |
|-----------------|-----------------|
| Meta table | `## Meta` |
| Purpose | `## Purpose` |
| Trigger | `## Trigger` |
| Workflow | `## Workflow` |
| Guardrails | `## Guardrails` |
| Decisions Log | `## Decisions Log` |

If any required section is missing, warn the user and fall back to normal create-skill flow.

## Section mapping to create-skill steps

| Spec section | Maps to create-skill step | Effect when spec present |
|-------------|--------------------------|-------------------------|
| **Meta** (name, plugin, invocable) | Step 1 — Understand the intent | Pre-fills answers; confirm instead of ask |
| **Purpose** (what/why/not) | Step 1 — Understand the intent | Pre-fills core action and scope; confirm instead of discover |
| **Trigger** (description draft, activation phrases) | Step 3 — Write the description | Use draft as starting point; still validate against description patterns |
| **Input Contract** | Step 4 — Write the SKILL.md body | Informs input handling and validation logic |
| **Workflow** | Step 4 — Write the SKILL.md body | Provides step-by-step structure for the skill body |
| **Output Contract** | Step 4 — Write the SKILL.md body | Defines output format and location |
| **Dependencies** | Step 2 — Design the structure | Informs which directories are needed (references/, scripts/, templates/) |
| **Cross-Skill State** | Step 4 — SKILL.md `## External state` section | Documents shared resources |
| **Guardrails** | Step 5 — Apply quality techniques | Seeds anti-patterns and must-do rules |
| **Decisions Log** | Step 1 — Understand the intent | Audit trail — shows what was already decided and why |

## What create-skill can SKIP with a spec

- **Step 1 intent discovery questions** — The spec already answers "what should it do?", "when should it activate?", and "is it user-invocable?". Present a summary for confirmation instead of asking from scratch.
- **Step 1.1 scope classification** — The spec defines a single skill with clear boundaries. No multi-action parsing needed unless the user adds new requests on top of the spec.

## What create-skill must STILL do with a spec

These steps are NEVER skippable, even with a perfect spec:

| Step | Why it cannot be skipped |
|------|------------------------|
| **Step 2 — Design structure** | Spec suggests structure but final layout must be verified against actual content |
| **Step 3 — Write description** | Spec provides a draft; must still validate against `description-patterns.md` |
| **Step 4 — Write SKILL.md** | The actual writing — spec informs but doesn't replace implementation |
| **Step 5 — Quality techniques** | Must apply craftsmanship repetition, anti-patterns — spec doesn't do this |
| **Step 7 — Review checklist** | Non-negotiable quality gate |
| **Step 8 — Register** | Runtime step — must execute `setup.sh` |
| **Step 8b — Test** | Runtime step — must test activation |
| **Step 9 — Update READMEs** | Runtime step — must run `/create-readme` |
| **Step 10 — Update STRUCTURE.md** | Runtime step — must verify entries |
| **Step 11 — Push** | Runtime step — must push changes |
