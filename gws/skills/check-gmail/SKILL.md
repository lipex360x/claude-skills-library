---
name: check-gmail
description: >
  Scan Gmail inbox, detect filter gaps by comparing against the existing changelog,
  and update filters + labels with structured user decisions. Full pipeline:
  auth check → inbox scan → gap detection → categorization → filter updates → changelog sync.
  Use when the user says "check gmail", "scan inbox", "organize email", "filter gaps",
  "update gmail filters", "check my email", "inbox cleanup", "email organization",
  "limpar inbox", "organizar email", "verificar gmail",
  or wants to review and organize unfiltered emails — even if they don't explicitly say "gmail."
metadata:
  category: email-management
  tags:
    - gmail
    - email
    - filters
    - inbox
    - gws
user-invocable: true
---

# check-gmail

Scan the Gmail inbox, find senders that slip through existing filters, and fix the gaps — all in one session.

## Prerequisites

This skill depends on external infrastructure components that must be set up before use:

- **GWS wrapper** (`~/.brain/integrations/gws/gws-claude.sh`) — OAuth-aware CLI wrapper that bypasses macOS Keyring
- **Auth script** (`~/.brain/integrations/gws/gws-auth.sh`) — Re-authenticates when tokens expire
- **Changelog** (`~/.brain/integrations/gws/gmail-changelog.json`) — Persistent filter state for gap detection across sessions
- **GWS rules** (`~/.brain/rules/gws.md`) — Integration configuration and conventions

Without these, the skill cannot authenticate or track filter state.

## Input contract

- **Required**: none — scans inbox by default
- **Optional**: `maxResults` (integer, default 50) — number of inbox messages to fetch in the scan

## Key paths

- **Wrapper**: `~/.brain/integrations/gws/gws-claude.sh` (NEVER bare `gws`)
- **Changelog**: `~/.brain/integrations/gws/gmail-changelog.json`
- **GWS rules**: `~/.brain/rules/gws.md`
- **Scan script**: use the `scripts/scan-inbox.py` from this skill's directory

## Process

### Phase 0: Pre-flight + Scan

1. Run the scan script:

```bash
python3 ~/.claude/skills/check-gmail/scripts/scan-inbox.py [maxResults]
```

Default is 50 messages. The script handles auth checking, inbox listing, and message detail fetching in a single pipeline. It outputs JSON to stdout and progress to stderr.

2. If auth fails (script exits with error), tell the user to re-authenticate:

```bash
~/.brain/integrations/gws/gws-auth.sh
```

Then retry.

3. Parse the JSON output. Each entry has: `id`, `from_raw`, `from_email`, `subject`, `custom_labels`, `all_labels`.

4. If the inbox is empty (0 messages), report it and stop.

### Phase 1: Load filter state

1. Read `~/.brain/integrations/gws/gmail-changelog.json`.
2. Build a **sender → label** map from the most recent filter entries. For each filter name (Jobs, Finance, Dev, Travel, Marketing, LinkedIn Social), extract the full `from` field and split by ` OR ` to get individual sender emails.
3. Also note each filter's current `filter_id` — needed for the delete+create cycle later.

### Phase 2: Gap detection

1. Extract unique `from_email` values from the scan results.
2. For each sender, check if it exists in the sender → label map.
3. Categorize unfiltered senders into three buckets:

| Bucket | Criteria | Example |
|--------|----------|---------|
| **Auto-match** | Sender domain or pattern clearly matches an existing label | `noreply@github.com` → Dev |
| **New candidate** | Multiple messages from same sender, clear category | 3 emails from `newsletter@cooking.com` → candidate for new label |
| **Needs decision** | Ambiguous — could be multiple labels, or unknown | `updates@stripe.com` — Finance? Dev? Marketing? |

4. Present findings as a structured summary table showing: sender, message count, proposed category, and confidence level.

### Phase 3: User decisions

Structured flow — not a wall of questions.

**Step 1 — Auto-matches (batch confirmation):**

Group all auto-categorized senders by label. Present each group:

```
These 3 senders match Finance:
- todomundo@nubank.com.br (2 msgs)
- contaxp@info.xpi.com.br (1 msg)
- no-reply@iugu.com (1 msg)
```

Use `AskUserQuestion` with options: `["Confirm all", "Review individually"]`

**Step 2 — Ambiguous senders (one-by-one or batched):**

For each ambiguous sender, use `AskUserQuestion` with selectable options:

```
Where should updates@stripe.com go?
```
Options: `["Jobs", "Finance", "Dev", "Travel", "Marketing", "LinkedIn Social", "Keep in inbox", "Skip"]`

If multiple senders appear to belong to the same category, batch them:

```
These look like Marketing — confirm?
- newsletter@cooking.com
- promo@store.example.com
```
Options: `["Confirm as Marketing", "Review individually"]`

