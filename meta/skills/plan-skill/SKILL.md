---
name: plan-skill
description: Plan and spec out a Claude Code skill from raw input — a document, conversation, verbal idea, or rough notes. Produces a structured spec file that /create-skill consumes directly. Use this skill whenever the user says "plan a skill", "spec for a skill", "structure this idea into a skill", "prepare input for create-skill", "think through a skill before building it", or describes a skill idea they want to formalize — even if they don't explicitly say "plan".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - WebSearch
  - WebFetch
---

# Plan Skill

Analyze raw input (document, conversation, verbal idea) and produce a structured spec file. The spec pre-makes 90% of decisions so `/create-skill` can execute without ambiguity. The output is a self-contained spec — a fresh session can read it and build the skill without prior context.

## Usage

**With file path:** `/plan-skill path/to/input.md` — reads the file and extracts skill design from its content.

**With skill name hint:** `/plan-skill my-skill-name` — uses the arg as the skill name, draws input from conversation context.

**No arguments:** `/plan-skill` — uses the current conversation as input.

## Input contract

### Required inputs

| Name | Source | Validation |
|------|--------|------------|
| Skill idea | At least one of: file path (args), conversation context, or verbal description | Must contain enough signal to identify what the skill does. If no input source is detected, stop and ask |

### Optional inputs

| Name | Default | Description |
|------|---------|-------------|
| Skill name | Inferred from input | Arg value treated as skill name hint if it matches kebab-case (`verb-subject` pattern). If ambiguous, infer from the skill's core action |

### Input parsing rules

1. If args contain a valid file path (file exists on disk), read the file as primary input
2. If args contain a kebab-case string that is not a file path, treat it as the skill name hint
3. If no args, summarize the current conversation as input
4. Multiple sources can combine — a file path plus conversation context both feed the analysis

## Steps

### 1. Parse input

Detect the input source and extract raw material for analysis.

- **File path in args:** Read the file with the Read tool. Validate it exists. Extract the full content as input.
- **Conversation context:** Summarize the relevant parts of the conversation — what the user described, constraints they mentioned, examples they gave. Discard noise (greetings, tangents, meta-discussion).
- **Verbal description:** Use the raw text as-is.
- **Skill name hint:** If args contain a kebab-case string that is not a file path, record it as the candidate skill name. Validate it follows the verb-subject naming convention. If it does not (e.g., `skill-creator` instead of `create-skill`), note the violation but do not fix it yet — Step 5 handles naming.

If no input source yields usable content, stop and ask via `AskUserQuestion`:

```
question: "I couldn't detect a skill idea from the input. What would you like to plan?"
options:
  - label: "Let me describe it now"
    description: "I'll describe the skill idea in the next message"
  - label: "Let me provide a file path"
    description: "I have a document with the skill idea"
```

### 2. Run completeness checklist

Read `references/completeness-checklist.md` for the full checklist (8 categories, 40 questions).

Iterate through every category and every question. For each item:

1. Search the parsed input for explicit answers, implicit signals, or related context
2. Classify using the rules in `references/decision-model.md`:
   - Clear answer with high confidence → `[inferred]`
   - No answer but non-blocking (safe default exists) → `[gap]`
   - Ambiguous or has architectural implications → `[ask]`
3. Record the classification, the decision (if inferred), and the rationale

Do not skip categories that seem irrelevant — check them and mark items as `[gap]` with "not applicable" if truly irrelevant. Skipping categories silently is how specs ship with blind spots.

After completing all categories, produce the scoring summary:

```markdown
| Category | Items | Inferred | Gaps | Asks |
|----------|-------|----------|------|------|
| External deps | 5 | ... | ... | ... |
| Cross-skill state | 5 | ... | ... | ... |
| Input ambiguity | 5 | ... | ... | ... |
| Resource cost | 5 | ... | ... | ... |
| Idempotency | 4 | ... | ... | ... |
| Error surface | 5 | ... | ... | ... |
| Guardrails | 5 | ... | ... | ... |
| VCS impact | 5 | ... | ... | ... |
| **Total** | **39** | **X** | **Y** | **Z** |
```

If the gap count exceeds 10, warn the user that the input may need more detail before proceeding to `/create-skill`.

### 3. Present decisions

Follow the presentation order defined in `references/decision-model.md`. The order builds trust: show what was understood, then ask what is genuinely unclear, then flag what is missing.

**3a. Show inferred decisions**

Present all `[inferred]` items in a table:

```markdown
| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Plugin is `meta` | Input explicitly states skill management context |
| 2 | User-invocable: true | Skill is a /command, not auto-triggered |
```

State: "Review these inferred decisions. Override any that are wrong — otherwise they'll be locked into the spec."

**3b. Batch ask items**

Group related `[ask]` items and present via `AskUserQuestion` with concrete options. Rules:

- Maximum 4 questions per AUQ call
- Each option must have a label and description with concrete trade-offs
- If more than 4 asks exist, split into sequential AUQ calls ordered by dependency (decisions that inform later questions go first)
- Never present open-ended questions — always provide selectable options. If you cannot generate concrete options, the item is likely a `[gap]`, not an `[ask]`

