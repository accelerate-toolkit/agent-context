---
name: develop-securely
description: Use when reasoning about security during design, implementation, review, testing or delivery, including libraries and infrastructure code. Apply proportionate secure-development practices and identify where local technical guidance is needed.
---

# Develop securely

Integrate security into the work being undertaken. Establish the assets, actors,
trust boundaries and plausible misuse relevant to the change, and inspect existing
requirements, decisions and local skills. Scale the depth to the exposure and
consequences; a small repository does not automatically mean low risk.

This is organization guidance informed by NCSC, not an NCSC certification or a
mandate to adopt every provision of its Software Security Code of Practice.
Installing this skill does not establish compliance. Do not turn an ordinary task
into an unsolicited whole-repository audit or impose new approval gates.

## Read only the relevant themes

- For feature design, dependencies and security tests, read
  [design and development](references/design-and-development.md).
- For repository, CI or release changes, read
  [source and build integrity](references/source-and-build.md).
- For updates, vulnerabilities, incidents and support, read
  [maintenance and communication](references/maintenance-and-communication.md).
- For authoritative provisions, applicability or refreshing the baseline, read
  [sources](references/sources.md). Consult the actual source before attributing
  a specific recommendation to NCSC.

## Connect guidance to the commission

Trace proposed system changes to existing approved requirements, including fixing
gaps against those requirements. Propose new obligations to their owning layer
before implementation when the current commission does not cover them. Routine
design choices within scope need no duplicate requirement. Use the repository's
existing requirement shape and review process.

Choose observations that exercise relevant abuse and failure cases as well as
successful behavior. Report the scope, revision assessed, actual evidence and
remaining uncertainty. A scanner result is limited to what it checks; missing
evidence is unassessed. Component evidence supports, but does not establish,
security of the assembled system. Use existing issues and the established
cross-repository communication protocol for affected shared boundaries, within
the user's messaging authorization.

## Develop local technical guidance

When recurring domain decisions need detail beyond these principles, encourage
the repository to create or improve a local skill. Examples include session and
OAuth/OIDC handling for an identity service, provider IAM and state protection for
infrastructure, or parser misuse cases for a library. Do not prescribe a token
lifetime, protocol, cloud service or architectural topology from this generic skill.

A useful local skill identifies its activation scope, authoritative standards and
provider references with revisions, the repository's adopted requirements, and
checks of the relevant technical boundaries. Keep private configuration and
project-specific decisions local. Skill installation supplies guidance; the
owning layer approves obligations. Create the local skill when it serves the
authorized work, rather than generating one for every incidental security topic.
