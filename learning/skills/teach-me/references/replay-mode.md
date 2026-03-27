# Replay Mode — File State Spec and Flow

Replay mode is triggered when the student says "replay", "repeat", "reescrever", or "quero reescrever". It supports brute-force repetition — the student re-implements something they already learned, with the instructor providing validation but reduced hints.

## Entry conditions

- The student has a completed implementation (all tests green)
- The student explicitly requests replay
- If no completed implementation exists, warn the student and suggest learn mode instead

## File state preparation

When the student triggers replay, the instructor prepares exactly three file states. The instructor handles all file management — the student never does file cleanup.

### 1. Reference file (`<Name>Final.<ext>`)

The complete working implementation, preserved as a commented-out reference.

**Rules:**
- File name: original class name + `Final` suffix (e.g., `Either.java` -> `EitherFinal.java`)
- Location: same directory as the original source file
- Content: the complete working implementation with ALL lines commented using `//`
- Class name: renamed to `<Name>Final` (e.g., `class Either` -> `class EitherFinal`)
- Purpose: the student can peek if truly stuck, but it's not runnable code

**Example:**
```java
// package com.example;
//
// import java.util.function.Function;
//
// public class EitherFinal<L, R> {
//     private final L left;
//     private final R right;
//     private final boolean isLeft;
//
//     // ... all methods commented
// }
```

### 2. Source file (`<Name>.<ext>`)

Reset to bare minimum — only the structural skeleton.

**Rules:**
- Keep: `package` declaration and empty `class` declaration
- Remove: ALL imports, generics, fields, methods, constructors
- The class must compile (empty class is valid)

**Example:**
```java
package com.example;

public class Either {
}
```

### 3. Test file

All test methods commented out, structural elements preserved.

**Rules:**
- Keep uncommented: `package`, `import` statements, class declaration, class closing brace
- Comment out: ALL `@Test` methods (including the annotation) using `//`
- Preserve method order — the student uncomments top-to-bottom
- Each test method should be visually separated for easy identification

**Example:**
```java
package com.example;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

class EitherTest {

    // @Test
    // void shouldCreateRightWithValue() {
    //     Either<String, Integer> either = Either.right(42);
    //     assertThat(either.getRight()).isEqualTo(42);
    // }

    // @Test
    // void shouldCreateLeftWithValue() {
    //     Either<String, Integer> either = Either.left("error");
    //     assertThat(either.getLeft()).isEqualTo("error");
    // }
}
```

## Replay flow

1. **Prepare files** — Create the three file states as described above
2. **Announce** — Tell the student: "Arquivos prontos. Descomente o primeiro teste e implemente."
3. **Student uncomments one test** — They pick the next commented test and uncomment it
4. **Student implements** — They write the code to make it green
5. **Student signals green** — "green", "pronto", "verde"
6. **Instructor validates** — Read the source and test files, verify correctness
7. **Review names** — Check identifiers for semantic accuracy (same as learn mode)
8. **Feedback** — If correct, brief acknowledgment + move to next. If wrong, use hint escalation but start at Level 2 (skip provoke in replay — the student already learned this)
9. **Repeat** — Go to step 3 until all tests are uncommented and green

## Reduced hints in replay

Since the student already learned the concept:
- Skip Level 1 (provoke) — they've already had that conversation
- Start at Level 2 (hint) if they get stuck
- If they need Level 4 twice on the same concept across replays, note it — this concept needs more practice
- Comprehension checks are optional in replay — use them only if the implementation suggests a gap

## Multiple replays

The student may replay the same implementation multiple times. Each replay:
- Re-prepares the three file states (fresh start)
- The reference file stays the same
- Track informally whether the student needs fewer hints each time

## Session checkpoint on replay

If the session ends mid-replay, the checkpoint file (`teach-session.md`) should note:
- Mode: replay
- Which tests were completed
- Which test is next
- Any concepts that needed Level 3+ hints (candidates for extra practice)
