<div align="center">

# Written

*Compelling content and persuasive copy that sounds like you wrote it*

[![Claude Code](https://img.shields.io/badge/Claude_Code-skill-7c3aed?style=flat-square)](https://github.com/lipex360x/claude-skills-library)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](../../LICENSE)

[How It Works](#how-it-works) • [What It Covers](#what-it-covers) • [References](#references) • [Installation](#installation)

</div>

A Claude Code skill for writing content that sounds authentically human — not like AI. Combines storytelling science, conversion copywriting principles, insights from 38 product leaders, and your personal voice profile to produce LinkedIn posts, articles, marketing copy, emails, landing pages, and more.

## How It Works

1. **Loads your voice profile** from `~/.brain/memory/voice-profile.md` — vocabulary, rhythm, tone, punctuation habits
2. **Clarifies intent** — format, audience, goal, and tone register before writing anything
3. **Picks a structure** — ABT, Story Circle, Pixar's Story Spine, StoryBrand, Pyramid Principle, or Problem-Solution-Benefit
4. **Drafts with voice fidelity** — applies your expressions, code-switching patterns, and sentence rhythm
5. **Reviews against a checklist** — story structure, voice authenticity, hook quality, content density, platform limits
6. **Polishes without bloating** — tightens what exists instead of adding more

Supports iterative refinement via `r:` prefix messages.

## What It Covers

| Content Type | Details |
|---|---|
| **Social media** | LinkedIn posts (hook optimization for 210-char truncation, hashtag strategy, engagement-first CTAs) |
| **Long-form** | Articles, memos, business writing (Pyramid Principle, causal chains over lists) |
| **Marketing copy** | Landing pages, hero sections, headlines, CTAs, value propositions, taglines |
| **Short-form** | Emails, announcements, micro-copy |

### Storytelling Frameworks

| Framework | Best For |
|---|---|
| ABT (And, But, Therefore) | Universal backbone — forces narrative tension into any piece |
| Story Circle | Narrative posts — simplified hero's journey |
| Pixar's Story Spine | Storytelling with causal chains |
| StoryBrand | Reader-as-hero positioning |
| Pyramid Principle | Business writing — conclusion first |
| Problem-Solution-Benefit | Marketing copy and conversion pages |

### Built-in Guardrails

The skill actively prevents common AI writing anti-patterns:

- "I'm thrilled to share..." and other AI tells
- Generic hooks ("Have you ever wondered...?")
- Hero/guru positioning instead of guide/builder
- Motivational fluff and vague superlatives
- Topic jumps without transitions
- Post-climax appendix that weakens endings

## References

The `references/` directory contains supporting material loaded on-demand:

| File | Contents |
|---|---|
| `copy-frameworks.md` | Headline formulas, page section types, landing page templates |
| `guest-insights.md` | 61 insights from 38 product leaders (Wes Kao, Julie Zhuo, Claude Hopkins, and others) |
| `natural-transitions.md` | Transition phrase libraries and AI tells to avoid |

## Installation

```bash
npx claude-skills install written -a claude-code
```

> [!IMPORTANT]
> This skill requires a voice profile at `~/.brain/memory/voice-profile.md`. Without it, the skill still works but produces generic-sounding output. Run the [myvoice](../myvoice) skill first to generate your profile.
</div>
