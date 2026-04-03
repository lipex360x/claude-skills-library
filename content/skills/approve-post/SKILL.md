---
name: approve-post
description: >-
  Approve the current draft, generate English translation, and publish to local
  files and Google Drive. Use this skill when the user says "approve post",
  "publish post", "post approve", "ship the post", or wants to finalize and
  publish a draft — even if they don't explicitly say "approve."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# Approve Post

Finalize a LinkedIn draft — review both language versions, publish to local files, and optionally sync to Google Drive.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `draft-filename` | $ARGUMENTS | no | File exists in `drafts/linkedin/` | List available drafts, AUQ to pick one |

If no argument is provided, the most recent draft is selected automatically (highest number prefix).

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Metadata file | `published/linkedin/<number>/meta.md` | yes | YAML frontmatter |
| PT-BR content | `published/linkedin/<number>/pt-br.txt` | yes | Plain text |
| EN translation | `published/linkedin/<number>/en.txt` | yes | Plain text |
| Google Drive copy | Google Drive folder | yes | Plain text files |
| Report | stdout | no | Markdown summary |

Read `references/output-formats.md` for the exact format of each published file.

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Draft files | `drafts/linkedin/*.md` | R | Markdown with YAML frontmatter |
| Published directory | `published/linkedin/` | W | Directory with numbered subdirs |
| Google Drive | via `gws` CLI | W | Plain text upload |

</external_state>

## Pre-flight

<pre_flight>

1. Posts directory exists and contains `drafts/linkedin/` → if not: "No drafts directory found. Create a draft first with /write-content." — stop.
2. At least one `.md` file exists in `drafts/linkedin/` → if none: "No drafts found in drafts/linkedin/." — stop.
3. If argument provided, that file exists → if not: list available drafts, AUQ to pick one.
4. Draft file contains valid YAML frontmatter between `---` delimiters with at minimum `title` and `date` fields → if malformed: report the specific parsing error — stop.
5. **Flight table.** Read `.claude/project-setup.json` for `show-flight-tables` (defaults to `true` when absent). If enabled, present all pre-flight results as a markdown table: **Check** | **Status** | **Detail**. Use ✅ pass, ⚠️ warning, ❌ fail, ⏭️ skipped.

</pre_flight>

## Steps

### 1. Find and read the draft

Glob `drafts/linkedin/*.md` inside the posts directory. If a specific filename was passed as argument, use that file. Otherwise pick the file with the highest number prefix because drafts are numbered sequentially.

Read the draft. Extract:
- **Frontmatter** — all YAML fields (title, date, tags, etc.)
- **Post body** — everything after the closing `---` of frontmatter

### 2. Translate to English

Translate the PT-BR body to English. Preserve tone, line breaks, hashtags, mentions, and emoji placement because the translated version must feel like it was written natively — not machine-translated. Pay special attention to idiomatic expressions: translate the intent, not the literal words.

### 3. Review before publishing

Present both versions side-by-side to the user:
- The original PT-BR body
- The EN translation

Ask for approval before proceeding. This checkpoint exists because translation errors or tone mismatches are much cheaper to fix before publishing than after.

If the user requests changes, apply them and present again. Only proceed when the user confirms both versions are ready.

### 4. Publish to local directory

Create a new directory under `published/linkedin/` using the draft's number prefix. Inside it, create three files following `references/output-formats.md`:

- `meta.md` — structured frontmatter metadata (status set to `published`, `published_at` added)
- `pt-br.txt` — the PT-BR content (plain text, no frontmatter)
- `en.txt` — the EN translation (plain text, no frontmatter)

### 5. Upload to Google Drive

Check if the `gws` CLI is available by running `which gws`.

**If `gws` is not found:** warn the user that Google Drive upload will be skipped. Continue to Step 6 — do not fail the entire flow because of a missing optional dependency.

**If `gws` is available:** upload both `pt-br.txt` and `en.txt` to the appropriate Google Drive folder. If the upload fails (network error, auth expired, folder not found), report the specific error and continue — local files are already saved.

### 6. Clean up

Remove the draft file from `drafts/linkedin/` only after confirming that local published files were written successfully. Never delete the draft before publish is verified because the draft is the only source of truth until published files exist.

### 7. Report

<report>

Present concisely:
- **Published:** directory path and files created
- **Translation:** approval status (approved / revised N times)
- **Google Drive:** link if upload succeeded, or "skipped" with reason
- **Content audit:** summary of verification results
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Share the published post on LinkedIn. Copy from `pt-br.txt` for the Portuguese audience or `en.txt` for the English audience.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — draft existed, frontmatter was valid
2. **User approved both versions?** — review step was not skipped
3. **All three files created?** — `meta.md`, `pt-br.txt`, `en.txt` exist in published directory
4. **Draft removed?** — only after confirming published files exist on disk
5. **Anti-patterns clean?** — no literal translations, no skipped review, no premature draft deletion

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Translation accuracy?** — EN version preserves the original meaning, tone, and intent of the PT-BR body. Idiomatic expressions are translated to equivalent English idioms, not literal translations.
2. **Formatting preserved?** — line breaks, paragraph spacing, hashtags, mentions, and emoji placement match between PT-BR and EN versions.
3. **Metadata correct?** — `meta.md` contains all original frontmatter fields, `status` is `published`, `published_at` timestamp is current.
4. **No content loss?** — published `pt-br.txt` matches the approved PT-BR body exactly (no truncation, no extra whitespace).
5. **Output format matches spec?** — all three files follow the templates in `references/output-formats.md`.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| No drafts found | Report and suggest `/write-content` — stop |
| Malformed frontmatter | Report specific parsing error — stop |
| `gws` CLI not found | Warn, skip Drive upload, continue with local publish |
| Drive upload fails | Report error with details, continue — local files are primary |
| Write to published directory fails | Report error — do NOT delete draft |
| Draft deletion fails | Warn — published files already exist, manual cleanup needed |

## Anti-patterns

- **Publishing without user review.** Skipping the side-by-side review step leads to tone mismatches going live — because translation errors are much cheaper to fix before publishing than after.
- **Translating idioms literally.** "Matar dois coelhos com uma cajadada" is not "kill two rabbits with one stick" — because the goal is native-sounding English, not word-for-word conversion. Find the equivalent English idiom.
- **Deleting draft before confirming publish.** If the write fails silently, the content is lost — because the draft is the only source of truth until published files exist on disk.
- **Failing the entire flow on Drive error.** Local publish is the primary output; Drive is a convenience copy — because a network hiccup should not block the user from having their content saved locally.
- **Assuming frontmatter fields exist.** Validate before accessing — because a missing `title` field should produce a clear error, not a crash.

## Guidelines

- **Local-first publishing.** The local filesystem is the source of truth. Google Drive is a sync target, not the primary store — always ensure local files are written before attempting any remote upload.

- **Translation is creative work.** Treat translation as content creation, not mechanical conversion. The EN version should read as if originally written in English — preserving the author's voice, humor, and rhetorical style.

- **Graceful degradation.** If `gws` is not available, skip the Drive step silently. If Drive upload fails, report and continue. The core job (review + local publish) should always complete even when optional steps fail.

- **User approval is mandatory.** The review step (Step 3) is a hard gate, not a suggestion. Never bypass it — even if the translation looks perfect. The user's judgment on tone and accuracy is final.
