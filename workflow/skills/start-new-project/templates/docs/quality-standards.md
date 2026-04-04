# Quality Standards — Reference Template

Complete reference for generating `quality.md` in new projects. Adapt every rule and code example to the project's specific stack (language, framework, patterns). Remove sections that don't apply (e.g., no Frontend section for CLI projects, no database rules for static sites).

**How to use:** Read this entire file. Then generate `quality.md` at the project root, translating each rule and pattern to the project's actual languages and frameworks. The output must contain concrete code examples — not placeholders.

---

# Code Quality Standards

Non-negotiable rules for [project name]. Read this before writing any code.

---

# Shared (all layers)

## DON'Ts

1. **DON'T use magic numbers.** No raw `0.1`, `2.5`, `24 * 60 * 60 * 1000` in logic. Every number gets a named constant.
2. **DON'T nest if/else.** No `if { if { else { if } } }`. Use fail-first (early return) or switch/match/case.
3. **DON'T use single-letter variables.** No `const v = n`, no `r = result`. Every variable describes what it holds.
4. **DON'T skip type-check.** `tsc --noEmit` (TypeScript), `mypy` (Python), or equivalent must pass before push.
5. **DON'T write unnecessary comments.** Code must be self-explanatory. Only comment genuinely non-obvious logic. No `// Register user` above `registerUser()`.
6. **DON'T use deprecated APIs.** Check for deprecation warnings. Fix immediately.
7. **DON'T mask errors with fallbacks.** No `process.env.X ?? ""` or `os.environ.get("X", "")` — if the variable is missing, fail loudly. Use Zod (TS) or Pydantic Settings (Python) for env validation.
8. **DON'T blanket-disable linter rules per directory.** Use inline disable with a justification comment on the specific line.
9. **DON'T use workarounds.** No hardcoded values to bypass bugs, no temporary flags, no monkey-patches, no skipped validations, no `# type: ignore`, no `as any`. Fix the root cause or flag it as a blocker.
10. **DON'T write horizontal TDD.** No "write all tests first, then implement all". One test, one implementation, repeat.
11. **DON'T pre-install dependencies.** Install at the moment of first use — not in advance "for later steps". Unused deps pollute the lockfile and require `ignoreDependencies` workarounds.
12. **DON'T create files before they're consumed.** No `env.ts`, `browser.ts`, or helper files "for later". Create at the moment of first import — same principle as dependencies.
13. **DON'T use `sed` on GitHub issue bodies.** A malformed pattern silently writes empty string and `gh issue edit` applies it without warning — destroying the entire issue content irrecoverably. Use `gh api` with GraphQL mutations or a script that parses, validates, and writes safely.

## DOs

1. **DO use fail-first pattern.** Guard clauses at the top, happy path at the bottom.
2. **DO use switch/match/case for value-based branching.** When branching on a finite set, switch/match is clearer than if/else chains.
3. **DO use named constants.** `MAX_RETRY_ATTEMPTS`, `DEFAULT_PAGE_SIZE`, `MILLISECONDS_PER_DAY`.
4. **DO use semantic variable names.** `discountRate`, `remainingBalance`, `expiresAt`. Names describe the value, not the type.
5. **DO use vertical TDD.** RED, GREEN, REFACTOR — one behavior at a time.
6. **DO isolate test data by prefix.** Each test file uses unique prefixes. Cleanup targets only its own data.
7. **DO pin dependency versions across workspaces.** Same version everywhere. Mismatched versions cause type incompatibilities.
8. **DO use path aliases.** `@/` maps to `src/`. Configured in `tsconfig.json` (TS) or equivalent.
9. **DO validate all env vars at startup.** Fail-fast with structured error messages. No raw `process.env` or `os.environ` in production code.

---

# Backend

> Adapt this section to the project's backend language and framework. Examples below show both TypeScript (Hono/Express) and Python (FastAPI) — use whichever matches the project.

## DON'Ts

