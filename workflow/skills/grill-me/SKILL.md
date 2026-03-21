---
name: grill-me
description: Deep structured interview about a plan, feature, or project — extracts decisions, constraints, and context to generate PRD input. Use when the user says "grill me", "me entrevista", "quero detalhar isso", "vamos aprofundar", "let's flesh this out", "stress-test this idea", or wants to think through a plan deeply — even if they don't explicitly say "grill."
user-invocable: true
allowed-tools: AskUserQuestion, Bash, Read, Glob, Grep
---

# Grill Me

Relentless, structured interview that extracts every decision, constraint, and context needed to generate a complete PRD. Works for both greenfield projects (no codebase) and features in existing codebases.

## Usage

`/grill-me` or `/grill-me <brief description of the idea>`

If invoked without an argument, ask for the initial description. If invoked with an argument, use it as the starting point.

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

## Guidelines

- **Respect the chosen language.** Every user-facing interaction — questions, options, summaries, branch signals, checkpoint, output document — must use the language selected in Step 1. Skill instructions are in English for portability, but execution adapts to the user's choice.

- **Smart options, not generic ones.** `AskUserQuestion` options must demonstrate you understood the context. If the user is talking about a B2B SaaS, don't offer "social media users" as an audience option. Derive options from what's already been said — this shows competence and speeds up the interview.

- **Depth > breadth.** 3 deeply explored branches are better than 7 superficial ones. When the user answers something unexpected, pursue that thread before returning to the script.

- **Don't invent decisions.** If the user didn't mention something, ask — don't assume. The skill extracts information, it doesn't generate plans.

- **Adapt to detail level.** If the user is answering with short responses ("yes", "no"), the questions are good. If they're writing paragraphs, the options aren't capturing what they mean — adjust.

- **Codebase as oracle.** In existing projects, the code is truth. If the user says "we don't have authentication" but there's an `auth/` in the project, gently confront: "I found an auth/ module — want to leverage it or replace it?"

- **Handle interruptions gracefully.** If the user abandons the interview mid-way (stops responding, changes topic, or explicitly cancels), save whatever has been collected so far to `.claude/grill-output.md` with a `status: partial` marker in the header and a list of unresolved branches. This ensures no context is lost if the user returns later.

- **Budget codebase exploration.** When exploring an existing codebase in Step 3/4, limit code reading to the top-level structure and directly relevant modules. Do not attempt to read the entire codebase — focus on files that answer the current question. If the project is too large to navigate efficiently, ask the user to point you to the relevant areas.

- **Avoid these anti-patterns:**
  - Open-ended questions without options (violates the core rule)
  - Generic options that don't reflect context ("Option A", "Option B")
  - Skipping branches because the user seems decided (they might be wrong)
  - Generating output without the alignment checkpoint (Step 5)
  - Mixing interview with solutioning — the skill extracts the problem, it doesn't propose the technical solution
