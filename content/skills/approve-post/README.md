# approve-post

> Approve the current draft, generate English translation, and publish to local files and Google Drive.

Finalizes a LinkedIn post draft by extracting content, translating it from PT-BR to English, organizing published files locally, uploading to Google Drive, and cleaning up the draft. Includes a review checkpoint before publishing.

## Usage

```text
/approve-post
/approve-post 042-my-post.md
```

> [!TIP]
> Also activates when you say "approve post", "publish post", "post approve", "ship the post", or want to finalize and publish a draft.

## How it works

1. **Find latest draft** -- Globs `drafts/linkedin/*.md` and picks the most recent file by number prefix. Validates the draft exists and has proper frontmatter
2. **Extract and translate** -- Separates frontmatter from post body, saves PT-BR version, and translates to English preserving tone, idioms, line breaks, and hashtags
3. **Review checkpoint** -- Presents both PT-BR and EN versions side-by-side for user approval before proceeding
4. **Publish locally** -- Creates a numbered directory under `published/linkedin/` with `meta.md`, `pt-br.txt`, and `en.txt`
5. **Upload to Drive** -- Uses `gws` CLI to upload both language versions to Google Drive (gracefully skipped if `gws` is not available)
6. **Clean up** -- Removes the draft file only after confirming published files exist, then reports location and Drive link

## Directory structure

```text
approve-post/
├── SKILL.md              # Core instructions
├── README.md             # This file
└── references/
    └── output-formats.md # Exact format for meta.md, pt-br.txt, en.txt
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill approve-post
```
