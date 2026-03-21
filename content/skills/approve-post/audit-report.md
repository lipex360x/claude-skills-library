# Audit Report: approve-post

Plugin: content
Audited: 2026-03-21

## Results

| # | Check | Status | Finding |
|---|-------|--------|---------|
| 1 | Description pushy enough? | PASS | Lists 5 trigger phrases: "approve post", "publish post", "post approve", "ship the post", finalize a draft (line 3) |
| 2 | WHAT + WHEN? | PASS | States what (approve draft, translate, publish) and when (trigger phrases + "even if" clause) |
| 3 | "Even if" pattern? | PASS | `"even if they don't explicitly say 'approve.'"` present (line 3) |
| 4 | Under 500 lines? | PASS | SKILL.md is 33 lines |
| 5 | Imperative form? | PASS | Uses imperative throughout: "Glob", "Read the draft", "Extract", "Create", "Remove" |
| 6 | Constraints reasoned? | FAIL | No reasoning for any constraint. E.g., "pick the most recent file by name (highest number prefix)" — no "because" explaining why newest-first. "preserving tone, line breaks, and hashtags" has no rationale |
| 7 | Numbered steps? | PASS | 5 numbered steps (lines 9-32) |
| 8 | Output formats defined? | PARTIAL | File names specified (`meta.md`, `pt-br.txt`, `en.txt`) but no format/content template for any of them. What goes in `meta.md`? Just raw frontmatter? What format for the txt files? |
| 9 | Input contract? | FAIL | No input contract. No mention of required vs optional inputs, no validation (e.g., what if no draft exists? what if frontmatter is malformed?) |
| 10 | Quality repeated at key points? | FAIL | No quality gates. Translation quality is unguarded — no instruction to verify tone fidelity, no review step before publishing |
| 11 | Anti-patterns named? | FAIL | None. E.g., should warn against publishing without reading the draft, translating idioms literally, or uploading before local save succeeds |
| 12 | Refinement step? | FAIL | No refinement or review step. Content goes straight from draft to published with no checkpoint |
| 13 | Error handling patterns? | FAIL | No error handling. What if glob returns no files? What if `gws` upload fails? What if Drive folder doesn't exist? What if draft has no frontmatter? |
| 14 | Invoked with realistic input? | N/A | Testing — cannot verify from static audit |
| 15 | Activation tested (3+ trigger phrases)? | N/A | Testing — cannot verify from static audit |
| 16 | Failure modes checked? | N/A | Testing — cannot verify from static audit |
| 17 | Subagents: context complete? | N/A | No subagents used |
| 18 | Subagents: tool access explicit? | N/A | No subagents used |
| 19 | Subagents: two-phase build? | N/A | No subagents used |
| 20 | Subagents: race conditions? | N/A | No subagents used |
| 21 | Standard layout? | PARTIAL | Has SKILL.md and README.md. No `references/` or `templates/` directory — acceptable given skill simplicity, but output file templates would benefit from a `templates/` dir |
| 22 | References one level deep? | N/A | No references directory |
| 23 | Large refs have TOC? | N/A | No references |
| 24 | Self-contained (no cross-skill deps)? | FAIL | Depends on `gws` CLI (line 28) without explaining what it is, how to install it, or what happens if it's missing. Also references `~/.brain/` paths which couples it to a specific environment |
| 25 | README generated? | PASS | README.md present with usage, how-it-works, directory structure, and installation sections |
| 26 | CLAUDE.md compliance? | PARTIAL | Follows most conventions. However, uses local paths (`~/.brain/memory/posts/`) which violates the MEMORY.md rule about no local paths in skills. Skills must be project-agnostic per CLAUDE.md |

## Score: 8/19

(Excluding 7 N/A items from the denominator: 3 testing, 4 subagent)

## Priority fixes (ordered by impact)

1. **Error handling** — Add validation for: no drafts found (empty glob), missing frontmatter in draft, `gws` CLI not installed or upload failure, Drive folder missing. Each step should fail gracefully with a clear message.
2. **Input contract** — Define required inputs (a draft must exist in `drafts/linkedin/`), optional inputs (specific draft file override), and validation rules (frontmatter must contain at minimum certain fields).
3. **Self-contained** — Remove dependency on external `gws` CLI without explanation. Either inline the upload logic, add a `references/gws-usage.md` explaining the dependency, or make Drive upload an optional step.
4. **Project-agnostic paths** — Replace hardcoded `~/.brain/memory/posts/` paths with placeholders or configurable paths. Current form violates the "project-agnostic content only" rule in CLAUDE.md.
5. **Output format templates** — Define the exact format for `meta.md`, `pt-br.txt`, and `en.txt`. Consider adding a `templates/` directory with examples.
6. **Refinement step** — Add a review checkpoint between translation and publishing (e.g., "Show the user both versions side-by-side and ask for approval before proceeding to publish").
7. **Anti-patterns** — Add warnings: don't translate idioms literally, don't publish if translation looks truncated, don't delete draft before confirming upload success.
8. **Constraint reasoning** — Add "because" clauses: why newest-first selection, why preserve line breaks in translation, why separate meta.md from content files.
