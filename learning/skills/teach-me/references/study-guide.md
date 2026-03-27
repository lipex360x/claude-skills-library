# Study Guide — Gist Creation Guidelines

When the teaching topic is non-trivial, offer to create a GitHub gist as a structured study guide. This gives the student a roadmap, progress tracking, and a persistent reference.

## When to offer

- After understanding the scope (Step 1 of the teaching loop)
- When the topic has 3+ distinct concepts or phases
- Ask: "Quer que eu crie um guia de estudo como gist? Se tiver um gist de referencia pro estilo, manda o link."

## Style matching

Before writing the guide, ask if the student has an existing gist or document to use as a style reference. If provided:

1. Fetch the reference gist via `gh gist view <id>`
2. Analyze formatting patterns: section structure, emoji usage, table vs list preference, collapsible sections, navigation links
3. Match the discovered style in the new guide

If no reference is provided, use the default GFM style described below.

## Structure

### Header

```markdown
# [Topic] — Guia de Estudo

> [One-line description of what the student will learn]

## Sumario

- [Fase 1 — Name](#fase-1--name)
- [Fase 2 — Name](#fase-2--name)
- ...
- [Tabela de conceitos](#tabela-de-conceitos)
- [Referencias](#referencias)
```

### Phases

Organize in phases of increasing difficulty. **Always start with the old/known pattern** so the student feels the pain before learning the solution.

```markdown
## Fase 1 — [Name]

> [One-line goal for this phase]

- [ ] Task 1 description
- [ ] Task 2 description
- [ ] Task 3 description

<details>
<summary>Testes desta fase</summary>

- `shouldDoX`
- `shouldDoY`
- `shouldDoZ`

</details>

<details>
<summary>Dica visual</summary>

[ASCII diagram, side-by-side comparison, or conceptual illustration]
[NEVER a direct answer — always a visual that helps the student reason]

</details>

[Voltar ao sumario](#sumario)
```

### Repetition sections

After key phases (typically after phases that introduce core concepts), add a repetition section:

```markdown
### Repeticao — Fase [N]

Reescreva a implementacao da Fase [N] do zero. Use `/teach-me replay` para preparar os arquivos.

- [ ] Reescrita 1
- [ ] Reescrita 2 (sem olhar a referencia)
```

### Concepts table

At the end, a summary table mapping concepts to phases:

```markdown
## Tabela de conceitos

| Conceito | Fase | Resumo |
|----------|------|--------|
| Either monad | 2 | Container que representa sucesso (Right) ou falha (Left) |
| map | 3 | Transforma o valor Right sem desembrulhar |
| flatMap | 4 | Transforma o valor Right, funcao retorna Either |
```

### References section

```markdown
## Referencias

- [Link 1 — Description](url)
- [Link 2 — Description](url)
```

## GFM formatting rules

- Use `<details><summary>` for all hints and test lists — never expose them directly
- Visual tips use ASCII diagrams or side-by-side code comparisons, never direct answers
- Tables for structured data (concept mappings, endpoint lists, type comparisons)
- Back-to-top links (`[Voltar ao sumario](#sumario)`) after every phase
- Checkboxes (`- [ ]`) for every actionable task
- Emoji in section headers only if the student's reference style uses them

## Gist creation

Use `gh` CLI to create the gist:

```bash
gh gist create --public --desc "[Topic] — Guia de Estudo" guide.md
```

Or private if the student prefers:

```bash
gh gist create --desc "[Topic] — Guia de Estudo" guide.md
```

After creation, share the URL with the student and update it as the session progresses (using `gh gist edit`).

## Updating during session

As the student completes phases, offer to check off items in the gist. Use `gh gist edit <id>` to update checkboxes from `- [ ]` to `- [x]`.

## Anti-patterns for study guides

- **Direct answers in hints** — hints should be visual/conceptual, never code solutions
- **Generic structure** — always match the student's documentation style
- **Too many phases** — keep it to 5-8 phases max; split larger topics into separate guides
- **No repetition sections** — key concepts need replay opportunities built into the guide
- **Flat structure** — use collapsible sections to keep the guide scannable
