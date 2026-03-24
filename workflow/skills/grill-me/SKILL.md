---
name: grill-me
description: >-
  Deep structured interview about a plan, feature, or project — extracts
  decisions, constraints, and context to generate PRD input. Use when the user
  says "grill me", "me entrevista", "quero detalhar isso", "vamos aprofundar",
  "let's flesh this out", "stress-test this idea", or wants to think through
  a plan deeply — even if they don't explicitly say "grill."
user-invocable: true
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Glob
  - Grep
---

# Grill Me

Relentless, structured interview that extracts every decision, constraint, and context needed to generate a complete PRD. Works for both greenfield projects (no codebase) and features in existing codebases.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `description` | $ARGUMENTS | no | Free text — brief description of the idea | AUQ prompting for initial description |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Grill output document | `.claude/grill-output.md` | yes | Markdown (structured PRD input) |
| Report | stdout | no | Markdown |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Project files | Working directory | R | Various (package.json, go.mod, etc.) |
| Output template | `templates/grill-output.md` | R | Markdown |
| Interview branches | `references/interview-branches.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `AskUserQuestion` tool is available → if not: "AskUserQuestion is required for the interview flow." — stop.
2. Working directory is accessible → if not: "Cannot access working directory." — stop.
3. Output template exists at `templates/grill-output.md` → if not: warn and use inline structure.

</pre_flight>

## Steps

### 1. Choose interview language

Use `AskUserQuestion` to let the user pick the language for the entire interview — questions, options, summaries, and the output document. **Respect this exact option order — do not reorder based on user locale or global instructions:**

1. **English (Recommended)** — first option, always
2. **Português (BR)** — second option, always

The user can pick "Other" to type any language (e.g., Español, Français, Deutsch). The built-in "Other" option in `AskUserQuestion` handles this.

All subsequent interaction (questions, options, branch signals, checkpoint, output document) must use the chosen language. The skill instructions here are in English, but execution follows the user's choice.

### 2. Capture the starting point

If the user provided a description, use it as initial context. If not, ask with `AskUserQuestion` — a single open-ended option set encouraging a brief description of what they want to build or solve.

### 3. Detect context — existing codebase or greenfield

Check whether the current working directory has a real project (not `.brain/` or a config directory). Look for indicators: `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `src/`, `app/`, `.git` with relevant commit history.

Use `AskUserQuestion` to confirm:

- **"Existing project"** — there's a codebase to explore
- **"Greenfield"** — starting from scratch
- **"Not sure"** — need help figuring it out

This decision changes the flow: existing projects allow code exploration to validate assertions; greenfield focuses on architectural decisions.

### 4. Conduct the interview by branches

The interview follows a decision tree. Each branch must be resolved before moving to the next. Branch order adapts to context, but all branches must be covered.

Read `references/interview-branches.md` for the full branch tree and question patterns.

**Interview rules:**

1. **Every question uses `AskUserQuestion` with options.** Never ask an open-ended question without options. Always include options based on context collected so far. The user can always choose "Other" for free text (built-in to `AskUserQuestion`).

2. **Maximum 2 questions per turn** via `AskUserQuestion` (up to 4 questions allowed, but keep 1-2 per turn to avoid overload). Each question with 2-4 concrete options derived from context.

3. **Go deep before moving on.** If an answer opens sub-branches, explore them before switching topics. The decision tree is not linear — it's deep.

4. **If there's a codebase, explore the code.** When a question can be answered by the codebase (existing modules, patterns in use, current integrations), explore the code instead of asking. Tell the user what you found and ask for confirmation.

5. **Contextualize the options.** Options must reflect what has already been discussed. If the user said "delivery app", the audience options should be "Restaurants", "Drivers", "End customers" — not generic placeholders.

6. **Signal when a branch is resolved.** When finishing a branch, briefly inform: "Problem understood. Moving to [next branch]."

### 5. Alignment checkpoint

After covering all branches, present an executive summary of decisions made. Use `AskUserQuestion`:

