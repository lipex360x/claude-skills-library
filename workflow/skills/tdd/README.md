# /tdd

Execute Test-Driven Development with strict red-green-refactor discipline using vertical slices.

## Triggers

- `/tdd`
- "test first", "red green refactor", "write tests", "test driven"
- "let's TDD this"

## How it works

1. **Understand** — reads the codebase to learn test patterns, frameworks, and interfaces
2. **Plan behaviors** — lists observable outcomes to test (approval gate)
3. **Design interface** — considers testability, dependency injection, surface area
4. **Execute loop** — RED (write test, must fail) → GREEN (minimal code to pass) → REFACTOR (clean up with confidence). One cycle per behavior.
5. **Verify** — runs full test suite, reports what was added

## Usage

```bash
/tdd implement user authentication
/tdd add discount code support to orders
/tdd
```

## Directory structure

```
tdd/
├── SKILL.md
├── README.md
└── references/
    └── tdd-methodology.md    # Deep modules, mocking rules, good vs bad tests
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill tdd
```
