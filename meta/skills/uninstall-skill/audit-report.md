# Audit Report: uninstall-skill

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 5 triggers: "uninstall skill", "remove skill", "delete skill", "skill uninstall", "wants to remove an installed skill" |
| 2 | WHAT + WHEN | ✅ | What: "Uninstall a skill by name, local or global". When: user wants to remove a skill |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "uninstall."` |
| 4 | Under 500 lines | ✅ | 29 lines — extremely thin |
| 5 | Imperative form | ✅ | "Check both locations", "Delete the skill directory", "Report removal" |
| 6 | Constraints reasoned | ❌ | No reasoning anywhere. Step 3 says `rm -rf` with no justification or safety consideration. No explanation for why STRUCTURE.md should be updated |
| 7 | Numbered steps | ✅ | 4 numbered steps |
| 8 | Output formats defined | ⚠️ | "Report removal with the skill name and which location was cleaned" — very vague, no template |
| 9 | Input contract | ✅ | `$ARGUMENTS` referenced, `argument-hint: <skill-name>`, `allowed-tools` defined |
| 10 | Quality repeated at key points | ❌ | No quality reinforcement at any point. Bare procedural steps |
| 11 | Anti-patterns named | ❌ | No anti-patterns section. Critical gaps: removing skills that other skills depend on, deleting without confirmation in destructive cases, not cleaning symlinks |
| 12 | Refinement step | ❌ | No review or verification. Deletes and reports — no confirmation that symlinks were cleaned, no post-delete verification |
| 13 | Error handling | ❌ | No handling for: skill not found in either location, permission denied, skill is a symlink vs real directory, setup.sh not re-run after global removal |
| 14 | Standard layout | ✅ | SKILL.md + README |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ⚠️ | References `~/www/claude/.brain/STRUCTURE.md` but should reference `~/www/claude/skills-library/STRUCTURE.md` for global skill removal. Inconsistent with install-skill |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set, `allowed-tools` defined |

## Score: 7/16

## Priority fixes (ordered by impact)

1. **Error handling** — Add handling for: skill not found (search and suggest similar names), permission errors, skill is a symlink (follow to source). This is a destructive operation — errors must be caught before `rm -rf`.
2. **Constraints reasoned** — Add safety reasoning: why confirm before deleting, why re-run setup.sh after global removal, why check for dependents.
3. **Anti-patterns section** — Add: deleting without confirming scope, not re-running setup.sh (leaves orphaned symlinks), removing skills other skills depend on, deleting STRUCTURE.md entry but not the symlink.
4. **Refinement step** — After deletion, verify: symlink removed, STRUCTURE.md updated, no orphaned references. Run `setup.sh` for global removals to clean stale symlinks.
5. **STRUCTURE.md reference** — Step 3 references `.brain/STRUCTURE.md` but global skills are tracked in `skills-library/STRUCTURE.md`. Fix to match install-skill's behavior.
6. **Output format** — Define a report template: skill name, location removed, symlink status, STRUCTURE.md updated, any warnings.
