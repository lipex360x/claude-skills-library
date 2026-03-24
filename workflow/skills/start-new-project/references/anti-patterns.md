# Start New Project — Anti-patterns

- **Checkboxes without TDD order.** Implementation before test, or tests missing entirely — because the test-first order IS the enforcement mechanism. Always: test checkbox first, then implementation checkbox.
- **Generic checkboxes without file paths.** "Add tests" instead of specifying the test file and expected behavior — because vague checkboxes produce vague implementations.
- **Steps that mix concerns.** Backend + frontend in one Step — because mixed concerns make the Step harder to verify and impossible to parallelize.
- **Missing verification checkboxes.** No way to confirm the Step works — because unverified work is assumed work, not done work.
- **Monolithic issues with 10+ steps.** When the mandatory split rule should have triggered — because progress gets buried and milestone tracking becomes useless.
- **Front-loading detail on later phases.** Phase 1 should be precise, later phases can be higher-level — because over-specifying Phase 3 when Phase 1 hasn't started wastes planning effort on assumptions that will change.
- **Local/absolute paths in issue content.** `~/.brain/`, `/Users/...` in issue body — because issue content is public and portable. Always use project-relative paths.
- **Workarounds or hacks.** Hardcoded values, temporary flags, `any` casts — because if it needs a TODO comment, the step is incomplete.
- **Comments that restate code.** Self-documenting code replaces narration — because comments that say what the code does add noise, not clarity.