1. **DON'T use anemic entities.** No plain interfaces/types/dicts pretending to be domain objects. No standalone functions operating on raw data.
2. **DON'T use raw primitives for domain concepts.** No bare `string`/`str` for email, currency, status. Wrap in value objects.
3. **DON'T raise/throw exceptions for business logic.** Use the Result/Either pattern — `Ok(value)` / `Err(error)`. Exceptions reserved for infrastructure failures only.
4. **DON'T write N+1 queries.** No loops doing DB queries per item. Use JOINs, batch operations, or eager loading.
5. **DON'T use top-level singletons.** No `const db = createDb()` or `db = create_engine()` at module scope. Use lazy factories (`getDb()`, `get_db()`).
6. **DON'T use global TRUNCATE in tests.** No `TRUNCATE users CASCADE` that destroys other test files' data.
7. **DON'T mix domain logic with infrastructure.** No SQL, no HTTP, no subprocess inside domain entities.
8. **DON'T use bare catch/except.** Always catch specific exceptions. Never `except: pass` or `catch (e) {}` without re-raising or returning `Err`.
9. **DON'T use dynamic imports in route handlers.** No `await import("...")` inside request handlers. Static imports at the top.
10. **DON'T import infrastructure in services.** No `from supabase import ...` or `import { createClient } from '@supabase/supabase-js'` in the service layer. Services depend on Repository/Port interfaces. Concrete clients belong in `infra/`.
11. **DON'T couple domain to a specific provider.** No `SupabaseThread`, no `AWSUser`. Domain entities and value objects must be provider-agnostic. Provider-specific details live in the adapter that implements the port.

## DOs

1. **DO use rich domain entities.** Classes with behavior: `order.cancel()`, `thread.add_message(content)`. Immutable — methods return new instances or Result.
2. **DO use value objects for every domain concept.** Validation in the factory, immutable, single responsibility.
3. **DO use `create()` and `reconstitute()` factories.** `create()` validates input and returns `Result[T, ValidationError]`. `reconstitute()` hydrates from DB without validation.
4. **DO return Result/Either from all services.** Route handlers unwrap Result and map `Err` to HTTP status codes. Never let service errors propagate as exceptions.
5. **DO separate domain tests from integration tests.** Domain tests for entities/VOs in isolation (<10ms). Integration tests for the full HTTP stack.
6. **DO use dependency injection.** Pass external dependencies (DB client, API clients, subprocess runners) as parameters. Never create them inside service methods.
7. **DO use lazy initialization.** `getDb()`, `get_supabase()` create connections on first call, not at import time.
8. **DO use structured logging.** Silent in test, pretty in dev, JSON in prod. Logger is lazy-initialized.
9. **DO configure security from day one.** CORS (origin from env), secure headers, rate limiting, input validation via schema (Pydantic, Zod, etc.).
10. **DO use Repository interfaces for data access.** Define `Protocol`/`interface` in the domain layer (`domain/repositories/`). Implementations in `infra/<provider>/`. Services receive repositories via constructor injection.
11. **DO use Port/Adapter for external services.** Auth, storage, messaging, LLM — define a Port (`Protocol`/`interface`) with the contract, implement an Adapter per provider. Swapping providers = new adapter file, zero service changes.

---

# Frontend

> Include this section only for projects with a web frontend. Adapt to the project's frontend framework (Next.js, Vite+React, Vue, Svelte, etc.).

## DON'Ts

1. **DON'T use `useEffect` for derived state.** No `useEffect(() => setFullName(first + last), [first, last])`. Compute in render or use `useMemo`.
2. **DON'T fetch data in `useEffect`.** Use a data-fetching library (TanStack Query, SWR, or framework-native like Supabase Realtime) for all API calls.
3. **DON'T use `any` or `as any`.** Type properly or create the type.
4. **DON'T use inline styles when Tailwind classes exist.** No `style={{ marginTop: 8 }}`. Use `mt-2`.
5. **DON'T use `index` as key in dynamic lists.** Keys must be stable identifiers. Index-as-key causes state bugs on reorder/delete.
6. **DON'T put business logic in components.** Extract to custom hooks or stores. Components render UI, nothing else.
7. **DON'T prop-drill beyond 2 levels.** If a prop passes through intermediary components that don't use it, lift to state management or context.
8. **DON'T use `document.querySelector` in React.** Use `useRef` for DOM access. Direct DOM manipulation bypasses reconciliation.
9. **DON'T create god components.** No component file >200 lines or with multiple responsibilities. Split into composition.
10. **DON'T ignore loading/error states.** Every data-fetching component must handle `isLoading`, `isError`, and empty states explicitly.
11. **DON'T hardcode API URLs.** Use env vars (`NEXT_PUBLIC_API_URL`, `VITE_API_URL`). No `fetch("http://localhost:3001/...")` in production code.
12. **DON'T use relative parent imports.** No `from "../../lib/db"`. Use path aliases: `from "@/lib/db"`.
13. **DON'T use `suppressHydrationWarning` as a fix.** Solve the hydration mismatch at the root cause.

## DOs

