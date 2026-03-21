# Audit Report: deploy-vercel

Plugin: deploy
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ❌ | "Deploy, manage, and develop projects on Vercel from the command line" — too generic, no trigger contexts, no WHEN |
| 2 | WHAT + WHEN in description? | ❌ | Only WHAT. Missing WHEN — no "Use when..." clause |
| 3 | "Even if" pattern? | ❌ | Missing entirely |
| 4 | Under 500 lines? | ✅ | 66 lines |
| 5 | Imperative form? | ⚠️ | Mixed — decision tree is good, but intro uses passive "The Vercel CLI deploys..." instead of imperative |
| 6 | Constraints reasoned? | ✅ | Anti-patterns explain WHY: "creates project.json, which only tracks one project" |
| 7 | Numbered steps? | ❌ | No numbered process steps — body is a decision tree + anti-patterns but no step-by-step flow |
| 8 | Output formats defined? | ❌ | No output format defined — doesn't specify what result looks like after deployment |
| 9 | Input contract? | ❌ | No input contract — doesn't define what user must provide (project path? environment? flags?) |
| 10 | Quality repeated at key points? | ❌ | No quality gates |
| 11 | Anti-patterns named? | ✅ | 7 anti-patterns at lines 60-66 with clear explanations |
| 12 | Refinement step? | ❌ | No refinement or verification step after execution |
| 13 | Error handling patterns? | ⚠️ | "When something goes wrong, check how things are linked first" (line 19) — partial, only for linking issues |
| 14 | Invoked with realistic input? | N/A | Audit scope — not tested |
| 15 | Activation tested? | N/A | Audit scope — not tested |
| 16 | Failure modes checked? | N/A | Audit scope — not tested |
| 17 | Subagents — context complete? | N/A | No subagents |
| 18 | Standard layout? | ⚠️ | Has SKILL.md, references/, README.md, plus `command/vercel.md` (non-standard). No templates/ but not needed |
| 19 | References one level deep? | ✅ | All references in `references/` flat directory (16 files) |
| 20 | Large refs have TOC? | ✅ | Decision tree in SKILL.md serves as TOC routing to all references |
| 21 | Self-contained? | ✅ | No cross-skill dependencies |
| 22 | README generated? | ✅ | Present and comprehensive |
| 23 | CLAUDE.md compliance? | ✅ | No CLAUDE.md in skill (not required) |

## Score: 7/17

(Excluding N/A items)

## Priority fixes (ordered by impact)

1. **Rewrite description** — Add WHEN triggers: "Use when deploying to Vercel, configuring domains, setting up environment variables, managing CI/CD pipelines, or troubleshooting deployment issues — even if they don't explicitly say 'Vercel'"
2. **Add numbered process steps** — Transform decision tree into: 1) Identify task type, 2) Verify project linking, 3) Read relevant reference, 4) Execute commands, 5) Verify result
3. **Define output format** — Specify what a successful execution looks like (deployment URL? status summary?)
4. **Add input contract** — Required: project directory. Optional: environment (preview/production), team, flags
5. **Add refinement/verification step** — After deployment: check status, verify URL, confirm environment variables
6. **Add quality checkpoints** — E.g., "Before deploying to production, verify preview deployment works"
