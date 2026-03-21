# Audit Report: {{skill-name}}

Plugin: {{plugin}}
Audited: {{ISO-8601 date}}
Checklist version: {{date or commit of review-checklist.md}}

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description: pushy triggers | {{✅/❌/⚠️}} | {{specific finding with counts/quotes}} |
| 2 | Description: WHAT + WHEN | {{✅/❌/⚠️}} | {{specific finding}} |
| 3 | Description: "even if" pattern | {{✅/❌/⚠️}} | {{specific finding}} |
| 4 | SKILL.md: under 500 lines | {{✅/❌/⚠️}} | {{line count}} |
| 5 | SKILL.md: imperative form | {{✅/❌/⚠️}} | {{specific finding}} |
| 6 | SKILL.md: constraints reasoned | {{✅/❌/⚠️}} | {{specific finding}} |
| 7 | SKILL.md: numbered steps | {{✅/❌/⚠️}} | {{specific finding}} |
| 8 | SKILL.md: output formats | {{✅/❌/⚠️}} | {{specific finding}} |
| 9 | SKILL.md: input contract | {{✅/❌/⚠️}} | {{specific finding}} |
| 10 | Quality: repeated at key points | {{✅/❌/⚠️}} | {{specific finding}} |
| 11 | Quality: anti-patterns named | {{✅/❌/⚠️}} | {{specific finding}} |
| 12 | Quality: refinement step | {{✅/❌/⚠️}} | {{specific finding}} |
| 13 | Quality: error handling | {{✅/❌/⚠️}} | {{specific finding}} |
| 14 | Testing: realistic input | {{✅/❌/⚠️}} | {{specific finding}} |
| 15 | Testing: activation tested | {{✅/❌/⚠️}} | {{specific finding}} |
| 16 | Testing: failure modes checked | {{✅/❌/⚠️}} | {{specific finding}} |
| 17 | Subagents: context complete | {{✅/❌/⚠️/N/A}} | {{specific finding}} |
| 18 | Subagents: tool access explicit | {{✅/❌/⚠️/N/A}} | {{specific finding}} |
| 19 | Subagents: two-phase build | {{✅/❌/⚠️/N/A}} | {{specific finding}} |
| 20 | Subagents: race conditions | {{✅/❌/⚠️/N/A}} | {{specific finding}} |
| 21 | Structure: standard layout | {{✅/❌/⚠️}} | {{specific finding}} |
| 22 | Structure: references depth | {{✅/❌/⚠️}} | {{specific finding}} |
| 23 | Structure: large refs have TOC | {{✅/❌/⚠️/N/A}} | {{specific finding}} |
| 24 | Structure: self-contained | {{✅/❌/⚠️}} | {{specific finding}} |
| 25 | Structure: README generated | {{✅/❌/⚠️}} | {{specific finding}} |
| 26 | Compliance: CLAUDE.md | {{✅/❌/⚠️}} | {{specific finding}} |

## Score: {{pass-count}}/{{total-applicable}}

## Priority fixes (ordered by impact)

1. **{{fix title}}** — {{specific finding with evidence}}
2. **{{fix title}}** — {{specific finding with evidence}}
3. **{{fix title}}** — {{specific finding with evidence}}

## Recommended action

- [ ] Run `/create-skill {{skill-name}}` with this report to apply fixes