1. **DO use server components by default** (Next.js/RSC). Add `"use client"` only when the component needs hooks, event handlers, or browser APIs.
2. **DO use semantic HTML.** `<nav>`, `<main>`, `<section>`, `<article>`, `<button>` (not `<div onClick>`). Accessibility starts with correct elements.
3. **DO design mobile-first.** Default styles = mobile. Use `md:` for tablet, `lg:` for desktop. Touch targets minimum 44x44px.
4. **DO use framework error boundaries.** `loading.tsx` and `error.tsx` in Next.js, `ErrorBoundary` in React, etc.
5. **DO use page objects in Playwright tests.** Abstract page interactions into reusable classes (`AuthPage.login()`, `ChatPage.sendMessage()`).
6. **DO extract reusable hooks.** Custom hooks > inline `useEffect`. Name describes the capability: `useThread`, `useMessages`, `useRealtimeSubscription`.
7. **DO use `React.memo`/`useMemo` only when measured.** Profile first with React DevTools, memoize only proven bottlenecks.

---

# Patterns

> Include concrete code examples in the project's actual languages. Below are examples in both TypeScript and Python — use whichever matches the project, or both if full-stack.

## Domain directory structure

### TypeScript
```
src/
├── domain/
│   ├── value-objects/       # Immutable, validated, single-responsibility
│   │   ├── index.ts         # Barrel export
│   │   ├── email.ts         # Format validation, normalized lowercase
│   │   ├── money.ts         # Currency-aware, immutable arithmetic
│   │   └── date-range.ts    # Start < end invariant, contains(), overlaps()
│   ├── entities/            # Rich behavior, immutable, create()/reconstitute()
│   │   ├── index.ts         # Barrel export
│   │   ├── order.ts         # cancel(), addItem(), calculateTotal()
│   │   └── user.ts          # changeEmail(), deactivate(), hasPermission()
│   ├── repositories/        # Data access interfaces (no infra imports)
│   │   └── thread-repository.ts
│   └── ports/               # External service contracts
│       └── auth-port.ts
├── infra/                   # Provider-specific implementations
│   └── supabase/            # (or aws/, firebase/, etc.)
│       ├── supabase-thread-repository.ts
│       └── supabase-auth-adapter.ts
├── services/                # Use cases returning Result<T, Error>
├── routes/                  # HTTP handlers (unwrap Result → response)
└── middleware/              # Cross-cutting concerns
```

### Python
```
app/
├── domain/
│   ├── value_objects/       # Immutable, validated, single-responsibility
│   │   ├── __init__.py
│   │   ├── email.py         # Format validation, normalized lowercase
│   │   ├── message_role.py  # Enum: user, assistant, system
│   │   └── thread_title.py  # Non-empty, max length
│   ├── entities/            # Rich behavior, immutable, create()/reconstitute()
│   │   ├── __init__.py
│   │   ├── thread.py        # create(user_id, title), rename(), add_message()
│   │   └── message.py       # create(thread_id, content, role)
│   ├── repositories/        # Data access Protocol interfaces
│   │   └── thread_repository.py
│   └── ports/               # External service contracts
│       └── auth_port.py
├── infra/                   # Provider-specific implementations
│   └── supabase/            # (or aws/, firebase/, etc.)
│       ├── supabase_thread_repository.py
│       └── supabase_auth_adapter.py
├── core/                    # Result types, config, shared infra
├── services/                # Use cases returning Result[T, ServiceError]
├── routes/                  # HTTP handlers (unwrap Result → response)
└── middleware/              # Cross-cutting concerns
```

## Entity pattern

### TypeScript
```typescript
export class Order {
  private constructor(private readonly props: OrderProps) {}

  // Factory: validates input, creates new instance
  static create(input: CreateOrderInput): Result<Order, ValidationError> {
    if (input.items.length === 0) {
      return err(new ValidationError("Order must have at least one item"));
    }
    return ok(new Order({ id: crypto.randomUUID(), ...input, status: "draft" }));
  }

  // Hydration: trusts DB data, no validation
  static reconstitute(props: OrderProps): Order {
    return new Order(props);
  }

  // Behavior: returns new instance (immutable)
  cancel(): Result<Order, DomainError> {
    if (this.props.status === "shipped") {
      return err(new DomainError("Cannot cancel shipped order"));
    }
    return ok(new Order({ ...this.props, status: "cancelled" }));
  }

  // Serialization: for HTTP responses
  toPlain(): OrderProps {
    return { ...this.props };
  }
}
```

