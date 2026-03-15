# Design Spec Template

The Design Spec is a structured, self-contained reference passed verbatim to every subagent. No agent should ever need to see the original image — the spec is their single source of truth.

## Structure

```
## Design Spec — {Project Name}

### Tokens (from tokens.css)
- --color-primary: #HEXVAL (role)
- --color-dark: #HEXVAL (role)
- ... (all tokens, with var() names and hex fallbacks)

### Typography
- Font: {family name}
- Display: {size}px / {weight}
- H1: {size}px / {weight}
- ... (full scale)

### Component Patterns
- Buttons: padding, border-radius, font-weight, variants
- Cards: padding, border-radius, shadow
- ... (all patterns extracted)

### Section Layout
- Section {N}: {description}, {bg color}, {padding}
- ... (each section from the reference)

### Lorem Ipsum Rule
ALL text must be lorem ipsum. Zero original text. Zero real-language labels.
Use Latin words only: "Lorem", "Ipsum", "Dolor Sit", "Amet Consectetur", etc.
NEVER use Portuguese, English, or any real language for labels, nav items, buttons, or footer links.
```
