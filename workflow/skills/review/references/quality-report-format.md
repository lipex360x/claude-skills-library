# Quality Report Format

Template for `.docs/reviews/<issue>-cycle-<N>.md`. The coordinator fills this after merging all sub-agent results.

## Template

```markdown
## Quality Review — Issue #<issue> (cycle <N>)

### Static analysis

| # | Rule | File | Line | Status | Detail |
|---|------|------|------|--------|--------|
| S1 | <rule-name> | `<file-path>` | <line> | FAIL | <description> |
| S2 | <rule-name> | `<file-path>` | <line> | WARN | <description> |

**Summary:** Errors: <N> | Warnings: <N> | Suppressed: <N>

> If static review was skipped: "SKIPPED: QA-static — <reason> (re-run with `/review --rerun static`)"

### Semantic review

| # | Rule | File | Verdict | Reasoning |
|---|------|------|---------|-----------|
| Q1 | <rule-name> | `<file-path>` | FAIL | <LLM reasoning> |
| Q2 | <rule-name> | `<file-path>` | WARN | <LLM reasoning> |

**Summary:** Errors: <N> | Warnings: <N> | Suppressed: <N>

> If semantic review was skipped: "SKIPPED: QA-semantic — <reason> (re-run with `/review --rerun semantic`)"

### Runtime validation

| # | Check | Status | Detail |
|---|-------|--------|--------|
| R1 | Unit tests | PASS | 47/47 passed |
| R2 | Integration tests | FAIL | <detail> |
| R3 | E2E tests | PASS | 12/12 passed |
| R4 | App logs | WARN | 3 deprecated API warnings |
| R5 | Browser console | FAIL | Hydration mismatch in <component> |

**Summary:** Errors: <N> | Warnings: <N> | Suppipped: <N>

> If runtime review was skipped: "SKIPPED: QA-runtime — <reason> (re-run with `/review --rerun runtime`)"

### Action items

- [ ] [S1] <action description with file and line>
- [ ] [Q1] <action description with file>
- [ ] [R2] <action description>
- [ ] [R5] <action description>

### Warnings (non-blocking)

- [S2] <warning description>
- [Q2] <warning description>
- [R4] <warning description>

### Justified (accepted from prior cycles)

- ~~[Q3]~~ <rule> — justified: "<developer's reasoning>"

### Developer notes

> To justify an item, reply to this comment with: `justify <ID>: <reason>`
> Or add to `.claude/review-justifications.json`: `{ "<ID>": "<reason>" }`

---
Reviewed: <ISO-8601 timestamp> | Files: <count> | Scope: `git diff <base>..<head>` | Tier: <Minimum|Basic|Standard|Full|Custom>
```

## Field definitions

| Field | Description |
|-------|------------|
| `#` | Sequential ID: S-prefix (static), Q-prefix (semantic), R-prefix (runtime) |
| `Rule` | The quality rule violated (from quality-audit config, quality.md, or runtime check) |
| `File` | Relative file path in backticks |
| `Line` | Line number (static only — semantic and runtime may not have precise lines) |
| `Status` | FAIL (blocking), WARN (non-blocking), PASS (included for context in runtime) |
| `Verdict` | Semantic equivalent of Status — uses FAIL/WARN/PASS |
| `Detail` | Concrete description of the issue |
| `Reasoning` | LLM's reasoning for semantic verdicts (why the code violates the rule) |

## ID assignment rules

- Static items: `S1, S2, S3...` — ordered by severity (FAIL first, then WARN)
- Semantic items: `Q1, Q2, Q3...` — ordered by severity
- Runtime items: `R1, R2, R3...` — ordered by check type (unit > integration > e2e > logs > console)
- IDs are stable across cycles: if S1 was "magic number in order.ts" in cycle 1, it keeps that ID in cycle 2 (matched by rule + file)
- New items in cycle 2+ get the next available number in their prefix

## Cycle 2+ behavior

On re-review cycles, the report includes ALL items (not just open ones):
- `open` items re-checked and updated
- `justified` items listed in the Justified section (strikethrough)
- Items fixed (no longer detected) are removed from Action items
- New items from newly changed files are appended with new IDs

## Sub-agent XML output format

Each sub-agent wraps its output in XML tags for deterministic parsing:

```xml
<review-result agent="static">
  <item id="1" rule="no-magic-numbers" file="src/domain/order.ts" line="42" status="FAIL">
    Raw numeric literal 0.1 used instead of named constant
  </item>
  <item id="2" rule="max-line-length" file="src/utils/format.ts" line="88" status="WARN">
    Line exceeds 120 characters (134)
  </item>
  <summary errors="1" warnings="1" />
</review-result>
```

The coordinator parses these tags, assigns prefixed IDs (S1, Q1, R1), and merges into the report template above.
