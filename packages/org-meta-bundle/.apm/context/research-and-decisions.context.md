# Research evidence and architecture decisions

Use research to answer a concrete question, and decision records to explain an
adopted choice. Neither substitutes for requirements, contracts, implementation
evidence or product acceptance. Apply the [evidence model](requirements.context.md)
and preserve the difference between planned checks and observed results.

## Question-driven investigations

Define the question and completion criteria before an experiment. Retain enough
input, output, source revisions and dates to assess what was demonstrated. Record
relevant environment, tools and controlled variables when known. Do not invent
missing metrics, model versions, providers or controls to fill an incomplete record.

State which observation supports each conclusion and distinguish measured results
from interpretation. A successful historical path demonstrates that path under
its recorded conditions, not a later architecture, broader capability or production
readiness. Structural validation alone may not establish that a generated result
preserves intended meaning; compare against the reviewed baseline where relevant.

Bring useful conclusions into maintained product or component context. Keep research with the plan or WIP it supports, and retain useful observations
and reports in evidence with retrievable artifact citations. No dedicated research
or archive directory is required. Retiring an investigation does not mean discarding its
reasoning. Historical scripts are records; do not claim their environments still
run or require replay simply to understand the conclusion. Reproduction, when
needed, is a separately scoped activity with its own prerequisites.

## Record decisions and their limits

An architecture decision record captures the decision rationale, briefly describes
the options actually assessed and their assessment, and states the resulting change
and consequences. Link a subject-named design document when the resulting system
needs more detail; a small decision can be self-contained. Use a stable sequential
index plus topic name for the ADR filename. State its status and
scope so readers can distinguish a proposal from an accepted choice. Acceptance
of an ADR does not accept every proposal in a linked design or establish that the
choice has been implemented or verified.

Keep record identity stable. Recording order may differ from the chronology of
the original agreement; retrospective records should identify the agreement's
actual chronology and source baseline rather than silently rewriting history.
Do not import archived decisions wholesale as current policy.

When changing a decision, record its successor and explicitly mark supersession
while preserving the old rationale. Reconcile affected requirements, contracts,
plans and implementation through their owning processes. Keep current navigation
and historical citations distinct under the [reference guidance](knowledge-maintenance.context.md).