**Step 3 — New label candidates:**

If any senders suggest a new category, present it:

```
5 senders don't fit existing labels. Create a new label?
```
Options: `["Yes, let's create one", "Add to existing label", "Skip all"]`

### Phase 4: Filter updates

After all decisions are collected:

1. Group new senders by target filter.
2. For each filter that needs updating:
   - Get the current `from` field from the changelog (full OR-separated list).
   - Append new senders to create the updated `from` field.
   - Note the current `filter_id` for deletion.

3. Execute in two parallel rounds:

**Round 1 — Delete old filters (all in parallel):**

```bash
~/.brain/integrations/gws/gws-claude.sh gmail users settings filters delete \
  --params '{"userId": "me", "id": "FILTER_ID"}' --output /dev/null
```

Launch ALL deletes in a single message — they are independent.

**Round 2 — Create new filters (all in parallel, after ALL deletes complete):**

Read `references/gws-cli-patterns.md` for the exact create command with `--params` and `--json` flags.

Launch ALL creates in a single message. Capture the response — it contains the new `filter_id`.

Never mix delete and create for the same filter in the same round.

4. **Verify created filters** — After all creates complete, list filters to confirm each new `filter_id` exists:

```bash
~/.brain/integrations/gws/gws-claude.sh gmail users settings filters list \
  --params '{"userId": "me"}'
```

Check that every expected `filter_id` from the create responses appears in the list. If any are missing, report the failure to the user before proceeding.

### Phase 5: Message labeling

For inbox messages that match the updated filters and should be retroactively organized:

1. Group messages by target label + action.
2. Execute message modify calls in parallel — each message is independent.

```bash
~/.brain/integrations/gws/gws-claude.sh gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"addLabelIds": ["Label_XX"], "removeLabelIds": ["INBOX", "UNREAD"]}'
```

For archive-only labels (Marketing, LinkedIn Social), omit `addLabelIds`.

Batch ALL independent message modify calls in one message. A typical session touches 20+ messages — parallel execution cuts this from 20+ sequential calls to one round.

### Phase 6: Changelog update (mandatory)

This step is NOT optional. A stale changelog breaks the next session's gap detection.

1. Read current `~/.brain/integrations/gws/gmail-changelog.json`.
2. Determine the next change ID (increment from last entry's `id`).
3. Append entries matching the existing schema:
   - `filters_updated` if any filters were modified — include `filter_id`, `old_filter_id`, full `from` field, `added_senders` array.
   - `batch_label_applied` if any messages were labeled — include `label`, `action`, `count`, `senders` with counts.
4. Write the updated changelog.

Read `references/gws-cli-patterns.md` for the exact JSON schema of each entry type.

## Critical constraints

### Wrapper only
Every GWS call goes through `~/.brain/integrations/gws/gws-claude.sh`. Bare `gws` fails in Claude Code sandbox because macOS Keyring blocks token access. The wrapper refreshes OAuth tokens from plain `tokens.json` — no Keyring involved.

### format: full, never metadata
The GWS CLI silently drops `metadataHeaders` array params with `format: metadata`. The API returns 200 with empty headers — no error, just missing data. Always use `format: full` and extract headers in Python/jq.

### --json for body, --params for URL
Two flags, not interchangeable. `--body` doesn't exist. Embedding request body inside `--params` fails silently. Read `references/gws-cli-patterns.md` for the exact flag for each operation.

### No tail stripping
`gws-claude.sh` outputs clean JSON. `tail -n +2` chops the opening `{` and causes "Extra data" JSON parse errors. Parse output directly.

### Parallel everything independent
Batch independent API calls in parallel tool calls:
- Round 1: all filter deletes (parallel)
- Round 2: all filter creates (parallel, after deletes)
- Round 3: all message modifies (parallel)

This reduces 50+ sequential calls to ~3 rounds.

### --output /dev/null on deletes
Without it, GWS saves a `download.html` junk file to the current directory.

### Changelog is sacred
`gmail-changelog.json` is both the safety net (revert instructions) and the input for gap detection. If you skip the changelog update, the next session will compare against stale data and miss senders that should already be filtered.

## Anti-patterns

- Calling bare `gws` instead of the wrapper — auth will fail every time.
- Using `format: metadata` with `metadataHeaders` — headers will be empty.
- Using `tail -n +2` on wrapper output — JSON will be truncated.
- Shell `for id in $ids` loops — quoting issues cause silent failures. Use Python.
- Using `--body` or `--params` for request body — neither works. Use `--json`.
- Sequential API calls for independent operations — wastes time.
- Skipping changelog update — cascades into wrong analysis next session.
- Asking multiple open-ended questions at once — use structured AskUserQuestion with selectable options.
