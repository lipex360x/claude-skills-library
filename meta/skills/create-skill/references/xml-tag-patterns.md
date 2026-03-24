# XML Tag Patterns in Skills

When and how to use XML tags versus markdown in skill files, based on Anthropic's guidance for Claude 4.6.

## Decision Table

| Content type | Use XML | Use Markdown | Why |
|---|---|---|---|
| Contract tables (input, output, external state) | `<input_contract>` | -- | Explicit data boundaries prevent bleed between sections |
| Audit checklists (pre-flight, self-audit, content audit) | `<pre_flight>` | -- | Discrete verification blocks that may be copy-pasted to subagents |
| Report structure | `<report>` | -- | Structured output that needs consistent parsing |
| Subagent context injection | `<checklist>`, `<context>` | -- | Isolates context segments forwarded to subagents |
| Sequential workflow steps | -- | Numbered `###` headers | Steps are naturally sequential; markdown numbered lists work best |
| Prose instructions | -- | Paragraphs and bullets | XML adds noise to readable prose |
| Anti-patterns and guidelines | -- | Bold + bullet format | These are principles, not data structures |

## Canonical Tag Patterns

### `<pre_flight>` -- Validation before execution

Used for numbered checks that must all pass before the skill proceeds.

```xml
<pre_flight>
1. Confirm current branch is not `main` — run `git branch --show-current`
2. Verify `gh auth status` succeeds
3. Check for uncommitted changes — abort if working tree is dirty
4. Validate that ARCHITECTURE.md exists in the project root
</pre_flight>
```

### `<input_contract>` -- What the skill receives

Used for tabular data defining inputs with source, validation, and fallback behavior.

```xml
<input_contract>

| Input | Source | Required | Validation | On invalid |
|---|---|---|---|---|
| `--message` / `-m` | CLI flag | No | Non-empty string | Derive from diff |
| Branch name | `git branch --show-current` | Yes | Not `main` | Abort with error |
| Issue number | Branch name pattern `feat/<id>-*` | Yes | Matches open issue | Skip issue update |

</input_contract>
```

### `<output_contract>` -- What the skill produces

Used for tabular data defining artifacts, their location, and persistence.

```xml
<output_contract>

| Artifact | Path | Persists | Format |
|---|---|---|---|
| Git commit | Local + remote | Yes | Conventional commit message |
| Issue update | GitHub issue body | Yes | Checked checkbox in task list |
| Console summary | stdout | No | Markdown with commit hash and issue link |

</output_contract>
```

### `<external_state>` -- Resources read or modified

Used for tabular data defining external resources the skill interacts with.

```xml
<external_state>

| Resource | Path | Access | Format |
|---|---|---|---|
| GitHub issue | `gh issue view <id>` | Read + Write | Markdown body with checkboxes |
| Git history | `.git/` | Read + Write | Commits on current branch |
| Project board | GitHub Projects V2 | Write | Card status field |

</external_state>
```

### `<self_audit>` -- Post-execution verification

Used for numbered checks the skill runs on its own output before finishing.

```xml
<self_audit>
1. Verify commit exists on remote — `git log origin/<branch> --oneline -1`
2. Confirm issue checkbox was updated — re-read issue body and check the target line
3. Validate no untracked files were left behind — `git status --short`
</self_audit>
```

### `<content_audit>` -- Quality checks for generated content

Used for numbered criteria that verify content quality, accuracy, and tone.

```xml
<content_audit>
1. All code examples compile or pass lint without errors
2. Technical claims are traceable to a source document or official documentation
3. Tone matches the project voice profile — no marketing language, no filler
4. Section headers follow the lesson template structure
5. Links resolve to valid URLs (run validate-links.sh)
</content_audit>
```

### `<report>` -- Structured output summary

Used for structured summaries with consistent formatting for downstream consumption.

```xml
<report>
**Skill:** push
**Plugin:** workflow
**Steps executed:** 7/7
**Commit:** abc1234
**Issue updated:** #42 -- checked "Implement push logic"
**Warnings:** none
</report>
```

### `<checklist>` and `<context>` -- Subagent injection

Used when forwarding isolated context segments to subagents, keeping boundaries clear.

```xml
<context>
You are reviewing a skill file for compliance with the canonical skeleton.
The skill is located at: meta/skills/create-skill/SKILL.md
The review checklist is provided below.
</context>

<checklist>
1. Input contract defines all inputs with source and validation columns
2. Output contract lists every artifact with persistence flag
3. Pre-flight checks validate all preconditions before step 1
4. Error handling covers every step that can fail
5. Anti-patterns section has at least 3 entries
</checklist>
```

## Claude 4.6 Language Guidance

Claude 4.6 is significantly more responsive to system prompts and instruction-following than previous versions. This changes how skills should be written:

**Use normal language with reasoning instead of aggressive emphasis.**

- Replace: "CRITICAL: You MUST use this tool when..."
- With: "Use this tool when..."

- Replace: "ALWAYS check the branch before pushing"
- With: "Check the branch before pushing because force-pushing to main can overwrite teammates' work"

- Replace: "NEVER skip the pre-flight checks"
- With: "Run pre-flight checks before proceeding because skipping them has caused silent failures in production"

**Why this matters.** Claude 4.6 overtriggers on aggressive prompting. Excessive use of ALWAYS, NEVER, CRITICAL, and MUST causes the model to treat every instruction as maximum priority, which paradoxically reduces compliance on the instructions that actually matter. When everything is critical, nothing is.

**Constraints work better with reasoning.** Instead of bare prohibitions, explain the consequence:

- Weak: "NEVER commit directly to main"
- Strong: "Avoid committing directly to main because it bypasses CI checks and can break the deploy pipeline"

The model internalizes constraints more reliably when it understands the failure mode. This also helps it make correct judgment calls in edge cases that the rule author did not anticipate.

**Calibrate intensity to actual risk.** Reserve strong language for genuinely dangerous operations (data deletion, credential exposure, force pushes). For everything else, plain language with a brief reason is more effective.

## Hybrid Approach

Anthropic's own pattern in Claude Code: skill instructions use markdown for readability, while the runtime harness uses XML for machine-readable boundaries. Skills should follow the same split:

**XML wraps data blocks.** Contracts, checklists, and reports are structured data. XML tags give them explicit boundaries that prevent content from bleeding between sections. This is especially important when sections are extracted and forwarded to subagents — the tags act as reliable delimiters.

**Markdown wraps everything else.** Step descriptions, prose instructions, anti-patterns, and guidelines are written for human readers. Markdown headers, bullets, and bold text are natural and readable. Wrapping these in XML tags adds syntactic noise without improving clarity or parseability.

**The boundary rule.** If the content is a table, a numbered checklist, or a structured report that might be extracted programmatically or sent to a subagent, wrap it in an XML tag. If the content is prose that a human (or the model acting as a human reader) will read sequentially, use markdown.
