# Outcome-led roadmaps and milestone plans

A roadmap orders useful outcomes and the value they unlock. Link those outcomes
to approved requirements and derive implementation work from observed gaps.
Keep the roadmap concise: outcome, value, requirement links, sequence and status.
Distinguish agreed scope from possible later work; ordering an outcome does not
commit a delivery date or every detail of its implementation.

## Shape a milestone before execution

Create a milestone plan when actively shaping the outcome. Record scope,
acceptance links, proposed work, dependencies, planned verification and open
review questions. Select a small useful end-to-end journey rather than requiring the entire
future product. Distinguish prerequisites from merely earlier items in the roadmap.

Keep detailed test procedures in the acceptance suite and implementation tasks in
the owning component's work tracker. Link these to the requirements and milestone
rather than copying their full contents into a second plan. A roadmap sequences
work; it does not redefine requirement authority or replace assignments.

When execution starts, distribute the plan into maintained subject-based design
docs and an active `docs/wip/<effort>/` folder, then remove the consumed plan and
update references. The WIP entry point records current progress and the next action;
it may link to additional documents as needed. `docs/plans/` holds unstarted work.
Keep consequential choices and assessments in ADRs. Follow `maintain-repo-docs`
for these transitions and reconcile durable docs before removing completed WIP.

## Update from feedback

After each feedback loop, update what was observed, what remains uncertain or
incomplete, and what comes next. Distinguish plans, verified capabilities and
accepted outcomes. Preserve historical evidence when scope or assumptions change;
reconcile active trackers and future plans with the decision rather than continuing
an obsolete list.

A milestone is complete when its agreed product acceptance has passed with
retained evidence and the responsible owner's assessment. A component release
alone does not establish delivery. Milestone coverage is a selected subset of
journeys, not a waiver of other component obligations; apply the
[conformity and coverage distinction](specifications.context.md#component-conformity-and-milestone-coverage-are-separate).

Local context identifies the current roadmap and active milestone WIP trackers as the
sequencing authority. Broader direction documents can retain rationale and history
without becoming a competing status register.
