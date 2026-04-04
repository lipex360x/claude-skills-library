# Start Issue — Anti-patterns

- **Checkboxes without TDD order.** Implementation before test, or tests missing entirely — because the test-first order IS the enforcement mechanism. Always: test checkbox first, then implementation checkbox.
- **Generic checkboxes without file paths.** "Add tests" instead of "Add test for login in `src/__tests__/auth.test.ts` — expect 200 with valid credentials" — because vague checkboxes produce vague implementations.
- **Steps that mix concerns.** Backend + frontend in one Step — because mixed concerns make the Step harder to verify and impossible to parallelize.
- **Missing verification checkboxes.** No way to confirm the Step works — because unverified work is assumed work, not done work.
- **Over-expanding simple issues.** 10+ Steps when 3 would suffice — because planning overhead should not exceed implementation effort.
- **Duplicating acceptance criteria.** Copying criteria verbatim as checkboxes instead of expanding them into concrete actions — because the plan should add detail, not echo the brief.
- **Local/absolute paths in issue content.** `~/.brain/`, `/Users/...` in issue body — because issue content is public and portable. Always use project-relative paths.
- **Workarounds or hacks.** Hardcoded values, temporary flags, `any` casts — because if it needs a TODO comment, the step is incomplete.
- **Comments that restate code.** Self-documenting code replaces narration — because comments that say what the code does add noise, not clarity.
- **Horizontal TDD.** Writing all tests first, then all implementations — because vertical slices (RED→GREEN→RED→GREEN) enforce discipline and catch design issues early.
- **Using sed/regex on GitHub issue body.** sed can corrupt markdown structure, and GitHub's issue API has no merge — last write wins. Always edit `.docs/issues/<N>.md` locally and publish with `gh issue edit <N> --body "$(cat .docs/issues/<N>.md)"`.
- **Spawning Explore when .docs/architecture.md exists.** An Explore agent costs ~50k tokens. .docs/architecture.md has the same context in ~2k tokens — because it's updated by `/update-docs` after development. Read it first. Only explore areas it doesn't cover.
