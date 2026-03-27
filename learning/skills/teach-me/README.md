# teach-me

Guided TDD teaching sessions where Claude acts as instructor. Reads student code after each step, provokes with questions instead of giving answers, and explains only when explicitly asked.

## Trigger phrases

- "teach me", "ensine-me", "quero aprender", "me ensina"
- "teach me about X", "how does X work" (in learning context)
- Any request for a guided hands-on session to learn a concept

## Modes

### Learn (default)

Full guided TDD loop:
1. Instructor gives a test description
2. Student implements (test + code)
3. Instructor reads files and validates
4. If wrong: progressive hint escalation (provoke -> hint -> partial code -> full explanation)
5. If correct: comprehension check, then next test

### Replay

Brute-force repetition for internalization:
1. Instructor prepares three file states (reference, bare source, commented tests)
2. Student uncomments one test at a time and reimplements
3. Instructor validates with reduced hints

Trigger: "replay", "repeat", "reescrever"

### Study guide (optional)

GitHub gist with phased roadmap, checkboxes, visual hints, and repetition sections. Offered early in non-trivial sessions.

## Example session flow

```
User: me ensina Either em Java
Claude: [asks scope, offers study guide gist]
Claude: "Primeiro teste: Crie Either.right(42) e verifique que o resultado e um Either contendo 42."
User: pronto
Claude: [reads files, validates, asks comprehension question]
User: [explains]
Claude: [corrects if needed, gives next test]
...
User: travei
Claude: [reads files, identifies issue, provokes with question]
User: nao sei
Claude: [gives conceptual hint]
User: ainda nao
Claude: [shows partial code with ???]
...
User: chega por hoje
Claude: [writes teach-session.md checkpoint]
```

## Installation

```bash
npx skills add lipex360x/claude-skills-library --skill teach-me
```
