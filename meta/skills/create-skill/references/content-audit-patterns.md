# Content Audit Patterns

Reference for the Content audit section of the skill skeleton. Covers when skills should verify their own output, what types of verification exist, and how content audit integrates with the broader audit system.

---

## Three Audit Levels

The skills ecosystem has three distinct audit levels. Each operates at a different scope and trigger point.

### 1. Process audit (Self-audit)

Universal — every skill runs this. Verifies the skill's own execution quality:

- Did all steps complete in order?
- Was output created where expected?
- Were anti-patterns avoided?
- Were approval gates honored (no silent skips)?

This is the "Self-audit" section in the skeleton. It runs at the end of every skill execution regardless of skill type.

### 2. Content audit

For content-producing skills. Verifies the accuracy and quality of what the skill generated:

- Are factual claims correct?
- Does the output match the declared format or schema?
- Do cited references actually exist?
- Are all expected parts present?

This is the "Content audit" section in the skeleton. It runs only in skills that generate verifiable output. Skills that display, move, or toggle existing data mark this section as N/A.

### 3. Structural audit

External — run by `/audit-skill`, not by the skill itself. Verifies that a skill conforms to the skeleton standard:

- Are all 13 sections present?
- Is `skill-meta.json` generated?
- Is `SKILL.md` under 500 lines?
- Are references self-contained (no cross-skill dependencies)?

This is NOT part of a skill's own execution. It is a separate evaluation tool that inspects skills from the outside.

---

## Audit Type Taxonomy

Content audits fall into four types. A skill may use one or more depending on what it generates.

### Factual audit

Verify claims against authoritative sources via WebSearch.

**When to use:** Skills that generate educational content, documentation, or technical references.

**Example:** `/add-lesson` Step 11 reads the full lesson JSON, fact-checks every definition, example, and exercise answer against authoritative sources. Each finding is logged as verified, corrected, or flagged. New reference URLs discovered during verification are added to the lesson's references section.

**Pattern:**
1. Read the generated content
2. For each factual claim: run WebSearch against authoritative sources
3. Compare the claim against search results
4. Log finding as verified / corrected / flagged
5. Present audit report with all findings
6. Apply corrections to the content

### Quality audit

Verify output against a skill-specific checklist.

**When to use:** Skills that generate creative or structured content (posts, copy, READMEs).

**Example:** `/write-content` Step 6 runs a 20-item checklist covering:
- Story structure: ABT backbone present? Peak moment identified? Open loops resolved?
- Voice authenticity: Sounds like the user? Avoids AI tells (filler phrases, hedge words)?
- Hook quality: First 210 characters stop the scroll?
- Content density: Every paragraph passes the "so what?" test?

Each item gets a pass/fail result. Failed items trigger a polish pass before presenting to the user.

**Pattern:**
1. Read the generated output
2. Check each criterion on the skill's checklist
3. Present pass/fail results
4. Polish failed items before presenting final output

### Structural audit (output-level)

Verify output matches a declared format or schema.

Not to be confused with the structural audit level (which inspects skills themselves). This audit type inspects whether a skill's output conforms to an expected structure.

**When to use:** Skills that generate structured data (JSON, YAML, configs, issue bodies).

**Example:** `/start-issue` verifies the proposed plan has:
- What/Why sections present
- Acceptance criteria formatted as checkboxes
- Numbered Steps (each with 2-6 checkboxes)
- TDD order (test step before implementation step)
- File paths included where codebase context is known

Missing or malformed sections are flagged before presenting the plan for approval.

**Pattern:**
1. Read the generated output
2. Validate against the expected structure definition
3. Flag missing or malformed sections
4. Fix structural issues before presenting

### Completeness audit

Verify all expected items are present.

**When to use:** Skills that generate multi-part output (translations, catalog entries, checklists).

**Example:** `/add-lesson` Step 8 verifies catalog consistency:
- `courses.json` has the subject in its `subjects` array
- `subjects.json` has the subject entry with all locale translations
- `lessons.json` has the lesson entry with all locales

Missing any locale for any catalog entry means the output is incomplete. The skill must fill gaps before proceeding.

**Pattern:**
1. Read the generated output
2. Enumerate all expected items (locales, entries, parts)
3. Check each item exists and is well-formed
4. Report gaps and fill them before proceeding

---

## Scoped Audit Principle

A skill audits only what it generated or modified in the current session. It does not re-audit pre-existing content that was not touched.

| Scenario | Audit scope | Reason |
|---|---|---|
| `/create-skill` creates a new skill | Audit the entire skill | The skill created everything from scratch |
| `/update-skill` modifies two sections | Audit only those two sections | The rest was audited when originally created |
| `/add-lesson` creates a new lesson | Audit the entire lesson before translation | The skill generated all content |
| `/update-lesson` fixes one exercise | Audit only the modified exercise | The rest was audited at creation time |

Full re-audit of an entire skill (all sections, all references, all metadata) is the job of `/audit-skill`, not the skill's own content audit. A skill is responsible for verifying its own session output, not for policing everything that already exists.

---

## N/A Classification

Not every skill needs a content audit. The deciding factor is whether the skill generates verifiable output.

| Skill type | Content audit | Reason |
|---|---|---|
| Read-only (`list-issues`, `list-backlog`) | N/A | Displays existing data, generates nothing |
| State management (`open-tasks`, `clean-tasks`, `close-tasks`) | N/A | Toggles state, generates no content |
| Move/transition (`cancel-issue` board moves, `push` git operations) | N/A | Moves existing artifacts, generates no content |
| Sync/install (`sync-claude`, `install-skill`, `uninstall-skill`) | N/A | Manages existing files, generates no content |
| Content generation (`write-content`, `add-lesson`, `create-diagram`) | Required | Generates verifiable output |
| Plan generation (`start-issue`, `start-new-project`, `add-backlog`) | Required | Generates structured plans with verifiable checkboxes |
| Skill creation (`create-skill`, `update-skill`) | Required | Generates SKILL.md files that must follow standards |
| Interview (`grill-me`, `inspire-me`) | Partial | Generates output document -- verify structure, but content is user-driven |

When a skill marks Content audit as N/A, it should state "Skipped -- [reason]" in the skeleton section rather than leaving it blank. This makes the classification explicit and auditable by `/audit-skill`.

---

## Integration with Self-audit and Report

Content audit is not standalone. It feeds into the Self-audit checklist and the final Report step.

### Execution order

1. Skill completes its generation steps
2. **Content audit runs** (verifies generated output)
3. Corrections from content audit are applied to the output
4. **Self-audit runs** (verifies the skill's process, including that content audit happened)
5. **Report step** summarizes everything

### How results appear in the Report

The Report step includes a content audit summary line:

```
Content audit: 12 items verified, 1 corrected (exercise Q3 answer), 0 flagged
```

Or for N/A skills:

```
Content audit: Skipped -- skill displays existing data, generates nothing
```

### Self-audit dependency

Self-audit check #3 ("Output exists and is correct?") depends on content audit having run first. It verifies:
- Content audit actually executed (was not silently skipped)
- Corrections identified by content audit were applied to the output
- No "flagged" items remain unresolved

### Flagged items requiring user decision

If content audit finds issues that cannot be auto-corrected (ambiguous facts, subjective quality judgments, conflicting sources), these are classified as "flagged" rather than "corrected." Flagged items must be presented to the user before the Report step, with clear options for resolution. The Report then reflects the user's decisions.