**3c. List gap items**

Present `[gap]` items as a non-blocking warning list:

```markdown
**Gaps (non-blocking — will use safe defaults):**
- Idempotency behavior: default to overwrite with warning
- Exact error messages: deferred to implementation
```

State: "These gaps have safe defaults. `/create-skill` will resolve them during implementation. Flag any that need explicit decisions now."

### 4. Self-containment check

Scan the accumulated decisions and draft spec content for opaque references. A spec must be readable by a fresh session with zero prior context.

**Flag and rewrite any of these:**

- Bare issue numbers without context (e.g., "#12" → "Issue #12: plan-skill creation")
- "See above" / "as mentioned" / "the previous" without specifying what
- Pronouns without clear antecedents ("it should handle this" — what is "it", what is "this"?)
- References to conversation context that won't exist when the spec is read later
- Unexpanded acronyms or jargon specific to the current conversation

For each violation found, rewrite the reference inline to be self-contained. Do not ask the user — this is a mechanical quality pass.

### 5. CLAUDE.md compliance check

Read the user's global CLAUDE.md (at `~/.claude/CLAUDE.md` or the path resolved from the working directory). Validate the draft spec against its rules.

**Check specifically for:**

- **Naming convention:** Skill name follows verb-subject pattern (e.g., `plan-skill`, not `skill-planner`). If the name from Step 1 violates this, propose a corrected name
- **disable-model-invocation:** Must not be set to `true` unless the user explicitly requested it. If the spec sets it, flag the violation
- **Plugin structure:** Skill must target a valid plugin from the CLAUDE.md plugin list. If the target plugin is unclear, mark as `[ask]`
- **Self-contained:** No cross-skill runtime dependencies. References to other skills as documentation of contracts are fine; imports or calls to other skills at runtime are not
- **SKILL.md line limit:** If the planned skill's content would exceed 500 lines, flag it and suggest what to extract to `references/`

Present any violations to the user with the rule that was violated and the proposed fix.

### 6. Generate spec

Read `templates/spec-template.md` for the output format.

Fill every section of the template with the decisions from Steps 2-5:

- **Meta table:** skill name, plugin, user-invocable, input sources, output description
- **Purpose:** what it does, why it exists, what it does NOT do
- **Trigger:** description draft (from the accumulated understanding), activation phrases
- **Input contract:** required/optional inputs, parsing rules
- **Workflow:** numbered steps with Action, Inputs, Outputs, Failure path for each
- **Output contract:** format, location, post-output actions
- **Dependencies:** external tools, file reads, file writes
- **Cross-skill state:** reads from / writes for other skills, shared resources
- **Guardrails:** must do, must NOT do, idempotency, resource cost
- **Decisions log:** every decision from Step 2 with classification and rationale

Write the completed spec to `downloads/<skill-name>-spec.md`.

Present a summary to the user:

```markdown
## Spec generated: `<skill-name>`

- **Location:** `downloads/<skill-name>-spec.md`
- **Decisions:** X inferred, Y asked, Z gaps
- **Ready for:** `/create-skill` — pass the spec file as input
- **Gaps to resolve:** [list if any critical gaps remain]
```

## Guidelines

### Anti-patterns to avoid

- **Asking what can be inferred.** If the CLAUDE.md rules, codebase patterns, or input provide a clear answer, infer it. Every unnecessary question erodes user trust and slows the process. When in doubt, infer and show for review — overriding an inference is faster than answering a question.
- **Presenting raw checklist output.** The user does not need to see 40 questions with `[inferred]` tags. Present the scoring summary table, then the grouped decisions per Step 3. The checklist is an internal tool, not a user-facing artifact.
- **Skipping the self-containment check.** Specs written during a conversation are full of opaque references that make no sense a day later. Step 4 exists because every spec that skipped it caused confusion when consumed by `/create-skill`.
- **Open-ended AUQ questions.** "What should the error handling look like?" is useless. "How should the skill handle missing input?" with 3 concrete options is actionable. Always provide selectable options with trade-off descriptions.
- **Generating incomplete specs.** Every section of `templates/spec-template.md` must be filled. Empty sections signal that the planning was incomplete. If a section is genuinely not applicable, write "N/A — [reason]" instead of leaving it blank.
- **Treating gaps as blockers.** Gaps are non-blocking by design. A spec with 8 gaps and 0 asks is ready for `/create-skill`. A spec where gaps were promoted to asks because the planner was overly cautious wastes user time.

## External state

| Resource | Path | Access | Purpose |
|----------|------|--------|---------|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | Read | Compliance check against user's global rules (Step 5) |
| Spec output | `downloads/<skill-name>-spec.md` | Write (create) | Generated spec file consumed by `/create-skill` |
| Completeness checklist | `references/completeness-checklist.md` | Read | 8-category analysis framework (Step 2) |
| Decision model | `references/decision-model.md` | Read | Classification rules for [inferred]/[gap]/[ask] (Step 2) |
| Spec template | `templates/spec-template.md` | Read | Output format for the generated spec (Step 6) |
