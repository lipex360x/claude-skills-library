---
name: create-readme
user-invocable: true
description: Create or review a README.md for the project. Use when the user says "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or wants documentation for a repository — even if they don't explicitly say "readme." Detects whether a README already exists and switches between creation and review mode automatically.
---

# Create README

Generate or review README.md files that are appealing, informative, and easy to read.

## Input

- `$ARGUMENTS` — optional. Accepts a target directory path (defaults to project root) or an explicit mode override (`create` or `review`).
- If no arguments provided, auto-detect mode based on whether `README.md` exists at the target path.

## Process

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
3. Draft the README following the formatting rules below.
4. Present the draft to the user before writing.

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

### 4. Formatting rules

Apply these in both modes:

- **Language: English by default.** Always write READMEs in English unless the user explicitly requests another language. READMEs are public-facing documentation — English maximizes reach. If the user says "em português", "en español", or similar, follow their request.
- **GFM** (GitHub Flavored Markdown) for all formatting.
- **GitHub admonitions** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) where they add clarity — not decoration.
- **No emoji overuse.** One or two in the title is fine. Emoji-heavy section headers are not.
- **No LICENSE, CONTRIBUTING, CHANGELOG sections.** Those have dedicated files.
- **Project logo/icon** in the header if one exists in the repo.
- **Concise.** Every section must earn its place. If it doesn't help the reader set up, use, or understand the project — cut it.
- **Scannable.** Tables over prose for structured data. Code blocks with syntax highlighting. Short paragraphs. White space.
- **Navigation.** For READMEs over 100 lines, add a content index (inline or vertical) and back-to-top links after major sections.

## Anti-patterns

- **Emoji soup** — emoji in every section header dilutes meaning and looks unprofessional. One or two in the title is fine.
- **Wall-of-text install** — multi-paragraph install instructions with inline explanations. Use numbered steps or a single code block instead.
- **Outdated badges** — badges that link to dead CI pipelines or show failing status. Only add badges for active, maintained integrations.
- **Copy-paste boilerplate** — generic template content that doesn't match the project (e.g., "Built with love" footer, placeholder author names, irrelevant sections).
- **Feature laundry list** — long bullet lists of features without context or examples. Show, don't tell — a code snippet beats a bullet point.
- **Stale screenshots** — screenshots of UI that no longer matches the current state. If you can't keep them updated, prefer text descriptions.
