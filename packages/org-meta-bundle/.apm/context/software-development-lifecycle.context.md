# Software development lifecycle

These principles guide planning, architecture, implementation, testing and delivery
in software projects consuming `org-meta-bundle`. Apply Context, Feedback loops
and Trajectory together throughout the work. Non-software projects are outside
this bundle's scope; a separate fork can define their guidance when needed.

## Context

Ensure we have the context needed to reason about the work: business purpose,
aspirations, personas, user journeys, diagrams, constraints and relevant decisions.
Documentation should explain both the intended outcome and why it matters.
Identify gaps and distinguish current decisions from historical plans, proposals
and implementation evidence. An old task list is not sufficient justification
for continuing work when the architecture or intended outcome has changed.

Maintain enough context to make the next decision responsibly. Update it when
feedback changes our understanding, rather than treating documentation as a
one-time preparation phase.

## Feedback loops

Design feedback loops from the start. Use acceptance test driven development:
describe the user outcome, starting conditions, actions and observable pass
criteria before deriving implementation tasks. Work backwards from product
acceptance into smaller loops that expose uncertainty early.

For each loop, identify the question being answered, the check or experiment,
the evidence it produces and the decision that evidence informs. Record actual
results and use them to adjust the next step. Tests that have not run establish
an expectation, not a pass. Component checks support product acceptance but do
not replace the complete user journey.

Feedback loops can produce pass/fail results, quantitative measurements, or both.
Define the observation method before execution. Use acceptance criteria to
establish correctness and quantitative measures to track improvement. Apply
quantitative pass thresholds only when explicitly agreed; an initial measurement
can establish a baseline without imposing a target.

Correctness and experience quality are separate assessments. A functional pass
can retain a warning for an explicitly accepted MVP limitation. Distinguish measured
values, aspirational targets and binding acceptance limits; missing a target is not
a failure unless that limit was agreed. Record the rationale and follow-up for
accepted deviations without using them to waive required correctness criteria.

Generate reporting from run evidence and versioned expectations rather than
maintaining a second status system. Missing data is not a successful result or a
zero measurement. Preserve historical verdicts and compare only compatible runs.

## Setup as a reusable feedback loop

Setup is part of the user experience and deserves its own acceptance journeys.
Separate first-user onboarding from later integrations and scenario activation.
Distinguish shared environment prerequisites from scenario-specific state. Define
each journey's starting state, retained outcome and explicit dependencies. Ordering
in the suite helps humans walk through it but does not make every journey depend
on every preceding one.

A successful setup can be persistent test state. Record its environment, versions,
identities and configuration, then check and reference that baseline in dependent
runs. Preserve it during routine scenario cleanup. Reset only when deliberately
retesting the relevant setup; record changes and assess affected dependents. Do not
silently repair an unavailable baseline and report an uninterrupted pass.

Make the result observable through the intended user interface. A connection flag
is not evidence of successful source enumeration; enumeration is not evidence of
content writes; advertised capabilities are not evidence that those operations work.
Each loop should establish only its stated outcome, with supporting evidence.

Measure difficulty as well as correctness. Record active effort separately from
elapsed waiting, define interaction/retry/assistance counts, and note familiarity
with the process. Fix controllable variables and record those controlled by hosted
providers. Use those measurements to identify improvement opportunities without
inventing pass thresholds after observing results.

## Trajectory

The patterns established now should remain sustainable over the long run.
Architecture, contracts, standards and development practices are part of the
outcome, alongside working functionality. Do not introduce hacks or knowingly
unsustainable patterns simply to demonstrate a milestone.

Keep the implemented scope narrow while maintaining sound component boundaries
and repeatable development and delivery practices. Defer capabilities where
appropriate; avoid speculative complexity. Explain consequential tradeoffs and
check that each decision supports continued development.

## Applying the three principles together

These are continuous concerns rather than sequential phases. Acceptance design
can reveal missing context; implementation feedback can expose an architectural
problem; user feedback can change the intended outcome. Revisit all three as
evidence arrives.

For milestone planning, establish the human outcome and relevant context, design
the acceptance journey and smaller feedback loops, and assess whether the proposed
architecture and practices set a sustainable direction. Derive component work
from that reasoning rather than allowing an inherited backlog to set the direction.

## Responsibility layers and acceptance

Every layer owns requirements, architecture, delivery and acceptance within its
scope. It can satisfy an obligation directly, decompose it or delegate delivery.
The commissioning layer owns interfaces between the parts it commissions and
accepts their combined outcome. Receiving layers own derived requirements,
internal design and verification within their commissions. Changes to a
commissioned obligation return to its definition authority.

One requirement has one definition authority and one accountable delivery owner.
Split multi-party delivery into separately owned contributions before delegation.
Direct satisfaction needs no duplicate child. Decompose only far enough to
commission meaningful work; leave detailed specification to the receiving layer.
Business provenance, technical subject and quality category do not create fixed
hierarchy levels. Local context supplies parties, repositories and boundaries.

Product acceptance demonstrates the integrated outcome. Component tests and
conformity claims support it but do not replace the commissioning owner's
assessment. Setup is a prerequisite and measurable experience burden; reusing it
must not hide its first-use cost. Record evidence against the actual assigned
requirements and contract revisions, preserving limitations and historical results.

## Shared manual and local application

The SDLC manual lives together in `org-meta-bundle`. Read the relevant reference
when doing the corresponding work:

- [Requirements, delegation and evidence](requirements.context.md): authoring,
  ownership, registers, identity, assignments and satisfaction assessments.
- [Specifications, contracts and acceptance](specifications.context.md): exchange
  authority, edition compatibility, immutable baselines and acceptance boundaries.
- [Specification change workflow](specification-change-workflow.context.md):
  inspect, decide, prepare, validate, publish and hand off a coherent change.
- [Engineering guidance and adoption](engineering-guidance.context.md): guidance
  versus obligations, delivery measures, context updates and migration assessment.

Consumer context identifies local parties, namespace, authoritative registers,
acceptance journeys, tooling, artifact names and decisions. Keep those details
local and refer to this manual for methods. This package does not install product
requirements, validators, service implementations or live acceptance environments.

When adopting this responsibility model from the earlier centralized model,
reconcile authority and delegated scope explicitly. Preserve requirement IDs,
published baselines and historical evidence; do not silently reassign work or
claim migration complete from a successful context installation.
