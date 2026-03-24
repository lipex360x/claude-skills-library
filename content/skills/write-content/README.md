# write-content

> Help the user create compelling written content and marketing copy that sounds authentically like them and drives action.

Combines storytelling science, conversion copywriting principles, insights from 38 product leaders, and the user's personal voice profile to produce LinkedIn posts, articles, emails, landing pages, and more. Supports iterative refinement via `r:` prefix messages.

## Usage

```text
/write-content
```

> [!TIP]
> Also activates when you say "write a post", "review this text", "polish this draft", "write copy for", "improve this copy", "marketing copy", "headline help", "CTA copy", "value proposition", or "make this more compelling".

## How it works

1. **Load voice profile** — Reads the user's voice profile for vocabulary, rhythm, tone, and punctuation habits
2. **Clarify intent** — Determines format, audience, goal, and tone register before writing
3. **Choose the structure** — Picks the best framework: ABT, Story Circle, Pixar's Story Spine, StoryBrand, Pyramid Principle, or Problem-Solution-Benefit
4. **Draft with voice and precision** — Applies the user's expressions, code-switching patterns, and sentence rhythm with storytelling principles
5. **CTA copy (for marketing pages)** — Crafts strong calls-to-action using the formula: Action Verb + What They Get + Qualifier
6. **Review against checklist** — Validates story structure, voice authenticity, hook quality, content density, and platform limits
7. **Polish, don't add** — Tightens what exists instead of adding more
8. **Present and iterate** — Shares the draft with key decision notes for feedback
9. **Refinement mode (`r:`)** — Applies targeted changes from `r:` prefixed messages while re-verifying platform limits
10. **Report** — Summarizes format, draft path, checklist results, voice match confidence, and any errors

## Directory structure

```text
write-content/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── copy-frameworks.md      # Headline formulas, page templates
    ├── guest-insights.md       # 61 insights from 38 product leaders
    ├── natural-transitions.md  # Transition phrases and AI tells to avoid
    └── storytelling-science.md # Storytelling science principles
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill write-content
```
