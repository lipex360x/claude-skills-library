# write-content

> Help the user create compelling written content and marketing copy that sounds authentically like them and drives action.

Full content creation pipeline powered by the user's voice profile, 6 narrative frameworks (ABT, Story Circle, Pixar's Story Spine, StoryBrand, Pyramid Principle, Problem-Solution-Benefit), and 61 insights from 38 product leaders. Covers LinkedIn posts, articles, emails, landing pages, taglines, and headlines. Enforces a 210-character hook gate, platform-specific character limits via `wc -c`, and iterative refinement through a `r:` prefix mode that tightens existing prose instead of adding more.

## Usage

```text
/write-content
```

> [!TIP]
> Also activates when you say "write a post", "review this text", "polish this draft", "write copy for", "improve this copy", "marketing copy", "headline help", "CTA copy", "value proposition", or "make this more compelling".

### Examples

```text
/write-content                  # start an interactive session to define format, audience, and goal
r: make the hook more contrarian # refine the last draft without restarting
r: cut 200 characters           # tighten for LinkedIn limits
```

## How it works

1. **Load voice profile** — Reads the user's voice profile for vocabulary, rhythm, tone, and punctuation habits
2. **Clarify intent** — Determines format (post, article, email, landing-page, tagline, headline), audience, goal, and tone register. For marketing copy, also gathers page-type, primary-action, and problem
3. **Choose the structure** — Picks the best narrative framework: ABT for universal tension, Story Circle for narratives, StoryBrand when the reader is the hero, Pyramid Principle for business writing, or Problem-Solution-Benefit for marketing
4. **Draft with voice and precision** — Applies the user's actual expressions, code-switching patterns, and sentence rhythm. Hook must create tension or curiosity in the first 210 characters
5. **CTA copy (for marketing pages)** — Crafts strong calls-to-action using the formula: Action Verb + What They Get + Qualifier
6. **Review against checklist** — Validates story structure, voice authenticity, hook quality, content density, platform limits, and copywriting quality
7. **Polish, don't add** — Tightens what exists: stronger verbs, cut filler, remove redundant stats
8. **Present and iterate** — Shares the draft with key decision notes for feedback
9. **Refinement mode (`r:`)** — Applies targeted changes from `r:` prefixed messages while re-verifying platform limits and flagging principle conflicts
10. **Report** — Summarizes format, draft path, character count, checklist results, voice match confidence, and any errors

[↑ Back to top](#write-content)

## Directory structure

```text
write-content/
├── SKILL.md              # Core skill instructions
├── README.md             # This file
├── skill-meta.json       # Skill metadata
└── references/
    ├── copy-frameworks.md      # Headline formulas, page structure templates, CTA patterns
    ├── guest-insights.md       # 61 insights from 38 product leaders on content quality
    ├── natural-transitions.md  # Transition phrase libraries and AI tells to avoid
    └── storytelling-science.md # Neuroscience behind narrative patterns (dopamine, Zeigarnik, peak-end)
```

[↑ Back to top](#write-content)

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill write-content
```
