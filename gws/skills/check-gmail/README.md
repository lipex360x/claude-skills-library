# check-gmail

> Scan Gmail inbox, detect filter gaps by comparing against the existing changelog, and update filters + labels with structured user decisions.

End-to-end Gmail filter maintenance pipeline in 8 steps: scans inbox messages via a dedicated Python script, diffs senders against a persistent changelog to find gaps, categorizes unfiltered senders into auto-match/ambiguous/new buckets, collects structured user decisions (no open-ended questions), then executes parallel filter delete+create cycles and retroactive message labeling. All changes are logged to a changelog that powers the next session's gap detection.

## Usage

```text
/check-gmail [maxResults]
```

> [!TIP]
> Also activates when you say "check gmail", "scan inbox", "organize email", "filter gaps", "update gmail filters", "check my email", "inbox cleanup", "email organization", "limpar inbox", "organizar email", or "verificar gmail."

### Examples

```text
/check-gmail             # scan the 50 most recent inbox messages (default)
/check-gmail 100         # scan the 100 most recent inbox messages
```

> [!NOTE]
> Requires Google Workspace OAuth configured via `~/.brain/integrations/gws/`. The GWS wrapper (`gws-claude.sh`) and auth script (`gws-auth.sh`) must be installed, and `gmail-changelog.json` should exist for accurate gap detection. Run `gws-auth.sh` if authentication has expired.

## How it works

1. **Scan inbox** — Runs the Python scanner pipeline to fetch and parse inbox messages as structured JSON
2. **Load filter state** — Reads the changelog to build a sender-to-label map with current filter IDs
3. **Detect gaps** — Compares scan results against existing filters, categorizing unfiltered senders into auto-match, new candidate, and needs-decision buckets
4. **Collect user decisions** — Structured AskUserQuestion flow: batch-confirm auto-matches, walk through ambiguous senders individually
5. **Update filters** — Parallel delete+create cycles for modified filters (Gmail API has no update endpoint)
6. **Label existing messages** — Parallel message modify calls to retroactively organize inbox messages
7. **Update changelog** — Mandatory sync of `gmail-changelog.json` with all changes and revert instructions
8. **Report** — Summary of scanned messages, gaps found, filters updated, messages labeled, and changelog status

[↑ Back to top](#check-gmail)

## Directory structure

```text
check-gmail/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
├── references/
│   └── gws-cli-patterns.md  # Exact CLI commands, known API workarounds, changelog JSON schema
└── scripts/
    └── scan-inbox.py     # Python inbox scanner (auth check + message list + detail fetch pipeline)
```

[↑ Back to top](#check-gmail)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill check-gmail
```
