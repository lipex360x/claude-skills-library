---
name: review-postgres
description: >-
  Postgres performance optimization and best practices from Supabase. Use this
  skill when writing, reviewing, or optimizing Postgres queries, schema designs,
  or database configurations — even if they don't explicitly mention Postgres,
  even if they're just writing a migration, or even if the question is about
  "my query is slow."
user-invocable: true
allowed-tools:
  - Read
  - Glob
---

# Supabase Postgres Best Practices

Review and optimize Postgres queries, schemas, and configurations using Supabase best practices across 8 rule categories prioritized by impact.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| SQL/schema/migration | Conversation or file | yes | Contains SQL or schema-related content | Ask the user to share the relevant SQL or schema |
| Review scope | Conversation | no | One of: query, schema, migration, general | Default to full review across all categories |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Review report | stdout | no | Markdown table with findings grouped by severity |
| Corrected SQL | stdout | no | SQL code block |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Rule reference files | `references/*.md` | R | Markdown with SQL examples |
| Sections index | `references/_sections.md` | R | Markdown index |

</external_state>

## Pre-flight

<pre_flight>

1. Input contains SQL, schema definition, migration file, or database-related question → if not: "Please share the SQL, schema, or migration you'd like reviewed." — stop.
2. Rule reference files are accessible → if not: "Reference files missing at `references/`." — stop.
3. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Identify scope

Determine what the user needs reviewed. Read the provided SQL, schema, migration, or description. Classify each item by the rule categories below to decide which reference files to load. If the input is not SQL or schema-related (e.g., an ORM model or application code), extract the database-relevant parts or ask the user to provide the generated SQL. If no rule categories match the identified scope, inform the user and suggest what input would help.

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

Deliver findings grouped by severity, highest first:

```markdown
## Postgres Review — [brief scope description]

### Findings

| # | Severity | Rule | Finding | Recommendation |
|---|----------|------|---------|----------------|
| 1 | CRITICAL | query-missing-indexes | Full table scan on `users` | `CREATE INDEX ...` |

### Summary

- **Critical:** N findings
- **High:** N findings
- **Medium:** N findings
- **Low:** N findings
- **Rules checked:** [list of rule prefixes reviewed]

### Corrected SQL

[Full corrected version, if applicable]
```

### 5. Refine if needed

If the user questions a finding or provides additional context, re-evaluate that specific rule application. Adjust the severity or recommendation accordingly. Repeat until the user is satisfied with the review.

### 6. Report

Present concisely:
- **What was done** — categories reviewed, number of findings by severity
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

> _Skipped: "Review complete — user decides next steps based on findings."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — input contained reviewable SQL/schema content
2. **CRITICAL categories checked?** — query performance, connection management, and security were always reviewed
3. **Every finding has a fix?** — no finding is just a description without a concrete recommendation
4. **Corrected SQL compiles?** — no syntax errors in recommendations
5. **Anti-patterns scanned?** — common traps were checked even if outside the explicit request scope

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **SQL correctness?** — recommended fixes are valid Postgres syntax
2. **Rule application accurate?** — each finding correctly matches the rule it cites
3. **Severity appropriate?** — CRITICAL is reserved for performance/security issues with measurable impact
4. **References valid?** — rule file prefixes cited in findings exist in `references/`

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Input is not SQL/schema-related | Ask user to provide the generated SQL or relevant schema |
| Rule reference files missing | Report which files are missing, proceed with available rules |
| Ambiguous input scope | Ask user to clarify what they want reviewed |

## Anti-patterns

- **Missing indexes on FK columns.** Foreign key columns without indexes cause slow JOINs and cascading deletes — because the planner falls back to sequential scans on the referenced table.
- **Sequential scans on large tables.** Any `Seq Scan` on tables with >10k rows deserves an index review — because full table scans grow linearly with data size.
- **SELECT \*.** Fetching all columns when only a subset is needed — because it wastes I/O, memory, and prevents index-only scans.
- **N+1 queries.** Looping queries inside application code instead of using JOINs or batch fetches — because each round-trip adds network latency and connection overhead.
- **Long-running transactions.** Holding locks for extended periods — because it causes contention, deadlocks, and blocks autovacuum.
- **Missing connection pooling.** Direct connections without a pooler — because connection limits are exhausted under load.
- **Overly permissive RLS.** Policies that default to `true` or skip auth checks — because they expose data to unauthorized users.
- **No EXPLAIN ANALYZE.** Optimizing queries without checking the actual execution plan — because assumptions about query behavior are often wrong.
- **Implicit type casts in WHERE.** Comparing mismatched types (e.g., `varchar` to `int`) — because it prevents index usage and forces sequential scans.

## Guidelines

- **Priority-ordered review.** Always start with CRITICAL categories (query, conn, security) before moving to lower-priority ones — because the highest-impact issues should be surfaced first regardless of what the user asked about.
- **Concrete fixes over descriptions.** Every finding must include corrected SQL, not just an explanation of the problem — because actionable recommendations save the user from having to research the fix themselves.
- **Scan anti-patterns proactively.** Check for common anti-patterns even if they fall outside the explicit request scope — because users often don't know what they don't know about database performance.
- **Respect Supabase context.** When applicable, include Supabase-specific notes (RLS, connection pooling via Supavisor, edge functions) — because many users of this skill are on the Supabase platform.
