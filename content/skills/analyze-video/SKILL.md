---
name: analyze-video
description: >-
  Extract structured data from YouTube videos using subtitles, frame analysis,
  or both combined. Full pipeline: detect available sources, download subtitles
  and/or video, clean transcripts, extract frames, analyze with Claude, and
  produce structured output. Use when the user says "analyze video",
  "extract from video", "video transcript", "get questions from video",
  "analyze this YouTube", "extract frames", "video to text", or wants to
  pull structured information from a video — even if they don't explicitly
  say "analyze."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
argument-hint: "<youtube-url> [--mode subtitle|frame|hybrid] [--lang en]"
---

# Analyze Video

Extract structured data from YouTube videos by combining subtitle extraction, frame analysis, and Claude-powered interpretation into a single automated pipeline.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `url` | $ARGUMENTS or AUQ | yes | Valid YouTube URL (video or playlist) | AUQ: "Provide a YouTube video or playlist URL" |
| `--mode` | $ARGUMENTS | no | One of: `subtitle`, `frame`, `hybrid`, `auto` | Default: `auto` |
| `--lang` | $ARGUMENTS | no | ISO 639-1 language code | Default: `en` |
| `--output` | $ARGUMENTS | no | Output directory path | Default: `./video-analysis/<video-id>/` |
| `--prompt` | $ARGUMENTS | no | Path to custom extraction prompt | Default: use built-in prompts based on content type |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Extracted data | `<output>/extracted.json` | yes | JSON (structure depends on prompt) |
| Clean transcript | `<output>/transcript.txt` | yes | Plain text (subtitle mode only) |
| Raw subtitles | `<output>/downloads/*.srt` | yes | SRT |
| Frames | `<output>/frames/*.jpg` | yes | JPEG (frame/hybrid mode only) |
| Analysis report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| YouTube API | youtube.com | Read | HTTP (via yt-dlp) |
| Reference scripts | skill `scripts/` dir | Read/Execute | Bash/Python |
| Reference prompts | skill `templates/` dir | Read | Markdown |
| Video Analyzer guide | `~/www/claude/projects/video-analyzer/` | Read | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. `which yt-dlp` → if missing: "yt-dlp required. Install: `brew install yt-dlp`" — stop.
2. `which ffmpeg` → if missing AND mode is `frame` or `hybrid`: "ffmpeg required. Install: `brew install ffmpeg`" — stop.
3. `which jq` → if missing: "jq required. Install: `brew install jq`" — stop.
4. URL is a valid YouTube URL → if not: AUQ with prompt for URL.
5. Output directory is writable → if not: create it.

</pre_flight>

## Steps

### 1. Detect mode

If mode is `auto` (default), probe the video to determine the best approach:

1. Run `yt-dlp --skip-download --write-auto-sub --sub-lang <lang> --list-subs <url>` to check subtitle availability.
2. Ask the user about the video content via AUQ:

| Video type | Recommended mode |
|---|---|
| Lecture/podcast where everything is narrated | `subtitle` |
| Visual content (diagrams, code, slides) without narration | `frame` |
| Tutorial with both narration and visual content | `hybrid` |
| Unsure | `hybrid` (safest default) |

Present the recommendation based on subtitle availability, but let the user override.

### 2. Download sources

Run the appropriate download script based on selected mode.

**Subtitle mode:**
```bash
yt-dlp --skip-download --write-auto-sub --sub-lang <lang> --convert-subs srt \
  -o "%(id)s.%(ext)s" --paths "<output>/downloads" "<url>"
```

**Frame mode:**
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --write-info-json -o "%(id)s.%(ext)s" --paths "<output>/downloads" "<url>"
```

**Hybrid mode:** combine both — download video with subtitles:
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --write-info-json --write-auto-sub --sub-lang <lang> --convert-subs srt \
  -o "%(id)s.%(ext)s" --paths "<output>/downloads" "<url>"
```

If subtitle download fails (no auto-captions available), inform the user and suggest switching to `frame` mode or using Whisper as fallback.

### 3. Process sources

**Subtitles** — clean SRT to plain text:

Read and execute the cleaning logic from `scripts/clean-srt.py`:
```bash
python3 <skill-dir>/scripts/clean-srt.py <srt-file> <output>/transcript.txt
```

**Frames** — extract at appropriate density:

```bash
ffmpeg -i <video-file> -vf "fps=<rate>" -q:v 2 "<output>/frames/frame_%04d.jpg"
```

Frame rate guidance — ask the user via AUQ if not obvious:

| Content type | fps value | Result |
|---|---|---|
| Slides / static | `1/10` | 1 frame per 10s |
| Code tutorial | `1/3` | 1 frame per 3s |
| Animation / dynamic | `1` | 1 frame per second |
| Fast demo | `2` | 2 frames per second |

### 4. Choose extraction prompt

If the user provided `--prompt`, use it. Otherwise, determine the content type via AUQ:

