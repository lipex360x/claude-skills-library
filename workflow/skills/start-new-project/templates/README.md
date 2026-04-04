# Templates

Organized by destination in the target project.

## docs/

Templates for project documentation files (root or `.docs/`).

- `architecture.md` -- ARCHITECTURE.md skeleton (codebase knowledge cache)
- `quality-standards.md` -- Reference for generating `quality.md` (code quality rules)
- `dev-scripts.md` -- Reference for creating `scripts/dev-start.sh` and `scripts/dev-stop.sh`

## config/

Templates for `.claude/` configuration files.

- `project-settings.json` -- Chrome CDP and page registry settings
- `validate-issue.config.json` -- Rules and thresholds for the issue validator

## scripts/

Templates for scripts and hooks copied into target projects.

- `issue-backup.sh` -- SQLite backup for GitHub issue bodies
- `validate-issue.sh` / `validate-issue.py` -- Issue structure validator (wrapper + engine)
- `pre-issue-edit-hook.sh` -- PreToolUse hook: snapshot before `gh issue edit`
- `post-merge-compact-hook.sh` -- PostToolUse hook: compact backups after PR merge
- `start-chrome.sh` -- Chrome CDP launcher for `.claude/`
- `cdp-run-all.ts` -- CDP runner: auto-discovers and runs `verify-*.ts` scripts
- `cdp-test-example.ts` -- CDP verification script template for `e2e/cdp/`

## Root

- `issue-template.md` -- GitHub issue body structure template
