# review-postgres

> Postgres performance optimization and best practices from Supabase.

Comprehensive Postgres optimization guide maintained by Supabase, containing rules across 8 priority categories -- from critical (query performance, connection management, security/RLS) to incremental (advanced features). Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics.

## Usage

```text
/review-postgres
```

> [!TIP]
> Also activates when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations.

## How it works

1. **Rule-based analysis** -- Applies prioritized rules across 8 categories (query performance, connection management, security/RLS, schema design, concurrency/locking, data access patterns, monitoring, advanced features)
2. **Error-first examples** -- Each rule shows the incorrect pattern first, then the correct approach with quantified impact (e.g., 10-100x faster)
3. **Reference lookup** -- Reads individual rule files from `references/` for detailed explanations and SQL examples

## Rule categories by priority

| Priority | Category | Impact |
|----------|----------|--------|
| 1 | Query Performance | CRITICAL |
| 2 | Connection Management | CRITICAL |
| 3 | Security & RLS | CRITICAL |
| 4 | Schema Design | HIGH |
| 5 | Concurrency & Locking | MEDIUM-HIGH |
| 6 | Data Access Patterns | MEDIUM |
| 7 | Monitoring & Diagnostics | LOW-MEDIUM |
| 8 | Advanced Features | LOW |

## Directory structure

```text
review-postgres/
├── SKILL.md              # Core instructions (Agent Skills spec)
├── AGENTS.md             # [GENERATED] Compiled references document
├── CLAUDE.md             # Claude Code integration
└── references/           # Individual rule files
    ├── _template.md      # Reference template
    ├── _sections.md      # Section definitions
    ├── _contributing.md  # Writing guidelines
    └── *.md              # Individual references
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill review-postgres
```
