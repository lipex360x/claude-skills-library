# start-issue

> Pull an issue and start implementation — reads the issue, expands acceptance criteria into a detailed step-by-step plan with checkboxes, rewrites the issue, creates branch and tasks.

Turns an issue with high-level acceptance criteria into a detailed implementation plan with Steps and checkboxes, then sets up the branch and tasks. Reads ARCHITECTURE.md and issue comments for context, enforces TDD order in every behavioral step, detects CDP configuration for web projects, and auto-selects an execution strategy (Agent, Teammate, or Sequential) when Agent Teams is enabled. One approval gate: the proposed plan. Everything else is automated.

## Usage

```text
/start-issue [issue-number]
```

> [!TIP]
> Also activates when you say "start issue", "work on issue #N", "pull from backlog", "start #N", or want to begin implementing an issue.

### Examples

```text
/start-issue           # pick from Backlog/Todo issues interactively
/start-issue 42        # start working on issue #42 directly
/start-issue #42       # same — accepts both formats
```

> [!NOTE]
> Requires GitHub CLI (`gh`) authenticated and an initialized git repository with a clean working tree. Run `gh auth login` if not set up. A project board is required — the skill will offer to create one if none exists.

## How it works

1. **Select issue** — Pick from Backlog/Todo issues by number or present a list
2. **Analyze the issue** — Fetch details, read comments for context, explore the codebase (ARCHITECTURE.md first, exploration agent only if needed), detect CDP configuration for web projects
3. **Determine execution strategy** — If Agent Teams is enabled, classify steps as sequential or parallelizable, choose Agent/Teammate/Sequential strategy
4. **Enforce development standards** — Verify TDD is present, reject workarounds, remove unnecessary code comments
5. **Propose the detailed plan** — Expand acceptance criteria into Steps with checkboxes, file paths, and TDD order (limits from `validate-issue.config.json`; splits into multiple issues if step count exceeds max)
6. **Update the issue** — Rewrite the issue body with the approved plan and assign
7. **Create branch linked to issue** — Create `feat/<number>-<slug>` from main, move board card to "In Progress"
8. **Create tasks** — One task per Step with dependency tracking
9. **Spawn workers (automatic when Execution strategy is present)** — Launch parallel agents or teammates based on strategy, with progressive auditing as each worker completes
10. **Report** — Summary with branch name, step count, task list, and execution strategy