| Content type | Template |
|---|---|
| Exam questions | `templates/extract-questions.md` |
| Tutorial / how-to | `templates/extract-tutorial.md` |
| Frame analysis | `templates/analyze-frames.md` |
| Custom | Ask user to describe what to extract |

### 5. Extract structured data

**Subtitle-based extraction:**
```bash
claude -p "$(cat <prompt>) $(cat <output>/transcript.txt)" \
  --model sonnet --output-format text --dangerously-skip-permissions
```

Validate output is valid JSON. If not, retry once with a stricter prompt. If still invalid, save raw output as `extracted.raw.txt` and report the failure.

**Frame-based extraction:**
Read frames using the Read tool (Claude's vision capability interprets them natively). Group related frames and analyze in batches of 5-10 to manage context.

**Hybrid extraction:**
Feed both transcript and frames to Claude. Use the hybrid prompt pattern:
- Transcript provides narrative flow and context
- Frames provide exact visual data (text, diagrams, numbers)
- When they conflict, trust frames for exact content, transcript for explanations

Save validated output to `<output>/extracted.json`.

### 6. Playlist handling

For playlist URLs, process each video sequentially:

1. Get video list: `yt-dlp --flat-playlist --print "%(id)s|%(title)s" <playlist-url>`
2. Create subdirectory per video: `<output>/<index>-<id>/`
3. Process each video through steps 2-5
4. Skip already-processed videos (check for existing `extracted.json`)
5. Report progress after each video

For large playlists (>10 videos), warn about processing time and offer to process a subset first.

### 7. Report

<report>

Present concisely:
- **Mode used** — subtitle / frame / hybrid
- **Videos processed** — count (for playlists)
- **Output location** — path to extracted.json
- **Extraction summary** — item count, key stats
- **Quality notes** — any issues (failed JSON, missing subtitles, low-quality frames)
- **Errors** — issues encountered or "none"

</report>

## Next action

Review `extracted.json` and refine the extraction prompt if needed. For playlists, run again to process any skipped/failed videos.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — all tools installed, URL valid
2. **Mode appropriate?** — selected mode matches video content
3. **Sources downloaded?** — SRT/video files exist in downloads/
4. **Processing complete?** — transcript.txt and/or frames/ populated
5. **Output valid?** — extracted.json is valid JSON
6. **Cleanup done?** — no temporary files left behind
7. **Anti-patterns clean?** — no violations detected

</self_audit>

## Content audit

<content_audit>

Before finalizing, verify:

1. **JSON valid?** — `jq . extracted.json` succeeds
2. **Extraction complete?** — spot-check 2-3 items against source material
3. **No hallucinated content?** — extracted data exists in the source (transcript/frames)
4. **Format consistent?** — all entries follow the same schema

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| yt-dlp fails (403/blocked) | Suggest `yt-dlp -U` to update. If persists, add `--sleep-interval 5` |
| No auto-captions available | Inform user, suggest frame mode or Whisper fallback: `whisper audio.mp3 --model medium` |
| ffmpeg not found | Stop with install instructions |
| Claude extraction returns invalid JSON | Retry once with stricter prompt. If fails, save raw output |
| Video is DRM-protected | Report that automated extraction is not possible — stop |
| Rate limited by YouTube | Add `--sleep-interval 5 --max-sleep-interval 30` and retry |
| Playlist too large | Warn user, offer to process subset |

## Anti-patterns

- **Downloading video when only subtitles are needed.** Subtitle mode uses `--skip-download` to avoid unnecessary bandwidth — because videos can be hundreds of MB while subtitles are a few KB.
- **Extracting too many frames.** Using high fps on long videos produces thousands of images that overwhelm context — because Claude Vision works best with curated, distinct frames rather than near-duplicate sequences.
- **Skipping JSON validation.** Raw LLM output may contain markdown fences or extra text — because saving invalid JSON silently breaks downstream consumers.
- **Processing all playlist videos without skip logic.** Re-processing already-extracted videos wastes time and API calls — because idempotent processing with skip checks is trivial to implement.
- **Using frame mode for narrated content.** If the speaker reads everything aloud, subtitle extraction is faster, cheaper, and more accurate — because auto-captions capture speech directly while frame OCR is indirect.

## Guidelines

- **Auto-detect first, ask second.** Probe for subtitle availability before asking the user to choose a mode — because informed choices are better than blind ones.
- **Prefer the lightest approach.** Subtitle-only is cheaper and faster than frame extraction. Only escalate to heavier modes when the lighter one is insufficient — because bandwidth, storage, and processing time all increase with video downloads.
- **Idempotent processing.** Skip already-processed videos in playlists. Check for existing output before re-downloading — because re-running a partially completed batch should resume, not restart.
- **Validate early.** Check JSON validity immediately after extraction. A single retry with a stricter prompt catches most formatting issues — because catching errors at extraction time is cheaper than debugging corrupt output later.
- **Hybrid for maximum accuracy.** When both sources are available, cross-referencing subtitles with frames produces the most accurate extraction — because each source compensates for the other's blind spots.
