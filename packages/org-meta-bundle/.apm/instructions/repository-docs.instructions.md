---
description: Maintain repository documentation placement, navigation and lifecycle when creating or changing docs.
applyTo: "**"
---

# Repository documentation

Use `maintain-repo-docs` when creating, generating, editing, moving or removing
repository documentation, including documentation affected by implementation.
Reconcile affected docs as part of completing the work. Keep routine edits scoped;
this is not an instruction to reorganise unrelated existing documents.

Use `docs/README.md` as a concise navigation map. Link to the authoritative homes
below without duplicating their progress or assessment summaries:

| Location under `docs/` | Purpose |
| --- | --- |
| `context/` | Purpose, users, journeys and constraints. |
| `requirements/` | Owned and received obligations, component allocation and planned verification coverage. |
| `decisions/` | ADRs with stable indices plus topic names; rationale, assessed options and consequences. |
| `design/` | Subject-named, maintained system designs and permanent technical information. |
| `plans/` | Future work: draft, awaiting review, approved but unstarted, or deferred. |
| `wip/` | One folder per active implementation effort; README entry point, one or many documents. |
| `evidence/` | Observations, assessments, limitations and links to retained results. |
| `runbooks/` | Hands-on procedures, prerequisites, verification and recovery. |
| `workbench/` | Optional staging for future Cypherdown ingestion; no mandatory usage. |

Create folders only when needed. Until an actual ingestion/generation pipeline
exists, maintain documents directly without labelling them generated. Link to
established tool/module docs, contracts, schemas and executable tests where they
live rather than duplicating them. No dedicated `archive/` or `research/` is required.
Research accompanies plans/WIP; retained findings feed evidence, ADRs and design.

When execution starts, distribute the plan into subject-based design docs and a
WIP folder, record consequential decisions in ADRs, remove the consumed plan and
repair links. Before removing completed WIP, reconcile maintained docs and preserve
useful evidence and unresolved work. Git retains history. Superseded ADRs retain
their identities and successor links. Document location never establishes approval,
implementation, verification or acceptance.