[↑ Back to top](#start-issue)

## Issue validator rules

The issue validator (created by `/start-new-project`, run automatically by `/start-issue` after rewriting) is data-driven: `validate-issue.py` reads all rules from `validate-issue.config.json`. Change levels (`error`/`warn`/`off`), thresholds, or add new rules by editing the JSON only. It enforces these rules:

### Structure (errors)

| Rule | Validation |
|------|------------|
| `## What` section | Required |
| `## Why` section | Required |
| `## Acceptance criteria` | Required, ≥1 checkbox |
| Step count | Within `min_steps`–`max_steps` from config |
| Step numbering | Sequential, no gaps or duplicates |
| Step title format | Must use em dash (`—`), not hyphen |

### Sizing

| Rule | Level | Validation |
|------|-------|------------|
| Checkboxes per step | error | Max 8 (hard limit) — **work checkboxes only** |
| Checkboxes per step | warning | Recommended ≤6 — **work checkboxes only** |
| Checkbox text length | warning | Max 200 chars — break into multiple, never shorten |
| Empty step | error | Must have ≥1 checkbox |

> Process gates (`[PW]`, `[HUMAN]`, `[DOCS]`, `[AUDIT]`) are excluded from checkbox counting via `count_excluded_tags` in `validate-issue.config.json`. This means a step can have 8 work checkboxes plus process gates without triggering the limit.

### Checkbox tags

Every checkbox must have a tag: `` `[TAG]` ``. Valid tags and ordering:

```
RED → GREEN → INFRA → WIRE → E2E → PW → HUMAN → DOCS → AUDIT
```

| Rule | Level | Validation |
|------|-------|------------|
| `[GREEN]` requires `[RED]` | error | No GREEN without RED in same step |
| `[E2E]` requires `[PW]` | error | E2E tests need visual verification |
| `[PW]` requires `[HUMAN]` | error | Visual verification needs human approval |
| `[HUMAN]` requires `[PW]` | error | Human approval needs visual verification |
| `[AUDIT]` mandatory | error | Every step must end with AUDIT |
| `[AUDIT]` must be last | error | No tags after AUDIT |
| Frontend UI → full chain | error | UI work requires E2E + PW + HUMAN |
| Tag ordering | warning | Must follow the sequence above (RED/GREEN may alternate) |
| `[DOCS]` required | error | Mandatory when step has GREEN or WIRE |
| `[E2E]` without `[RED]` | warning | E2E without unit tests is fragile |

### Semantic rules per tag

| Tag | Level | Validation |
|-----|-------|------------|
| `[RED]` | error | Must mention "test" or "spec" |
| `[RED]` after `[RED]` | error | No consecutive RED without GREEN (horizontal TDD) |
| `[GREEN]` after `[GREEN]` | error | No consecutive GREEN without RED (vertical TDD) |
| `[GREEN]` before `[RED]` | error | GREEN can't appear before RED |
| Tag ordering with alternation | — | RED/GREEN may alternate freely (`repeatable_groups` in config) |
| `[GREEN]` writes tests | warning | Shouldn't mention writing tests |
| `[E2E]` | error | Must mention test/spec/playwright |
| `[PW]` | warning | Should mention screenshots/verification |
| `[HUMAN]` | warning | Should mention iterate/feedback (user tests the app, not screenshot review) |
| `[AUDIT]` | warning | Should mention quality.md |
| `[DOCS]` | warning | Should mention ARCHITECTURE.md |
| `[INFRA]` writes tests | warning | Shouldn't mention writing tests |
| `[WIRE]` | warning | Should mention integration/connection |

### Other

| Rule | Level | Validation |
|------|-------|------------|
| Duplicate checkboxes | error | No duplicate text in same step |
| Empty checkbox text | error | Must have description after tag |
| Last AUDIT mentions quality.md | warning | Final audit should reference quality.md |

### Extending the validator

All rules live in `validate-issue.config.json`. To add a new rule, append to the appropriate section with an existing `type`. Available rule types:

| Type | Scope | Description |
|------|-------|-------------|
| `body_match` | issue | Regex match on full issue body |
| `section_has_checkboxes` | issue | Named section must contain ≥1 checkbox |
| `step_count` | issue | Step count within min/max thresholds |
| `step_numbering` | issue | Sequential numbering without gaps |
| `step_title_format` | issue | Step title must contain em dash |
| `step_not_empty` | step | Step must have ≥1 checkbox |
| `checkbox_count_max` | step | Hard checkbox limit per step |
| `checkbox_count_recommended` | step | Soft checkbox limit per step |
| `checkbox_text_length` | step | Max chars per checkbox text |
| `checkbox_text_not_empty` | step | Checkbox must have text after tag |
| `tag_requires` | step | Tag A requires tag B in same step |
| `tag_required` | step | Tag must exist in every step |
| `tag_must_be_last` | step | Tag must be the last in the step |
| `tag_ordering` | step | Tags must follow defined order |
| `tag_recommended_with` | step | Tag recommended when other tags present |
| `ui_chain` | step | Frontend UI work requires specific tags |
| `tag_content_match` | checkbox | Checkbox with tag must match pattern |
| `tag_content_reject` | checkbox | Checkbox with tag must NOT match pattern |
| `tag_no_consecutive` | checkbox | No consecutive same-tag without separator |
| `tag_requires_before` | checkbox | Tag can't appear before required tag |
| `last_tag_content_match` | checkbox | Last occurrence of tag must match pattern |
| `no_duplicates` | step | No duplicate checkbox text |

To add a completely new rule type: add a handler in `validate-issue.py` + the JSON entry.

[↑ Back to top](#start-issue)

## Directory structure

```text
start-issue/
├── SKILL.md              # Core skill instructions (8 steps, 1 approval gate)
├── README.md             # This file
├── skill-meta.json       # Skill metadata and skeleton compliance
├── references/
│   ├── anti-patterns.md              # 13 common mistakes to avoid during planning
│   ├── cdp-best-practices.md         # Chrome DevTools Protocol setup and verification
│   ├── development-guidelines.md     # General development standards (TDD, no workarounds)
│   ├── execution-strategy.md         # Agent vs Teammate vs Sequential decision matrix
│   ├── guidelines.md                 # 22 skill-specific guidelines and verification matrix
│   ├── project-board-operations.md   # Board GraphQL mutation patterns and field IDs
│   ├── project-board-setup.md        # Board column definitions (7 columns) and custom fields
│   └── tdd-methodology.md            # Test-driven development methodology and examples
└── templates/
    └── step-template.md              # Step checkbox format template with naming conventions
```

[↑ Back to top](#start-issue)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill start-issue
```
