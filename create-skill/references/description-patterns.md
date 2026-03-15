# Description Patterns

Claude decides whether to activate a skill based solely on `name` + `description`. A weak description means the skill never fires, no matter how good the instructions are.

## The "pushy" technique

Claude tends to **undertrigger** — it won't use a skill unless the match is obvious. Counter this by including specific trigger phrases and contexts, not just a dry summary.

**Weak:**
```yaml
description: Run database migrations.
```

**Strong:**
```yaml
description: Run, create, and manage database migrations safely. Use this skill when the user mentions "migrate", "schema change", "add a column", "create a table", or wants to modify the database structure — even if they don't explicitly say "migration."
```

The **"even if they don't explicitly say X"** pattern is particularly effective. It tells Claude to look for intent, not just keywords.

## Include both WHAT and WHEN

The description should answer two questions:
1. **What does this skill do?** (the action)
2. **When should Claude activate it?** (the trigger contexts)

## More examples

**A code review skill:**
```yaml
description: Review pull requests for code quality, security issues, and architectural consistency. Use this when the user says "review this PR", "check my code", shares a PR link, or asks for feedback on changes — even if they just say "take a look."
```

**A deployment skill:**
```yaml
description: Build, validate, and deploy the application to staging or production. Use this when the user says "deploy", "ship it", "push to prod", or after completing a feature that's ready to go live.
```

**A project scaffolding skill:**
```yaml
description: Plan and scaffold new projects with structured issues and phased implementation. Use this when the user wants to start a new project, plan phases, create a project structure, or set up a new repo — even if they just say "let's start something new."
```
