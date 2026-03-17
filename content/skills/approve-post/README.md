# approve-post

> Approve the current draft, generate English translation, and publish to local files and Google Drive.

Finalizes a LinkedIn post draft by extracting content, translating it from PT-BR to English, organizing published files locally, uploading to Google Drive, and cleaning up the draft.

## Usage

```text
/approve-post
```

> [!TIP]
> Also activates when you say "approve post", "publish post", "post approve", "ship the post", or want to finalize and publish a draft.

## How it works

1. **Find latest draft** -- Globs `~/.brain/memory/posts/drafts/linkedin/*.md` and picks the most recent file by number prefix
2. **Extract and translate** -- Separates frontmatter from post body, saves PT-BR version, and translates to English preserving tone, line breaks, and hashtags
3. **Publish locally** -- Creates a numbered directory under `published/linkedin/` with `meta.md`, `pt-br.txt`, and `en.txt`
4. **Upload to Drive** -- Uses `gws` CLI to upload both language versions to Google Drive
5. **Clean up** -- Removes the draft file and reports the published location and Drive link

## Directory structure

```text
approve-post/
└── SKILL.md              # Core instructions
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill approve-post
```
