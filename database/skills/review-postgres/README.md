# review-postgres

> Postgres performance optimization and best practices from Supabase.

Comprehensive Postgres code review engine powered by 34 rule files across 8 priority-ranked categories (query performance, connection management, security/RLS, schema design, concurrency/locking, data access patterns, monitoring, and advanced features). Each rule includes incorrect vs. correct SQL examples, EXPLAIN ANALYZE output, and Supabase-specific notes. Findings are severity-classified and delivered with concrete fixes — never just descriptions.

## Usage

```text
/review-postgres
```

> [!TIP]
> Also activates when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations — even if they don't explicitly mention Postgres, even if they're just writing a migration, or even if the question is about "my query is slow."

### Examples

```text
/review-postgres                  # review SQL or schema already in the conversation
```

Also triggered by natural language:

```text
"review this migration"           # activates on migration files
"my query is slow"                # activates on performance questions
"check my schema design"          # activates on schema review requests
```

## How it works

1. **Identify scope** — Determine what the user needs reviewed and classify items by the 8 rule categories
2. **Load relevant rules** — Read reference files matching the identified scope, starting with CRITICAL categories (query, connection, security)
3. **Apply rules and produce findings** — Compare user's code against loaded rules, recording violations with severity and recommended fixes
4. **Present the review** — Deliver findings grouped by severity in a structured table with corrected SQL
5. **Refine if needed** — Re-evaluate findings based on user questions or additional context
6. **Report** — Present categories reviewed, findings by severity, audit results, and any errors

[↑ Back to top](#review-postgres)

## Directory structure

```text
review-postgres/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/           # 34 rule files organized by category prefix
    ├── _contributing.md              # Writing guidelines for new rule files
    ├── _sections.md                  # Category index and prefix-to-section mapping
    ├── _template.md                  # Starter template for new rule files
    ├── query-missing-indexes.md      # Detect missing indexes causing full table scans
    ├── query-composite-indexes.md    # Composite index column ordering rules
    ├── query-covering-indexes.md     # Index-only scans via covering indexes
    ├── query-index-types.md          # B-tree, GIN, GiST, and BRIN index selection
    ├── query-partial-indexes.md      # Partial indexes for filtered query optimization
    ├── conn-pooling.md               # Connection pooling via Supavisor/PgBouncer
    ├── conn-limits.md                # Connection limit configuration
    ├── conn-idle-timeout.md          # Idle connection timeout tuning
    ├── conn-prepared-statements.md   # Prepared statement usage with poolers
    ├── security-rls-basics.md        # Row Level Security fundamentals
    ├── security-rls-performance.md   # RLS policy performance optimization
    ├── security-privileges.md        # Role and privilege management
    ├── schema-primary-keys.md        # Primary key design patterns
    ├── schema-foreign-key-indexes.md # Indexes on foreign key columns
    ├── schema-constraints.md         # Check and unique constraint usage
    ├── schema-data-types.md          # Optimal data type selection
    ├── schema-lowercase-identifiers.md # Identifier casing conventions
    ├── schema-partitioning.md        # Table partitioning strategies
    ├── lock-deadlock-prevention.md   # Deadlock prevention techniques
    ├── lock-advisory.md              # Advisory lock patterns
    ├── lock-short-transactions.md    # Short transaction best practices
    ├── lock-skip-locked.md           # SKIP LOCKED for queue patterns
    ├── data-n-plus-one.md            # N+1 query detection and fixes
    ├── data-batch-inserts.md         # Bulk insert optimization
    ├── data-pagination.md            # Cursor vs. offset pagination
    ├── data-upsert.md                # UPSERT (INSERT ON CONFLICT) patterns
    ├── monitor-explain-analyze.md    # EXPLAIN ANALYZE interpretation
    ├── monitor-pg-stat-statements.md # pg_stat_statements monitoring
    ├── monitor-vacuum-analyze.md     # VACUUM and ANALYZE tuning
    ├── advanced-full-text-search.md  # Full-text search with tsvector/tsquery
    └── advanced-jsonb-indexing.md    # JSONB GIN indexing strategies
```

[↑ Back to top](#review-postgres)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill review-postgres
```
