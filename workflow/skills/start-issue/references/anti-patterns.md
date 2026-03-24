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
- **Skipping Agent Teams check.** Proposing a plan without checking `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` first — because if enabled, the Execution mode section at the top is mandatory, not optional.
- **Placing Agent Teams section at bottom.** The agent reads top-down and will default to isolated worktree agents if it doesn't see the execution mode first — because placement determines behavior.
- **Multiple agents editing the same issue body.** Last `gh issue edit --body` wins, earlier edits silently lost — because GitHub's issue API has no merge. Use internal tasks for parallel progress tracking.
- **Full context in TeamCreate prompts.** Duplicates content, causes drift between approved plan and actual execution — because the issue is the single source of truth, not the prompt.
