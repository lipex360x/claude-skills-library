---
name: sync-claude
description: Synchronize the Claude Code environment (skills-library + .brain) across machines. Pulls latest from both repos, rebuilds symlinks via setup.sh, and verifies the installation. Use this skill when the user says "sync claude", "sync skills", "sync brain", "pull skills", "update claude code", "update skills", "atualiza skills", "sincroniza", or wants to bring their environment up to date — even if they don't explicitly say "sync."
user-invocable: true
allowed-tools: Bash, AskUserQuestion, Read, Glob, Grep
---

Synchronize the Claude Code environment on this machine. Pull latest state from remote repos, rebuild symlinks, and verify everything is in sync.

## External state

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| skills-library | `~/www/claude/skills-library/` | Read (git pull) | Git repo with plugin directories |
| .brain | `~/www/claude/.brain/` | Read (git pull) | Git repo with config, hooks, rules |
| setup.sh | `~/www/claude/.brain/scripts/setup.sh` | Execute | Bash script that creates symlinks |
| symlinked skills | `~/.claude/skills/` | Read (verify) | Symlinks to skills-library |

## Steps

### 1. Pre-flight checks

Verify both directories exist:

```bash
ls -d ~/www/claude/skills-library/ 2>/dev/null && echo "skills-library: OK" || echo "skills-library: MISSING"
ls -d ~/www/claude/.brain/ 2>/dev/null && echo ".brain: OK" || echo ".brain: MISSING"
```

If either is missing, use `AskUserQuestion` for each missing directory with options `["Clone it", "Skip this repo"]`.

If "Clone it":
- For skills-library: `git clone <remote-url> ~/www/claude/skills-library/`
- For .brain: `git clone <remote-url> ~/www/claude/.brain/`

Detect the remote URL from the other repo if it exists (same GitHub owner), or ask the user.

If both are missing and both skipped, stop — nothing to sync.

### 2. Check working tree status

For each existing directory, check for uncommitted changes:

```bash
cd ~/www/claude/skills-library/ && git status --porcelain
cd ~/www/claude/.brain/ && git status --porcelain
```

If either has uncommitted changes, use `AskUserQuestion` with options:
- `"Stash and pull"` — run `git stash` before pulling, `git stash pop` after
- `"Skip this repo"` — leave it as-is, continue with the other
- `"Abort"` — stop the entire sync

### 3. Pull latest

For each repo that passed the working tree check:

```bash
cd ~/www/claude/skills-library/ && git pull 2>&1
cd ~/www/claude/.brain/ && git pull 2>&1
```

Capture the output to report what changed. If `git pull` fails (diverged branches, network error), use `AskUserQuestion` with options:
- `"Rebase"` — run `git pull --rebase`
- `"Skip this repo"` — leave it behind, continue
- `"Abort"` — stop

Track results per repo: commits pulled count, or "already up to date", or "skipped".

### 4. Rebuild symlinks

Run setup.sh to recreate all symlinks:

```bash
bash ~/www/claude/.brain/scripts/setup.sh
```

Capture the output — it reports which links were created, updated, or already correct.

### 5. Verify sync

Compare skills-library against the symlinked skills directory:

```bash
diff -rq ~/www/claude/skills-library/ ~/.claude/skills/ 2>/dev/null | grep -v '.git' | head -20
```

If discrepancies are found, list them. Common issues:
- **Orphaned symlinks** — skill removed from library but symlink persists
- **Missing symlinks** — new skill added but setup.sh didn't create the link
- **Stale content** — symlink exists but points to wrong location

### 6. Report

Present a concise summary:

```
## Sync complete

### skills-library
- Status: pulled 3 new commits (was abc1234, now def5678)
- Branch: main

### .brain
- Status: already up to date
- Branch: main

### Symlinks
- setup.sh: 35 skills linked
- Discrepancies: none (or list issues found)
```

If any repo was skipped or had errors, note it clearly.

## Guidelines

- **Never force-push or force-pull.** If branches have diverged, let the user decide. Data loss on a config repo is painful because there's no easy recovery path.
- **Stash is safe, reset is not.** When handling dirty trees, `git stash` preserves work. Never run `git checkout .`, `git reset --hard`, or `git clean -f`.
- **Report, don't fix.** If verification finds discrepancies, report them clearly but don't auto-fix. The user might have intentional local overrides.
- **Run setup.sh exactly once.** Multiple runs are idempotent but waste time. One run after both pulls is sufficient.
- **Handle partial sync gracefully.** If one repo syncs but the other fails, still run setup.sh and verify — a partial sync is better than no sync.
