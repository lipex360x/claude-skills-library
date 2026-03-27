# Hint Escalation — 4-Level Progressive System

When a student gets stuck, never jump to the answer. Escalate through these four levels in order. Advance to the next level **only** when the student explicitly signals they are still stuck ("nao sei", "travei", "nada", "still stuck").

## Level 1 — Provoke (question)

Ask a question that points at the issue without naming it. Force the student to look at their own code from a new angle.

**Goal:** Student discovers the problem themselves.

**Examples:**
- "O que acontece se alguem passar `null` pra esse metodo?"
- "Qual o tipo de retorno do `fn.apply(value)`? E qual o tipo de retorno do `flatMap`?"
- "Se `map` retorna um `Either`, e `flatMap` tambem retorna um `Either`... qual a diferenca no que `fn` retorna?"

**When it works:** Student has the knowledge but hasn't connected it yet. The question triggers the insight.

**When to skip:** Never skip this level. Even if the concept is brand new, a provocation reveals what the student does and doesn't know.

## Level 2 — Hint (conceptual nudge, no code)

Give a directional hint using concepts and words, not code. Name the area where the problem lives without showing the fix.

**Goal:** Student knows where to look and what concept to apply.

**Examples:**
- "Voce precisa de uma forma de verificar se e Left ou Right antes de aplicar a funcao."
- "Pense no tipo generico — o `R` do `Either<L, R>` precisa mudar quando voce aplica `map`."
- "A diferenca entre `map` e `flatMap` esta no que a funcao retorna — um valor puro ou um valor ja embrulhado."

**When it works:** Student understands the concepts but can't see how they connect to the current problem.

## Level 3 — Partial code (structure with `???`)

Show the code structure with `???` placeholders where the student must fill in. Never show more than the minimum structure needed.

**Goal:** Student sees the shape of the solution and fills in the logic.

**Examples:**
```java
public <U> Either<L, U> map(Function<R, U> fn) {
    if (???) {
        return ???;
    }
    return Either.right(???);
}
```

```java
public <U> Either<L, U> flatMap(Function<R, ???> fn) {
    // ...
}
```

**Rules:**
- Use `???` consistently — never `___`, `TODO`, or natural language placeholders
- Show only the method/block in question, not the entire class
- Include the method signature (the student needs the types to reason about the body)
- If the student fills `???` wrong, drop back to Level 1 for that specific gap

## Level 4 — Full explanation (complete code with reasoning)

Show the complete working code with line-by-line reasoning. This is the last resort — the student explicitly asked for the answer.

**Goal:** Student understands the complete solution and the reasoning behind each part.

**Format:**
```java
public <U> Either<L, U> map(Function<R, U> fn) {
    if (this.isLeft()) {           // Left values pass through unchanged
        return (Either<L, U>) this; // safe cast — L type is same, R is unused
    }
    return Either.right(fn.apply(this.value)); // apply fn to Right value, wrap result
}
```

**Rules:**
- After showing the full explanation, ask the student to explain it back in their own words
- If their explanation has gaps, correct those specific gaps — don't repeat the whole explanation
- Then move to the next test prompt to apply the concept

## Escalation reset

The escalation level resets to Level 1 for each new concept or test prompt. A student who needed Level 4 for `map` might only need Level 1 for `flatMap` — because they now have the pattern.

## Tracking

Do not track escalation levels between sessions. Within a session, remember the current level per concept so you don't repeat a level the student already saw.
