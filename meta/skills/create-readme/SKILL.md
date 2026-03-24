---
name: create-readme
user-invocable: true
description: Create or review a README.md for the project. Use when the user says "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or wants documentation for a repository — even if they don't explicitly say "readme." Detects whether a README already exists and switches between creation and review mode automatically.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Create README

Generate or review README.md files that are appealing, informative, and easy to read.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `$ARGUMENTS` | invocation | no | Optional directory path or mode override (`create` / `review`). Defaults to project root with auto-detect. | Use project root, auto-detect mode |

- If no arguments provided, auto-detect mode based on whether `README.md` exists at the target path.

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| README.md | `{target-path}/README.md` | yes | GitHub Flavored Markdown |
| Review findings | stdout | no | Markdown numbered list |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Reference READMEs list | `references/readme-references.md` | R | Markdown with file paths |
| Reference README samples | `references/*.md` (excluding readme-references.md) | R | Markdown |
| Existing README (review mode) | `{target-path}/README.md` | R/W | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. Parse `$ARGUMENTS` for directory path or mode override → default to project root.
2. Check if `README.md` exists at the target path → determines mode (create vs review).
3. Scan project for minimum context (source files, package.json, config) → if empty project: AUQ asking what the project is about before continuing.
4. If monorepo with multiple READMEs and target is root: note sub-READMEs exist, focus on root only.

</pre_flight>

## Steps

### 1. Detect mode

Parse `$ARGUMENTS` for a directory path or mode override. Default to the project root.

Check if `README.md` exists at the target path.

- **No README found** → **Create mode** (step 2)
- **README found** → **Review mode** (step 3)

**Edge cases — handle before proceeding:**
- **Empty project** (no source files, no package.json, no config): inform the user there's not enough context to generate a meaningful README. Ask what the project is about before continuing.
- **Monorepo with multiple READMEs**: if the target is the root and subdirectories contain their own READMEs, focus on the root README only. Mention the sub-READMEs exist but don't modify them.
- **Binary-only or asset-only project**: if no source code is found but assets exist (images, models, datasets), adapt the README structure to describe the assets rather than code.

### 2. Create mode

Build a README from scratch by analyzing the project.

1. Scan the project: package.json, source structure, config files, CI/CD, tests, docs.
2. Read `references/readme-references.md` for the list of local reference READMEs. Read at least 2 that match the project type for structure and tone inspiration.
3. Re-read the formatting rules (Guidelines section) and anti-patterns below before drafting — the draft must pass all of them. Every section must earn its place, structure must be scannable, and no anti-pattern should slip through.
4. Draft the README.
5. Present the draft to the user before writing.

### 3. Review mode

Analyze the existing README against the formatting standards and reference patterns. Preserve domain-specific content — the user built it for a reason.

1. Read the current README.
2. Read `references/readme-references.md` for the list of local reference READMEs. Read at least 2 that match the project type for comparison.
3. Identify improvements in **formatting and structure only**:
   - Missing navigation (content index, back-to-top links)
   - Missing GFM admonitions where appropriate
   - Header weight inconsistency
   - Sections that could benefit from tables, collapsible blocks, or visual separators
   - Missing tagline or subtitle
   - Badge opportunities (build status, version, license)
4. Check for **content gaps** — sections that exist in reference READMEs but are missing here, and would add value. Suggest, don't assume.
5. Present findings using this format for each item:

   ```
   **[N]. [Category]** (line [L])
   Current: [what's there now]
   Suggested: [concrete improvement]
   Why: [one-line reason]
   ```

   Do not rewrite the README — let the user choose which improvements to apply.

### 4. Report

<report>

Present concisely:
- **Mode:** create or review
- **Target:** path to README.md
- **Action taken:** file created / findings presented
- **References used:** which reference READMEs were consulted
- **Errors:** issues encountered (or "none")

</report>

## Next action

If create mode: review the generated README for accuracy, then commit. If review mode: choose which suggestions to apply, then run the skill again to verify.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — mode detected, project context gathered
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — README written (create) or findings presented (review)
4. **Formatting rules applied?** — GFM, admonitions, navigation, conciseness all checked
5. **Anti-patterns clean?** — scan output for emoji soup, boilerplate, wall-of-text
6. **References consulted?** — at least 2 reference READMEs read and applied

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **GFM compliance?** — all formatting uses GitHub Flavored Markdown correctly
2. **Section justification?** — every section earns its place; no filler content
3. **Navigation present?** — content index and back-to-top links for READMEs over 100 lines
4. **Accuracy?** — project details (tech stack, commands, paths) match actual project state
5. **Badge validity?** — only badges for active, maintained integrations
6. **Language correct?** — English by default unless user explicitly requested another language

Audit is scoped to content generated in THIS session.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Empty project (no source files) | AUQ: "What is this project about?" → use answer as context |
| Target path doesn't exist | AUQ: "Path not found. Which directory?" with suggestions |
| Reference READMEs missing | Proceed without references, warn user about reduced quality |
| README write fails | Present content in stdout, warn about file creation failure |
| Monorepo ambiguity | AUQ: "Multiple READMEs found. Which one?" with paths |

## Anti-patterns

- **Emoji soup** — emoji in every section header dilutes meaning and looks unprofessional. One or two in the title is fine.
- **Wall-of-text install** — multi-paragraph install instructions with inline explanations. Use numbered steps or a single code block instead.
- **Outdated badges** — badges that link to dead CI pipelines or show failing status. Only add badges for active, maintained integrations.
- **Copy-paste boilerplate** — generic template content that doesn't match the project (e.g., "Built with love" footer, placeholder author names, irrelevant sections).
- **Feature laundry list** — long bullet lists of features without context or examples. Show, don't tell — a code snippet beats a bullet point.
- **Stale screenshots** — screenshots of UI that no longer matches the current state. If you can't keep them updated, prefer text descriptions.

## Guidelines

- **Language: English by default.** Always write READMEs in English unless the user explicitly requests another language. READMEs are public-facing documentation — English maximizes reach. If the user says "em português", "en español", or similar, follow their request.

- **GFM everywhere.** GitHub Flavored Markdown for all formatting. Use GitHub admonitions (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) where they add clarity — not decoration.

- **No emoji overuse.** One or two in the title is fine. Emoji-heavy section headers are not.

- **Dedicated files stay separate.** No LICENSE, CONTRIBUTING, CHANGELOG sections in the README. Those have dedicated files.

- **Project logo/icon.** Include in the header if one exists in the repo.

- **Concise.** Every section must earn its place. If it doesn't help the reader set up, use, or understand the project — cut it.

- **Scannable.** Tables over prose for structured data. Code blocks with syntax highlighting. Short paragraphs. White space.

- **Navigation.** For READMEs over 100 lines, add a content index (inline or vertical) and back-to-top links after major sections.
