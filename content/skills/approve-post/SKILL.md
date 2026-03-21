---
name: approve-post
description: Approve the current draft, generate English translation, and publish to local files and Google Drive. Use this skill when the user says "approve post", "publish post", "post approve", "ship the post", or wants to finalize and publish a draft — even if they don't explicitly say "approve."
user-invocable: true
disable-model-invocation: false
allowed-tools: Bash, Read, Write, Edit, Glob
---

## Input contract

**Required:** A draft file must exist in `drafts/linkedin/` within the posts directory.

**Optional argument:** A specific draft filename to approve (e.g., `/approve-post 042-my-post.md`). If omitted, the most recent draft is selected automatically.

**Draft format:** Each draft must contain YAML frontmatter (between `---` delimiters) with at minimum `title` and `date` fields, followed by the post body in PT-BR.

## 1. Find the latest draft

Glob `drafts/linkedin/*.md` inside the posts directory. Pick the most recent file by name (highest number prefix) because drafts are numbered sequentially — the highest number is the latest.

**If no drafts are found:** inform the user "No drafts found in drafts/linkedin/. Create a draft first with /write-content." and stop.

**If a specific filename was passed as argument:** use that file instead of auto-selecting. If the file doesn't exist, list available drafts and ask the user to pick one.

## 2. Extract and prepare content

Read the draft. Validate that it contains YAML frontmatter between `---` delimiters.

**If frontmatter is missing or malformed:** inform the user with the specific parsing error and stop. Do not attempt to guess the metadata.

Extract:
- **Frontmatter** — all YAML fields (title, date, tags, etc.)
- **Post body** — everything after the closing `---` of frontmatter

Save the PT-BR body to a temporary file.

Translate the PT-BR body to English. Preserve tone, line breaks, and hashtags because the translated version must feel like it was written natively — not machine-translated. Pay special attention to idiomatic expressions: translate the intent, not the literal words.

Save the EN translation to a temporary file.

## 3. Review before publishing

Present both versions side-by-side to the user:
- The original PT-BR body
- The EN translation

Ask for approval before proceeding. This checkpoint exists because translation errors or tone mismatches are much cheaper to fix before publishing than after.

If the user requests changes, apply them and present again. Only proceed to Step 4 when the user confirms both versions are ready.

## 4. Publish to local directory

Create a new directory under `published/linkedin/` using the draft's number prefix. Inside it, create three files following the templates in `references/output-formats.md`:

- `meta.md` — structured frontmatter metadata
- `pt-br.txt` — the PT-BR content (plain text, no frontmatter)
- `en.txt` — the EN translation (plain text, no frontmatter)

Read `references/output-formats.md` for the exact format of each file.

## 5. Upload to Google Drive

Check if the `gws` CLI is available by running `which gws`.

**If `gws` is not found:** warn the user that Google Drive upload will be skipped. Inform them that files were saved locally and they can upload manually or install the `gws` plugin. Continue to Step 6 — do not fail the entire flow because of a missing optional dependency.

**If `gws` is available:** upload both `pt-br.txt` and `en.txt` to the appropriate Google Drive folder. If the upload fails (network error, auth expired, folder not found), report the specific error and continue to Step 6 — local files are already saved.

## 6. Clean up

Remove the draft file from `drafts/linkedin/` only after confirming that local published files were written successfully. Never delete the draft before publish is verified because the draft is the only source of truth until published files exist.

Report:
- Published directory path
- Google Drive link (if upload succeeded) or "Drive upload skipped" with reason

## Anti-patterns

- **Never publish without showing the user both versions first.** Skipping the review step leads to tone mismatches going live.
- **Never translate idioms literally.** "Matar dois coelhos com uma cajadada" is not "kill two rabbits with one stick" — find the equivalent English idiom.
- **Never delete the draft before confirming the published files exist on disk.** If the write fails silently, the content is lost.
- **Never fail the entire flow because Drive upload failed.** Local publish is the primary output; Drive is a convenience copy.
- **Never assume frontmatter fields exist.** Validate before accessing — a missing `title` field should produce a clear error, not a crash.
