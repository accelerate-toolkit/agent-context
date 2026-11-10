# Engineering guidance and adoption

## Guidance, obligations, decisions and evidence

Packaged context and skills provide the engineering manual: principles, methods, recognized
standards and reference material. Keep source attribution and applicable revisions
visible. Requirements record the obligations adopted for the system in scope.
Architectural decisions record chosen mechanisms, rationale and tradeoffs.
Evidence and owner assessments record what has actually been demonstrated.

A proposed product or system change must trace to an approved requirement or
measurable NFR, including remediation of a gap against an existing obligation.
New guidance alone does not authorize implementation changes. Assess applicability,
then propose a requirement change if the intended outcome is not already covered.
Routine implementation choices within an existing commission need no new requirement.

For security, select and interpret relevant guidance against assets,
data, threats and trust boundaries. Propose applicable requirements and evidence
expectations, recording source provisions, revisions and applicability rationale.
The normal requirements process approves and delegates obligations. A citation is
neither automatic adoption of every recommendation nor evidence of compliance.
The reference baseline must be selected explicitly; this bundle selects none.

## Measurable delivery outcomes

Architectural principles guide design across initiatives. Their application should
identify the requirement or NFR and the expected measurable benefit. For delivery,
use a balanced assessment of change lead time, deployment frequency, failed
deployment recovery time, change fail rate and deployment rework rate, inspired by
[DORA's delivery metrics](https://dora.dev/guides/dora-metrics/).

The responsible layer defines the service and environment boundary, observation
window, units, event definitions, aggregation and data sources before assessment.
Baseline observations, desired targets, mandatory thresholds and actual results
are distinct. Report all dimensions and uncertainty rather than a single pass flag;
faster delivery cannot hide deterioration in failures, recovery or rework. No
universal numeric targets are imposed by this method. No events means insufficient
observation for the relevant rate or recovery measure, not a measured zero.

Before production evidence is available, use explicitly labelled rehearsals to
investigate mechanisms; do not report them as production delivery performance.
Component checks support assessment of the full delivery path but do not establish
it. Delegate contributions within each recipient's control rather than copying an
identical top-level metric target into every component's register.

Release independence and managed/serverless execution are examples of architectural
directions whose benefits must be assessed. A technology choice is not proof of
improved delivery or operability. Record expected benefits, costs and tradeoffs in
the decision; derive initiative-specific obligations before implementing changes.
This guidance does not introduce a universal serverless mandate.

## Versioned engineering context

Keep Context, Feedback loops, Trajectory and guidance adoption in
`org-meta-bundle`. The separately selectable `work-with-requirements` package
owns the detailed requirements, contracts, verification planning and assessment
methods. Its skills share one maintained model. Preserve the repository's
lockstep release process; separate installation does not imply independent
version streams.

Consumers pin accepted releases and commit resolved lockfiles. Preserve source
artifact, owning package and version attribution in installed context and change
summaries. Project names, authority mappings, requirements, decisions and evidence
remain in the consuming repositories.

Classify versions by the impact on supported consumers, including obligations and
agent behavior, rather than file type:

| Release | Consumer impact | Adoption |
| --- | --- | --- |
| Patch | Correction or clarification; no required consumer changes | Eligible for automerge after required checks under the agreed repository policy |
| Minor | Optional or compatible additions; no required consumer changes | Eligible for automerge after required checks under the agreed repository policy |
| Major | Adoption requires changes to a consumer's code, requirements, architecture, configuration, workflows or agent instructions | Manual review with migration assessment |

Routine installation and regeneration of packaged context is the delivery mechanism;
it is distinct from a required change in how the consumer works or what it delivers.
A mandatory reassessment or migration is a major change, even if the package diff
contains only prose. Classify for all supported consumers: some may already comply
with a major release. During 0.x, a breaking release advances to 1.0.0 under the
existing release policy. Never move published tags.

Renovate proposes pin/lock updates and applies the agreed merge policy. Validate
installation, compilation and relevant behavior; checks alone cannot establish
semantic compatibility. A misclassified mandatory change must be corrected at its
source. Publication, repository adoption, refreshed agent context and completion of
migration are separate states. Refresh installed context after adoption and restart
sessions as required by the agent runtime.

## Major-update assessment

When assessing a guidance upgrade, compare accepted and proposed artifacts, release notes and
migration guidance. Identify applicable changes against local requirements,
architecture and implementation, and record already-compliant or inapplicable
findings with rationale. Propose requirement/NFR changes before implementation
work where new obligations are needed.

Create actionable repository work items for necessary changes with ownership,
acceptance criteria, dependencies and source attribution, within the caller's
messaging authorization. Summarize the diff, impact, proposed migration and any
exceptions for manual review. Do not merge or assert conformity automatically.
Adoption can precede implementation only with an explicit migration decision and
visible gaps; incompatible transitions must be sequenced before adoption.

## Trajectory changes and notification

Changes to adopted principles, obligations or shared architectural commitments
require an explicit decision at the layer owning the affected boundary. Identify
affected requirements, interfaces, parties and expected metric effects. Notify the
affected maintainers through their established handoff protocol, with old and new
baselines, rationale and required reconciliation. Propagate effects through actual
assignments; do not assume publication or a dependency PR alone establishes adoption.
An update PR is a useful notification and review surface, but unresolved migration
work remains visible after merge. Preserve historical evidence and decisions.
