# check-gmail

Scan Gmail inbox, detect filter gaps, and update filters with structured user decisions.

## Triggers

- `/check-gmail`
- "check my email", "scan inbox", "organize email"
- "filter gaps", "update gmail filters", "inbox cleanup"
- "limpar inbox", "organizar email", "verificar gmail"

## How it works

1. **Pre-flight + Scan** — Validates auth via wrapper, scans inbox with Python pipeline (single tool call), outputs structured JSON
2. **Filter gap detection** — Loads existing filters from changelog, diffs against scan results, categorizes unfiltered senders
3. **User decisions** — Structured AskUserQuestion flow: batch-confirm auto-matches, walk through ambiguous senders one-by-one
4. **Filter updates** — Parallel delete+create cycles for modified filters (Gmail API has no update)
5. **Message labeling** — Parallel message modify calls to retroactively organize inbox messages
6. **Changelog sync** — Mandatory final step: update `gmail-changelog.json` with all changes and revert instructions

## Usage

```
/check-gmail
/check-gmail 100    # scan up to 100 messages
```

Typical session: scan inbox → see 15 unfiltered senders → confirm 10 auto-matches, decide 5 ambiguous → update 3 filters → label 20 messages → changelog updated.

## Directory structure

```
check-gmail/
├── SKILL.md              # Core instructions (phases, constraints, anti-patterns)
├── README.md             # This file
├── scripts/
│   └── scan-inbox.py     # Python inbox scanner (auth + list + fetch pipeline)
└── references/
    └── gws-cli-patterns.md  # Exact CLI commands, known limitations, changelog schema
```

## Dependencies

- GWS CLI (`gws`) installed
- Auth configured via `~/.brain/integrations/gws/gws-auth.sh`
- Wrapper at `~/.brain/integrations/gws/gws-claude.sh`
- Changelog at `~/.brain/integrations/gws/gmail-changelog.json`

## Installation

```bash
npx skills add <repo-url> --skill check-gmail
```
