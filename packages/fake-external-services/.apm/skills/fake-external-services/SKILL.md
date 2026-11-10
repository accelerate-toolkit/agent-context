---
name: fake-external-services
description: Design, implement, or review external service fakes in a component test harness, including protocol fidelity, state, fault injection, and checks against the real dependency. Use for service-boundary testing, not ordinary in-process unit mocks.
---

# Fake external services

Build the smallest fake that supports the component's acceptance scenarios at the
real dependency boundary. Keep it in the consuming component's test harness,
alongside its scenarios and fidelity checks, unless the project already has an
explicit shared ownership model. A fake does not inherently need a separate
published artifact or a prescribed framework.

## Establish the boundary and scenarios

Read the consumed contract and its version, the production client configuration,
and the acceptance scenarios before choosing the fake's shape. For a third-party
service without a versioned project contract, record the provider API version and
relevant authoritative documentation or observed behavior. Identify the operations,
state transitions and failure cases the tests need, and how each outcome will be
observed. Resolve ambiguous obligations with their owner; do not invent convenient
behavior solely to make the consumer pass.

Exercise the actual protocol and exchanges through the production client or
adapter. Configure the dependency endpoint through the component's normal
configuration mechanism. Replacing the client with an in-process mock does not
verify serialization, transport, authentication exchanges or error handling at
the service boundary. Scope fidelity to what the scenarios exercise and record
what remains unverified.

## Implement controllable behavior

- Preserve relevant request/response shapes, status codes, error meanings and
  state changes from the consumed contract. Model only the needed subset;
  unsupported operations fail explicitly instead of silently succeeding.
- Keep setup, inspection, fault injection and reset controls separate from the
  product interface. Test controls may be harness methods or a separate management
  endpoint; do not add fake-only operations to the production service contract.
- Make scenario state and faults deterministic. Seed required data, isolate test
  runs, and reset state so tests can run independently and repeatedly. Use
  controllable clocks or fault schedules where timing is part of the scenario.
- Model failures where the consumer observes them. Choose relevant cases such as
  rejected credentials, rate limits, timeouts or partial effects from the contract
  and scenarios; do not implement a catalogue of speculative behavior.
- Expose enough inspection to assert observable effects and diagnose a failure.
  Keep assertions about user outcomes separate from incidental request ordering
  unless ordering itself is contractual.

Reuse the repository's harness and tooling where suitable. Keep live-service
credentials out of offline tests and fail visibly if the fake is unavailable;
never silently fall back to the real service.

## Verify fidelity and report limits

Check representative successful exchanges, relevant failures, state transitions
and reset/repeat behavior. Validate exchanges against the formal contract where
one exists. Where feasible, run the same boundary cases against the fake and an
authorized disposable real-service environment to detect drift. Keep live checks
separately selectable; creating a fake does not authorize provisioning resources
or changing a live service.

Document the consumed baseline, supported scenarios, material omissions and how
to run the harness. Update the fake and fidelity checks when that baseline changes.
If live verification is unavailable, report that gap rather than claiming parity.

Passing against a fake supports component acceptance. It does not establish real
interoperability or integrated product acceptance; those require their own evidence.
