---
name: maintain-repo-docs
description: Use when creating, generating, editing, moving or removing repository documentation, including documentation changes accompanying implementation, ADRs, design documents, plans and WIP trackers. Covers document placement, lifecycle, navigation and consistency; not read-only browsing or prose outside a repository.
---

# Maintain repository documentation

Give each topic one maintained home. Before changing docs, inspect the repository's
navigation map, affected documents and their incoming references. Apply the
[document types and lifecycle](references/document-types.md) for the types involved.
Keep a narrow edit narrow; creating or updating a document does not authorize a
repository-wide reorganisation, execution of a plan or acceptance of a decision.

## Placement and navigation

Use `docs/README.md` as a concise navigation map, not a duplicate status register.
The standard homes are `product/`, `requirements/`, `decisions/`, `design/`,
`plans/`, `wip/`, `evidence/` and `runbooks/` under `docs/`. Create directories
only when they hold useful content. Optional `docs/workbench/` stages material
for future Cypherdown ingestion; do not require authors to use it. Until an actual
ingestion/generation pipeline exists, maintain the other documents directly and
do not label them generated. Preserve an existing real generated-source workflow.

Use `product/` for product intent and direction. Where that subject does not fit,
choose a meaningful subject name rather than a generic catch-all. Keep shared
methods in the adopted guidance and local application in the repository.

Keep tightly coupled tool/module documentation, executable tests, schemas and
contracts in their established authoritative homes and link to them. Respect
existing IDs, published baselines and repository ownership. Adopt the structure
within the requested work; describe wider migration needs without silently moving
unrelated documents. Do not introduce `archive/` or a dedicated `research/` category.
Preserve existing historical material until its references and retention needs are
understood; this convention does not require deleting an existing archive.

## Reconcile changes

When implementation changes documented behaviour, update affected design and
runbooks as part of that work. Keep proposed, accepted, implemented and verified
claims distinct. Preserve reviewed meaning, source attribution and uncertainty;
never infer approval from a document's folder or from a successful check.

At execution start, distribute a plan's agreed design into subject-named design
docs and its execution content into a WIP folder, capturing consequential choices
in ADRs. Remove the consumed plan and repair incoming links. At completion,
reconcile durable docs and retain useful evidence and outstanding work before
removing the WIP folder. Git retains document history; ensure uncommitted source
material is preserved in the resulting documents before removal. Do not discard
needed evidence on the assumption that all external artifacts exist in Git.

Use the installed `work-with-requirements` skills, when available, for requirement
definition, allocation, coverage planning, contract changes and evidence assessment.
This skill governs placement and maintenance, not those methods or authority to
change commissioned obligations. If those skills are unavailable, preserve the
consumer's existing requirements conventions rather than inventing replacements.

## Check the result

Check affected relative links, anchors and navigation after edits or moves. Use
existing documented repository checks where available. Confirm that no competing
current plan, duplicated definition or stale progress claim was introduced, and
that cited historical revisions still identify the content relied on. Report
unavailable evidence or remaining reconciliation explicitly. Structural checks do
not prove that a design is implemented or that requirements are satisfied.