### Python
```python
@dataclass(frozen=True)
class Thread:
    id: str
    user_id: str
    title: str
    created_at: datetime

    @classmethod
    def create(cls, user_id: str, title: str) -> Result[Thread, ValidationError]:
        if not title.strip():
            return Err(ValidationError("Title cannot be empty"))
        return Ok(cls(
            id=str(uuid4()), user_id=user_id,
            title=title.strip(), created_at=datetime.utcnow(),
        ))

    @classmethod
    def reconstitute(cls, **kwargs) -> Thread:
        return cls(**kwargs)

    def rename(self, new_title: str) -> Result[Thread, ValidationError]:
        if not new_title.strip():
            return Err(ValidationError("Title cannot be empty"))
        return Ok(Thread(
            id=self.id, user_id=self.user_id,
            title=new_title.strip(), created_at=self.created_at,
        ))
```

## Value object pattern

### TypeScript
```typescript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export class Email {
  private constructor(public readonly value: string) {}

  static from(input: string): Email {
    const normalized = input.trim().toLowerCase();
    if (!EMAIL_REGEX.test(normalized)) {
      throw new Error(`Invalid email: ${input}`);
    }
    return new Email(normalized);
  }

  equals(other: Email): boolean {
    return this.value === other.value;
  }
}
```

### Python
```python
@dataclass(frozen=True)
class MessageRole:
    value: str

    VALID_ROLES = {"user", "assistant", "system"}

    def __post_init__(self) -> None:
        if self.value not in self.VALID_ROLES:
            raise ValueError(f"Invalid role: {self.value}. Must be one of {self.VALID_ROLES}")
```

## Service pattern (Result)

### TypeScript
```typescript
export class AuthService {
  constructor(private readonly db: Database) {}

  async login(email: string, password: string): Promise<Result<Session, AuthError>> {
    const user = await this.db.findUserByEmail(email);
    if (!user) return err(new AuthError("Invalid credentials"));

    const valid = await verify(password, user.passwordHash);
    if (!valid) return err(new AuthError("Invalid credentials"));

    const session = await this.db.createSession(user.id);
    return ok(session);
  }
}
```

### Python
```python
class AuthService:
    def __init__(self, supabase_client):
        self._client = supabase_client

    async def signup(self, email: str, password: str) -> Result[User, AuthError]:
        try:
            response = self._client.auth.sign_up({"email": email, "password": password})
            if response.user is None:
                return Err(AuthError("Signup failed"))
            return Ok(User.reconstitute(**response.user.model_dump()))
        except Exception as e:
            return Err(AuthError(f"Signup error: {e}"))
```

## Branching rules

```typescript
// WRONG: nested if/else
if (status === "cancelled") {
  // ...
} else {
  if (items.length === 0) {
    // ...
  } else {
    // ...
  }
}

// RIGHT: fail-first + switch
if (order.isCancelled()) {
  return this.handleCancelled(order);
}
return this.process(order);

function calculateDiscount(tier: CustomerTier): Money {
  switch (tier) {
    case "bronze":  return Money.fromCents(BRONZE_DISCOUNT_CENTS);
    case "silver":  return Money.fromCents(SILVER_DISCOUNT_CENTS);
    default:        return baseDiscount.scaleBy(tier.multiplier);
  }
}
```

```python
# WRONG: nested if/elif
if status == "cancelled":
    ...
else:
    if len(items) == 0:
        ...
    elif len(items) == 1:
        ...

# RIGHT: fail-first + match
if order.is_cancelled():
    return handle_cancelled(order)
return process(order)

def calculate_discount(tier: str) -> Money:
    match tier:
        case "bronze": return Money.from_cents(BRONZE_DISCOUNT_CENTS)
        case "silver": return Money.from_cents(SILVER_DISCOUNT_CENTS)
        case _:        return base_discount.scale_by(tier_multiplier)
```

## Page object pattern (Playwright)

```typescript
export class AuthPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto("/login");
    await this.page.fill("[name=email]", email);
    await this.page.fill("[name=password]", password);
    await this.page.click("button[type=submit]");
    await this.page.waitForURL(url => !url.pathname.includes("/login"), { timeout: 10000 });
  }
}
```

## Repository pattern

### TypeScript
```typescript
// domain/repositories/thread-repository.ts — interface only, no infra imports
export interface ThreadRepository {
  findById(id: string): Promise<Thread | null>;
  findByUserId(userId: string): Promise<Thread[]>;
  save(thread: Thread): Promise<void>;
  delete(id: string): Promise<void>;
}

// infra/supabase/supabase-thread-repository.ts — concrete implementation
export class SupabaseThreadRepository implements ThreadRepository {
  constructor(private readonly client: SupabaseClient) {}

  async findById(id: string): Promise<Thread | null> {
    const { data } = await this.client.from("threads").select().eq("id", id).single();
    return data ? Thread.reconstitute(data) : null;
  }
  // ...
}
```

