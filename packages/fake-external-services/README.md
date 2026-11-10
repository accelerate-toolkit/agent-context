# Fake external services

Optional APM package supplying the [fake-external-services skill](.apm/skills/fake-external-services/SKILL.md).
It guides component-owned service fakes, contract fidelity, state and fault controls,
human control interfaces, live inspectors, and verification limits. It supplies guidance, not a fake server or a framework.
It has no dependency on org-meta-bundle and can be selected independently.

## Adoption

The package was introduced in v0.10.0. The development-fake blueprint is a new
addition and is not available in that original release. After its publication,
install `accelerate-toolkit/agent-context/packages/fake-external-services` pinned
to an actual release containing the blueprint. Preview installation, review the
manifest and lockfile together, install and compile, then restart the agent session.
Do not use an unpublished tag or a sibling checkout as a consumer dependency.

Maintainers develop it through the root local devDependency. Existing bundle
consumers receive it only when they explicitly add the optional package. Projects
retain their ownership rules and acceptance obligations; replace duplicated method
guidance only once the published skill has been adopted.
