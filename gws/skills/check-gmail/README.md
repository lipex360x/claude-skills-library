# check-gmail

> Scan Gmail inbox, detect filter gaps by comparing against the existing changelog, and update filters + labels with structured user decisions.

Automates the full Gmail filter maintenance pipeline: scans your inbox for unfiltered senders, compares them against your existing filter changelog, and walks you through structured decisions to update filters and labels. Keeps your inbox organized without manual filter management.

## Usage

```text
/check-gmail [maxResults]
```

> [!TIP]
> Also activates when you say "check gmail", "scan inbox", "organize email", "filter gaps", "update gmail filters", "check my email", "inbox cleanup", "email organization", "limpar inbox", "organizar email", "verificar gmail"

## How it works

1. **Scan inbox** — Runs the Python scanner pipeline to fetch and parse inbox messages as structured JSON
2. **Load filter state** — Reads the changelog to build a sender-to-label map with current filter IDs
3. **Detect gaps** — Compares scan results against existing filters, categorizing unfiltered senders into auto-match, new candidate, and needs-decision buckets
4. **Collect user decisions** — Structured AskUserQuestion flow: batch-confirm auto-matches, walk through ambiguous senders individually
5. **Update filters** — Parallel delete+create cycles for modified filters (Gmail API has no update endpoint)
6. **Label existing messages** — Parallel message modify calls to retroactively organize inbox messages
7. **Update changelog** — Mandatory sync of `gmail-changelog.json` with all changes and revert instructions
8. **Report** — Summary of scanned messages, gaps found, filters updated, messages labeled, and changelog status

## Directory structure

```text
check-gmail/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── gws-cli-patterns.md  # Exact CLI commands, known limitations, changelog schema
└── scripts/
    └── scan-inbox.py     # Python inbox scanner (auth + list + fetch pipeline)
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill check-gmail
```
