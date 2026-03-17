# Issue Update Guide

How to find, parse, and update GitHub issue checkboxes after a push.

## Fetching the issue

```bash
# Get issue body as raw text
gh issue view <N> --json body -q '.body'

# Get issue title + body
gh issue view <N> --json title,body
```

## Parsing checkboxes

Issue bodies use GitHub-flavored markdown checkboxes:

```markdown
- [ ] Unchecked task
- [x] Checked task
```

Parse the full body line by line. Track each checkbox with:
- **Line number** (position in the body)
- **State** (checked or unchecked)
- **Text** (the task description)
- **Context** (which Part/Step it belongs to — from preceding headers)

## Matching heuristics

Compare the changes in the current commit against unchecked boxes. Match from most specific to least:

### 1. File path match (strongest signal)
If a checkbox mentions a specific file path and that file was modified in the commit:
```
Checkbox: "- [ ] Create `src/routes/auth.ts` with login endpoint"
Commit modifies: src/routes/auth.ts
→ Strong match
```

### 2. Step title keyword match
If the checkbox text contains keywords that align with the commit message or changed files:
```
Checkbox: "- [ ] Add user authentication middleware"
Commit message: "feat: add auth middleware"
→ Good match
```

### 3. Part-level inference
If all checkboxes in a step are file-path matches and all are now done, the step is complete.

### Confidence levels

- **High confidence** — file path appears in both checkbox and diff, or checkbox text closely matches commit message. Mark automatically.
- **Medium confidence** — keywords overlap but not exact. Present to user: "This commit added `src/auth.ts`. Should I check off: `Create auth module`?"
- **Low confidence** — vague checkbox text, no file paths, generic description. Skip — let the user decide.

## Updating the issue

```bash
# Replace the full body (checkboxes toggled)
gh issue edit <N> --body "$(cat <<'EOF'
<full updated body here>
EOF
)"
```

The body must be the **complete** issue body with only the checkbox states changed. Do not modify any other content.

### Safe update process

1. Fetch the current body (`gh issue view`)
2. Store it in a variable
3. Toggle only the matched checkboxes (`- [ ]` → `- [x]`)
4. Write back the full body (`gh issue edit --body`)

This avoids race conditions where someone else edited the issue between fetch and update. For critical cases, fetch again after update and verify.

## Edge cases

### Partial step completion
A step has 4 checkboxes. The commit completes 2 of them. Mark only those 2 — don't mark the step header or remaining checkboxes.

### Files not yet created
A checkbox references a file that doesn't exist yet:
```
- [ ] Create `src/db/schema.ts` with users table
```
If the commit doesn't touch this file, don't mark it — even if related work was done.

### Multiple issues reference the same file
Rare, but possible. Only update the issue that matches the current branch.

### Issue body has been edited externally
If the body doesn't parse cleanly (e.g., someone added non-standard formatting), fall back to showing the user which checkboxes you think should be marked and let them confirm.

### Very large issue bodies
Some issues have 50+ checkboxes. Don't try to match all of them against the commit. Focus on checkboxes in the Part/Step that the commit message or branch context suggests.

## Reporting

After updating, report to the user:

```
Updated issue #14:
  ✓ Create src/routes/auth.ts with login endpoint (Step 3)
  ✓ Add auth middleware (Step 3)

Remaining: 12 open checkboxes (Step 4-6)
```

Keep it concise. The user can check the issue for full details.
