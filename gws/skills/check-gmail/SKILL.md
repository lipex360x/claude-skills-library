---
name: check-gmail
description: >-
  Scan Gmail inbox, detect filter gaps by comparing against the existing changelog,
  and update filters + labels with structured user decisions. Full pipeline:
  auth check → inbox scan → gap detection → categorization → filter updates → changelog sync.
  Use when the user says "check gmail", "scan inbox", "organize email", "filter gaps",
  "update gmail filters", "check my email", "inbox cleanup", "email organization",
  "limpar inbox", "organizar email", "verificar gmail",
  or wants to review and organize unfiltered emails — even if they don't explicitly say "gmail."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
---

# Check Gmail

Scan the Gmail inbox, find senders that slip through existing filters, and fix the gaps — all in one session.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `maxResults` | $ARGUMENTS | no | Positive integer | Default to 50 |
| `account` | $ARGUMENTS or AUQ | no | "personal", "ireland", or "cct" | AUQ with account list |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Updated Gmail filters | Gmail API | yes | Filter rules via GWS CLI |
| Labeled messages | Gmail API | yes | Label + archive actions |
| Changelog entry | `~/.brain/integrations/gws[-ireland\|-cct]/gmail-changelog.json` (per account) | yes | JSON |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| GWS wrapper (personal) | `~/.brain/integrations/gws/gws-claude.sh` | R | Bash script (OAuth-aware) |
| GWS wrapper (ireland) | `~/.brain/integrations/gws-ireland/gws-claude.sh` | R | Bash script (OAuth-aware) |
| GWS wrapper (cct) | `~/.brain/integrations/gws-cct/gws-claude.sh` | R | Bash script (OAuth-aware) |
| Changelog (personal) | `~/.brain/integrations/gws/gmail-changelog.json` | R/W | JSON |
| Changelog (ireland) | `~/.brain/integrations/gws-ireland/gmail-changelog.json` | R/W | JSON |
| Changelog (cct) | `~/.brain/integrations/gws-cct/gmail-changelog.json` | R/W | JSON |
| Re-auth script | `~/.brain/scripts/gws-reauth.py` | R | Python (Playwright + CDP) |
| Playwright venv | `~/.brain/scripts/.venv/bin/python3` | R | Python 3 with playwright |
| GWS rules | `~/.brain/rules/gws.md` | R | Markdown |
| Scan script | `scripts/scan-inbox.py` | R | Python script |
| CLI patterns | `references/gws-cli-patterns.md` | R | Markdown |

</external_state>

## Pre-flight

<pre_flight>

1. **Account selection.** If `account` not provided in arguments, AUQ: `["Personal (lipex360@gmail.com)", "Ireland (irish.bambirra@gmail.com)", "CCT (2026033@student.cct.ie)"]`. Map the selection to the account key: `personal`, `ireland`, or `cct`.

2. **Resolve account paths.** Based on the selected account:

   | Account | Wrapper | Changelog |
   |---------|---------|-----------|
   | `personal` | `~/.brain/integrations/gws/gws-claude.sh` | `~/.brain/integrations/gws/gmail-changelog.json` |
   | `ireland` | `~/.brain/integrations/gws-ireland/gws-claude.sh` | `~/.brain/integrations/gws-ireland/gmail-changelog.json` |
   | `cct` | `~/.brain/integrations/gws-cct/gws-claude.sh` | `~/.brain/integrations/gws-cct/gmail-changelog.json` |

3. **GWS wrapper exists** → if missing: "GWS wrapper not installed. Set up `~/.brain/integrations/gws[-ireland]/` first." — stop.

4. **Scan script exists** at `scripts/scan-inbox.py` → if missing: "Scan script missing." — stop.

