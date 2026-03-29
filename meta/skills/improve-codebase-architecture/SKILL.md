---
name: improve-codebase-architecture
description: Explore a codebase for architectural friction, surface shallow modules and coupling issues, and propose deep-module refactors as GitHub issue RFCs. Use when the user says "improve architecture", "refactor modules", "codebase review", "make code agent-friendly", "deep modules", "module boundaries", "architectural friction", "simplify codebase", or wants to restructure code for better testability and maintainability — even if they don't explicitly say "architecture."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# Improve Codebase Architecture

Explore a codebase like an agent would, surface architectural friction, and propose module-deepening refactors as GitHub issue RFCs. Based on John Ousterhout's "A Philosophy of Software Design" — deep modules (small interface, large implementation) improve testability, navigability, and agent output quality.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

- **Required:** A codebase with source files to analyze (the current working directory)
- **Optional:** Specific area or module to focus on (if not provided, explore the entire codebase)
- **Skip for tiny projects:** If the codebase has fewer than 5 source files, inform the user that architecture analysis isn't meaningful at this scale and suggest waiting until the project grows

</input_contract>

## Output contract

<output_contract>

- A numbered list of deepening candidates with friction signals, dependency categories, and effort estimates (step 2)
- Three radically different interface designs for the chosen candidate, with a comparative analysis and recommendation (step 4)
- A GitHub issue RFC with problem description, chosen design, migration plan, and verification criteria (step 6)
- A final report summarizing what was analyzed, what was proposed, and next steps (step 7)

</output_contract>

## External state

<external_state>

- **GitHub repo** — the skill creates issues via `gh issue create`; requires an authenticated `gh` CLI and a remote repository
- **ARCHITECTURE.md** — if present in the project root, read it first to orient exploration (but verify against actual code)
- **Backlog milestone** — if a milestone named "Backlog" exists, the created issue is added to it
- **`refactor` label** — applied to the created issue; must exist in the repository or `gh` will create it

</external_state>

## Pre-flight

<pre_flight>

1. Verify the current directory is a codebase with source files (not an empty or non-code directory)
2. Count source files — if fewer than 5, inform the user and exit gracefully
3. Check that `gh` CLI is available and authenticated (`gh auth status`); if not, warn the user that the RFC will be saved as a local markdown file instead

</pre_flight>

## Steps

### 1. Explore the codebase

Use the Agent tool with `subagent_type=Explore` to navigate the codebase organically. The friction you encounter IS the signal. Look for:

- **Shallow modules** — interface nearly as complex as implementation (many exports, thin wrappers, pass-through functions)
- **File scatter** — understanding one concept requires bouncing between many small files
- **Testability extractions** — pure functions extracted solely for testability while real bugs hide in the calling patterns
- **Tight coupling** — modules that can't change independently because they share types, state, or assumptions
- **Untested areas** — parts of the codebase with no tests, or tests that only verify implementation details

Do NOT follow rigid heuristics — explore organically and note where understanding breaks down. If `ARCHITECTURE.md` exists, read it first to orient yourself, but don't trust it blindly — verify against the actual code.

### 2. Present candidates

Present a numbered list of deepening opportunities. For each candidate:

- **Cluster** — which modules/concepts are involved (with file paths)
- **Friction signal** — what made this hard to understand or navigate
- **Why they're coupled** — shared types, call patterns, co-ownership of a concept
- **Dependency category** — read `references/dependency-categories.md` for the four categories
- **Test impact** — what existing tests would be replaced by boundary tests
- **Estimated effort** — S/M/L

Do NOT propose interfaces yet. Use `AskUserQuestion` with numbered options for the user to pick which candidate to explore.

### 3. Frame the problem space

For the chosen candidate, write a clear explanation of:

- The constraints any new interface would need to satisfy
- The dependencies it would need to handle
- A rough illustrative code sketch to make constraints concrete — this is NOT a proposal, just a way to ground the discussion

Present this to the user.

### 4. Design multiple interfaces

Spawn 3 sub-agents in parallel using the Agent tool. Each produces a **radically different** interface for the deepened module. Use `allowed_tools: ["Read", "Glob", "Grep"]` for each sub-agent — they need to read the actual code to produce grounded designs.

