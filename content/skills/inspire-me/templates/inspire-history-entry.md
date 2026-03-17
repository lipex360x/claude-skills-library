# Inspire History Entry Format

Each entry appended to `inspire-history.md` follows this format:

```markdown
### {{date}} — {{domain}}

**Block:** {{one-line summary of the block}}
**Core insight:** {{the breakthrough sentence from the session}}
**Action:** {{the immediate next step agreed upon}}
**Previous action status:** {{done-helped | done-didnt-help | not-done | first-session}}
**Energy at start:** {{energized | tired | overwhelmed | curious}}
**Materials used:** {{none | documents: [list] | web research | both}}
```

## History file structure

The `inspire-history.md` file has this overall shape:

```markdown
# Inspire History

> Cumulative record of /inspire-me sessions. Read by the skill at the start of each session to detect patterns and follow up on actions.

## Patterns

{{Updated after 3+ entries. Synthesizes recurring themes, common root causes, and effective strategies. Written in second person: "You tend to...", "What works for you is..."}}

## Sessions

{{Entries in reverse chronological order — newest first.}}
```

## Rules

- Append new entries at the top of the `## Sessions` section (newest first).
- Update the `## Patterns` section after every session once there are 3+ entries.
- Keep entries compact — this file should be scannable, not verbose.
- Use the user's chosen language for block and insight descriptions.
- The `## Patterns` section is the most valuable part — invest in making it insightful, not just a list.
