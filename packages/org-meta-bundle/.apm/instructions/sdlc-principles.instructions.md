---
description: Apply the three SDLC principles whenever reasoning about planning, architecture, implementation, testing or delivery.
applyTo: "**"
---

# SDLC principles

Whenever reasoning about software development and delivery, apply all three
principles together:

1. **Context:** establish the necessary business context, aspirations, personas,
   user journeys, diagrams and constraints. Identify missing context and check
   whether existing plans still reflect current decisions before deriving work.
2. **Feedback loops:** design feedback loops from the start, using acceptance
   test driven development. Define the intended outcome and observable acceptance
   criteria before implementation, then derive smaller loops. Each loop must
   answer a question, produce evidence and inform the next decision. Distinguish
   planned behavior from observed results and component checks from product acceptance.
   Loops can yield pass/fail results, quantitative measurements, or both. Define
   observation methods up front and apply quantitative thresholds only when agreed.
3. **Trajectory:** establish architecture, standards and practices that remain
   sustainable as the product evolves. Keep scope small without introducing hacks
   or knowingly unsustainable patterns. Make tradeoffs explicit and preserve the
   intended component boundaries and repeatable delivery practices.

These are continuous concerns, not sequential phases. Revisit context and
trajectory as feedback changes what is known.

Before SDLC planning or recommendations, read the
[software development lifecycle](../context/software-development-lifecycle.context.md)
for the maintained explanation. Establish how the consuming project applies these
principles using its own requirements, acceptance journeys and delivery context.

For test or delivery planning, also read
[testing and continuous delivery](../context/testing-and-delivery.context.md).
Deployable repositories own their infrastructure code. PR evidence covers local
functional acceptance using `4dev` fakes and candidate deployment plus live-provider
smoke. Exploration refines fake fidelity and automated regressions; it is not a
routine manual promotion gate. Record adoption gaps rather than claiming existing
pipelines implement this strategy.

Use the separately installed `work-with-requirements` skills for detailed
requirement definition, decomposition, verification planning, evidence assessment,
specification changes and visualisation. The linked manual retains adoption
pointers and guidance adoption methods. Planned coverage is not actual evidence.
Each responsibility layer owns derived requirements within its commission;
changes to commissioned obligations return to their definition authority.
Keep initiative-specific parties, assignments, decisions and evidence in local context.

Keep `4dev` fakes with the consumers: the component whose tests use a substitute
owns its source, scenarios and fidelity checks in its own repository. Do not move
a fake to the simulated service's repository. Shared contract authority and real
provider conformance remain separate. Reusable fake packaging does not transfer
ownership; the owning consumer publishes it when needed. Use lowercase fake names.
