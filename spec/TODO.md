# Issue #90 — Remaining work

## Done (in branch feat/90-decompose-start-issue)
- [x] 4 new skills created: /review, /pw, /validate, /update-docs
- [x] /start-issue simplified (420 → 219 lines)
- [x] /continue-issue updated (307 → 198 lines)
- [x] Tags simplified 12 → 5
- [x] Templates organized into docs/, config/, scripts/
- [x] STRUCTURE.md + plugin.json updated
- [x] 115 tests for validator scripts
- [x] Spec + references complete

## Pending (next sessions)
- [ ] Update /simplify skill with code-simplifier patterns (see reference-code-simplifier.md)
- [ ] Test the full pipeline on RAG Phase 3 (first real-world validation)
- [ ] Update start-new-project SKILL.md to scaffold .docs/ directory (currently only templates exist, SKILL.md steps not updated)
- [ ] Verify symlinks work after setup.sh for new skills
- [ ] Run tests: `cd workflow/skills/start-new-project/templates/scripts && python -m pytest test_validate_issue.py test_validate_issue_config.py`
- [ ] Consider squashing commits before merge to main

## Future backlog items (separate issues)
- Organize start-new-project/templates/ further (currently a mix of concerns)
- Create UI Designer super agent (Apple-level layouts)
- Lean skeleton migration for remaining 42 skills (incremental)
- Update /create-skill and /update-skill to understand new dynamics
