# Specification change, publication and handoff

Use this workflow for changes to commissioned requirements or shared technical
contracts. Apply the [authority and compatibility rules](specifications.context.md).
The loop is inspect, decide, prepare, validate, publish, reassign and close.
An assessment request alone does not authorize publication or external messaging;
respect the caller's existing authorization and execution permissions throughout.

## Inspect and decide

Read the originating request and its discussion, current assignments, published
baselines and prior decisions. Issue text may lag a reassignment. Use `work-on-gh-issues` when installed and beginning repository issue work;
otherwise inspect the current issue and discussion through available tools.

State the decision, affected requirements and contracts, producer/consumer scope,
and observable acceptance before editing. Trace all affected parties rather than
only the requester. Components retain ownership of internal design, harnesses and
provider research. Keep required baselines separate from accepted deliveries.

## Prepare the coherent change

Update authoritative clauses, technical exchanges, affected edition indexes,
acceptance obligations and current planning records. Preserve superseded decisions
as history. A behavioral requirement list does not substitute for protocol bindings,
schemas, field and error meanings, trust, ordering, retry effects and compatibility.
A complete narrow contract can publish while unrelated drafts remain blocked.

Assign new versions only to changed artifacts and explain the consumer impact.
Follow the compatibility policy; do not generalize an initiative's pre-live
exception into permission to move tags or downgrade breaking changes. Edition
titles and normative links must describe the exact intended publication.

Existing contract dependencies identify exact tags and full commits. For an
explicitly co-published new contract, name its exact tag and require its resolved
commit to equal the edition's own immutable commit; link the same-snapshot
contract definition. Verify that equality during publication. Moving branches,
sibling checkouts and unresolved placeholders are not binding baselines.

## Validate and review

Run `make` to discover repository actions, then the applicable documented checks.
Validate documentation links, schemas, examples and relevant failure boundaries.
Schema validation does not establish provider interoperability or product acceptance.
Report executed checks and their limits. Add meaningful tests for consequential
publication tooling if it changes.

Edit instruction/package sources rather than generated agent files. Preview APM
installation before refreshing managed content, compile instructions, and review
the manifest/lock and generated changes. Dependency upgrades are deliberate
adoption decisions, not incidental consequences of editing a specification.

Prepare a reviewable diff and a complete Conventional Commit message. Follow the
repository's commit and publication authorization; do not ask again for actions
already authorized. A restricted execution profile still applies: prepare allowed
artifacts and human commands instead of using another mechanism to bypass it.

## Publish immutable baselines

Inspect the reviewed commit pushed to the intended remote and the existing remote
tags before creating references. Publish only new tags for changed artifacts. If
a tag already resolves to the expected commit, reuse it; if it points elsewhere,
stop and report the conflict. Never force, move or replace a published artifact.

Use the repository's established release mechanism. On retries, inspect remote
state and resume matching publication rather than blindly creating references.
Resolve annotated tags to commits. Verify remote tag commits before assigning
exact baselines, and record publication separately from implementation acceptance.

## Reassign, notify and close

Within authorized messaging scope, use `collaborate-cross-repos` for handoffs when installed; otherwise prepare
the handoff through the project's established authorized communication process.
Update current assignment titles and bodies as well as recording the decision in
the discussion; preserve history and existing implementation checklists.

Each handoff identifies previous and new baselines, exact edition/contract tags
and commits, immutable index links, changed obligations, required producer/consumer
evidence and remaining blockers. Read back assignments to verify the references.
Keep delivery work open until its own acceptance; publication does not promote a
conformity claim or accepted version automatically.

Close the originating clarification only when its scoped publication and handoff
are complete, with links to the evidence. If the user explicitly requests earlier
closure, name the remaining work. Refresh edition/status records without changing
historical tagged snapshots. Scope draft blockers precisely: publishing one
contract does not make adjacent unfinished protocols ready for integration.
