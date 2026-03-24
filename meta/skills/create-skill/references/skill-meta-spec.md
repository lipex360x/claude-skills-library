# skill-meta.json Specification

Auxiliary metadata file generated alongside every skill's SKILL.md. Provides instant context for editing and auditing without parsing the full skill file.

## Purpose

- One JSON file per skill, co-located with SKILL.md
- Gives `/update-skill` scoped edit context and `/audit-skill` compliance state in a single Read (roughly 20 lines)
- Eliminates re-discovery: no need to parse SKILL.md headers, count steps, or scan for missing sections
- Machine-readable complement to the human-readable SKILL.md

## JSON Schema

```json
{
  "schema": 1,
  "skeletonVersion": 1,
  "name": "<string>",
  "plugin": "<string>",
  "created": "<YYYY-MM-DD>",
  "lastModified": "<YYYY-MM-DD>",
  "lineCount": "<number>",
  "skeleton": {
    "inputContract": "<boolean | string>",
    "outputContract": "<boolean | string>",
    "externalState": "<boolean | string>",
    "preFlight": "<boolean | string>",
    "selfAudit": "<boolean | string>",
    "contentAudit": "<boolean | string>",
    "errorHandling": "<boolean | string>",
    "antiPatterns": "<boolean | string>",
    "guidelines": "<boolean | string>"
  },
  "steps": "<number>",
  "approvalGates": "<number>",
  "references": ["<string>"],
  "templates": ["<string>"],
  "scripts": ["<string>"],
  "dependencies": {
    "tools": ["<string>"],
    "configs": ["<string>"],
    "skills": ["<string>"]
  },
  "audit": {
    "lastRun": "<YYYY-MM-DD | null>",
    "score": "<string | null>",
    "gaps": ["<string>"]
  }
}
```

## Field Reference

### Top-level fields

| Field | Type | Description | Validation |
|---|---|---|---|
| `schema` | number | Schema version. Always `1` for this spec | Must be `1` |
| `skeletonVersion` | number | Version of the canonical skeleton this skill was built against. Incremented in `skeleton-template.md` when the skeleton structure changes (new sections, renamed sections, new required fields). Used by `/audit-skill` to detect drift and by `/update-skill` to find outdated skills | Must match the current version in `skeleton-template.md` |
| `name` | string | Skill invocation name (without `/` or plugin prefix) | Must match the skill directory name |
| `plugin` | string | Plugin namespace the skill belongs to | Must match a registered plugin in `skills-library/` |
| `created` | string | Date the skill was first generated (ISO 8601 date) | Format `YYYY-MM-DD`, immutable after creation |
| `lastModified` | string | Date of most recent edit to SKILL.md or references | Format `YYYY-MM-DD`, updated on every edit |
| `lineCount` | number | Total line count of SKILL.md | Positive integer, should stay under 500 per repo rules |

### `skeleton` object

Maps each canonical skeleton section to its presence status. Values:

- `true` — section is present and complete
- `false` — section is missing and needs to be added
- `string` — section was intentionally skipped, with a justification reason

| Field | Skeleton section | Notes |
|---|---|---|
| `inputContract` | Input Contract | What the skill receives: flags, arguments, implicit context |
| `outputContract` | Output Contract | Artifacts the skill produces: files, commits, messages |
| `externalState` | External State | Resources read or modified: APIs, config files, databases |
| `preFlight` | Pre-flight Checks | Validations before execution begins |
| `selfAudit` | Self-audit Checklist | Post-execution verification the skill runs on its own output |
| `contentAudit` | Content Audit | Quality checks for generated content (factual accuracy, tone). Set to a string reason when the skill does not generate verifiable content |
| `errorHandling` | Error Handling | How the skill recovers from failures at each step |
| `antiPatterns` | Anti-patterns | Known failure modes to avoid |
| `guidelines` | Guidelines | Behavioral principles and constraints |

### Workflow fields

| Field | Type | Description | Validation |
|---|---|---|---|
| `steps` | number | Total numbered steps in the skill workflow | Positive integer |
| `approvalGates` | number | Steps that pause for user confirmation before proceeding | Non-negative integer, must be <= `steps` |

### Asset fields

| Field | Type | Description | Validation |
|---|---|---|---|
| `references` | string[] | Filenames in the skill's `references/` directory | Each file must exist in `references/` |
| `templates` | string[] | Filenames in the skill's `templates/` directory | Each file must exist in `templates/` |
| `scripts` | string[] | Filenames in the skill's `scripts/` directory | Each file must exist in `scripts/` |

