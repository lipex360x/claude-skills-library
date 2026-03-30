# analyze-video

Extract structured data from YouTube videos using subtitles, frame analysis, or both combined.

## Install

```bash
npx @anthropic-ai/claude-code skills add lipex360/skills-library/content analyze-video
```

## Usage

```
/analyze-video <youtube-url>
/analyze-video <youtube-url> --mode hybrid --lang en
/analyze-video <playlist-url> --mode subtitle
```

## Modes

| Mode | When to use | Downloads |
|------|-------------|-----------|
| `subtitle` | Narrated content (lectures, podcasts) | Subtitles only (~KB) |
| `frame` | Visual content (diagrams, code, slides) | Full video (~MB) |
| `hybrid` | Both narration and visuals | Video + subtitles |
| `auto` | Let the skill decide (default) | Probes first, then downloads |

## Triggers

- "analyze video"
- "extract from video"
- "video transcript"
- "get questions from video"
- "analyze this YouTube"
- "extract frames"

## Dependencies

- `yt-dlp` — YouTube download
- `ffmpeg` — frame extraction (frame/hybrid modes)
- `jq` — JSON validation
- `python3` — SRT cleaning

## Templates

| Template | Purpose |
|----------|---------|
| `extract-questions.md` | Exam question extraction |
| `extract-tutorial.md` | Tutorial content extraction |
| `analyze-frames.md` | Visual frame analysis |

## Plugin

Part of the **content** plugin.
