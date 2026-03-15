# Description Patterns

Claude decides whether to activate a skill based solely on `name` + `description`. A weak description means the skill never fires, no matter how good the instructions are.

## The "pushy" technique

Claude tends to **undertrigger** — it won't use a skill unless the match is obvious. Counter this by including specific trigger phrases and contexts, not just a dry summary.

**Weak:**
```yaml
description: Create a design system from a reference image.
```

**Strong:**
```yaml
description: Analyze a design image and create a full design system project with separated artboards. Use this skill whenever the user provides a reference image, screenshot, or mockup and wants to extract a design system, create artboards, build a component library, or reverse-engineer visual patterns — even if they don't explicitly say "design system."
```

The **"even if they don't explicitly say X"** pattern is particularly effective. It tells Claude to look for intent, not just keywords.

## Include both WHAT and WHEN

The description should answer two questions:
1. **What does this skill do?** (the action)
2. **When should Claude activate it?** (the trigger contexts)

## More examples

**A push skill:**
```yaml
description: Commit, push changes, and auto-update related GitHub issue checkboxes. Use this when the user says "push", "send it", "ship it", or after completing a task that has an open issue.
```

**A project scaffolding skill:**
```yaml
description: Plan and scaffold new projects with structured GitHub issues and phased implementation. Use this when the user wants to start a new project, plan phases, create a project structure, or set up a new repo — even if they just say "let's start something new."
```
