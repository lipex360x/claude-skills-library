# approve-post

> Approve the current draft, generate English translation, and publish to local files and Google Drive.

Finalizes a LinkedIn post draft by reviewing both PT-BR and English versions side-by-side, publishing organized files locally, and optionally syncing to Google Drive. Ensures translation quality through an explicit approval checkpoint before any publishing happens.

## Usage

```text
/approve-post [draft-filename]
```

> [!TIP]
> Also activates when you say "approve post", "publish post", "post approve", "ship the post", or want to finalize and publish a draft.

## How it works

1. **Find and read the draft** — Globs `drafts/linkedin/*.md` and picks the file with the highest number prefix, or uses the specified filename
2. **Translate to English** — Translates the PT-BR body preserving tone, idioms, line breaks, hashtags, and emoji placement
3. **Review before publishing** — Presents both PT-BR and EN versions side-by-side for user approval before proceeding
4. **Publish to local directory** — Creates a numbered directory under `published/linkedin/` with `meta.md`, `pt-br.txt`, and `en.txt`
5. **Upload to Google Drive** — Uses `gws` CLI to upload both versions (gracefully skipped if `gws` is not available)
6. **Clean up** — Removes the draft file only after confirming published files were written successfully
7. **Report** — Summarizes published paths, translation status, Drive link, and any errors

## Directory structure

```text
approve-post/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── output-formats.md # Exact format for meta.md, pt-br.txt, en.txt
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill approve-post
```
