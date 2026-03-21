# Audit Report: check-gmail

Plugin: gws
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | ✅ | Rich trigger list including Portuguese variants: "check gmail", "scan inbox", "organize email", "limpar inbox", "organizar email", "verificar gmail" |
| 2 | WHAT + WHEN in description? | ✅ | Full pipeline described (auth → scan → gap detection → categorization → filter updates → changelog sync) with explicit WHEN triggers |
| 3 | "Even if" pattern? | ✅ | "even if they don't explicitly say 'gmail'" (line 10) |
| 4 | Under 500 lines? | ✅ | 217 lines |
| 5 | Imperative form? | ✅ | Steps use imperative: "Run the scan script", "Read current changelog", "Extract unique from_email values", "Present findings" |
| 6 | Constraints reasoned? | ✅ | All constraints have WHY: "Bare gws fails in Claude Code sandbox because macOS Keyring blocks token access" (line 183), "format: metadata silently drops metadataHeaders" (line 186) |
| 7 | Numbered steps? | ✅ | 6 phases with numbered sub-steps throughout |
| 8 | Output formats defined? | ✅ | Structured summary table format (line 75), AskUserQuestion patterns with exact option arrays (lines 92, 101, 110, 119) |
| 9 | Input contract? | ⚠️ | Optional maxResults parameter documented (line 37-43), but no explicit "required vs optional" section — input is implicit |
| 10 | Quality repeated at key points? | ✅ | "This step is NOT optional" for changelog (line 169), "Changelog is sacred" section (line 205), constraints repeated in anti-patterns |
| 11 | Anti-patterns named? | ✅ | 8 anti-patterns (lines 210-217): bare gws, format:metadata, tail stripping, shell loops, wrong flags, sequential calls, skipping changelog, open-ended questions |
| 12 | Refinement step? | ❌ | No post-execution verification — doesn't check if filters actually work after creation |
| 13 | Error handling patterns? | ✅ | Auth failure handling (lines 48-51), empty inbox handling (line 55), scan script has comprehensive error handling |
| 14 | Invoked with realistic input? | N/A | Audit scope — not tested |
| 15 | Activation tested? | N/A | Audit scope — not tested |
| 16 | Failure modes checked? | N/A | Audit scope — not tested |
| 17 | Subagents — context complete? | N/A | No subagents |
| 18 | Standard layout? | ✅ | SKILL.md, references/, scripts/, README.md — well organized |
| 19 | References one level deep? | ✅ | Single reference file `gws-cli-patterns.md` in `references/` |
| 20 | Large refs have TOC? | ✅ | `gws-cli-patterns.md` has clear sections with headers |
| 21 | Self-contained? | ⚠️ | References external paths: `~/.brain/integrations/gws/` for wrapper, changelog, auth script. These are integration dependencies, not cross-skill deps, but they make the skill non-portable |
| 22 | README generated? | ✅ | Present with triggers, workflow, directory structure, and dependencies |
| 23 | CLAUDE.md compliance? | ✅ | Follows all rules |

## Score: 14/17

(Excluding N/A items)

## Priority fixes (ordered by impact)

1. **Add refinement/verification step** — After creating filters, verify at least one filter works by listing filters and confirming the new filter_id exists
2. **Add explicit input contract** — Section clarifying: Required: none (scans inbox by default). Optional: maxResults (integer, default 50)
3. **Document external dependencies explicitly** — The skill depends on `~/.brain/integrations/gws/` which makes it non-portable. Add a "Prerequisites" section in SKILL.md noting these are required infrastructure components
