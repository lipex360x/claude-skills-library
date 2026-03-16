---
name: create-readme
description: Create or review a README.md for the project. Use when the user says "create a readme", "generate readme", "review the readme", "improve the readme", "update the readme", or wants documentation for a repository — even if they don't explicitly say "readme." Detects whether a README already exists and switches between creation and review mode automatically.
---

# Create README

Generate or review README.md files that are appealing, informative, and easy to read.

## Process

### 1. Detect mode

Check if `README.md` exists in the project root.

- **No README found** → **Create mode** (step 2)
- **README found** → **Review mode** (step 3)

### 2. Create mode

Build a README from scratch by analyzing the project.

1. Scan the project: package.json, source structure, config files, CI/CD, tests, docs.
2. Fetch reference READMEs for structure and tone inspiration. Read `references/readme-references.md` for the list.
3. Draft the README following the formatting rules below.
4. Present the draft to the user before writing.

### 3. Review mode

Analyze the existing README against the formatting standards and reference patterns. Preserve domain-specific content — the user built it for a reason.

1. Read the current README.
2. Fetch at least 2 reference READMEs for comparison. Read `references/readme-references.md` for the list.
3. Identify improvements in **formatting and structure only**:
   - Missing navigation (content index, back-to-top links)
   - Missing GFM admonitions where appropriate
   - Header weight inconsistency
   - Sections that could benefit from tables, collapsible blocks, or visual separators
   - Missing tagline or subtitle
   - Badge opportunities (build status, version, license)
4. Check for **content gaps** — sections that exist in reference READMEs but are missing here, and would add value. Suggest, don't assume.
5. Present findings as a numbered list of specific, actionable improvements with line references. Do not rewrite the README — let the user choose which improvements to apply.

### 4. Formatting rules

Apply these in both modes:

- **GFM** (GitHub Flavored Markdown) for all formatting.
- **GitHub admonitions** (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, `> [!CAUTION]`) where they add clarity — not decoration.
- **No emoji overuse.** One or two in the title is fine. Emoji-heavy section headers are not.
- **No LICENSE, CONTRIBUTING, CHANGELOG sections.** Those have dedicated files.
- **Project logo/icon** in the header if one exists in the repo.
- **Concise.** Every section must earn its place. If it doesn't help the reader set up, use, or understand the project — cut it.
- **Scannable.** Tables over prose for structured data. Code blocks with syntax highlighting. Short paragraphs. White space.
- **Navigation.** For READMEs over 100 lines, add a content index (inline or vertical) and back-to-top links after major sections.
