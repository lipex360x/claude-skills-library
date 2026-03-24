---
name: extract-design-system
description: >-
  Analyze a design image and create a full design system project with separated
  artboards (foundations, components, sections) via MCP tools. Use this skill
  whenever the user provides a reference image, screenshot, or mockup and wants
  to extract a design system, create artboards, build a component library, or
  reverse-engineer visual patterns from an existing design — even if they don't
  explicitly say "design system."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Agent
  - AskUserQuestion
  - TaskCreate
argument-hint: "[project-slug]"
---

# Extract Design System

Extract a design system from a reference image and create a complete project with separated artboards. The user stays on the project hub throughout — thumbnails appear progressively as each agent completes its artboard.

## Input contract

<input_contract>

| Input | Source | Required | Validation | On invalid |
|-------|--------|----------|------------|------------|
| `project-slug` | $ARGUMENTS | no | Lowercase + hyphens string | Infer from image filename or AUQ |
| Reference image(s) | `design/` folder | yes | PNG, JPG, or WebP files exist | "No reference images found in `design/`. Place at least one image and try again." — stop |

</input_contract>

## Output contract

<output_contract>

| Artifact | Path | Persists | Format |
|----------|------|----------|--------|
| Design tokens | `<project>/tokens.css` | yes | CSS custom properties |
| Artboard HTML files | `<project>/*.html` | yes | HTML (one per artboard) |
| Project manifest | `<project>/manifest.json` | yes | JSON (created by `create_artboards`) |
| Report | stdout | no | Markdown summary |

</output_contract>

## External state

<external_state>

| Resource | Path | Access | Format |
|----------|------|--------|--------|
| Reference images | `design/**/*.{png,jpg,jpeg,webp}` | R | Image files |
| MCP design server | Local dev server | R/W | HTTP API + WebSocket |
| Browser | System | R/W | Project hub view |

</external_state>

## Pre-flight

<pre_flight>

1. MCP tools available (`create_project`, `navigate`, `create_artboards`, `get_screenshot`) → if any missing: "MCP tool `{name}` not available. Configure the design system server." — stop.
2. Reference images exist in `design/` folder → `Glob: design/**/*.{png,jpg,jpeg,webp}` → if none: "No reference images found in `design/`." — stop.
3. Project slug determined → from $ARGUMENTS, image filename, or AUQ — must resolve before proceeding.

</pre_flight>

## Steps

### 1. Discover and analyze reference image

Read all images found in `design/`. Analyze as a **design reference** — reverse-engineer the visual language, not clone the content.

Extract: color palette (exact hex), typography (families, weight scale, size hierarchy), spacing rhythm, components (buttons, cards, badges, nav, forms), sections, and a one-sentence visual direction.

### 2. Plan artboards

Read `references/artboard-guidelines.md` for the standard artboard structure and per-artboard content guidelines. Typical split: Foundations, Components, Hero & Navigation, Content Sections, Footer & CTA. Aim for 3–6 artboards depending on reference complexity.

### 3. Present Design Brief

Write a **Design Brief** with:
- All extracted design tokens
- Artboard plan — table with artboard name, file, content, and agent count
- Total agent count summary (e.g., "5 artboards, 5 agents in parallel")

**Gate: user must approve before proceeding.** Use `AskUserQuestion` with approve/adjust options.

### 4. Build Design Spec

After approval, compile a **Design Spec** — structured, self-contained reference for subagents. Read `templates/design-spec.md` for the template. The spec is passed verbatim to every agent prompt so they can write HTML immediately without re-analyzing the image.

### 5. Setup and launch agents

The build is a **two-phase sequence.** Setup must complete before agents start.

#### Phase A — Setup (single response, all in parallel)

- `create_project` — create the project
- Write `tokens.css` from extracted design tokens
- `navigate` — open the project hub
- `create_artboards` — batch create with skeleton HTML (shimmer cards appear)

Wait for all setup calls to complete.

#### Phase B — Launch agents (follow-up response)

One Agent per artboard, all in a **single message** (foreground). Each receives the Design Spec and writes via `curl` to the HTTP API. Read `references/agent-prompt.md` for prompt requirements, curl template, and quality standards.

Create one TaskCreate per artboard for progress tracking.

**Error handling for this step:**
- If `create_project` or `create_artboards` fails in Phase A → stop and report — do not launch agents against broken setup.
- If an agent fails in Phase B (curl error, crash, timeout) → report which artboard failed. User can re-run individual agents without restarting the whole build.

### 6. Final verification

