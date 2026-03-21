# Audit Report: install-skill

Plugin: meta
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough | ✅ | 4 triggers: "install skill", "add skill", "skill install", "provides an npx skills command" |
| 2 | WHAT + WHEN | ✅ | What: "Install a skill from an npx skills link, with local or global selection". When: user mentions installing or provides npx command |
| 3 | "Even if" pattern | ✅ | `even if they don't explicitly say "install."` |
| 4 | Under 500 lines | ✅ | 144 lines |
| 5 | Imperative form | ✅ | "Run the npx command", "Move the skill directory", "Run setup.sh" |
| 6 | Constraints reasoned | ⚠️ | Some reasoning ("This is idempotent" line 95, "The installation is not complete until changes are pushed" line 135) but most steps are bare instructions without justification |
| 7 | Numbered steps | ✅ | 12 numbered steps (3.1-3.12 for global) |
| 8 | Output formats defined | ✅ | Report format in step 3.12 with 5 items to report |
| 9 | Input contract | ✅ | `$ARGUMENTS` referenced, `argument-hint: <npx-skills-add-command>`, `allowed-tools` defined |
| 10 | Quality repeated at key points | ❌ | No quality reinforcement at key steps. Steps are procedural without quality gates |
| 11 | Anti-patterns named | ❌ | No anti-patterns section. Common failures: installing duplicate skills without checking, forgetting to push, leaving npx artifacts |
| 12 | Refinement step | ❌ | No review or verification step before pushing. Goes straight from README update to push |
| 13 | Error handling | ⚠️ | Handles git pull failure (step 3.1), duplicate detection (step 3.2), but no handling for: npx command failure, skill without SKILL.md, setup.sh failure, push failure |
| 14 | Standard layout | ✅ | SKILL.md + README |
| 15 | References one level deep | N/A | No references directory |
| 16 | Self-contained | ❌ | Cross-skill dependencies: step 3.10 invokes `/create-readme` skill, step 3.11 invokes `/push` skill. These should be inline instructions or self-contained |
| 17 | README generated | ✅ | README.md exists |
| 18 | CLAUDE.md compliance | ✅ | `user-invocable: true` set, `allowed-tools` defined |

## Score: 10/16

## Priority fixes (ordered by impact)

1. **Cross-skill dependencies** — Steps 3.10 and 3.11 invoke `/create-readme` and `/push` skills. This violates the "self-contained" rule. Inline the necessary README generation and push instructions, or reference them as optional post-steps the user can run separately.
2. **Anti-patterns section** — Add: installing skills that conflict with existing ones, skipping STRUCTURE.md update, leaving npx artifacts in the project, pushing without verifying the skill works.
3. **Refinement step** — Add a verification step before pushing: confirm the skill is discoverable (`/` autocomplete test or symlink verification), SKILL.md is valid, README is generated.
4. **Error handling** — Add handling for npx failures, malformed skills (no SKILL.md), setup.sh failures, and push failures.
5. **Quality at key points** — Add quality gate at step 3.5 (verify SKILL.md has required frontmatter) and step 3.9 (verify STRUCTURE.md entry is correct).
