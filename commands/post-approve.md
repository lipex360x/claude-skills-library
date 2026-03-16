---
description: Approve current draft, generate EN translation, publish to local files and Google Drive
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, Glob
---

## Steps

### 1. Find the latest draft

Glob `~/.brain/memory/posts/drafts/linkedin/*.md` and pick the most recent file by name (highest number prefix).

### 2. Extract and prepare content

Read the draft. Extract the post body (everything after the closing `---` of frontmatter). Save to `/tmp/post-ptbr.txt`.

Translate the PT-BR body to English, preserving tone, line breaks, and hashtags. Save to `/tmp/post-en.txt`.

### 3. Update local published/ directory

Derive the slug from the draft filename (e.g., `002-design-canvas.md` → `001-design-canvas` published dir — use the existing published dir that matches the topic, or create a new one).

Overwrite these files in `~/.brain/memory/posts/published/linkedin/<slug>/`:
- `pt-br.txt` — PT-BR body
- `en.txt` — EN body
- `meta.md` — update `status: approved`, `approved: <today>`, `draft_ref`, `gdrive_ids` (after step 4)

### 4. Upload to Google Drive

Use these exact gws patterns (do NOT deviate):

1. **Find the `posts/linkedin` folder:**
   ```bash
   gws drive files list --params '{"q": "name=\"linkedin\" and mimeType=\"application/vnd.google-apps.folder\"", "pageSize": 5, "fields": "files(id,name,parents)"}'
   ```
   Then verify the parent folder is named "posts" using `gws drive files get`.

2. **Delete old docs** if `meta.md` has `gdrive_ids` — for each ID:
   ```bash
   gws drive files delete --params '{"fileId": "OLD_ID"}' --output /dev/null
   ```

3. **Create empty Google Docs:**
   ```bash
   gws docs documents create --params '{"title": "NNN — Title [PT-BR]"}'
   gws docs documents create --params '{"title": "NNN — Title [EN]"}'
   ```

4. **Upload content to each doc:**
   ```bash
   gws drive files update --params '{"fileId": "DOC_ID"}' --upload /tmp/post-ptbr.txt
   gws drive files update --params '{"fileId": "DOC_ID"}' --upload /tmp/post-en.txt
   ```

5. **Move docs to the linkedin folder:**
   ```bash
   gws drive files update --params '{"fileId": "DOC_ID", "addParents": "FOLDER_ID"}'
   ```

### 5. Update frontmatter

Set `status: approved` in the draft file. Update `meta.md` with the new `gdrive_ids`.

### 6. Report

Print a summary: draft approved, files updated, Drive links (doc IDs).
