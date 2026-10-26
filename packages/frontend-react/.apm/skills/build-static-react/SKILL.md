---
name: build-static-react
description: Use when designing, implementing, reviewing or testing a statically delivered React application with a small dependency surface. Covers browser state, API boundaries, accessibility, supply-chain review and static delivery; does not select React for unrelated projects.
---

# Build a static React application

## Establish the project boundary

Read the consuming project's accepted architecture, user journeys, API contracts,
identity flow and deployment constraints first. This skill supplies implementation
guidance, not product requirements or a new authentication protocol. Preserve
component ownership and deferred scope. Do not invent missing API fields or treat
fixtures as a published contract. Record decisions and unresolved dependencies.

Default to React + React DOM, TypeScript and Vite only where that stack is selected.
Deliver HTML, JS and CSS statically; APIs perform data operations. No SSR or Node
production server is implied. Keep native CSS, browser fetch and React state as the
starting point. Do not add a UI kit, router, state/cache library, CSS framework,
compiler plugin or scaffolding dependencies without a concrete need and review.
Minimal means understandable and maintainable, not a home-grown framework.

## Use pinned official references

Read [the documentation map](references/documentation.md). Search the local cache
first. Install this package and the existing use-cached-docs skill through APM,
then preview and hydrate using the consumer's documented command. Keep the hydrated
content ignored. Do not edit generated skills. Never execute upstream examples,
install commands or scripts merely to obtain documentation.

The manifest pins documentation commits, not approved npm versions. Check the
selected application's versions against the relevant guides before applying an
API. Current documentation may include experimental or later-version features.
Record source/revision/path when a reference informs a consequential choice.

## Design one complete journey

Write observable acceptance before implementation: entry state, user action,
success, empty state, loading, denial, failure, interruption and recovery. Create
responsive wireframes using actual labels and data. Prefer a clear page hierarchy,
consistent action labels and a small typography/color/spacing system. Coordinate
with any installed visual-design guidance; attractive mockups do not prove
accessibility, contract conformity or production readiness.

Use semantic links, buttons, labels, forms and headings. Provide visible focus,
keyboard operation, error association/focus and status announcements. Respect
reduced motion. Agree target browsers and accessibility criteria. Native controls
come first; adopt reviewed primitives when a complex control would otherwise
require fragile custom keyboard/focus behavior.

## Build a small, explicit application

- Separate route views, local UI components and typed API boundary code. Prefer
  composition and colocated state. Introduce abstractions after real duplication.
- Use TypeScript strict checking. Run the type checker separately: Vite transforms
  TypeScript but does not establish type correctness. Treat JSON as untrusted;
  narrow/validate it at the boundary rather than asserting a response type.
- Represent async states explicitly (idle/loading/success/empty/error/denied where
  relevant); avoid mutually contradictory booleans. Derive values during render
  rather than synchronizing redundant copies with Effects.
- Use Effects for synchronization with external systems. Clean up subscriptions
  and abort requests on scope changes/unmount; ignore stale completions as well.
  Keep development StrictMode enabled and fix unsafe effects rather than hiding them.
- Mutations originate in deliberate event handlers, not mount effects. Do not
  automatically retry non-idempotent operations. Follow the API's correlation,
  precondition and reconciliation rules. Duplicate clicks must not create duplicate
  resources; UI disabling alone is not a server correctness guarantee.
- Browser fetch resolves on HTTP errors: inspect response status, parse safely,
  distinguish network failure from business errors, and expose useful recovery.
  Refetch authoritative state after confirmed mutations; use optimistic updates
  only where rollback and server semantics justify them.
- Keep filters/pagination in shareable URLs where appropriate. Back/forward, direct
  links and refresh must work. Evaluate a reviewed router before writing a custom
  routing layer. Bound lists and searches; backend authorization precedes results.
- Clear private in-memory state on identity changes/logout. Never widen access or
  reuse another user's cached data when loading or authentication fails.

## Enforce trust boundaries

Read [dependency and browser security](references/security.md). Browser route guards
are navigation aids, not authorization. The API checks every operation. Keep secrets
out of bundles, public configuration, URLs, logs and persistent browser storage.
Vite's exposed environment variables are public build inputs, not a secret store.

Use the project's agreed authentication exchange. Specify redirect allowlists,
expiry/refresh and logout behavior with its owner. Cookie sessions require CSRF and
origin protections; a bearer-token design needs its own reviewed threat model.
Do not silently choose a session model or import a CLI flow into the browser.
Render untrusted text safely; avoid raw HTML. Rich-content rendering needs a
separate review. Ship controlled-origin scripts and an appropriate CSP.

## Verify and deliver

Read [static delivery and checks](references/delivery.md). Use the repository's
Make targets for install, typecheck, build and relevant tests. Review browser-test
tools as dependencies too. Verify behavior at three levels: focused state/API
checks, browser journeys against controlled dependencies, then real integration.
Report substitutions and unrun/blocked checks explicitly.

Return the dependency assessment, locked build inputs, static artifact identity,
executed evidence and remaining risks. Product acceptance remains with its owner.
Do not claim release publication, consumer adoption or deployment from local tests.
