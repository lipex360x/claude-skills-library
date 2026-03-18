# GWS CLI Patterns for Gmail Operations

Exact working commands for every Gmail operation. These encode hard-won workarounds — do not deviate.

## Wrapper path

Always use the wrapper, never bare `gws`:

```
~/.brain/integrations/gws/gws-claude.sh
```

## Flag rules

| Flag | Purpose | Example |
|------|---------|---------|
| `--params` | URL/query parameters (userId, format, maxResults) | `--params '{"userId": "me"}'` |
| `--json` | Request body (filter criteria, message modifications) | `--json '{"criteria": {...}}'` |
| `--output /dev/null` | Suppress junk file creation on delete ops | Always add to delete commands |

`--body` does not exist. `--params` cannot carry request bodies. These are the two most common mistakes.

## Operations reference

### Profile (auth check)

```bash
gws-claude.sh gmail users getProfile --params '{"userId": "me"}'
```

### List messages

```bash
gws-claude.sh gmail users messages list \
  --params '{"userId": "me", "q": "in:inbox", "maxResults": 50}'
```

### Get message (full format)

```bash
gws-claude.sh gmail users messages get \
  --params '{"userId": "me", "id": "MSG_ID", "format": "full"}'
```

Never use `"format": "metadata"` with `"metadataHeaders"` — the GWS CLI silently drops array parameters. The API call succeeds (200) but returns empty headers. Always use `format: full` and extract headers client-side.

### Modify message (add label + archive)

```bash
gws-claude.sh gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"addLabelIds": ["Label_XX"], "removeLabelIds": ["INBOX", "UNREAD"]}'
```

For archive-only (Marketing, LinkedIn Social — no custom label):

```bash
gws-claude.sh gmail users messages modify \
  --params '{"userId": "me", "id": "MSG_ID"}' \
  --json '{"removeLabelIds": ["INBOX", "UNREAD"]}'
```

### Create filter

```bash
gws-claude.sh gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "sender1@example.com OR sender2@example.com"},
    "action": {
      "addLabelIds": ["Label_XX"],
      "removeLabelIds": ["INBOX"]
    }
  }'
```

For Marketing (archive + mark read, no custom label):

```bash
gws-claude.sh gmail users settings filters create \
  --params '{"userId": "me"}' \
  --json '{
    "criteria": {"from": "..."},
    "action": {
      "removeLabelIds": ["INBOX"],
      "markRead": true
    }
  }'
```

### Delete filter

```bash
gws-claude.sh gmail users settings filters delete \
  --params '{"userId": "me", "id": "FILTER_ID"}' \
  --output /dev/null
```

### List filters (verify current state)

```bash
gws-claude.sh gmail users settings filters list \
  --params '{"userId": "me"}'
```

## Known GWS CLI limitations

1. **Array params silently dropped** — `metadataHeaders`, `labelIds` in params are ignored. Pass arrays only in `--json` body.
2. **No filter update API** — Gmail API has no PATCH for filters. Must delete + create.
3. **Delete creates junk files** — Without `--output /dev/null`, delete operations save a `download.html` to the current directory.
4. **Wrapper outputs clean JSON** — `gws-claude.sh` does not add status lines. Do NOT use `tail -n +2` to strip output — it will chop the opening `{` and break JSON parsing.

## Changelog entry schema

### filters_updated entry

```json
{
  "id": "NNN",
  "date": "YYYY-MM-DD",
  "type": "filters_updated",
  "description": "Updated N filters with expanded sender lists (delete+recreate pattern)",
  "filters": [
    {
      "filter_id": "new_filter_id_from_api_response",
      "old_filter_id": "deleted_filter_id",
      "name": "Label → action description",
      "from": "full OR-separated sender list",
      "added_senders": ["only_the_new@senders.com"],
      "action": "addLabel Label, skip inbox"
    }
  ],
  "revert": "Delete filters via: gws gmail users settings filters delete --params '{\"userId\": \"me\", \"id\": \"FILTER_ID\"}'"
}
```

### batch_label_applied entry

```json
{
  "id": "NNN",
  "date": "YYYY-MM-DD",
  "type": "batch_label_applied",
  "description": "Applied labels to N inbox emails and archived them",
  "batches": [
    {
      "label": "LabelName (Label_XX)",
      "action": "addLabel + removeFromInbox + markRead",
      "count": 5,
      "senders": ["sender@example.com (count)"]
    }
  ]
}
```

IDs are sequential strings: "001", "002", etc. Always increment from the last entry in the changelog.
