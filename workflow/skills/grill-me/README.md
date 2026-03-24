# grill-me

> Deep structured interview about a plan, feature, or project — extracts decisions, constraints, and context to generate PRD input.

Relentless, branch-based interview that systematically extracts decisions, constraints, and context across all dimensions of a plan. Supports multilingual sessions (English, Portuguese, or any language), adapts to existing codebases by exploring code as evidence, and outputs a structured `.claude/grill-output.md` document ready for `/write-a-prd`. One alignment checkpoint before finalizing — every question uses `AskUserQuestion` with contextualized options, never open-ended.

## Usage

```text
/grill-me [description]
```

> [!TIP]
> Also activates when you say "grill me", "me entrevista", "quero detalhar isso", "vamos aprofundar", "let's flesh this out", "stress-test this idea", or want to think through a plan deeply.

### Examples

```text
/grill-me a SaaS for restaurant inventory management   # start with initial context
/grill-me                                               # interactive — prompts for description
```

Also triggered by natural language:

```text
"stress-test this idea"    # same effect via model invocation
"let's flesh this out"     # same effect via model invocation
```

## How it works

1. **Choose interview language** — User picks English, Portuguese, or any other language for the entire session
2. **Capture the starting point** — Collect the initial idea or description from arguments or interactively
3. **Detect context** — Scan for project files to determine existing codebase vs. greenfield, adapting the question strategy
4. **Conduct the interview by branches** — Walk through structured decision tree covering goals, audience, constraints, technical scope, and more (max 2 questions per turn, depth-first exploration)
5. **Alignment checkpoint** — Present executive summary of all decisions for confirmation or adjustment
6. **Generate the input document** — Produce the structured PRD input at `.claude/grill-output.md` using the output template
7. **Report** — Summary with output file path, branches covered, and decision count

[↑ Back to top](#grill-me)

## Directory structure

```text
grill-me/
├── SKILL.md              # Core skill instructions (7 steps, 1 approval gate)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
├── references/
│   └── interview-branches.md  # Full decision tree with question patterns per branch
└── templates/
    └── grill-output.md        # Structured output document template for PRD input
```

[↑ Back to top](#grill-me)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill grill-me
```
