---
name: approve-post
description: Approve the current draft, generate English translation, and publish to local files and Google Drive. Use this skill when the user says "approve post", "publish post", "post approve", "ship the post", or wants to finalize and publish a draft — even if they don't explicitly say "approve."
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob
---

## 1. Find the latest draft

Glob `~/.brain/memory/posts/drafts/linkedin/*.md` and pick the most recent file by name (highest number prefix).

## 2. Extract and prepare content

Read the draft. Extract the post body (everything after the closing `---` of frontmatter). Save to `/tmp/post-ptbr.txt`.

Translate the PT-BR body to English, preserving tone, line breaks, and hashtags. Save to `/tmp/post-en.txt`.

## 3. Update local published/ directory

Create a new directory under `~/.brain/memory/posts/published/linkedin/` using the draft's number prefix. Inside it, create:
- `meta.md` — frontmatter from the draft
- `pt-br.txt` — the PT-BR content
- `en.txt` — the EN translation

## 4. Upload to Google Drive

Use `gws` CLI to upload both files to the appropriate Google Drive folder.

## 5. Clean up

Remove the draft file from `drafts/linkedin/`. Report the published location and Drive link.
