---
name: review-postgres
description: "Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations — even if they don't explicitly mention Postgres, even if they're just writing a migration, or even if the question is about 'my query is slow'."
license: MIT
metadata:
  author: supabase
  version: "2.0.0"
  organization: Supabase
  date: January 2026
  abstract: Comprehensive Postgres performance optimization guide for developers using Supabase and Postgres. Contains performance rules across 8 categories, prioritized by impact from critical (query performance, connection management) to incremental (advanced features). Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics to guide automated optimization and code generation.
---

# Supabase Postgres Best Practices

Review and optimize Postgres queries, schemas, and configurations using Supabase best practices across 8 rule categories prioritized by impact.

## Input contract

Accepted inputs (one or more):
- **SQL queries** — `SELECT`, `INSERT`, `UPDATE`, `DELETE`, CTEs, subqueries
- **Schema definitions** — `CREATE TABLE`, `ALTER TABLE`, indexes, constraints
- **Migration files** — any `.sql` file or migration runner output
- **General request** — "review my database", "optimize this query", "check my schema"
- **Error/performance complaint** — "this query is slow", "connection timeout", "deadlocks"

If the input is ambiguous, ask the user to share the relevant SQL or schema before proceeding.

## Steps

### 1. Identify scope

Determine what the user needs reviewed. Read the provided SQL, schema, migration, or description. Classify each item by the rule categories below to decide which reference files to load.

### 2. Load relevant rules

Read the reference files that match the identified scope. Start with the highest-priority categories. Use `references/_sections.md` as the index.

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Performance | CRITICAL | `query-` |
| 2 | Connection Management | CRITICAL | `conn-` |
| 3 | Security & RLS | CRITICAL | `security-` |
| 4 | Schema Design | HIGH | `schema-` |
| 5 | Concurrency & Locking | MEDIUM-HIGH | `lock-` |
| 6 | Data Access Patterns | MEDIUM | `data-` |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM | `monitor-` |
| 8 | Advanced Features | LOW | `advanced-` |

Each rule file contains: explanation, incorrect vs. correct SQL examples, EXPLAIN output, and Supabase-specific notes.

### 3. Apply rules and produce findings

Compare the user's code against each loaded rule. For every violation or improvement opportunity, record:
- Which rule was violated
- The severity (CRITICAL / HIGH / MEDIUM / LOW)
- The specific line or pattern that triggered the finding
- The recommended fix with corrected SQL

### 4. Present the review

Deliver findings in the output format below. Group by severity, highest first.

### 5. Refine if needed

If the user questions a finding or provides additional context, re-evaluate that specific rule application. Adjust the severity or recommendation accordingly. Repeat until the user is satisfied with the review.

## Output format

Present the review as a structured report:

```markdown
## Postgres Review — [brief scope description]

### Findings

| # | Severity | Rule | Finding | Recommendation |
|---|----------|------|---------|----------------|
| 1 | CRITICAL | query-missing-indexes | Full table scan on `users` — no index on `email` column used in WHERE clause | `CREATE INDEX idx_users_email ON users (email);` |
| 2 | HIGH | schema-partial-indexes | Index on `orders.status` includes all rows but only 5% are `active` | `CREATE INDEX idx_orders_active ON orders (status) WHERE status = 'active';` |

### Summary

- **Critical:** N findings
- **High:** N findings
- **Medium:** N findings
- **Low:** N findings
- **Rules checked:** [list of rule prefixes reviewed]

### Corrected SQL

[Full corrected version of the reviewed SQL, if applicable]
```

## Anti-patterns

Watch for these common mistakes — flag them even if the user didn't ask:

- **Missing indexes on FK columns** — foreign key columns without indexes cause slow JOINs and cascading deletes
- **Sequential scans on large tables** — any `Seq Scan` on tables with >10k rows deserves an index review
- **SELECT \*** — fetching all columns when only a subset is needed wastes I/O and memory
- **N+1 queries** — looping queries inside application code instead of using JOINs or batch fetches
- **Long-running transactions** — holding locks for extended periods causes contention and deadlocks
- **Missing connection pooling** — direct connections without a pooler exhaust connection limits under load
- **Overly permissive RLS** — policies that default to `true` or skip auth checks entirely
- **No EXPLAIN ANALYZE** — optimizing queries without checking the actual execution plan is guessing
- **Implicit type casts in WHERE** — comparing mismatched types (e.g., `varchar` to `int`) prevents index usage

## Quality checkpoint

After completing the review, verify:
- [ ] All CRITICAL-priority categories were checked (query, conn, security)
- [ ] Every finding includes a concrete fix, not just a description of the problem
- [ ] The corrected SQL compiles (no syntax errors in recommendations)
- [ ] Anti-patterns were scanned even if outside the explicit request scope

## References

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security