5. **Auth is valid.** Run the scan script with the selected account. If auth fails (exit code 1):
   - **Auto re-auth:** Run `~/.brain/scripts/.venv/bin/python3 ~/.brain/scripts/gws-reauth.py <account> --manage-chrome --headless`
   - Wait for exit code.
   - If re-auth succeeds (exit 0): retry the scan script.
   - If re-auth fails: report the error to the user with AUQ `["Retry re-auth", "I'll fix manually"]`. On "Retry": run re-auth again (without `--headless` this time, so user can see what's happening). On manual: stop and wait.

6. **Changelog exists** → if missing: warn but continue with empty filter state.

</pre_flight>

## Steps

### 1. Scan inbox

Run the scan script with the selected account:

```bash
python3 ~/.claude/skills/check-gmail/scripts/scan-inbox.py [maxResults] <account>
```

Default is 50 messages. The `account` argument (`personal` or `ireland`) selects which GWS wrapper to use. The script handles auth checking, inbox listing, and message detail fetching in a single pipeline. It outputs JSON to stdout and progress to stderr.

Parse the JSON output. Each entry has: `id`, `from_raw`, `from_email`, `subject`, `custom_labels`, `all_labels`.

If the inbox is empty (0 messages), report it and stop.

### 2. Load filter state

1. Read the changelog for the selected account (see path table in Pre-flight step 2).
2. Build a **sender → label** map from the most recent filter entries. For each filter name, extract the full `from` field and split by ` OR ` to get individual sender emails.
3. Note each filter's current `filter_id` — needed for the delete+create cycle later.

### 3. Detect gaps

1. Extract unique `from_email` values from the scan results.
2. For each sender, check if it exists in the sender → label map.
3. Categorize unfiltered senders into three buckets:

| Bucket | Criteria | Example |
|--------|----------|---------|
| **Auto-match** | Sender domain/pattern clearly matches an existing label | `noreply@github.com` → Dev |
| **New candidate** | Multiple messages from same sender, clear category | `newsletter@cooking.com` → new label |
| **Needs decision** | Ambiguous — could be multiple labels | `updates@stripe.com` — Finance? Dev? |

4. Present findings as a structured summary table.

### 4. Collect user decisions

Structured flow — not a wall of questions.

**Batch 1 — Auto-matches:** Group all auto-categorized senders by label. Present each group. AUQ with options: `["Confirm all", "Review individually"]`

**Batch 2 — Ambiguous senders:** For each ambiguous sender, AUQ with selectable label options plus "Keep in inbox" and "Skip". Batch senders that appear to belong to the same category.

**Batch 3 — New label candidates:** If senders suggest a new category, AUQ: `["Yes, let's create one", "Add to existing label", "Skip all"]`

### 5. Update filters

After all decisions are collected:

1. Group new senders by target filter.
2. For each filter: get current `from` field from changelog, append new senders, note current `filter_id`.
3. **Round 1 — Delete old filters (all in parallel):**

```bash
~/.brain/integrations/gws[-ireland]/gws-claude.sh gmail users settings filters delete \
  --params '{"userId": "me", "id": "FILTER_ID"}' --output /dev/null
```

4. **Round 2 — Create new filters (all in parallel, after ALL deletes complete):**

Read `references/gws-cli-patterns.md` for the exact create command. Never mix delete and create for the same filter in the same round.

5. **Verify** — List filters to confirm each new `filter_id` exists:

```bash
~/.brain/integrations/gws[-ireland]/gws-claude.sh gmail users settings filters list \
  --params '{"userId": "me"}'
```

### 6. Label existing messages

For inbox messages matching updated filters:

1. Group messages by target label + action.
2. Execute message modify calls in parallel:

```bash
~/.brain/integrations/gws[-ireland]/gws-claude.sh gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"addLabelIds": ["Label_XX"], "removeLabelIds": ["INBOX", "UNREAD"]}'
```

For archive-only labels (Marketing, LinkedIn Social), omit `addLabelIds`. Batch ALL independent calls in one message.

### 7. Update changelog

This step is NOT optional — a stale changelog breaks the next session's gap detection.

1. Read current `~/.brain/integrations/gws[-ireland]/gmail-changelog.json`.
2. Determine next change ID (increment from last entry).
3. Append entries: `filters_updated` for modified filters, `batch_label_applied` for labeled messages.
4. Write the updated changelog.

Read `references/gws-cli-patterns.md` for the exact JSON schema.

### 8. Report

Present concisely:
- **Scanned:** N messages from inbox
- **Gaps found:** N unfiltered senders
- **Filters updated:** list of filters modified with sender counts
- **Messages labeled:** N messages across M labels
- **Changelog:** updated with change ID N
- **Audit results** — self-audit summary (or "all checks passed")
- **Errors** — issues encountered and how they were handled (or "none")

## Next action

> _Skipped: "Session complete — filters are live, changelog is updated."_

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — GWS wrapper accessible, auth valid, changelog loaded
2. **All user decisions collected?** — no unresolved ambiguous senders
3. **Filters verified?** — every created filter confirmed via list call
4. **Changelog updated?** — new entries appended with correct schema
5. **Anti-patterns clean?** — no bare `gws` calls, no `format: metadata`, no `tail -n +2`

</self_audit>

## Content audit

<content_audit>

> _Skipped: "N/A — skill manages email filters, does not generate verifiable content."_

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| Auth expired | Auto re-auth via `gws-reauth.py <account> --manage-chrome --headless`. If fails: AUQ with retry (visible Chrome) or manual fix. |
| Scan script fails | Report error with details → stop |
| Filter delete fails | Report which filter failed, continue with others |
| Filter create fails | Report error, do NOT update changelog for failed filter |
| Message modify fails | Report count of failures, continue with others |
| Changelog write fails | Report error — critical, user must fix manually |

## Anti-patterns

- **Bare `gws` calls.** Always use `~/.brain/integrations/gws[-ireland]/gws-claude.sh` — because bare `gws` fails in Claude Code sandbox due to macOS Keyring blocking token access.
- **`format: metadata` with `metadataHeaders`.** The API returns 200 with empty headers — because GWS CLI silently drops the array params. Always use `format: full`.
- **`tail -n +2` on wrapper output.** Chops the opening `{` — because `gws-claude.sh` outputs clean JSON that should be parsed directly.
- **Shell `for id in $ids` loops.** Quoting issues cause silent failures — because shell word splitting breaks on spaces in IDs. Use Python instead.
- **`--body` or `--params` for request body.** Neither works for body content — because `--json` is the correct flag for request bodies, `--params` is for URL parameters only.
- **Sequential API calls for independent operations.** Batch all independent calls in parallel — because sequential execution on 50+ messages wastes significant time.
- **Skipping changelog update.** Cascades into wrong analysis next session — because gap detection compares against changelog state, and stale data means missed senders.
- **Multiple open-ended questions at once.** Use structured AUQ with selectable options — because walls of questions overwhelm the user and produce inconsistent answers.

## Guidelines

- **Wrapper only.** Every GWS call goes through the selected account's `gws-claude.sh` wrapper — because the wrapper refreshes OAuth tokens from plain `tokens.json`, bypassing the macOS Keyring that blocks Claude Code sandbox. Use the path table in Pre-flight step 2 to resolve the correct wrapper.
- **Auto re-auth over manual.** When auth fails, run `gws-reauth.py` headless before asking the user — because the automated flow handles account selection, unverified app bypass, and consent granting in ~15 seconds without user intervention.
- **Parallel everything independent.** Batch independent API calls: Round 1 deletes, Round 2 creates, Round 3 message modifies — because this reduces 50+ sequential calls to ~3 rounds.
- **`--json` for body, `--params` for URL.** Two flags, not interchangeable — because embedding request body in `--params` fails silently with no error.
- **`--output /dev/null` on deletes.** Without it, GWS saves a `download.html` junk file — because the CLI defaults to saving response bodies.
- **Changelog is sacred.** Always update `gmail-changelog.json` — because it serves as both the safety net (revert instructions) and the input for next session's gap detection.
- **Structured decisions.** Present choices with `AskUserQuestion` and selectable options — because structured input is faster and less error-prone than open-ended questions.
