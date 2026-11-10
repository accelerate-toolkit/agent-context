---
name: decompose-and-allocate-requirements
description: Use when breaking a software requirement into derived obligations, assigning requirements to components, or reviewing decomposition, allocation and interface ownership. Covers requirement structure and commissions, not implementation task breakdown or individual work assignments.
---

# Decompose and allocate requirements

Read [the component model](../define-requirements/references/component-model.md) and
[requirements and ownership](../define-requirements/references/requirements.context.md).

Identify the current component, its received intent, definition authorities and
accountable delivery owners. Derive obligations through as many local requirement
layers as needed before allocating meaningful commissions. Do not invent
components to match requirement depth or force branches to equal depths.

Derivation creates a new stable requirement ID. Allocation references the same
ID inside the receiving component; it does not create a duplicate requirement.
Direct allocation and direct satisfaction are valid. A component may satisfy some
obligations itself while allocating others. Split multi-party obligations before
allocation; distinguish architectural component identity from the responsible
party and repository that delivers it.

Define interfaces between the immediate subcomponents at the commissioning
component's boundary. Record provide/use obligations and shared contract authority.
Use [specifications](../define-requirements/references/specifications.context.md) when exchanges or versioned
commissions need definition. Leave internal design to the receiving component.

Review whether the derived obligations plausibly cover the parent's intent and
whether interaction obligations are missing. An unlinked requirement signals a
traceability question: resolve an existing link, justify local derivation, or
propose an upstream change. It is not automatically proof of a missing parent.

Return the decomposition, allocations, interface ownership and unresolved gaps.
An external assignment or notification still requires the user's authorization.
