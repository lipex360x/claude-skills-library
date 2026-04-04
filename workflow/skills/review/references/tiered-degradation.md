# Quality Gate Contract — Tiered Degradation

The `/review` skill adapts to whatever infrastructure the project provides. Missing tiers degrade gracefully — the report notes what was skipped and why, instead of failing.

## Tiers

| Tier | What the project provides | What's enabled | Sub-agents affected |
|------|--------------------------|----------------|-------------------|
| **Minimum** | Git repo with a branch | Changed file scoping via `git diff`. Basic file existence checks. | None — coordinator only lists changed files |
| **Basic** | + `.docs/quality.md` | Semantic review: LLM judges code against quality rules | QA-semantic activated |
| **Standard** | + `quality-audit.config.json` + `quality-audit.py` (in `.claude/scripts/` or project root) | Static analysis: automated rule checking with exact line numbers | QA-static activated (full) |
| **Full** | + docker-compose (or equivalent) + `scripts/dev-start.sh` (or equivalent) + test runner + Playwright config | Runtime validation: tests, logs, browser console | QA-runtime activated |
| **Custom** | + `.claude/review-config.json` | Explicit overrides: custom paths, commands, thresholds, cycle limits | All — uses custom commands |

## Detection logic

The coordinator probes the project in pre-flight step 8. Detection order:

### 1. Static analysis tools

```
Search order for quality-audit:
1. .claude/scripts/quality-audit.py
2. scripts/quality-audit.py
3. quality-audit.py (project root)

Search order for config:
1. .claude/scripts/quality-audit.config.json
2. quality-audit.config.json (project root)

If neither found: QA-static falls back to lint + type-check only.
```

### 2. Lint, format, type-check commands

```
Detection priority (first match wins):

Lint:
1. .claude/review-config.json → lint_command
2. package.json → scripts.lint
3. Makefile → lint target
4. pyproject.toml → [tool.ruff] or [tool.flake8]

Format check:
1. .claude/review-config.json → format_command
2. package.json → scripts.format (append --check)
3. pyproject.toml → [tool.black] or [tool.ruff.format]

Type check:
1. .claude/review-config.json → typecheck_command
2. tsconfig.json exists → "npx tsc --noEmit"
3. pyproject.toml → [tool.mypy] or [tool.pyright]
4. mypy.ini exists → "mypy ."
```

### 3. Runtime infrastructure

```
Docker/containers:
1. docker-compose.yml or docker-compose.yaml or compose.yml
2. .claude/review-config.json → dev_start

Dev startup:
1. .claude/review-config.json → dev_start
2. scripts/dev-start.sh
3. docker compose up -d (if compose file found)

Test runner:
1. .claude/review-config.json → test_commands.*
2. package.json → scripts.test, scripts.test:unit, scripts.test:e2e
3. pytest.ini or pyproject.toml → [tool.pytest]
4. Makefile → test target

Playwright:
1. playwright.config.ts or playwright.config.js
2. package.json → devDependencies["@playwright/test"]
```

## Graceful degradation rules

1. **Never fail because a tier is missing.** Report what's available and what's skipped.
2. **Each sub-agent handles its own missing tools.** If QA-static can't find a linter, it reports `<skipped tool="lint" reason="no lint command detected" />` and continues with other checks.
3. **The report always has all 3 sections.** Missing sections show "SKIPPED" with the reason and the re-run command.
4. **Tier is noted in the report footer.** "Tier: Basic" tells the developer what level of review was possible.
5. **Upgrade hints.** When a tier is below Full, the report footer includes a one-liner suggesting what to add. Example: "Add `.docs/quality.md` to enable semantic review."

## Custom overrides via `.claude/review-config.json`

```json
{
  "quality_audit_path": ".claude/scripts/quality-audit.py",
  "quality_md_path": ".docs/quality.md",
  "lint_command": "npm run lint -- --check",
  "format_command": "npm run format -- --check",
  "typecheck_command": "npx tsc --noEmit",
  "test_commands": {
    "unit": "pytest tests/unit -x -v",
    "integration": "pytest tests/integration -x -v",
    "e2e": "npx playwright test"
  },
  "dev_start": "scripts/dev-start.sh",
  "dev_already_running": false,
  "log_sources": ["docker compose logs --tail=200"],
  "ports": [3000, 5432, 6379],
  "max_review_cycles": 3,
  "excluded_paths": ["node_modules", "dist", ".next", "__pycache__"],
  "severity_overrides": {
    "max-line-length": "WARN",
    "no-any": "FAIL"
  }
}
```

All fields are optional. When a field is present, it takes precedence over auto-detection.
