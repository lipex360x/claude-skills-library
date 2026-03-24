# review-postgres

> Postgres performance optimization and best practices from Supabase.

Review and optimize Postgres queries, schemas, and configurations using Supabase best practices across 8 rule categories prioritized by impact. Each rule includes detailed explanations, incorrect vs. correct SQL examples, query plan analysis, and specific performance metrics.

## Usage

```text
/review-postgres
```

> [!TIP]
> Also activates when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations — even if they don't explicitly mention Postgres, even if they're just writing a migration, or even if the question is about "my query is slow."

## How it works

1. **Identify scope** — Determine what the user needs reviewed and classify items by rule categories
2. **Load relevant rules** — Read reference files matching the identified scope, starting with highest-priority categories
3. **Apply rules and produce findings** — Compare user's code against loaded rules, recording violations with severity and recommended fixes
4. **Present the review** — Deliver findings grouped by severity in a structured table with corrected SQL
5. **Refine if needed** — Re-evaluate findings based on user questions or additional context
6. **Report** — Present categories reviewed, findings by severity, audit results, and any errors

## Directory structure

```text
review-postgres/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/           # Individual rule files (34 files)
    ├── _template.md      # Reference template
    ├── _sections.md      # Section definitions
    ├── _contributing.md  # Writing guidelines
    ├── query-*.md        # Query performance rules
    ├── conn-*.md         # Connection management rules
    ├── security-*.md     # Security & RLS rules
    ├── schema-*.md       # Schema design rules
    ├── lock-*.md         # Concurrency & locking rules
    ├── data-*.md         # Data access pattern rules
    ├── monitor-*.md      # Monitoring & diagnostics rules
    └── advanced-*.md     # Advanced feature rules
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill review-postgres
```
