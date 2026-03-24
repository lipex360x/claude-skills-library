# approve-post

> Approve the current draft, generate English translation, and publish to local files and Google Drive.

End-to-end publish pipeline for LinkedIn posts: translates PT-BR drafts to native-sounding English, gates on side-by-side user review, then writes three structured files (metadata, PT-BR, EN) to a numbered directory. Google Drive sync is optional and degrades gracefully when `gws` CLI is unavailable.

## Usage

```text
/approve-post [draft-filename]
```

> [!TIP]
> Also activates when you say "approve post", "publish post", "post approve", "ship the post", or want to finalize and publish a draft.

### Examples

```text
/approve-post                  # auto-selects the most recent draft (highest number prefix)
/approve-post 007-ai-tools.md  # approve a specific draft file from drafts/linkedin/
```

## How it works

1. **Find and read the draft** — Globs `drafts/linkedin/*.md` and picks the file with the highest number prefix, or uses the specified filename
2. **Translate to English** — Translates the PT-BR body preserving tone, idioms, line breaks, hashtags, and emoji placement. Idiomatic expressions are translated by intent, not literally
3. **Review before publishing** — Presents both PT-BR and EN versions side-by-side for user approval. Changes can be requested in a loop until both versions are confirmed
4. **Publish to local directory** — Creates a numbered directory under `published/linkedin/` with `meta.md`, `pt-br.txt`, and `en.txt` following the output format spec
5. **Upload to Google Drive** — Uses `gws` CLI to upload both versions (gracefully skipped if `gws` is not available or upload fails)
6. **Clean up** — Removes the draft file only after confirming published files were written successfully
7. **Report** — Summarizes published paths, translation approval status, Drive link, and any errors

[↑ Back to top](#approve-post)

## Directory structure

```text
approve-post/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    └── output-formats.md # Exact format templates for meta.md, pt-br.txt, and en.txt
```

[↑ Back to top](#approve-post)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill approve-post
```
