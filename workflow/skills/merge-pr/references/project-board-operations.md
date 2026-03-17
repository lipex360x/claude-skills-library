# Project Board Operations Reference

Reference for interacting with an existing GitHub Projects V2 board — moving cards, setting fields.

## Moving a Card to a Status

To move an issue to a different status (e.g., "In progress"):

```bash
# 1. Find the project for the repo
gh project list --owner "@me" --format json | jq '.projects[] | {number, title}'

# 2. Get the project node ID
PROJECT_ID=$(gh project view <number> --owner "@me" --format json | jq -r '.id')

# 3. Find the item ID for the issue in the project
ITEM_ID=$(gh project item-list <project-number> --owner "@me" --format json | jq -r '.items[] | select(.content.number == <issue-number>) | .id')

# 4. Get the Status field ID and option IDs
gh api graphql -f query='
  query($projectId: ID!) {
    node(id: $projectId) {
      ... on ProjectV2 {
        field(name: "Status") {
          ... on ProjectV2SingleSelectField {
            id
            options { id name }
          }
        }
      }
    }
  }
' -f projectId="$PROJECT_ID"

# 5. Update the item status
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" --single-select-option-id "<target-option-id>"
```

## Setting Priority and Size

If an issue doesn't have priority or size set, use the same `item-edit` pattern:

```bash
# Get field IDs
gh project field-list <project-number> --owner "@me" --format json

# Set priority
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$PRIORITY_FIELD_ID" --single-select-option-id "<option-id>"

# Set size
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$SIZE_FIELD_ID" --single-select-option-id "<option-id>"
```

## Board Structure Reference

### Status Columns (6)

| Column | Description |
|--------|-------------|
| Backlog | This item hasn't been started |
| Ready | This is ready to be picked up |
| In progress | This is actively being worked on |
| In review | This item is in review |
| Ready to PR | This is ready for a pull request |
| Done | This has been completed |

### Priority Options
- `P0` — Critical
- `P1` — High
- `P2` — Medium

### Size Options
- `XS` — Extra small (< 1h)
- `S` — Small (1-2h)
- `M` — Medium (half day)
- `L` — Large (full day)
- `XL` — Extra large (multi-day)

## Blocks / Dependencies

Use issue body notation — no custom field needed:

```markdown
> **Blocked by** #12
> **Blocks** #15
```

When picking up an issue, check for these annotations. If a blocking issue is still open, flag it to the user before starting work.
