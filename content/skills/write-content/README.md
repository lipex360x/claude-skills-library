# write-content

> Create compelling written content and marketing copy that sounds authentically like you and drives action.

Combines storytelling science, conversion copywriting principles, insights from 38 product leaders, and your personal voice profile to produce LinkedIn posts, articles, marketing copy, emails, landing pages, and more. Supports iterative refinement via `r:` prefix messages.

## Usage

```text
/write-content
```

> [!TIP]
> Also activates when you say "write a post", "review this text", "polish this draft", "write copy for", "marketing copy", "headline help", "CTA copy", "value proposition", or "make this more compelling".

## How it works

1. **Load voice profile** -- Reads `~/.brain/memory/voice-profile.md` for vocabulary, rhythm, tone, and punctuation habits
2. **Clarify intent** -- Determines format, audience, goal, and tone register before writing
3. **Choose structure** -- Picks the best framework: ABT, Story Circle, Pixar's Story Spine, StoryBrand, Pyramid Principle, or Problem-Solution-Benefit
4. **Draft with voice fidelity** -- Applies your expressions, code-switching patterns, and sentence rhythm
5. **Review against checklist** -- Validates story structure, voice authenticity, hook quality, content density, and platform limits
6. **Polish without bloating** -- Tightens what exists instead of adding more
7. **Present and iterate** -- Shares the draft with key decision notes; refine with `r:` prefix messages

## Directory structure

```text
write-content/
├── SKILL.md              # Core instructions
└── references/
    ├── copy-frameworks.md      # Headline formulas, page templates
    ├── guest-insights.md       # 61 insights from 38 product leaders
    └── natural-transitions.md  # Transition phrases and AI tells to avoid
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill write-content
```
