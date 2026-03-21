# Output Formats

Exact format for each file created in the `published/linkedin/<number>/` directory.

## meta.md

```markdown
---
title: "<post title>"
date: "<YYYY-MM-DD>"
platform: linkedin
status: published
tags: [tag1, tag2]
published_at: "<ISO 8601 timestamp>"
---
```

Contains only YAML frontmatter — no body content. All fields from the original draft frontmatter are preserved. The `status` field is set to `published` and `published_at` is added with the current timestamp.

## pt-br.txt

Plain text file with the original PT-BR post body. No frontmatter, no markdown formatting beyond what LinkedIn supports (line breaks, hashtags, mentions). Starts directly with the content — no blank lines at the top.

## en.txt

Plain text file with the English translation. Same formatting rules as `pt-br.txt`. The translation must preserve:
- Line break structure (paragraph spacing matters for readability on LinkedIn)
- Hashtags (kept in English or transliterated as appropriate)
- Mentions (@name) unchanged
- Emoji placement and usage
