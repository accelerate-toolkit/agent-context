# SDLC consolidation and migration

## Requirements package extraction

The current source extracts detailed requirements, specifications and change
workflows into `packages/work-with-requirements`, with six skills sharing references
under `define-requirements/references/`. The original context paths retain adoption
pointers. This supersedes the earlier decision to defer splitting these methods;
Context, Feedback loops and Trajectory remain in `org-meta-bundle`.

The new component model separates received intent, local requirement derivation
layers, allocation by unchanged IDs, interfaces, and verification planning.
Actual evidence assessment has a separate skill. Existing IDs, authority and
published baselines remain unchanged.

The owner classifies this extraction as a feature release without a breaking
change designation. Consumers relying on the extracted methods must explicitly
add the new package at a published immutable release and update references to
the installed skills. Preserve assignments and historical evidence; review plan
coverage without treating it as actual satisfaction. Lockstep version planning
remains automatic; no release or consumer adoption is claimed by these source
edits. This classification does not change the general compatibility policy.

The content map below records the previous consolidated locations, now adoption
pointers for the extracted references. The remaining manual stays in the bundle.

## Previous consolidation

Status: the initial consolidation shipped in v0.11.0. The additional references
for knowledge maintenance, assembly, planning and research are prepared source
changes, not yet published. Consumer adoption is separate from either publication. The shared
manual is consolidated in `org-meta-bundle` so it can evolve in one place.
This supersedes the package-splitting prerequisite in issue #3 for this work;
independent release streams and a separate migration skill are not implemented
or needed for this consolidation. The existing lockstep release process remains.
The optional fake-external-services package retains its published entry point.

## Content map

| Material | Maintained source in the bundle |
| --- | --- |
| Context, Feedback loops, Trajectory, reusable setup and responsibility layers | [SDLC entry point](../packages/org-meta-bundle/.apm/context/software-development-lifecycle.context.md) |
| Requirements, decomposition, ownership, register convention, identity and evidence | [Requirements](../packages/org-meta-bundle/.apm/context/requirements.context.md) |
| Technical contracts, compatibility, editions, assignments and acceptance | [Specifications](../packages/org-meta-bundle/.apm/context/specifications.context.md) |
| Clarification, validation, immutable publication and cross-repository handoff | [Change workflow](../packages/org-meta-bundle/.apm/context/specification-change-workflow.context.md) |
| Adopted obligations, delivery measurements, guidance upgrades and trajectory changes | [Guidance adoption](../packages/org-meta-bundle/.apm/context/engineering-guidance.context.md) |
| Moves, distillation, archival and reference provenance | [Knowledge maintenance](../packages/org-meta-bundle/.apm/context/knowledge-maintenance.context.md) |
| Artifact handoff, sandbox isolation and deployed assembly identity | [Assembly and deployment](../packages/org-meta-bundle/.apm/context/assembly-and-deployment.context.md) |
| Outcome-led roadmaps, active milestone plans and feedback updates | [Roadmaps and milestones](../packages/org-meta-bundle/.apm/context/roadmaps-and-milestones.context.md) |
| Question-driven research, evidence limits and decision supersession | [Research and decisions](../packages/org-meta-bundle/.apm/context/research-and-decisions.context.md) |

Consumer-specific names, IDs, repositories, issue assignments, deployment details,
acceptance prompts, waivers and one-time history corrections are excluded. Examples
are fictional. The register convention is guidance; no validator is distributed
by this change. No security baseline is selected or withdrawn guidance restored.

## Compatibility and adoption

The owner classifies this consolidation as a feature release without a breaking
change designation. The previous manual reserved all derived requirements to a
single product repository. The consolidated model clarifies each receiving layer's
authority over decomposition within its commission, while its commissioning layer
retains authority over the commissioned obligation and interfaces between parts.
The release workflow computes the version from reviewed commits; development
metadata does not claim the release already exists. This classification does not
change the general compatibility policy for future releases.

Before adopting a published release containing this change:

1. Map local parties, requirement definition authorities, delivery owners and
   commissioned interfaces. Reconcile conflicts with the old centralized model.
2. Review register conventions and existing tooling. Preserve stable IDs, published
   snapshots, assignments and historical evidence. Plan any layout/tooling migration
   explicitly; installation does not perform it or authorize mass renumbering.
3. Separate reusable methods from local obligations, decisions and evidence.
   Replace duplicated method prose with references to the adopted manual only
   after the replacement is available locally. Keep local boundary mappings and
   specific acceptance criteria. Preserve existing documentation anchors used by
   local records when reducing their method text.
4. Pin the actual immutable release, preview installation, review the lockfile,
   install and compile. Check installed reference links and repository checks.
   Restart agent sessions after refreshing context.
5. Record unresolved migration work and notify affected parties within the caller's
   authorization. Publication, installation, migration and acceptance are separate.

Existing consumers remain on their accepted pins until adoption. This preparation
does not update component assignments, release specifications or close issue #3.
Its independent-distribution and automated migration work remains outside this
change; the latest consolidation decision supersedes splitting as a prerequisite.
