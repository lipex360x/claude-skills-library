# TDD Methodology

Test-Driven Development is a non-negotiable default for every step that introduces new behavior. This reference covers the philosophy, workflow, and anti-patterns.

## Table of contents

- [Core principle](#core-principle)
- [Vertical slices — the only correct approach](#vertical-slices)
- [Good vs bad tests](#good-vs-bad-tests)
- [When to mock](#when-to-mock)
- [Deep modules](#deep-modules)
- [Interface design for testability](#interface-design-for-testability)
- [Refactor candidates](#refactor-candidates)
- [Checklist per cycle](#checklist-per-cycle)

## Core principle

Tests verify **behavior through public interfaces**, not implementation details. Code can change entirely; tests shouldn't break. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed.

## Vertical slices

**The only correct approach is vertical slices.** One test → one implementation → repeat. Each test responds to what you learned from the previous cycle.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

**Why horizontal slices produce bad tests:**
- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

## Good vs bad tests

### Good tests

Integration-style: test through real interfaces, not mocks of internal parts.

```typescript
// GOOD: Tests observable behavior through public interface
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});

// GOOD: Verifies through the same interface users use
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

Characteristics:
- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

### Bad tests

```typescript
// BAD: Tests implementation details — mocking internal collaborators
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});

// BAD: Bypasses interface to verify via database
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});
```

Red flags:
- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through external means instead of interface

## When to mock

Mock at **system boundaries** only:

| Mock | Don't mock |
|------|-----------|
| External APIs (payment, email) | Your own classes/modules |
| Databases (prefer test DB when possible) | Internal collaborators |
| Time/randomness | Anything you control |
| File system (sometimes) | |

### Design for mockability at boundaries

**Use dependency injection** — pass external dependencies in:

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock — creates dependency internally
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**Prefer SDK-style interfaces** — specific functions per operation:

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

## Deep modules

From "A Philosophy of Software Design" (Ousterhout):

**Deep module** = small interface + large implementation (good)
**Shallow module** = large interface + thin implementation (avoid)

When designing interfaces, ask:
- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

Deep modules are more testable because the interface is simple — fewer tests needed, each test exercises more real logic.

## Interface design for testability

1. **Accept dependencies, don't create them** (dependency injection)
2. **Return results, don't produce side effects** — pure functions are trivially testable
3. **Small surface area** — fewer methods = fewer tests needed, fewer params = simpler test setup

## Refactor candidates

After TDD cycle, look for:
- **Duplication** → extract function/class
- **Long methods** → break into private helpers (keep tests on public interface)
- **Shallow modules** → combine or deepen
- **Feature envy** → move logic to where data lives
- **Primitive obsession** → introduce value objects
- **Existing code** the new code reveals as problematic

**Never refactor while RED.** Get to GREEN first, then refactor with confidence.

## Checklist per cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

## Applying TDD in issue planning

When creating steps/checkboxes for issues:

1. **Every step with new behavior must have test checkbox BEFORE implementation checkbox.** This is not a suggestion — it's the default order.
2. **"You can't test everything."** Focus testing effort on critical paths and complex logic. Confirm with the user which behaviors matter most.
3. **Test isolation is mandatory.** Tests never touch production data. Docker-compose for test environment, `.env.test` for local URLs, runtime safety guard to abort if pointing at production.
4. **"Full test" = unit + lint + E2E.** Never say just "run tests" — expand to all layers.
