# Code Simplifier — Anthropic Official Plugin Reference

Source: `anthropics/claude-plugins-official/plugins/code-simplifier/agents/code-simplifier.md`

Saved as reference for upgrading the existing `/simplify` skill and informing QA-semantic review criteria.

## Key principles worth absorbing

1. **Scope to recently modified code** — never full codebase unless explicitly asked
2. **Preserve functionality** — only change HOW, not WHAT
3. **Apply project standards** — read CLAUDE.md / .docs/quality.md for project-specific rules
4. **Reduce unnecessary complexity** — nesting, redundant abstractions, obvious comments
5. **Avoid over-simplification** — don't create clever one-liners that are hard to debug
6. **Avoid nested ternaries** — prefer switch/if-else for multiple conditions
7. **Clarity over brevity** — explicit code > compact code
8. **Document only significant changes** — not obvious ones

## How this maps to our pipeline

- **QA-semantic** should check for these patterns (report, not fix)
- **`/simplify`** (existing skill) should apply these fixes (ad-hoc, user-triggered)
- **`/review`** can suggest running `/simplify` when QA-semantic detects simplification opportunities

## Refinement process (from Anthropic)

1. Identify recently modified code sections
2. Analyze for elegance and consistency opportunities
3. Apply project-specific best practices
4. Ensure functionality unchanged
5. Verify refined code is simpler and more maintainable
6. Document only significant changes

## Rules to add to QA-semantic review criteria

- Flag unnecessary nesting (>2 levels)
- Flag redundant abstractions (wrappers that add no value)
- Flag nested ternary operators
- Flag comments that restate the code
- Flag overly compact code that sacrifices readability
- Flag functions doing more than one thing (single responsibility)
