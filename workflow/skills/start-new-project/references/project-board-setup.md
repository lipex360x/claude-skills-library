# Project Board Setup Reference

Complete reference for setting up a GitHub Projects V2 board with custom columns and fields.

## Board Structure

### Status Columns (7)

| Column | Description |
|--------|-------------|
| Backlog | This item hasn't been started |
| Ready | This is ready to be picked up |
| In progress | This is actively being worked on |
| In review | This item is in review |
| Ready to PR | Review approved, ready to merge |
| Done | This has been completed |
| Cancelled | Closed without implementation (won't fix, duplicate, out of scope) |

### Custom Fields

**Priority** (Single Select):
- `P0` — Critical
- `P1` — High
- `P2` — Medium

**Size** (Single Select):
- `XS` — Extra small (< 1h)
- `S` — Small (1-2h)
- `M` — Medium (half day)
- `L` — Large (full day)
- `XL` — Extra large (multi-day)

## Setup Commands

### 1. Create the project

```bash
gh project create --title "<project name>" --owner "@me" --format json
```

Save the project number from the output.

### 2. Configure Status field

The default Status field has "Todo", "In Progress", "Done". Replace with the 7 custom columns.

**Get the project ID and Status field ID:**

```bash
# Get project node ID
PROJECT_ID=$(gh project view <number> --owner "@me" --format json | jq -r '.id')

# Get Status field ID and current option IDs
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
```

**Update the Status field with all 7 options:**

> **API gotcha:** The mutation uses `singleSelectOptions` (not `singleSelectField`), takes only `fieldId` (not `projectId`), and option objects do NOT accept an `id` field — the API replaces all options by name. Existing items retain their status if the option name matches.

```bash
STATUS_FIELD_ID="<from previous query>"

gh api graphql -f query='
  mutation {
    updateProjectV2Field(input: {
      fieldId: "'"$STATUS_FIELD_ID"'"
      singleSelectOptions: [
        { name: "Backlog", description: "This item hasn'\''t been started", color: GREEN }
        { name: "Ready", description: "This is ready to be picked up", color: YELLOW }
        { name: "In progress", description: "This is actively being worked on", color: ORANGE }
        { name: "In review", description: "This item is in review", color: PURPLE }
        { name: "Ready to PR", description: "Review approved, ready to merge", color: BLUE }
        { name: "Done", description: "This has been completed", color: GRAY }
        { name: "Cancelled", description: "Closed without implementation", color: RED }
      ]
    }) {
      projectV2Field {
        ... on ProjectV2SingleSelectField {
          id
          options { id name color }
        }
      }
    }
  }
'
```

### 3. Create Priority field

```bash
gh project field-create <number> --owner "@me" --name "Priority" --data-type "SINGLE_SELECT" --single-select-options "P0,P1,P2"
```

### 4. Create Size field

```bash
gh project field-create <number> --owner "@me" --name "Size" --data-type "SINGLE_SELECT" --single-select-options "XS,S,M,L,XL"
```

### 5. Add issues to the project

```bash
# Add each issue
ITEM_ID=$(gh project item-add <project-number> --owner "@me" --url <issue-url> --format json | jq -r '.id')
```

### 6. Set initial field values

After adding items, set their initial status, priority, and size:

```bash
# Set status to Backlog
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" --single-select-option-id "<backlog-option-id>"

# Set priority (get field ID from field-list first)
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$PRIORITY_FIELD_ID" --single-select-option-id "<option-id>"

# Set size
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$SIZE_FIELD_ID" --single-select-option-id "<option-id>"
```

## Moving Cards Between Columns

To move an item to a different status (e.g., "In progress"):

```bash
# 1. Find the project number for the repo
gh project list --owner "@me" --format json | jq '.projects[] | {number, title}'

# 2. Find the item ID for the issue
gh project item-list <project-number> --owner "@me" --format json | jq '.items[] | select(.content.number == <issue-number>) | .id'

# 3. Get field and option IDs
PROJECT_ID=$(gh project view <number> --owner "@me" --format json | jq -r '.id')

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

# 4. Update the item status
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" --field-id "$STATUS_FIELD_ID" --single-select-option-id "<target-option-id>"
```

## Blocks / Dependencies

Use issue body notation for blocking relationships — no custom field needed:

```markdown
> **Blocked by** #12
> **Blocks** #15
```

This is visible in the issue, portable, and doesn't require project field management. When creating issues with dependencies, include these annotations in the issue body.
