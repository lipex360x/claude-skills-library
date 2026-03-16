# Quality Techniques

These techniques produce measurably better output. Each one addresses a specific tendency in AI-generated content.

## Craftsmanship repetition

Repeat quality expectations at multiple points in the instructions, not just once. This is intentional prompt engineering — it combats the tendency to produce "good enough" output.

Use language like "meticulously crafted", "painstaking attention", "master-level execution" at key decision points throughout the instructions. This isn't filler — each repetition reinforces the quality bar at the moment the model is deciding how much effort to invest.

## Anti-patterns list

Explicitly name the specific failure modes to avoid. Generic instructions ("make it look good") produce generic output. Specific anti-patterns shift behavior:

```markdown
**Avoid these specific traps:**
- Boilerplate structure that looks like every other AI-generated output
- Inconsistent naming conventions across related files
- Overly verbose comments that restate what the code already says
- Missing edge case handling at system boundaries
```

The specificity matters. "Avoid boilerplate structure" is actionable. "Make it professional" is not. Tailor the anti-patterns list to your skill's domain — visual skills have different traps than code generation skills.

## Containment rules

For skills that produce bounded output (visual layouts, file structures, API responses), explicitly state boundary constraints with reasoning:

```markdown
Every generated component must be self-contained. No external dependencies beyond
what's declared. No implicit state shared between components. This is the most common
failure mode — components that look independent but silently depend on each other.
```

## Refinement over addition

Build in an explicit "polish, don't add" step. AI tends to solve "it doesn't feel complete" by adding more elements. The better answer is usually refining what exists.

Frame it as a guiding question in the instructions:

```markdown
"How can I make what's here more polished?" — not "What else can I add?"
```

## Output format examples

When a skill produces structured output, show the expected format. The model follows concrete shapes better than abstract descriptions:

```markdown
## Analysis Report

### Summary
| Item | Status | Notes |
|------|--------|-------|
| Auth module | Needs refactor | Circular dependency with user module |

### Recommended actions
1. Extract shared types to a common package
2. ...

**Total: 3 modules analyzed, 2 need changes**
```