After all agents complete:
1. All thumbnails should be visible on the hub.
2. Take screenshot via `get_screenshot()` and present to the user.

### 7. Refinement

Ask the user if any artboard needs adjustments. Use `AskUserQuestion` with options `["Looks good — done", "Adjust an artboard"]`. If changes needed, re-launch only the affected agent(s). Repeat until approved.

### 8. Report

<report>

Present concisely:
- **Project created:** slug, artboard count, token count
- **Design tokens:** color palette summary, typography, spacing rhythm
- **Artboards completed:** list with status (success/failed)
- **Audit results:** self-audit + content audit summary
- **Errors:** issues encountered and how they were handled (or "none")

</report>

## Next action

Review individual artboards in the editor for fine-tuning. Run `/push` if working inside a git repo.

## Self-audit

<self_audit>

Before presenting the Report, verify:

1. **Pre-flight passed?** — MCP tools available, reference images found, project slug resolved
2. **Steps completed?** — list any skipped steps with reason
3. **Output exists?** — `tokens.css` written, all artboard HTML files created, manifest populated
4. **Anti-patterns clean?** — lorem ipsum used (not real content), agents used `curl` (not Write), batch creation used (not one-by-one)
5. **Approval gates honored?** — Design Brief approved by user before Phase A setup

If any check fails, note it in the Report.

</self_audit>

## Content audit

<content_audit>

Before finalizing output, verify:

1. **Design tokens accurate?** — extracted hex colors match the reference image exactly. Typography families, weights, and size hierarchy reflect the original design.
2. **Artboard completeness?** — each artboard contains the components listed in the Design Brief. No empty sections, no missing elements from the plan.
3. **Visual consistency?** — all artboards use `var()` references to `tokens.css`. No hardcoded colors or font values in artboard HTML.
4. **Component extraction quality?** — buttons, cards, badges, nav, forms reflect the reference patterns. Spacing rhythm is consistent across artboards.
5. **Lorem ipsum compliance?** — all text content uses Latin placeholder text, not real content from the reference — because the goal is extracting the design system, not the content.

</content_audit>

## Error handling

| Failure | Strategy |
|---------|----------|
| MCP tool missing | Report which tool and server needed — stop |
| No reference images | Report: "No images in `design/`" — stop |
| `create_project` fails | Report error details — stop (do not launch agents) |
| `create_artboards` fails | Report error details — stop (do not launch agents) |
| Agent fails (curl error) | Report which artboard failed — user can re-run individually |
| `get_screenshot()` fails | Skip screenshot, report manually — continue |
| All agents fail | Report setup state, suggest MCP server restart — stop |

## Anti-patterns

- **Navigating away from the hub.** The user watches thumbnails appear progressively — because navigating to the editor breaks the visual feedback loop during the build.
- **Agents using Write tool instead of curl.** Write doesn't notify the browser — because no thumbnail update, robot keeps blinking, and the user sees no progress.
- **One-by-one artboard creation.** Use `create_artboards` for batch creation — because one MCP call shows all shimmer cards at once, giving immediate visual feedback.
- **Launching agents before setup completes.** Agents race against `create_artboards` — because they write to a manifest that doesn't exist yet, producing empty results.
- **Using real content instead of lorem ipsum.** The goal is extracting the design system, not content — because real language distracts reviewers from evaluating visual patterns.
- **Emojis in designs.** Use SVG or Unicode symbols for icons — because emojis render inconsistently across platforms and break visual coherence.
- **Hardcoded colors in artboard HTML.** Use `var()` references to `tokens.css` — because hardcoded values drift from the design system and make updates impossible.

## Guidelines

- **Lorem ipsum for all text.** The goal is extracting the design system, not the content. Real language distracts from visual pattern evaluation. Repeat this in every agent prompt — because agents don't inherit parent context.

- **Stay on the hub during builds.** The user watches thumbnails appear progressively. This is the primary feedback mechanism — because it shows real-time progress without requiring the user to check individual artboards.

- **Agents write via curl to HTTP API.** `POST /api/write-artboard` writes the file and notifies the browser in one call. MCP tools are not available to subagents — because subagents don't reliably inherit MCP tools from the parent process.

- **Batch creation via `create_artboards`.** One MCP call, not one per artboard — because this shows all shimmer cards at once and sets up the manifest atomically.

- **tokens.css is the single source of truth.** Define CSS variables from the extracted palette, then reference `var()` in all artboard HTML — because consistency across artboards built by different agents depends on a shared token file.

- **Two-phase build sequence.** Setup (Phase A) must complete before agents (Phase B) — because `create_artboards` populates the manifest that agents depend on.
