# Document types and lifecycle

## Context

Use enduring subject names such as `docs/context/product-purpose.md` and
`users-and-journeys.md`. Explain purpose, users, intended outcomes and constraints.
Keep context current; link precise obligations in requirements rather than defining
a competing set. Technical structure belongs in design; choices belong in ADRs.

## Requirements and allocation

Use `docs/requirements/README.md` to navigate `owned/` definitions, `upstream/`
received obligations with authoritative revisions, `allocations/` component
assignments and `verification/` planned checks, measurability and coverage gaps.
Keep requirement derivation separate from component containment: multiple derived
layers can precede allocation. Allocation references the same stable requirement
IDs; it does not create competing definitions. Preserve existing source-backed
assignment representations and published baselines during adoption. Actual
results and assessments belong in evidence, not planned coverage.

## Architecture decision records

Use stable sequential indices plus decision topics, for example
`docs/decisions/0001-separate-control-and-data-planes.md`. Do not renumber existing
ADRs to impose a padding convention or chronology. Record status and the actual
decision date; recording order may differ, particularly for retrospective records.

Capture the problem and decision drivers, briefly describe the credible options
actually assessed and the assessment of each, then state the choice and rationale.
Record the resulting change, consequences and accepted tradeoffs. Do not invent
alternatives or assessments that were never made; identify missing rationale.
Link supporting research and a design document when the resulting system needs
more detail. A small decision can be self-contained. Keep enough rationale in the
ADR to understand the choice without reconstructing a conversation.

Acceptance records a decision, not implementation or verification. Supersede a
changed decision explicitly, retaining the original rationale and a successor link.
Superseded ADRs remain in `decisions/` with their stable identities.

## Design

Use subject names such as `docs/design/identity-and-sessions.md`, not milestone
names. Describe scope, requirement links, responsibilities, boundaries, interfaces,
interactions and useful diagrams. Link ADR rationale instead of repeating its
option assessment. Identify unresolved proposals and known implementation gaps.

Keep the intended system coherent as choices evolve. Permanent technical
information belongs here; execution steps belong in plans/WIP and hands-on
procedures in runbooks. Milestones link to the designs they depend on rather than
creating competing milestone-specific descriptions of the same system.

## Plans

`docs/plans/` contains work that has not started. Use a subject-named document or
folder as needed. Record outcome, scope, linked requirements/designs, implementation
approach, planned verification, dependencies and questions awaiting review. State
whether the plan is draft, awaiting review, approved but unstarted, or deferred.
Approval of a plan does not itself mean execution has begun.

When execution starts, distribute agreed system detail into maintained design
docs and execution scope, steps, checks, dependencies and open questions into a
WIP folder. Capture consequential rationale in ADRs. Remove the consumed plan,
updating links to the appropriate destinations; do not retain a competing live
plan. Keep any genuinely unstarted, separable scope as an explicit remaining plan.
For abandoned plans, preserve useful conclusions and outstanding work before
removal. Git retains history; no archive directory is needed.

## Work in progress

Use one folder per coherent implementation effort, for example
`docs/wip/native-account-flows/`. Its `README.md` is the entry point and can be the
only document. Split into additional documents freely when useful; no fixed set
of implementation, verification or blocker files is required.

Make current outcome/scope, requirement/design/ADR links, remaining and completed
work, verification progress, evidence links, blockers and next action discoverable.
Maintain the folder across sessions rather than producing successive handovers.
Record significant discoveries and scope changes without accumulating transcripts.
Link shared issue trackers rather than maintaining competing task states.

Before removing a completed WIP folder, reconcile design and runbooks, retain
useful evidence and move unresolved work to an appropriate active tracker or future
plan. Completion describes the delivered scope; it does not establish wider product
acceptance. Preserve the useful content, not an archive copy of the tracker.

## Evidence

Use a folder per assessment or investigation, with a `README.md` entry point and
one or many documents as useful. Record what was assessed, requirement/contract
and implementation revisions, observations, interpretation, limitations and what
remains unproven. Link retained run artifacts rather than duplicating bulky logs.
Historical results keep their original context when the current assessment changes.
WIP links execution progress here; planned coverage remains under requirements.

Research lives with the plan or WIP it supports. Retained experiment observations
belong in evidence; conclusions feed ADRs and design. Do not create a separate
research category or assume a closed investigation's results can be discarded.

## Runbooks

Use task names such as `docs/runbooks/local-development.md`, `releasing.md` or
`recovering-a-failed-deployment.md`. Describe prerequisites, hands-on steps, expected
results, verification and recovery actions where relevant. Procedures must match
the current implementation; proposed procedures stay in plans/WIP until usable.
Link permanent architecture and lifecycle explanations in design docs instead of
duplicating them. A tool/module README may remain the authoritative procedural home.

## Optional workbench

`docs/workbench/` stages documents for future Cypherdown ingestion. It is neither
a mandatory authoring route nor an approval state. Staged material may be proposed
or agreed; identify its status explicitly. Incorporating it into maintained docs
must preserve meaning and provenance without implying ingestion or publication
occurred. Do not promise generated views before that system is implemented.
