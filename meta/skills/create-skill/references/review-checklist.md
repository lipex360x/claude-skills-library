# Skill Review Checklist

Validate every item before finalizing a skill. Present results to the user as a **markdown table** — this is the mandatory output format.

## Output format

Always present the checklist as a table with three columns: Item, Status, and Notas (notes). Group items by category using row headers. Use `OK` for passing items, `WARN` for warnings, `FAIL` for failures, and `N/A` for non-applicable items.

```markdown
**Review Checklist — <skill-name>:**

| Item | Status | Notas |
|------|--------|-------|
| **Description** | | |
| Pushy enough with trigger contexts? | OK | Includes "even if they don't explicitly say X" |
| WHAT + WHEN? | OK | Clear action + multiple triggers |
| **SKILL.md** | | |
| Under 500 lines? | OK | ~120 lines, lean |
| Imperative form? | OK | "Generate the spec", "Launch the agent" |
| ...etc | | |
```

This format is compact, scannable, and lets the user see pass/fail at a glance. Do NOT use bullet lists with checkboxes — always use the table format.

## Checklist items

### Description

| Item | What to check |
|------|---------------|
| Pushy enough? | Includes trigger contexts, not just a summary |
| WHAT + WHEN? | Answers what the skill does AND when it should activate |
| "Even if" pattern? | Includes "even if they don't explicitly say X" where appropriate |

### SKILL.md body

| Item | What to check |
|------|---------------|
| Under 500 lines? | Detail extracted to references/ if approaching limit |
| Imperative form? | "Extract X", not "You should extract X" |
| Constraints reasoned? | Uses "because X" rather than rigid "ALWAYS/NEVER" |
| Numbered steps? | Clear headers for major phases, numbers for sequential steps |
| Output formats? | Defined with concrete examples |
| Input contract? | Required vs optional inputs defined, with validation rules and type expectations |

### Quality

| Item | What to check |
|------|---------------|
| Quality repeated? | Quality expectations repeated at multiple key points, not just stated once |
| Anti-patterns named? | Specific failure modes listed, not just generic "make it good" |
| Refinement step? | Explicit "polish, don't add" step included |
| Error handling? | Dependency checks, input validation, and tool failure patterns applied where relevant (see `references/error-handling-patterns.md`) |

### Testing

| Item | What to check |
|------|---------------|
| Invoked with realistic input? | Skill was actually run with a real scenario, not just written and pushed |
| Activation tested? | 3+ natural trigger phrases tested — exact command, natural description, indirect reference — all activated correctly |
| Failure modes checked? | Verified: no undertriggering (fails to fire when it should), no overtriggering (fires when it shouldn't), no token bloat (loads excessive context), no silent failures (errors swallowed without user feedback) |

### Subagents (if applicable)

| Item | What to check |
|------|---------------|
| Agent context complete? | Each agent prompt includes ALL necessary context (specs, rules, quality standards) |
| Tool access explicit? | Which tools for parent, which for subagents |
| Two-phase build? | If agents depend on setup completing first |
| Race conditions? | Identified and mitigated |

### Structure

| Item | What to check |
|------|---------------|
| Standard layout? | Directory follows SKILL.md, references/, templates/ |
| References depth? | One level deep, no reference chains |
| Large refs have TOC? | References >300 lines have a table of contents |
| Self-contained? | No cross-skill dependencies |
| README generated? | README.md with all placeholders filled |

### Skeleton compliance

| Item | What to check |
|------|---------------|
| All 13 sections present? | Frontmatter, Title+Intro, Input contract, Output contract, External state, Pre-flight, Steps, Next action, Self-audit, Content audit, Error handling, Anti-patterns, Guidelines — all present in this exact order |
| Section names canonical? | "Anti-patterns" (not "Avoid these"), "Steps" (not "Process" or "Workflow"), "Guidelines" (not inline in other sections) |
| Skipped sections justified? | Every Skipped section has `> _Skipped: "reason"_` — not just omitted |
| Never-skip sections populated? | Pre-flight, Self-audit, Anti-patterns, and Guidelines always have real content — never Skipped |
| Report is last step? | The final numbered step in Steps is always "Report" with the standard structure (what was done, audit results, errors) |
| XML tags on contracts/audits? | `<input_contract>`, `<output_contract>`, `<external_state>`, `<pre_flight>`, `<self_audit>`, `<content_audit>`, `<report>` used where applicable |

### Metadata

| Item | What to check |
|------|---------------|
| `allowed-tools` declared? | Frontmatter includes explicit `allowed-tools` list — omitting means all tools available, which is rarely intended |
| `argument-hint` present? | If the skill accepts arguments, `argument-hint` shows in autocomplete |
| `skill-meta.json` generated? | Auxiliary metadata file exists alongside SKILL.md with correct schema (see `references/skill-meta-spec.md`) |
| `skill-meta.json` accurate? | `skeleton` object matches actual section states, `lineCount` matches, `references[]` lists all files in references/ |

### Content audit

| Item | What to check |
|------|---------------|
| Audit level classified? | Skill declares whether content audit applies or is N/A — never left ambiguous |
| Criteria defined (if applicable)? | If skill generates verifiable content, the Content audit section defines what to verify and how (factual, quality, structural, completeness) |
| Scoped appropriately? | For `/update-skill`: audit only modified sections. For `/create-skill`: audit the full skill. See `references/content-audit-patterns.md` |
| N/A justified (if skipped)? | If Skipped, reason clearly states why (e.g., "read-only — displays existing data, generates nothing") |

### Progressive disclosure

| Item | What to check |
|------|---------------|
| SKILL.md under 500 lines? | Detail extracted to references/ if approaching limit |
| No section exceeds ~15 lines? | Sections that exceed ~15 lines overflow to references with top 3-5 items inline and a Read pointer |
| No duplication? | Information lives in ONE place — either SKILL.md or references, never both |
| Large refs have TOC? | References >300 lines have a table of contents at the top |
| Grep patterns for huge refs? | References >10k words include grep search patterns in SKILL.md pointers |

### Compliance

| Item | What to check |
|------|---------------|
| CLAUDE.md compliance? | Frontmatter values don't violate global rules (e.g., `disable-model-invocation` default, naming conventions, plugin structure). Read the user's CLAUDE.md and verify no conflicts |
