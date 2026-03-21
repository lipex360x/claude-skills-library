# Hybrid Decision Model

Rules for classifying each checklist item as `[inferred]`, `[gap]`, or `[ask]`. The goal is to minimize user interruptions while maximizing spec accuracy.

## Classifications

### `[inferred]` — High confidence, shown for review

The input provides enough signal to make a decision with high confidence. The decision is recorded in the spec and shown to the user in a summary — they can override but aren't asked to confirm.

**When to infer:**

- The input explicitly states the answer (e.g., "this skill should read from a file path")
- The answer follows directly from a stated constraint (e.g., if the skill is in the `meta` plugin, it targets Claude Code skill management)
- Industry convention makes one choice overwhelmingly likely (e.g., a CLI skill that produces files writes to the current directory)
- The codebase context resolves it (e.g., existing skills in the same plugin follow a pattern — the new skill should too)
- The CLAUDE.md rules dictate it (e.g., naming convention is verb-subject, `disable-model-invocation` defaults to false)

**Confidence threshold:** You would bet money on this being the right choice. If you'd want to "just check" — it's an `[ask]`, not an `[inferred]`.

**Format in spec:**

```markdown
| 3 | Output path is `downloads/<skill-name>-spec.md` | [inferred] | Input explicitly states "produces spec file at downloads/" |
```

### `[gap]` — Flagged, non-blocking

The input doesn't address this item, but the spec can proceed without it. Gaps are listed as warnings — they represent decisions that `/create-skill` will need to make or that the user should fill in later.

**When to flag as gap:**

- The item is relevant but the input says nothing about it (e.g., no mention of idempotency behavior)
- The item has a safe default that can be assumed temporarily (e.g., "overwrite on re-run" is a common default)
- The item is important for quality but not for the core workflow (e.g., error messages for edge cases)
- Resolving it requires implementation experience that planning can't predict (e.g., exact error handling for a tool that hasn't been called yet)

**Non-blocking means:** The spec is usable without this answer. `/create-skill` can fill it in during implementation. But the gap is explicitly flagged so nothing falls through the cracks.

**Format in spec:**

```markdown
| 7 | Idempotency behavior (overwrite vs skip) | [gap] | Input doesn't specify. Safe default: overwrite with warning. Flag for user review during implementation |
```

### `[ask]` — AUQ for ambiguous/architectural choices

The item requires user input because the choice has significant implications and can't be safely inferred. These are batched into `AskUserQuestion` calls with concrete options.

**When to ask:**

- Multiple valid approaches exist with different trade-offs (e.g., "should the spec be written to a fixed path or configurable?")
- The choice affects architecture beyond this skill (e.g., "should this skill update STRUCTURE.md directly or defer to the user?")
- The input contains contradictory signals (e.g., "simple" but lists complex requirements)
- The choice involves user preferences that vary by context (e.g., "verbose output vs minimal output")
- Getting it wrong would require significant rework (e.g., the output format that another skill consumes)

**Never ask about:**

- Items where the CLAUDE.md rules provide a clear answer — infer instead
- Items with industry-standard conventions — infer instead
- Items that can be safely defaulted and changed later — flag as gap instead
- Implementation details that don't affect the spec — skip entirely

**Format in AUQ:**

```
question: "How should plan-skill handle re-runs on existing specs?"
options:
  - label: "Overwrite with warning"
    description: "Replace the existing spec after showing a diff summary"
  - label: "Create versioned file"
    description: "Write to downloads/<name>-spec-v2.md, keep the original"
  - label: "Ask each time"
    description: "Use AUQ to let the user decide per invocation"
```

**Batching rule:** Group related `[ask]` items into a single `AskUserQuestion` when they share context. Never present more than 4 questions at once — if there are more, split into sequential AUQ calls ordered by dependency (decisions that inform later questions go first).

## Decision flow

```
For each checklist item:
  1. Search input for explicit answer
     → Found with high confidence? → [inferred]
     → Found but ambiguous? → [ask]

  2. Check CLAUDE.md rules
     → Rule dictates the answer? → [inferred]
     → Rule is relevant but doesn't resolve? → [ask]

  3. Check codebase patterns
     → Clear convention exists? → [inferred]
     → Multiple patterns, unclear which? → [ask]

  4. Apply safe default
     → Safe default exists and item is non-critical? → [gap]
     → No safe default or item is critical? → [ask]
```

## Presentation order

When presenting results to the user:

1. **`[inferred]` summary** — table of all inferred decisions, shown for review. User scans and overrides if needed. No action required if correct.
2. **`[ask]` batch** — AUQ calls for architectural decisions. Grouped by topic, max 4 per call.
3. **`[gap]` warnings** — list of unresolved items with safe defaults noted. User acknowledges but doesn't need to resolve now.

This order is intentional: showing inferred decisions first builds trust ("it understood my intent"), then asks only what it genuinely can't resolve, and finally shows gaps as FYI.
