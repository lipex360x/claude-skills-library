---
name: plan-skill
description: >-
  Plan and spec out a Claude Code skill from raw input — a document,
  conversation, verbal idea, or rough notes. Produces a structured spec file
  that /create-skill consumes directly. Use this skill whenever the user says
  "plan a skill", "spec for a skill", "structure this idea into a skill",
  "prepare input for create-skill", "think through a skill before building it",
  or describes a skill idea they want to formalize — even if they don't
  explicitly say "plan".
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

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `skill idea` | $ARGUMENTS (file path), $ARGUMENTS (kebab-case name hint), or conversation context | yes | At least one source with enough signal to identify what the skill does | AUQ: "I couldn't detect a skill idea. What would you like to plan?" with options |
| `skill name` | $ARGUMENTS | no | Kebab-case, verb-subject pattern | Infer from input; fix naming in Step 5 |

**Parsing rules:**
1. If args contain a valid file path (file exists on disk), read the file as primary input
2. If args contain a kebab-case string that is not a file path, treat it as the skill name hint
3. If no args, summarize the current conversation as input
4. Multiple sources can combine — a file path plus conversation context both feed the analysis

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Spec file | `downloads/<skill-name>-spec.md` | yes | Markdown (spec template) |
| Decisions summary | stdout | no | Markdown table |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | R | Markdown |
| Completeness checklist | `references/completeness-checklist.md` | R | Markdown |
| Decision model | `references/decision-model.md` | R | Markdown |
| Spec template | `templates/spec-template.md` | R | Markdown |
| Spec output | `downloads/<skill-name>-spec.md` | W | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. At least one input source detected (file path, name hint, or conversation context) → if none: AUQ with options `["Let me describe it now", "Let me provide a file path"]` — stop if neither.
2. `references/completeness-checklist.md` readable → if missing: "Completeness checklist not found at references/completeness-checklist.md" — stop.
3. `references/decision-model.md` readable → if missing: "Decision model not found at references/decision-model.md" — stop.
4. `templates/spec-template.md` readable → if missing: "Spec template not found at templates/spec-template.md" — stop.

</pre_flight>

## Steps

### 1. Parse input

Detect the input source and extract raw material for analysis.

- **File path in args:** Read the file with the Read tool. Validate it exists. Extract full content.
- **Conversation context:** Summarize relevant parts — what the user described, constraints, examples. Discard noise.
- **Verbal description:** Use the raw text as-is.
- **Skill name hint:** If args contain a kebab-case string that is not a file path, record it as candidate name. Note any verb-subject violation — Step 5 handles naming.

If no input source yields usable content, stop and AUQ with options.

### 2. Run completeness checklist

Read `references/completeness-checklist.md` for the full checklist (8 categories, 40 questions).

Iterate through every category and every question. For each item:

1. Search the parsed input for explicit answers, implicit signals, or related context
2. Classify using rules in `references/decision-model.md`:
   - Clear answer with high confidence → `[inferred]`
   - No answer but non-blocking (safe default exists) → `[gap]`
   - Ambiguous or has architectural implications → `[ask]`
3. Record the classification, the decision (if inferred), and the rationale

Do not skip categories that seem irrelevant — check them and mark items as `[gap]` with "not applicable" if truly irrelevant.

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

If the gap count exceeds 10, warn the user that the input may need more detail.

### 3. Present decisions

Follow the presentation order defined in `references/decision-model.md`.

**3a. Show inferred decisions** — present all `[inferred]` items in a table with rationale. State: "Review these. Override any that are wrong."

**3b. Batch ask items** — group related `[ask]` items and present via AUQ with concrete options. Maximum 4 questions per AUQ call. Never present open-ended questions — always provide selectable options with trade-off descriptions.

**3c. List gap items** — present as a non-blocking warning list. State: "These gaps have safe defaults. `/create-skill` will resolve them during implementation."

### 4. Self-containment check

Scan accumulated decisions for opaque references. A spec must be readable by a fresh session with zero prior context.

**Flag and rewrite any of these:**
- Bare issue numbers without context
- "See above" / "as mentioned" without specifying what
- Pronouns without clear antecedents
- References to conversation context that won't exist later
- Unexpanded acronyms or jargon

Rewrite violations inline — this is a mechanical quality pass, do not ask the user.

### 5. CLAUDE.md compliance check

Read `~/.claude/CLAUDE.md`. Validate the draft spec against its rules:

- **Naming convention:** verb-subject pattern. If violated, propose corrected name.
- **disable-model-invocation:** must not be `true` unless user explicitly requested it.
- **Plugin structure:** skill must target a valid plugin.
- **Self-contained:** no cross-skill runtime dependencies.
- **SKILL.md line limit:** if planned content exceeds 500 lines, suggest `references/` extraction.

Present any violations with the rule and proposed fix.

### 6. Generate spec

Read `templates/spec-template.md` for the output format. Fill every section:

- **Meta table:** skill name, plugin, user-invocable, input sources, output description
- **Purpose:** what it does, why it exists, what it does NOT do
- **Trigger:** description draft, activation phrases
- **Input contract:** required/optional inputs, parsing rules
- **Workflow:** numbered steps with Action, Inputs, Outputs, Failure path
- **Output contract:** format, location, post-output actions
- **Dependencies:** external tools, file reads, file writes
- **Cross-skill state:** reads from / writes for other skills, shared resources
- **Guardrails:** must do, must NOT do, idempotency, resource cost
- **Decisions log:** every decision with classification and rationale

Write the completed spec to `downloads/<skill-name>-spec.md`.

### 7. Report

<report>

Present concisely:
- **Spec:** `downloads/<skill-name>-spec.md`
- **Decisions:** X inferred, Y asked, Z gaps
- **Ready for:** `/create-skill` — pass the spec file as input
- **Gaps to resolve:** list if any critical gaps remain
- **Audit results:** self-audit + content audit summary
- **Errors:** issues encountered (or "none")

</report>

## Next action

Run `/create-skill` and pass the generated spec file as input.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — input source detected, reference files readable
2. **Steps completed?** — all 6 steps executed, list any skipped with reason
3. **Output exists?** — spec file written at `downloads/<skill-name>-spec.md`
4. **Completeness checklist done?** — all 8 categories evaluated, scoring summary produced
5. **Self-containment clean?** — no opaque references in the spec
6. **CLAUDE.md compliant?** — naming, plugin, line limit all validated
7. **Anti-patterns clean?** — no unnecessary asks, no raw checklist output, no open-ended AUQ

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Spec self-contained?** — a fresh session can read it and build the skill without prior context
2. **All sections filled?** — no empty sections in the spec template (use "N/A — [reason]" if not applicable)
3. **Decisions consistent?** — no contradictions between inferred decisions and spec content
4. **References valid?** — all paths cited in the spec exist and are accessible
5. **Naming correct?** — skill name follows verb-subject pattern

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| No input source detected | AUQ with options to describe or provide file path → stop if neither |
| Reference file missing | Report which file and path → stop |
| Template file missing | Report path → stop |
| Input too vague for checklist | Warn user: "Input may need more detail" → proceed with high gap count |
| `downloads/` directory missing | Create it before writing spec |
| CLAUDE.md not found | Skip compliance check, note in report |

## Anti-patterns

- **Asking what can be inferred.** If CLAUDE.md rules, codebase patterns, or input provide a clear answer, infer it — because every unnecessary question erodes user trust and slows the process. Infer and show for review; overriding is faster than answering.
- **Presenting raw checklist output.** The user does not need 40 questions with `[inferred]` tags — because the checklist is an internal tool. Present the scoring summary, then grouped decisions per Step 3.
- **Skipping the self-containment check.** Specs written during a conversation are full of opaque references — because every spec that skipped Step 4 caused confusion when consumed by `/create-skill`.
- **Open-ended AUQ questions.** "What should error handling look like?" is useless — because concrete options with trade-offs are actionable while open questions stall the user.
- **Generating incomplete specs.** Every section of the template must be filled — because empty sections signal incomplete planning and force `/create-skill` to guess.
- **Treating gaps as blockers.** Gaps are non-blocking by design. A spec with 8 gaps and 0 asks is ready — because promoting gaps to asks wastes user time on decisions that have safe defaults.

## Guidelines

- **Infer aggressively, show for review.** The default posture is to make decisions and present them, not to ask. Overriding a wrong inference is faster than answering a question from scratch — because this keeps the planning flow fast and respects the user's time.

- **Self-contained specs above all.** The spec must be readable by a fresh session with zero prior context. No "see above", no bare issue numbers, no unexpanded jargon — because specs are consumed hours or days later in a completely different session.

- **Checklist is internal, decisions are external.** The 40-question checklist drives thoroughness. The user sees the scoring summary and grouped decisions — because exposing the internal process adds noise without value.

- **Gaps have safe defaults.** A gap means "no answer, but we can proceed." Only promote to `[ask]` when the decision has architectural implications — because over-asking is the most common failure mode in skill planning.
