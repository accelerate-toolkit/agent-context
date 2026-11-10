---
name: plan-requirement-verification
description: Use when deciding how requirements or interface obligations will be checked, reviewing their measurability, or finding missing, partial or unclear planned coverage. Covers verification planning, not test implementation or assessment of actual results.
---

# Plan requirement verification

Read [verification planning](../define-requirements/references/verification-planning.md) and
[the component model](../define-requirements/references/component-model.md). Start from authoritative
requirements and interface obligations at the current component boundary.

For each planned check, describe the demonstration, method, assessment criteria
references and coverage links. Requirements own satisfaction criteria; the plan
explains how to demonstrate them. If planning reveals missing or ambiguous
criteria, propose refinement at the definition authority instead of silently
creating new obligations in the check.

Assess coverage semantically, not just by counting links. Several checks may
collectively cover a requirement; one check may cover several obligations.
Explicitly identify partial scope. Plan requirement coverage, provider/consumer
interface conformance and combined outcome verification at this boundary.
Child coverage does not replace a parent integration plan.

Report missing checks, partial demonstrations, unclear criteria, unobservable or
unmeasurable statements, and missing combined outcome coverage. Separate
mechanically detectable missing links from reasoned judgments of sufficiency.
Keep actual execution results and acceptance decisions out of the planning status.
Use `assess-requirement-evidence` when the user asks what has been demonstrated.

Deliver or update a reviewable coverage plan and gap list using the project's
existing records. A complete plan means we know how we intend to check the
obligations; it does not establish implementation, execution or satisfaction.
