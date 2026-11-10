---
name: visualize-requirements
description: Use when creating or updating diagrams or interactive views that trace requirements through derivation, component allocation, interfaces and planned verification coverage. For deciding coverage use plan-requirement-verification; for judging actual results use assess-requirement-evidence.
---

# Visualize requirements

Read [the component model](../define-requirements/references/component-model.md) and
[verification planning](../define-requirements/references/verification-planning.md). Inspect authoritative
records before choosing a renderer. Preserve their IDs, scope and unresolved gaps.

Render one component boundary at a time:

1. Intent: requirements received by this component.
2. Explicit derived requirement layers below intent, at their actual depths.
3. Immediate subcomponent boxes repeating allocated requirement IDs, with
   interfaces and provide/use relationships between the boxes.
4. Verification plan: planned demonstrations linked to requirements, acceptance
   criteria and interface obligations at the current boundary.

Use distinct relations for derivation and allocation. Repeated allocated IDs
are references to the same entity. Expanding requirements stays within the current
component; zooming into a subcomponent makes its allocations the received intent.
Preserve edge interfaces when siblings disappear. Allow direct allocation, uneven
branches and local direct satisfaction without artificial nodes.

Show missing, partial and unclear planned coverage. A link alone must not imply
complete semantic coverage. Summarise child coverage gaps separately from the
current component's own plan; do not roll them into a misleading satisfaction
percentage. Actual results and acceptance belong in a separately requested
evidence view, using `assess-requirement-evidence`.

Use an existing project renderer when available; otherwise choose native diagrams
for a small static view or an interactive renderer for expansion and component
zoom. Keep definitions authoritative and generate views from them. Do not require
a new database, tool-specific schema or fixed HTML implementation merely to
visualise the model. Inspect the rendered result for legibility, correct identity
links, gap visibility and preservation of scope when navigating.
