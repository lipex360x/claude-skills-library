# Quality Techniques

These techniques produce measurably better output. Each one addresses a specific tendency in AI-generated content.

## Craftsmanship repetition

Repeat quality expectations at multiple points in the instructions, not just once. This is intentional prompt engineering — it combats the tendency to produce "good enough" output.

Use language like "meticulously crafted", "painstaking attention", "master-level execution" at key decision points throughout the instructions. This isn't filler — each repetition reinforces the quality bar at the moment the model is deciding how much effort to invest.

## Anti-patterns list

Explicitly name the specific failure modes to avoid. Generic instructions ("make it look good") produce generic output. Specific anti-patterns shift behavior:

```markdown
**Avoid these specific traps:**
- Generic gradients (especially purple-to-blue on white)
- Uniform spacing everywhere — vary rhythm intentionally
- Placeholder images as plain gray boxes — use colored rectangles with subtle gradients
- Oversized elements that waste space
- Tiny text that's unreadable at thumbnail scale
```

The specificity matters. "Avoid generic gradients" is actionable. "Make it look professional" is not.

## Containment rules

For visual or spatial skills, explicitly state boundary rules with the reasoning. AI-generated compositions commonly have elements that bleed off edges or overlap:

```markdown
Nothing falls off the artboard. Nothing overlaps unintentionally. Every element has
breathing room from its neighbors. This is the most common failure mode — elements
bleed off edges or stack on top of each other when the model runs out of planning space.
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
## Design Brief

### Tokens
| Token | Hex | Role |
|-------|-----|------|
| --color-primary | #2563EB | Main brand color |

### Artboard Plan
| Artboard | File | Content | Agent |
|----------|------|---------|-------|
| Foundations | foundations.html | Color palette, typography scale | Agent 1 |

**Total: 5 artboards, 5 agents in parallel**
```