### `dependencies` object

| Field | Type | Description | Validation |
|---|---|---|---|
| `tools` | string[] | External CLI tools the skill invokes (e.g., `gh`, `git`, `npx`) | Non-empty if skill runs shell commands |
| `configs` | string[] | Config files the skill reads or depends on (e.g., `ARCHITECTURE.md`) | Paths relative to project root |
| `skills` | string[] | Other skills this skill invokes or delegates to | Must be empty per self-containment rule; flag violations |

### `audit` object

| Field | Type | Description | Validation |
|---|---|---|---|
| `lastRun` | string or null | Date of the most recent `/audit-skill` run | Format `YYYY-MM-DD` or `null` if never audited |
| `score` | string or null | Audit result (e.g., `"9/10"`, `"PASS"`) | `null` if never audited |
| `gaps` | string[] | List of issues found in the last audit | Empty array if no gaps or never audited |

## Lifecycle

### Generated by

`/create-skill` generates `skill-meta.json` as the final step before push. The file is committed alongside SKILL.md and all references.

### Updated by

- `/update-skill` — refreshes `lastModified`, `lineCount`, and any `skeleton` fields that changed during the edit session
- `/audit-skill` — writes audit results into the `audit` object (`lastRun`, `score`, `gaps`) and corrects any stale `skeleton` booleans

### Read by

- `/update-skill` — reads the file first to get instant context: which sections exist, what references are available, current line count
- `/audit-skill` — reads current state before running checks, then writes results back
- Any agent exploring a skill — one Read gives the full picture without parsing SKILL.md

## Examples

### Example 1: `/push` (simple workflow skill)

```json
{
  "schema": 1,
  "skeletonVersion": 1,
  "name": "push",
  "plugin": "workflow",
  "created": "2025-12-15",
  "lastModified": "2026-03-24",
  "lineCount": 148,
  "skeleton": {
    "inputContract": true,
    "outputContract": true,
    "externalState": true,
    "preFlight": true,
    "selfAudit": true,
    "contentAudit": "N/A — does not generate verifiable content",
    "errorHandling": true,
    "antiPatterns": true,
    "guidelines": true
  },
  "steps": 7,
  "approvalGates": 0,
  "references": ["issue-update-guide.md"],
  "templates": [],
  "scripts": [],
  "dependencies": {
    "tools": ["gh", "git"],
    "configs": ["ARCHITECTURE.md"],
    "skills": []
  },
  "audit": {
    "lastRun": null,
    "score": null,
    "gaps": []
  }
}
```

A straightforward workflow skill. Content audit is skipped with justification because `/push` commits and pushes code but does not generate prose or content that requires factual verification. No approval gates — all steps execute automatically. Single reference file for issue checkbox update logic.

### Example 2: `/add-lesson` (complex content skill)

```json
{
  "schema": 1,
  "skeletonVersion": 1,
  "name": "add-lesson",
  "plugin": "content",
  "created": "2026-01-20",
  "lastModified": "2026-03-18",
  "lineCount": 412,
  "skeleton": {
    "inputContract": true,
    "outputContract": true,
    "externalState": true,
    "preFlight": true,
    "selfAudit": true,
    "contentAudit": true,
    "errorHandling": true,
    "antiPatterns": true,
    "guidelines": true
  },
  "steps": 14,
  "approvalGates": 2,
  "references": [
    "lesson-structure.md",
    "tone-guide.md",
    "factual-verification.md",
    "example-library.md"
  ],
  "templates": [
    "lesson-template.md"
  ],
  "scripts": [
    "validate-links.sh"
  ],
  "dependencies": {
    "tools": ["gh", "git"],
    "configs": ["ARCHITECTURE.md", "voice-profile.md"],
    "skills": []
  },
  "audit": {
    "lastRun": "2026-03-10",
    "score": "8/10",
    "gaps": ["content audit missing source citation step"]
  }
}
```

A complex content-generation skill. Content audit is `true` because the skill generates educational content that requires factual verification against source material. Two approval gates pause for user review: one after outline generation (step 4) and one before final publish (step 12). Multiple references provide structure, tone, and verification guidance. The last audit found one gap — the content audit section was missing explicit source citation verification, which has since been addressed.
