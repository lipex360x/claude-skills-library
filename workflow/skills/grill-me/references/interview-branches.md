# Interview Branches — Decision Tree

Each branch is an investigation axis. Order adapts to context: for greenfield, start with Problem; for existing codebase, start with Current State.

All questions, options, and signals must use the language chosen in Step 1. Examples below are in English — translate at execution time.

## Branch 1: Problem

What's driving this work? What pain or opportunity?

**Sample questions:**
- "What problem are you trying to solve?"
  - Options derived from the initial prompt (e.g., "Slow checkout performance", "No visibility into orders", etc.)
- "Who feels this pain today?"
  - Options: personas derived from context (e.g., "End users", "Internal team", "Partners/Integrators")
- "Is this urgent or a planned improvement?"
  - Options: "Urgent — impacts production", "Planned — next cycle", "Exploratory — still evaluating"
- "How do you solve this today (workaround)?"
  - Options derived from context + "No workaround exists"

**Sub-branches:**
- If urgent → explore impact (who's affected, since when, metrics)
- If exploratory → explore validation (how to know if it's worth it)

## Branch 2: Target Audience and Actors

Who are the users and stakeholders?

**Sample questions:**
- "Who are the main users of this feature/product?"
  - Options derived from context (e.g., for e-commerce: "Buyers", "Sellers", "Admins")
- "Are there secondary actors (integrations, bots, systems)?"
  - Options: "Yes — [context-based suggestions]", "No, humans only"
- "What's the technical level of the primary audience?"
  - Options: "Technical (devs, engineers)", "Semi-technical (product, design)", "Non-technical (end users)", "Mixed"

**Sub-branches:**
- If multiple actors → explore priority (which persona is the MVP focus?)
- If integrations → explore which systems and contracts

## Branch 3: Expected Behaviors

What should the system do? Main journeys and flows.

**Sample questions:**
- "Describe the main flow — the user's happy path"
  - Options: scenarios derived from context (e.g., "User creates account → sets up profile → places first order", etc.)
- "What happens when something goes wrong in this flow?"
  - Options: error cases derived from the flow (e.g., "Payment fails", "Product unavailable", "API timeout")
- "Any important secondary flows?"
  - Options derived from context + "Not for now"

**Sub-branches:**
- For each mentioned flow → detail steps and decisions
- If existing codebase → verify which flows already exist in code

## Branch 4: Technical Constraints

Stack, infrastructure, limitations.

**For greenfield:**
- "What stack are you considering?"
  - Options: common stacks for the project type (e.g., for web app: "Next.js + TypeScript", "Remix + TypeScript", "SvelteKit")
- "Where will it run?"
  - Options: "Vercel/Netlify", "AWS/GCP/Azure", "Docker self-hosted", "Don't know yet"
- "Any technology constraints (company, team, compliance)?"
  - Options: "Yes — must use [X]", "No, full freedom", "Compliance (GDPR, SOC2, etc.)"

**For existing codebase:**
- Explore the code first: detect stack, dependencies, patterns
- "I found [stack/patterns]. Any constraints for this change?"
  - Options derived from exploration (e.g., "Keep v2 API compatibility", "Breaking change is OK", "Needs feature flag")
- "Any areas of the code that are off-limits?"
  - Options: "Yes — [modules]", "No, everything is fair game", "Need to check with the team"

## Branch 5: Integrations

External systems, APIs, services.

**Sample questions:**
- "Does this feature need to communicate with any external service?"
  - Options derived from context (e.g., "Payment gateway", "Email service", "Third-party API") + "None"
- For each integration → "Do you have a contract/documentation for this API?"
  - Options: "Yes, I have the docs", "It exists but I need to check", "Needs to be defined"
- "Any dependency on something another team is building?"
  - Options: "Yes — [what]", "No, it's independent"

**Sub-branches:**
- For each integration → explore: authentication, rate limits, environments (sandbox?), fallback

## Branch 6: Scope and Boundaries

What's in and what's out.

**Sample questions:**
- "What is definitely NOT part of this scope?"
  - Options derived from what was discussed (e.g., "Mobile app", "Internationalization", "Offline mode") + "Nothing specific"
- "What's the MVP — the smallest version that solves the problem?"
  - Options: cut scenarios (e.g., "Only the main flow without edge cases", "Only for one user type", "No external integrations for now")
- "Any deadline or external milestone?"
  - Options: "Yes — [date]", "No, but want to move fast", "Exploratory, no pressure"

**Sub-branches:**
- If there's a deadline → explore what to cut to fit
- If MVP is defined → confirm it solves the problem from Branch 1

## Branch 7: Priorities

Must-have vs nice-to-have.

**Sample questions:**
- Present the list of discussed features/behaviors and ask for prioritization:
  - "Which of these features are must-have for launch?"
  - Use `multiSelect: true` with features as options
- For the remaining ones: "Are these nice-to-have or discarded?"
  - Options: "Nice-to-have (backlog)", "Discarded for now", "Need to think more"

## Suggested Order

**Greenfield:** Problem → Audience → Behaviors → Technical Constraints → Integrations → Scope → Priorities

**Existing codebase:** Explore code → Problem → Current State (what exists) → Behaviors (what changes) → Constraints → Integrations → Scope → Priorities

Order may change if the conversation naturally leads to a different branch. The important thing is covering all of them.
