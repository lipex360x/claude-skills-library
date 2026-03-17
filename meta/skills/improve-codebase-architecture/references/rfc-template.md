# RFC Issue Template

Use this format when creating refactor RFC issues with `gh issue create`.

## Template

```markdown
## Problem

**Friction signal:** {{what made this area hard to navigate — file scatter, shallow modules, tight coupling}}

**Affected modules:**
{{list of files/directories with brief role description}}

**Current interface surface:** {{number of exports, methods, or entry points callers use}}

**Dependency category:** {{Internal / Injected / Shared / Cross-boundary}} — see dependency-categories.md

## Proposed Design

### Interface

{{TypeScript/language signature of the new deep module interface}}

### Usage Example

{{How callers use the new interface — before and after comparison}}

### What It Hides

{{The complexity that moves behind the interface — what callers no longer need to know about}}

### Dependency Strategy

{{How dependencies are handled — injection, adapter, encapsulation}}

## Migration Plan

### Steps

1. {{Create the new module with its interface}}
2. {{Move implementation behind the interface}}
3. {{Update callers to use the new interface}}
4. {{Replace internal tests with boundary tests}}
5. {{Remove obsolete files}}

### Test Changes

| Before | After |
|--------|-------|
| {{old test file}} — tests {{what}} | {{new test file}} — boundary test for {{what}} |

## Verification

- [ ] All existing behavior preserved (boundary tests pass)
- [ ] Interface surface area reduced (from {{N}} exports to {{M}})
- [ ] No callers reference internal implementation
- [ ] Lint + full test suite passes
```

## Notes

- Keep the issue focused on ONE deepening operation. Multiple refactors = multiple issues.
- Include concrete file paths — vague descriptions ("improve the auth module") are not actionable.
- The migration plan should be independently executable — each step leaves the codebase in a working state.