### Python
```python
# domain/repositories/thread_repository.py — interface only, no infra imports
from typing import Protocol

class ThreadRepository(Protocol):
    async def find_by_id(self, thread_id: str) -> Thread | None: ...
    async def find_by_user_id(self, user_id: str) -> list[Thread]: ...
    async def save(self, thread: Thread) -> None: ...
    async def delete(self, thread_id: str) -> None: ...

# infra/supabase/supabase_thread_repository.py — concrete implementation
class SupabaseThreadRepository:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def find_by_id(self, thread_id: str) -> Thread | None:
        response = self._client.table("threads").select("*").eq("id", thread_id).single().execute()
        return Thread.reconstitute(**response.data) if response.data else None
    # ...
```

## Port/Adapter pattern

### TypeScript
```typescript
// domain/ports/auth-port.ts — contract only
export interface AuthPort {
  signup(email: string, password: string): Promise<Result<User, AuthError>>;
  login(email: string, password: string): Promise<Result<Session, AuthError>>;
  verifyToken(token: string): Promise<Result<User, AuthError>>;
}

// infra/supabase/supabase-auth-adapter.ts — provider-specific implementation
export class SupabaseAuthAdapter implements AuthPort {
  constructor(private readonly client: SupabaseClient) {}

  async signup(email: string, password: string): Promise<Result<User, AuthError>> {
    const { data, error } = await this.client.auth.signUp({ email, password });
    if (error) return err(new AuthError(error.message));
    return ok(User.reconstitute(data.user));
  }
  // ...
}
```

### Python
```python
# domain/ports/auth_port.py — contract only
from typing import Protocol

class AuthPort(Protocol):
    async def signup(self, email: str, password: str) -> Result[User, AuthError]: ...
    async def login(self, email: str, password: str) -> Result[Session, AuthError]: ...
    async def verify_token(self, token: str) -> Result[User, AuthError]: ...

# infra/supabase/supabase_auth_adapter.py — provider-specific implementation
class SupabaseAuthAdapter:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def signup(self, email: str, password: str) -> Result[User, AuthError]:
        try:
            response = self._client.auth.sign_up({"email": email, "password": password})
            if response.user is None:
                return Err(AuthError("Signup failed"))
            return Ok(User.reconstitute(**response.user.model_dump()))
        except Exception as e:
            return Err(AuthError(f"Signup error: {e}"))
    # ...
```

## Directory structure with infrastructure layer

### TypeScript
```
src/
├── domain/
│   ├── entities/            # Rich behavior, immutable
│   ├── value-objects/       # Validated, single-responsibility
│   ├── repositories/        # Interfaces only (no infra imports)
│   └── ports/               # External service contracts
├── infra/
│   └── supabase/            # Provider-specific implementations
│       ├── supabase-thread-repository.ts
│       └── supabase-auth-adapter.ts
├── services/                # Use cases — depend on interfaces, not infra
├── routes/                  # HTTP handlers
└── middleware/              # Cross-cutting concerns
```

### Python
```
app/
├── domain/
│   ├── entities/            # Rich behavior, immutable
│   ├── value_objects/       # Validated, single-responsibility
│   ├── repositories/        # Protocol interfaces only
│   └── ports/               # External service contracts
├── infra/
│   └── supabase/            # Provider-specific implementations
│       ├── supabase_thread_repository.py
│       └── supabase_auth_adapter.py
├── services/                # Use cases — depend on interfaces, not infra
├── routes/                  # HTTP handlers
└── middleware/              # Cross-cutting concerns
```

---

# Adaptation rules

When generating `quality.md` for a new project:

1. **Language match.** All code examples must use the project's actual languages. Remove the language that doesn't apply (e.g., remove Python examples for a TypeScript-only project).
2. **Framework match.** Rules reference the project's actual frameworks. FastAPI → Pydantic models. Hono → Zod validation. Next.js → server components. Vue → Composition API.
3. **Stack-specific sections only.** No Frontend section for CLI/API-only projects. No database rules for static sites. No Playwright for non-web projects.
4. **Result/Either library.** Use whatever matches the stack: `result` (Python), `neverthrow` (TypeScript), `Result` (Rust), `Either` (Scala/Haskell). The principle is always the same: explicit errors, no exceptions for business logic.
5. **DDD when applicable.** Rich entities and value objects for projects with domain logic. Skip for purely infrastructure/config/utility projects.
6. **State management.** Include rules for the project's state management approach (Zustand, Redux, Pinia, Supabase Realtime, etc.). Don't prescribe a library the project doesn't use.
7. **Data fetching.** Include rules for the project's data fetching approach (TanStack Query, SWR, Supabase client, etc.). Same principle — match what the project actually uses.
