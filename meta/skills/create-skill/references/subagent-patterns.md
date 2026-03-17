# Subagent Patterns

Practical patterns learned from building and debugging production skills that use subagents.

## The blank context problem

Subagents start with zero context. They don't inherit the parent conversation, the SKILL.md instructions, or any tool configurations. This means:

- Repeat every critical rule in the agent prompt (constraints, formatting, quality standards)
- Include all necessary context inline (specs, config, templates)
- Be explicit about which tools to use and which to avoid, with *why*
- Include quality standards — the agent won't know about them otherwise

## Foreground vs background agents

- **Foreground** (default): the user can watch each agent's tool calls in real time. Recommended when you want the user to follow progress and catch issues early.
- **Background** (`run_in_background: true`): the user sees nothing until the agent finishes. Faster perceived startup, but no visibility into what's happening.

Choose based on the user's need for visibility. If the skill produces output the user wants to watch appear progressively, use foreground.

## Two-phase build (setup → agents)

When agents depend on infrastructure being ready (files created, config populated, UI state set), split the work into two sequential phases:

**Phase A — Setup** (single response, all in parallel):
- Create project structure, files, scaffolding
- Initialize config and metadata
- Set up any required state (e.g., navigate the user to the right view)

**Phase B — Launch agents** (follow-up response, after setup completes):
- One agent per independent work unit, all in a single message

**Why sequential?** If agents run before setup completes, they race against infrastructure creation. Example: agents that write output files while the config that tracks those files hasn't been created yet — the files exist but the system doesn't know about them.

## Tool access for subagents

Subagents don't reliably inherit MCP tools from the parent process. If your skill depends on external tools:

- **Parent process:** has access to MCP tools and the full tool suite
- **Subagents:** may need alternative access methods (HTTP API, CLI commands, direct file writes)

When a backend exposes both MCP tools and an HTTP API, subagents can call the HTTP API directly — it's typically the same endpoint the MCP tool calls internally, without the intermediary.

Document this split explicitly in the SKILL.md so it's clear which tools are available where.

## Canary agent pattern

Before launching all agents, consider launching just one first to verify it follows the instructions correctly (uses the right tools, writes to the right location, produces correct output). If the canary fails, stop and diagnose before wasting N agents on the same mistake.

This is especially valuable when:
- The agent prompt is new or recently changed
- The tool access pattern is non-obvious (e.g., API call instead of direct file write)
- The output has strict formatting requirements

## Common race conditions

| Race | Cause | Fix |
|------|-------|-----|
| Agent writes before config exists | Setup and agents launched simultaneously | Two-phase build |
| Multiple agents write to same file | Shared state without coordination | Each agent owns one file exclusively |
| Agent finishes before UI is ready | Background agent completes instantly | Foreground agents, or setup includes UI navigation |
