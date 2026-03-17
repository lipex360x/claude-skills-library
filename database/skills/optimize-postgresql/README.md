# optimize-postgresql

> PostgreSQL-specific development assistant focusing on unique PostgreSQL features, advanced data types, and PostgreSQL-exclusive capabilities.

Provides expert guidance on PostgreSQL-specific features including JSONB operations, array types, custom types, range/geometric types, full-text search, window functions, and the extensions ecosystem. Covers query optimization with EXPLAIN ANALYZE, index strategies (composite, partial, expression, covering), connection/memory management, and common query anti-patterns.

## Usage

```text
/optimize-postgresql
```

> [!TIP]
> Also activates when working with PostgreSQL-specific features, optimizing queries, designing indexes, or using advanced data types like JSONB, arrays, and range types.

## How it works

1. **Feature guidance** -- Provides SQL examples and best practices for PostgreSQL-specific data types (JSONB, arrays, ranges, geometric, custom types/domains)
2. **Query optimization** -- Analyzes queries using EXPLAIN (ANALYZE, BUFFERS) and pg_stat_statements, suggests index strategies and query rewrites
3. **Performance tuning** -- Covers connection pooling, memory configuration, VACUUM/ANALYZE, and partitioning recommendations
4. **Anti-pattern detection** -- Identifies common mistakes (OFFSET pagination, inefficient JSON queries, missing indexes) and provides corrected alternatives
5. **Security review** -- Checks for parameterized queries, access controls, and row-level security

## Directory structure

```text
optimize-postgresql/
├── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill optimize-postgresql
```
