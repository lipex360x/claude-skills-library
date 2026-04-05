# Claude Model Selection — Reference

Summary for model decisions in the /start-issue decomposition.

## Models Available

| Model | Input $/MTok | Output $/MTok | Context | Speed | Reasoning |
|-------|-------------|--------------|---------|-------|-----------|
| **Opus 4.6** | $5 | $25 | 1M | Moderate | Exceptional |
| **Sonnet 4.6** | $3 | $15 | 1M | Fast | Very good |
| **Haiku 4.5** | $1 | $5 | 200k | Fastest | Good |

Cost ratio: Haiku is 5x cheaper than Sonnet, Sonnet is ~2x cheaper than Opus.

## Effort Levels

| Level | Available on | Effect |
|-------|-------------|--------|
| `low` | Opus, Sonnet | Faster, less thinking |
| `medium` | Opus, Sonnet | Default |
| `high` | Opus, Sonnet | Deeper thinking |
| `max` | Opus only | Deepest, no token limit |

## Model Override

- **Skill frontmatter:** `model: sonnet`
- **Sub-agent frontmatter:** `model: haiku`
- **Agent tool parameter:** `model: "sonnet"` when spawning
- **If omitted:** inherits session model

## Anthropic Guidance

- **Opus:** Complex reasoning, agents, multi-step analysis, judgment calls
- **Sonnet:** Code generation, data analysis, content creation, agentic tool use
- **Haiku:** Real-time apps, high-volume, cost-sensitive, straightforward sub-agent tasks