- **"Aligned, finalize it"**
- **"Need to adjust some points"**
- **"Want to go deeper on [area]"**

If the user asks for adjustments, return to the corresponding branch and iterate.

### 6. Generate the input document

Read `templates/grill-output.md` for the output template.

Generate the document at `.claude/grill-output.md` (in the project directory, or the working directory if greenfield). The document structures all decisions collected during the interview, organized as direct input for `/write-a-prd`.

Present the file path to the user and suggest: "When you're ready to turn this into a PRD, use `/write-a-prd`."

### 7. Report

Present concisely:
- **What was done** — interview completed, branches covered, decisions extracted
- **Output** — path to `.claude/grill-output.md` with document status (complete or partial)
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

Run `/write-a-prd` to turn the grill output into a full PRD.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — all validations green
2. **Steps completed?** — all interview branches covered, checkpoint done, document generated
3. **Output exists?** — `.claude/grill-output.md` exists and contains structured decisions
4. **Anti-patterns clean?** — no open-ended questions without options, no generic options, no skipped branches
5. **Approval gates honored?** — alignment checkpoint (Step 5) completed before document generation

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Decisions captured?** — every branch resolution maps to a section in the output document
2. **No invented decisions?** — all content traces back to user answers, not assumptions
3. **Format matches template?** — output follows `templates/grill-output.md` structure
4. **Context reflected in options?** — review that options throughout the interview were contextual, not generic

Audit is scoped to content generated in THIS session.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| User abandons mid-interview | Save partial output to `.claude/grill-output.md` with `status: partial` header and list of unresolved branches |
| Codebase too large to navigate | Ask user to point to relevant areas — do not attempt full scan |
| Template file missing | Generate output inline using expected structure, warn about missing template |
| AskUserQuestion unavailable | Report error — cannot conduct interview without interactive questioning |

## Anti-patterns

- **Open-ended questions without options.** Every question must use `AskUserQuestion` with concrete options — because optionless questions slow the interview and produce vague answers.
- **Generic options that don't reflect context.** "Option A", "Option B" or placeholders unrelated to the discussion — because they signal incompetence and force the user to type "Other" every time.
- **Skipping branches because the user seems decided.** They might be wrong or have blind spots — because the interview's value comes from systematic coverage, not speed.
- **Generating output without the alignment checkpoint.** Step 5 exists to catch misunderstandings before they're baked into the document — because fixing a PRD downstream is far more expensive than fixing a summary.
- **Mixing interview with solutioning.** The skill extracts the problem, it doesn't propose the technical solution — because premature solutioning narrows the design space before constraints are fully understood.

## Guidelines

- **Respect the chosen language.** Every user-facing interaction — questions, options, summaries, branch signals, checkpoint, output document — must use the language selected in Step 1 — because skill instructions are in English for portability, but execution adapts to the user's choice.

- **Smart options, not generic ones.** `AskUserQuestion` options must demonstrate you understood the context — because if the user is talking about a B2B SaaS, offering "social media users" as an audience option wastes their time and trust.

- **Depth > breadth.** 3 deeply explored branches are better than 7 superficial ones — because unexpected answers often contain the most valuable constraints when pursued.

- **Don't invent decisions.** If the user didn't mention something, ask — don't assume — because the skill extracts information, it doesn't generate plans.

- **Adapt to detail level.** If the user is answering with short responses ("yes", "no"), the questions are good. If they're writing paragraphs, the options aren't capturing what they mean — adjust.

- **Codebase as oracle.** In existing projects, the code is truth — because if the user says "we don't have authentication" but there's an `auth/` module, gently confronting with evidence produces better decisions.

- **Handle interruptions gracefully.** If the user abandons the interview, save whatever has been collected to `.claude/grill-output.md` with a `status: partial` marker — because no context should be lost if the user returns later.

- **Budget codebase exploration.** Limit code reading to top-level structure and directly relevant modules — because attempting to read the entire codebase wastes context and slows the interview. Ask the user to point to relevant areas if the project is too large.
