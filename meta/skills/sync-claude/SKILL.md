---
name: sync-claude
description: >-
  Synchronize the Claude Code environment (skills-library + .brain) across
  machines. Pulls latest from both repos, rebuilds symlinks via setup.sh, and
  verifies the installation. Use this skill when the user says "sync claude",
  "sync skills", "sync brain", "pull skills", "update claude code", "update
  skills", "atualiza skills", "sincroniza", or wants to bring their environment
  up to date — even if they don't explicitly say "sync."
user-invocable: true
allowed-tools:
  - Bash
  - AskUserQuestion
  - Read
  - Glob
  - Grep
---

# Sync Claude

Synchronize the Claude Code environment on this machine. Pull latest state from remote repos, rebuild symlinks, and verify everything is in sync.

**IMPORTANT:** Read the entire Pre-flight section before taking any action. Every failure scenario has a defined recovery path — never improvise or ask the user to run manual commands.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| *(none)* | — | — | — | — |

This skill takes no arguments. It operates on the well-known paths for `skills-library` and `.brain`.

</input_contract>

## Output contract

<output_contract>

| Artifact | Location | Persists | Format |
|----------|----------|----------|--------|
| Sync report | stdout | no | Markdown summary (repos pulled, symlinks verified, issues found) |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| skills-library | `~/www/claude/skills-library/` | Read (git pull) | Git repo with plugin directories |
| .brain | `~/www/claude/.brain/` | Read (git pull) | Git repo with config, hooks, rules |
| setup.sh | `~/www/claude/.brain/scripts/setup.sh` | Execute | Bash script that creates symlinks |
| symlinked skills | `~/.claude/skills/` | Read (verify) | Symlinks to skills-library |

</external_state>

## Pre-flight

<pre_flight>

1. **Verify directories exist:**

```bash
ls -d ~/www/claude/skills-library/ 2>/dev/null && echo "skills-library: OK" || echo "skills-library: MISSING"
ls -d ~/www/claude/.brain/ 2>/dev/null && echo ".brain: OK" || echo ".brain: MISSING"
```

2. **Handle missing directories:** If either is missing, use `AskUserQuestion` for each missing directory with options `["Clone it", "Skip this repo"]`.
   - If "Clone it":
     - For skills-library: `git clone <remote-url> ~/www/claude/skills-library/`
     - For .brain: `git clone <remote-url> ~/www/claude/.brain/`
   - Detect the remote URL from the other repo if it exists (same GitHub owner), or ask the user.
3. **Both missing and skipped → stop.** If both directories are missing and the user skipped both, there is nothing to sync.

</pre_flight>

## Steps

### 1. Check working tree status

For each existing directory, check for uncommitted changes:

```bash
cd ~/www/claude/skills-library/ && git status --porcelain
cd ~/www/claude/.brain/ && git status --porcelain
```

If either has uncommitted changes, use `AskUserQuestion` with options:
- `"Stash and pull"` — run `git stash` before pulling, `git stash pop` after
- `"Skip this repo"` — leave it as-is, continue with the other
- `"Abort"` — stop the entire sync

### 2. Pull latest

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

### 3. Rebuild symlinks

Run setup.sh to recreate all symlinks:

```bash
bash ~/www/claude/.brain/scripts/setup.sh
```

Capture the output — it reports which links were created, updated, or already correct.

### 4. Verify sync

Run three checks against `~/.claude/skills/`:

```bash
# 1. Broken symlinks (target no longer exists)
find ~/.claude/skills/ -maxdepth 2 -type l ! -exec test -e {} \; -print 2>/dev/null

# 2. Unmanaged items (non-symlink directories — not created by setup.sh)
find ~/.claude/skills/ -maxdepth 1 -mindepth 1 -not -type l 2>/dev/null

# 3. Symlinks pointing outside skills-library (stale or from old setup)
for link in ~/.claude/skills/*/; do
  [ -L "${link%/}" ] || continue
  target="$(readlink "${link%/}")"
  echo "$target" | grep -qv "skills-library" && echo "$(basename "${link%/}") -> $target"
done
```

setup.sh already reports warnings during step 3, but this step verifies nothing was missed.

Possible issues:
- **Broken symlinks** — target removed or renamed
- **Unmanaged directories** — leftover from manual installs or old setups
- **Wrong targets** — symlinks pointing outside skills-library (e.g., old `claude-dotfiles` paths)

If any issues are found, use `AskUserQuestion` with options:
- `"Remove unmanaged items"` — delete non-symlink directories and broken symlinks
- `"Re-run setup.sh"` — execute setup.sh again
- `"Both"` — remove orphans and re-run setup.sh
- `"Skip"` — leave as-is, just report them

### 5. Report

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

## Next action

> _Skipped: "N/A — sync-claude is a terminal operation with no follow-up skill."_

## Self-audit

<self_audit>

Before delivering the sync report, verify:
- [ ] Every repo that was pulled shows the correct before/after commit hashes
- [ ] setup.sh ran exactly once (after both pulls completed)
- [ ] Verification checks ran and results are included in the report
- [ ] Any skipped repos or errors are clearly noted
- [ ] No destructive git commands were used (no `--force`, `--hard`, `clean -f`)

</self_audit>

## Content audit

> _Skipped: "N/A — transient status report, not persistent content."_

## Error handling

| Error | Cause | Recovery |
|-------|-------|----------|
| Directory missing | `skills-library` or `.brain` not cloned on this machine | AUQ: offer to clone or skip |
| Dirty working tree | Uncommitted changes in a repo | AUQ: stash and pull, skip, or abort |
| Git pull fails | Diverged branches or network error | AUQ: rebase, skip, or abort |
| setup.sh not found | `.brain` was skipped or clone failed | Skip symlink rebuild, note in report |
| Broken symlinks | Target skill removed or renamed after pull | AUQ: remove, re-run setup.sh, both, or skip |
| Unmanaged directories | Leftover from manual installs or old setups | AUQ: remove, re-run setup.sh, both, or skip |

## Anti-patterns

- **Force-pulling over diverged branches.** Running `git pull --force` or `git reset --hard origin/main` silently discards local commits. Always let the user choose how to resolve divergence.
- **Resetting dirty trees.** Using `git checkout .`, `git reset --hard`, or `git clean -f` to get a clean tree destroys uncommitted work. Use `git stash` instead.
- **Auto-fixing discrepancies.** Automatically deleting orphaned symlinks or recreating missing ones can break intentional local overrides. Report first, then offer options.
- **Running setup.sh before pulling.** Rebuilding symlinks before pulling means they point to stale content. Always pull first, then rebuild.

## Guidelines

- **Never force-push or force-pull.** If branches have diverged, let the user decide. Data loss on a config repo is painful because there's no easy recovery path.
- **Stash is safe, reset is not.** When handling dirty trees, `git stash` preserves work. Never run `git checkout .`, `git reset --hard`, or `git clean -f`.
- **Report, don't fix.** If verification finds discrepancies, report them clearly but don't auto-fix. The user might have intentional local overrides.
- **Run setup.sh exactly once.** Multiple runs are idempotent but waste time. One run after both pulls is sufficient.
- **Handle partial sync gracefully.** If one repo syncs but the other fails, still run setup.sh and verify — a partial sync is better than no sync.
