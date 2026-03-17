# Dependency Categories

When analyzing module coupling, classify dependencies into one of four categories. The category determines the right refactoring strategy.

## 1. Internal — hide behind the interface

Dependencies that are implementation details. Callers don't know or care about them.

**Signal:** The dependency is only used inside the module, never exposed in the interface.

**Strategy:** Encapsulate completely. The deep module owns the dependency — callers never see it.

```typescript
// Caller sees: createUser(data) → User
// Hidden: bcrypt, uuid generation, validation logic
```

## 2. Injected — pass in from outside

Dependencies that vary by context (testing, environments, configurations).

**Signal:** The dependency needs to be swapped for tests, or different callers need different implementations.

**Strategy:** Accept via constructor/factory parameter. Define an interface the module depends on, let callers provide the implementation.

```typescript
// Module defines what it needs:
interface PaymentClient {
  charge(amount: number): Promise<Receipt>;
}

// Callers inject the real or test implementation:
const service = createOrderService({ payment: stripeClient });
const testService = createOrderService({ payment: mockPayment });
```

## 3. Shared — extract to a common layer

Dependencies used by multiple modules that should agree on the same abstraction.

**Signal:** Two or more modules import the same types, share the same data structures, or duplicate the same logic.

**Strategy:** Extract to a shared layer (types package, common module). Both modules depend on the shared abstraction, not on each other.

```typescript
// Shared: types/order.ts defines Order, LineItem
// Module A (pricing) imports Order
// Module B (fulfillment) imports Order
// Neither imports the other
```

## 4. Cross-boundary — adapter pattern

Dependencies that cross system boundaries (external APIs, databases, file systems, message queues).

**Signal:** The dependency is external to your codebase. It has its own release cycle, API changes, and failure modes.

**Strategy:** Wrap in an adapter that translates between the external interface and your domain. The adapter is the only place that knows about the external system's specifics.

```typescript
// Adapter hides Stripe-specific details:
class StripePaymentAdapter implements PaymentClient {
  charge(amount: number): Promise<Receipt> {
    const stripeResult = await this.stripe.paymentIntents.create({...});
    return this.toReceipt(stripeResult); // translate to domain type
  }
}
```

## Choosing the right category

| Question | If yes → |
|----------|----------|
| Does the caller ever need to know about this? | Not Internal |
| Does it need to be swapped for tests? | Injected |
| Do multiple modules need the same thing? | Shared |
| Does it cross a system boundary? | Cross-boundary |

A single dependency can be both Cross-boundary AND Injected (e.g., a database adapter that gets injected for testability). Categories are not mutually exclusive — choose the primary one based on what drives the design decision.
