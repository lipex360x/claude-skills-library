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

### Compliance

| Item | What to check |
|------|---------------|
| CLAUDE.md compliance? | Frontmatter values don't violate global rules (e.g., `disable-model-invocation` default, naming conventions, plugin structure). Read the user's CLAUDE.md and verify no conflicts |
