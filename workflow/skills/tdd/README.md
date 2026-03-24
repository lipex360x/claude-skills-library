# tdd

> Execute Test-Driven Development with strict red-green-refactor discipline.

Guides implementation through vertical slices — one behavior at a time, never batch. Plans testable behaviors from the caller's perspective, designs interfaces for dependency injection and minimal surface area, then executes strict RED (test must fail) to GREEN (minimal code to pass) to REFACTOR (clean up with passing tests) cycles. Adapts to any test framework the project already uses (Jest, Vitest, Pytest, Go test, etc.). One approval gate on the behavior list, then the loop runs autonomously.

## Usage

```text
/tdd <feature description>
```

> [!TIP]
> Also activates when you say "tdd", "test first", "red green refactor", "write tests", "test driven", "let's TDD this", or want to implement a feature with test discipline.

### Examples

```text
/tdd user checkout with discount codes     # implement with TDD discipline
/tdd add pagination to the issues list     # test-first for a specific feature
```

## How it works

1. **Understand what to build** — Read the codebase to learn existing test patterns, frameworks, naming conventions, and public interfaces
2. **Plan behaviors to test** — List observable outcomes from the caller's perspective (not implementation steps); user approves, adjusts, or adds behaviors
3. **Design interface for testability** — Consider dependency injection, return values over side effects, and minimal surface area before writing any test
4. **Execute the loop** — For each behavior: RED (write test, verify it fails) then GREEN (minimal code to pass) then REFACTOR (extract duplication, deepen modules, introduce value objects) — one cycle per behavior, never batch
5. **Verify** — Run the full test suite (not just new tests) to catch regressions
6. **Report** — Summary with behaviors implemented, test count, files created/modified, refactors performed, and any skipped behaviors

[↑ Back to top](#tdd)

## Directory structure

```text
tdd/
├── SKILL.md              # Core skill instructions (6 steps, 1 approval gate)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
└── references/
    └── tdd-methodology.md  # Deep modules, mocking rules, good vs bad test examples
```

[↑ Back to top](#tdd)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill tdd
```
