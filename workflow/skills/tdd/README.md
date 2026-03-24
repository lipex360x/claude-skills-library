# tdd

> Execute Test-Driven Development with strict red-green-refactor discipline.

Guides the agent through vertical slices — one test, one implementation, repeat. Enforces strict TDD discipline: never write all tests first, always verify the test fails before implementing.

## Usage

```text
/tdd [feature description]
```

> [!TIP]
> Also activates when you say "tdd", "test first", "red green refactor", "write tests", "test driven", "let's TDD this", or want to implement a feature with test discipline.

## How it works

1. **Understand what to build** — Read the codebase to learn test patterns, frameworks, and interfaces
2. **Plan behaviors to test** — List observable outcomes to test (approval gate)
3. **Design interface for testability** — Consider dependency injection and surface area
4. **Execute the loop** — RED (write test, must fail) → GREEN (minimal code to pass) → REFACTOR (clean up with confidence), one cycle per behavior
5. **Verify** — Run the full test suite and report what was added
6. **Report** — Summary with tests written, implementation files, and coverage

## Directory structure

```text
tdd/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── tdd-methodology.md  # Deep modules, mocking rules, good vs bad tests
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill tdd
```
