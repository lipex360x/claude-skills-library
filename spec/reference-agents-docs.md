# Claude Code Agents — Documentation Summary

Reference document summarizing Anthropic's official agent/sub-agent system documentation for evaluating the /start-issue decomposition spec.

---

## Agent Tool Basics

The Agent tool spawns subagents that run in isolated context windows. Each agent:
- Starts with ZERO parent conversation history
- Receives only its own prompt + spawn prompt
- Returns only its final message to the parent
- Intermediate tool calls are hidden from parent

## Subagent Types

| Type | Use case |
|------|----------|
| `general-purpose` | Ad-hoc exploration, research, verification |
| `Explore` | Codebase discovery, file searches |
| `Plan` | Architecture analysis, implementation planning |
| Custom (`.claude/agents/`) | Project-specific specialized agents |

## Spawning Modes

### Foreground (default)
- Parent blocks until subagent completes
- Result appears in conversation flow
- Token cost: included in session

### Background (`run_in_background: true`)
- Parent continues immediately
- Notification on completion
- Token cost: separate billing

## Agent Isolation

### Context isolation
- No parent history
- No other agents' findings
- Only: own prompt + project CLAUDE.md + spawn prompt

### Worktree isolation (`isolation: worktree`)
- Own git worktree with separate files
- Prevents file conflicts in parallel execution
- Auto-cleaned after completion

## Context Loading Order

1. Agent's own system prompt
2. Project CLAUDE.md
3. Skills (if listed)
4. MCP servers
5. **Spawn prompt** (critical — all task-specific context goes here)

## Agent Communication

### Subagents
- **One-way only**: subagent → parent (final result)
- No inter-agent messaging
- Parent must relay findings between agents

### Agent Teams (experimental, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)
- **Bidirectional** peer messaging via SendMessage
- Shared task list with file-locking
- Lead creates team, spawns teammates
- Each teammate = independent full Claude session

## Agent Teams vs Subagents

| Aspect | Subagents | Agent Teams |
|--------|-----------|-------------|
| Communication | One-way (result only) | Bidirectional peer |
| Context | Fresh, isolated | Independent per teammate |
| Coordination | Parent manages | Shared task list |
| Token cost | Moderate | High (N× session cost) |
| Use case | Focused subtasks | Complex parallel work |

## Agent Teams Details

- **Task list**: shared, file-locked, dependency-aware
- **Self-claim**: teammates pick next unassigned unblocked task
- **Plan mode**: require approval before implementation
- **Shutdown**: graceful — teammates finish current work
- **Max**: one team per session, no nesting
- **Cost**: ~3x for 3 teammates, ~7x in plan mode

## Briefing Best Practices

### What works
- Explicit scope ("review src/auth/ for JWT issues")
- Include constraints ("don't modify schema")
- Provide examples of expected output
- Repeat prior findings in spawn prompt
- One focused brief per agent

### Anti-patterns
- Relying on conversation history (agent doesn't see it)
- Vague descriptions ("helper agent")
- Over-constraining tools (empty tools list)
- Lengthy spawn prompts with irrelevant context
- Expecting agent teams for sequential work

## Token Optimization

1. **Reduce spawn prompt size** — only essential info
2. **Use cheaper models** for focused tasks (sonnet/haiku)
3. **Delegate verbose ops** — spawn agent to grep, not read entire log
4. **Right-size teams** — 3-4 teammates max
5. **Move static context to skills** — on-demand loading

## Key Limitations

### Subagents
- Cannot spawn their own subagents (no nesting)
- Cannot initiate contact with parent
- Cannot access parent conversation history
- Cannot know about other subagents without explicit briefing

### Agent Teams
- No nesting (teammates can't spawn teams)
- One team per session
- Can't resume in-process teammates
- Permissions set at spawn time
- Lead is fixed
- Task status can lag

## Claude Agent SDK

Programmatic access to the same patterns:

### AgentDefinition fields
| Field | Description |
|-------|-------------|
| `description` | When to invoke |
| `prompt` | System prompt |
| `tools` | Allowed tools |
| `model` | Model override |
| `skills` | Available skills |
| `mcpServers` | MCP servers |

### Permission modes
- `default` — ask for everything
- `acceptEdits` — auto-approve file edits
- `acceptAll` — auto-approve everything
- `plan` — read-only analysis

### Key patterns
- Sessions can be resumed via session ID
- Hooks via callback functions (Python/TS)
- Streaming messages (ToolUse, ToolResult, final result)

## Design Decision Matrix

| Task | Pattern |
|------|---------|
| Research, exploration | General-purpose subagent |
| Focused subtask | Custom subagent |
| Parallel independent tasks | Subagent worktrees |
| Complex multi-step coordination | Agent teams |
| Sequential workflow | Subagent handoff |
| Production automation | SDK agents |
