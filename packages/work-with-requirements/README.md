# Work with requirements

This separately selectable APM package provides one requirements model and six
workflows for software components. Context, Feedback loops and Trajectory remain
in `org-meta-bundle`. The packages release in the repository's lockstep stream.

| Skill | Outcome |
| --- | --- |
| define-requirements | Observable obligations and acceptance criteria. |
| decompose-and-allocate-requirements | Explicit derivation layers and allocation to components. |
| plan-requirement-verification | Planned checks, coverage relationships and gaps. |
| change-requirements-and-contracts | Controlled changes to obligations, contracts and assignments. |
| assess-requirement-evidence | Assessment of actual observations against revisions. |
| visualize-requirements | Component views generated from authoritative records. |

The shared manual is under
[define-requirements/references](.apm/skills/define-requirements/references/requirements.context.md).
All six skills ship together; their relative links work in source and installed
skill directories. No renderer, validator, requirement database, test harness or
result schema is installed. The visualisation skill guides rendering with the
consumer's tools; it does not ship the exploratory Claude artifact.

## Adoption and compatibility

This package is prepared source until an immutable release containing it exists.
Consumers select `accelerate-toolkit/agent-context/packages/work-with-requirements`
with an explicit published release pin; do not use the current development
version as evidence that such a release exists. In this repository, the root
manifest installs it through a repository-local path for development.

The compatibility contract includes skill entry points, reference paths,
requirement identity and ownership conventions, and prescribed workflow behavior.
Removing detailed methods from `org-meta-bundle` requires consumers that use them
to add this package. The owner classifies this extraction as a feature release; existing IDs and
records are preserved. Adding the package remains an explicit consumer adoption
step. This classification does not change the general compatibility policy.

Review existing registers, links, commissions and evidence before adoption.
Preserve IDs and published baselines. Do not infer migration completion from a
successful installation. Refresh and compile agent context, then restart sessions.

The verification plan is distinct from actual evidence: planned coverage does
not imply execution or acceptance. Evidence dashboard states and automatic
acceptance rules remain project decisions rather than new universal obligations.