Give each agent a separate technical brief (file paths, coupling details, dependency category, what's being hidden) plus a different design constraint. Each agent works in two phases: first outline the approach (interface sketch + rationale), then produce the full design — this reduces wasted work if the agent misunderstands the brief.

- **Agent 1: Minimalist** — "Minimize the interface — aim for 1-3 entry points max"
- **Agent 2: Flexible** — "Maximize flexibility — support many use cases and extension"
- **Agent 3: Ergonomic** — "Optimize for the most common caller — make the default case trivial"

Each sub-agent outputs:

1. Interface signature (types, methods, params)
2. Usage example showing how callers use it
3. What complexity it hides internally
4. Dependency strategy (injection, factory, adapter)
5. Trade-offs (what you gain, what you lose)

Present designs sequentially, then compare them in prose. Give your own recommendation — which design is strongest and why. If elements from different designs combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.

### 5. User picks an interface

Use `AskUserQuestion` with the design options plus "hybrid" if you proposed one.

### 6. Create GitHub issue RFC

Create a refactor RFC as a GitHub issue using `gh issue create`. Read `references/rfc-template.md` for the issue format.

The issue includes:
- Problem description with friction signals
- Chosen interface design with usage examples
- Migration plan (what moves where, what tests change)
- Verification criteria

Add to the Backlog milestone if it exists. Apply `refactor` label.

Present the issue URL to the user.

### 7. Report

Summarize the session:

- **Codebase analyzed** — what areas were explored and total friction signals found
- **Candidate chosen** — which deepening opportunity was selected and why
- **Design selected** — which interface design was picked (minimalist / flexible / ergonomic / hybrid)
- **Issue created** — link to the GitHub issue RFC
- **Suggested next steps** — when to implement the refactor, whether to run the skill again on other candidates

## Next action

After the RFC issue is created, the user can:
- Assign the issue and start implementing the refactor
- Run this skill again to explore additional candidates from step 2
- Schedule a follow-up run after the next development surge

## Self-audit

<self_audit>

Before presenting the final report, verify:

1. Every candidate in step 2 includes concrete file paths, not vague module names
2. All three sub-agent designs in step 4 are genuinely different approaches, not variations of the same idea
3. The RFC issue includes interface signatures, usage examples, migration steps, and verification criteria — not just a description of the problem
4. No absolute or local paths (`/Users/...`, `~/.brain/`) appear in the GitHub issue content
5. The recommendation in step 4 is opinionated with clear reasoning, not a neutral comparison

</self_audit>

## Content audit

<content_audit>

- Issue title is specific (e.g., "Deepen notification module: consolidate 4 files into single boundary") not generic ("Refactor notifications")
- Issue body uses project-relative paths only
- Migration plan is a concrete sequence of moves, not a wish list
- Verification criteria are testable conditions, not subjective judgments
- All content in the issue is in English

</content_audit>

## Error handling

- **No friction found** — celebrate it. Tell the user the codebase is well-structured and suggest re-running after the next development surge.
- **Sub-agent failure** — proceed with the remaining designs. Two designs are enough for a meaningful comparison; one is enough to draft an RFC.
- **`gh` CLI unavailable** — write the RFC as a local markdown file instead of a GitHub issue, and inform the user they can create the issue manually later.

## Anti-patterns

- **Blind proposals.** Proposing refactors without reading the code first — because the friction signal comes from exploration, not assumptions.
- **Rewrite mentality.** Suggesting rewrites instead of deepening — because the goal is consolidation, not starting over.
- **Test amnesia.** Ignoring existing tests when proposing changes — because understanding what's tested prevents regressions and informs migration plans.
- **Vague issues.** Creating issues with generic "improve this" descriptions — because every issue needs concrete file paths, interface signatures, and migration steps.
- **Over-splitting.** Breaking a small refactor into many issues — because if a refactor is small enough to do in one PR, don't create 5 issues for it.

## Guidelines

- **Deep modules over shallow.** The goal is always to reduce interface surface area while increasing implementation depth. A module with 1 method hiding 500 lines of logic is better than 10 modules with 50 lines each — because the 1-method module is trivially testable at the boundary and agents navigate it without confusion.

- **Agent-friendliness is human-friendliness.** If an agent struggles to navigate a part of the codebase (bouncing between files, losing context), humans struggle too. This skill surfaces the same friction humans feel but are too accustomed to notice.

- **Don't refactor everything.** Present candidates, let the user choose. Not every shallow module needs deepening — some are fine as-is because they rarely change. Focus on high-churn areas where coupling creates real problems.

- **Vertical slices in refactoring.** Each refactor should be independently completable and verifiable. Don't propose a plan that requires completing 5 refactors before anything works.

- **Tests change, not disappear.** When deepening a module, internal tests become boundary tests. The test count might decrease (because boundary tests cover more), but coverage should stay the same or increase.

- **Run weekly or after development surges.** This skill is most valuable when the codebase has grown organically and accumulated accidental complexity. After a feature push is the best time to consolidate.

- **English for all issue content.** Issues are public and portable — always write in English. Communication with the user follows their language preference.

- **No local paths in issues.** Use project-relative paths only. Never reference `~/.brain/`, `/Users/...`, or any absolute paths in issue content.
