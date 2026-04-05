# review-state.json Schema

Schema definition for `.claude/review-state.json` — the persistent state file that tracks review cycles across sessions.

## Location

`.claude/review-state.json` in the project root. This file MUST be gitignored (add to `.gitignore` if not already present).

## Schema (version 1)

```json
{
  "schema_version": 1,
  "session_id": "<string>",
  "issue": "<number>",
  "cycle": "<number>",
  "last_review_commit_sha": "<string>",
  "items": [
    {
      "id": "<string>",
      "agent": "<string>",
      "rule": "<string>",
      "file": "<string>",
      "line": "<number|null>",
      "status": "<string>",
      "detail": "<string>",
      "justification": "<string|null>",
      "accepted": "<boolean|null>"
    }
  ],
  "skipped_agents": ["<string>"]
}
```

## Field definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | integer | yes | Always `1`. Used to detect incompatible state from future versions. If the agent reads a version it doesn't understand, it warns and starts fresh. |
| `session_id` | string | yes | Opaque identifier for the current Claude Code session. Used to detect stale state from prior sessions. If the session ID doesn't match the current session, warn the user ("State from a different session found — continuing with existing cycle count"). |
| `issue` | integer | yes | GitHub issue number being reviewed. If the current branch's issue doesn't match, the state is stale — start fresh. |
| `cycle` | integer | yes | Current review cycle (1-indexed). Incremented after each full review pass. Max 3 for normal reviews. `--final` does not increment the cycle. |
| `last_review_commit_sha` | string | yes | The `git rev-parse HEAD` at the moment the review completed. Used by `--final` to scope delta: `git diff <this-sha>..HEAD`. Also used by cycle 2+ to detect newly changed files. **Never use timestamps** — git timestamps are unreliable (amends, rebases, cherry-picks). |
| `items` | array | yes | All review items across all cycles. Items persist — they are updated in place, never deleted. |
| `items[].id` | string | yes | Prefixed sequential ID: `S1`, `S2` (static), `Q1`, `Q2` (semantic), `R1`, `R2` (runtime). Stable across cycles — same rule + file = same ID. |
| `items[].agent` | string | yes | Which sub-agent produced this item: `"static"`, `"semantic"`, or `"runtime"`. |
| `items[].rule` | string | yes | The quality rule or check that was violated (e.g., `"no-magic-numbers"`, `"rich-vs-anemic"`, `"unit-tests"`). |
| `items[].file` | string | yes | Relative file path. `"n/a"` for runtime items not tied to a specific file (e.g., "app won't start"). |
| `items[].line` | number or null | no | Line number (static analysis only). Null for semantic and runtime items. |
| `items[].status` | string | yes | One of: `"open"`, `"fixed"`, `"justified"`, `"warning"`. See status lifecycle below. |
| `items[].detail` | string | yes | Description of the issue. For semantic items, includes the LLM's reasoning. |
| `items[].justification` | string or null | no | Developer's justification text (from reply comment or justifications file). Null if not justified. |
| `items[].accepted` | boolean or null | no | Whether the justification was accepted by the reviewer. Null if no justification provided. `true` = accepted, `false` = rejected with counter-proposal. |
| `skipped_agents` | array of strings | yes | Agents that failed or timed out in the most recent cycle. Empty array if all succeeded. Values: `"static"`, `"semantic"`, `"runtime"`. |

## Item status lifecycle

```
    open
    /    \
   /      \
fixed   justified
           |
      accepted=true  → stays "justified"
      accepted=false → back to "open" (with counter-proposal in detail)

After cycle 3 with status still "open":
  open → warning
```

- **open**: Issue detected, not yet resolved. Re-checked on next cycle.
- **fixed**: Item no longer detected on re-review (code was changed). Terminal state.
- **justified**: Developer provided a justification. `accepted` field determines if it holds.
- **warning**: Converted from `open` after max cycles reached. Non-blocking. Terminal state.

## Fallback behavior

| Condition | Action |
|-----------|--------|
| File missing | Create fresh state with cycle 1 |
| File is empty or invalid JSON | Warn, create fresh state with cycle 1 |
| `schema_version` != 1 | Warn ("incompatible review state version"), create fresh state |
| `issue` doesn't match current branch | Warn ("state from issue #X, current is #Y"), create fresh state |
| `session_id` doesn't match | Continue (warn only — cycles persist across sessions by design) |
| `last_review_commit_sha` not in git history | Warn ("review SHA not found — amend or rebase detected?"), treat as cycle 1 for scoping but preserve item history |

## Example: cycle 1 (fresh)

```json
{
  "schema_version": 1,
  "session_id": "sess_abc123",
  "issue": 42,
  "cycle": 1,
  "last_review_commit_sha": "a1b2c3d4e5f6",
  "items": [
    { "id": "S1", "agent": "static", "rule": "no-magic-numbers", "file": "src/domain/order.ts", "line": 42, "status": "open", "detail": "Raw numeric literal 0.1 used instead of named constant", "justification": null, "accepted": null },
    { "id": "Q1", "agent": "semantic", "rule": "rich-vs-anemic", "file": "src/domain/order.ts", "line": null, "status": "open", "detail": "Order entity has no behavior methods — data-only class violates rich domain model pattern", "justification": null, "accepted": null },
    { "id": "R1", "agent": "runtime", "rule": "e2e-tests", "file": "tests/e2e/checkout.spec.ts", "line": null, "status": "open", "detail": "checkout.spec.ts — timeout after 30s waiting for payment confirmation", "justification": null, "accepted": null }
  ],
  "skipped_agents": []
}
```

## Example: cycle 2 (after fixes + justification)

```json
{
  "schema_version": 1,
  "session_id": "sess_abc123",
  "issue": 42,
  "cycle": 2,
  "last_review_commit_sha": "f6e5d4c3b2a1",
  "items": [
    { "id": "S1", "agent": "static", "rule": "no-magic-numbers", "file": "src/domain/order.ts", "line": 42, "status": "fixed", "detail": "Raw numeric literal 0.1 used instead of named constant", "justification": null, "accepted": null },
    { "id": "Q1", "agent": "semantic", "rule": "rich-vs-anemic", "file": "src/domain/order.ts", "line": null, "status": "justified", "detail": "Order entity has no behavior methods — data-only class violates rich domain model pattern", "justification": "Order is a read model (CQRS) — behavior lives in OrderCommandHandler. Adding methods here would violate the pattern.", "accepted": true },
    { "id": "R1", "agent": "runtime", "rule": "e2e-tests", "file": "tests/e2e/checkout.spec.ts", "line": null, "status": "fixed", "detail": "checkout.spec.ts — timeout after 30s waiting for payment confirmation", "justification": null, "accepted": null },
    { "id": "Q2", "agent": "semantic", "rule": "error-handling", "file": "src/api/payments.ts", "line": null, "status": "open", "detail": "Generic catch block swallows PaymentError — loses error context for logging", "justification": null, "accepted": null }
  ],
  "skipped_agents": []
}
```
