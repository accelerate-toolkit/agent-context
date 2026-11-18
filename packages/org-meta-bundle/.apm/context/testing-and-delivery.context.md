# Testing and continuous delivery

Apply this strategy at each responsibility layer. A deployable repository owns
its implementation and deployment infrastructure code, including Terraform where
used. Components own their deployment interfaces and sandbox composition; the
assembling layer owns the composition and wiring between component deliveries.
Shared foundations retain their explicitly assigned owner. See
[assembly and deployment](assembly-and-deployment.context.md).

## Put coverage at the owning boundary

Use the smallest test boundary that owns the guarantee. Components own detailed
behaviour, local-provider acceptance, protocol handling, edge cases and fault
matrices. Product acceptance owns business-critical journeys through real assembled
components, their shared contracts and combined outcomes such as identity
isolation, recovery and durability. Do not copy component test matrices into the
Product suite. Repeated assertions should answer a different question at the
larger boundary or higher dependency fidelity.

Broad functional acceptance runs locally with controlled `4dev` fakes at the
system's external boundaries, without live-service credentials. A component can
fake its neighbours; Product uses the real internal components and fakes external
providers and clients. Local emulators may supply persistence. Identify each
binding and its limitations in evidence. Run real production clients/adapters
against protocol-compatible substitutes rather than bypassing those boundaries.

Fakes bear the weight of success, failure, recovery, onboarding, discovery and
authorization scenarios. Live smoke provides complementary evidence of deployed
wiring and selected real interactions; it does not repeat the entire acceptance
matrix. Neither a fake pass nor Terraform apply alone proves live interoperability.

## Require functional and deployment evidence before merge

For deployable changes, PR checks cover both:

1. Functional acceptance using local providers and controlled fakes.
2. Deployment of the candidate through the repository's infrastructure code and
   a passing smoke against the intended real providers.

Static Terraform checks and mocked plans provide earlier feedback but do not
replace deployment evidence. Scope smoke to meaningful application interactions
that establish routing, identity, permissions, configuration and provider access
for that deployment. Identify any fake clients or providers that remain; a
controlled client does not establish actual hosted-client compatibility.

Record the tested source, executable identities, infrastructure/module revisions,
configuration identity, provider lockfile, test revision and results. Never check
the last release and attribute that result to an unbuilt PR candidate. Invalidate
affected evidence after changes. Release the verified artifact; if rebuilding
changes its identity, qualify that artifact before promotion. Keep credentials,
tokens and raw secret-bearing state out of evidence.

Use applicable checks for documentation-only or non-deployable deliveries; do not
invent an environment deployment for an artifact that has none. The evidence
requirement does not prescribe GitHub-hosted deployment or grant cloud credentials
to dependency bots. A controlled runner can report checks through the existing
authorized mechanism. Missing execution machinery is an adoption gap, not a pass.

Dependency updates follow the automated delivery path while required checks remain
green. Behaviour changes first establish or update agreed automated acceptance
expectations and remain blocked while those expectations fail. A dependency update
requiring an intentional observable behaviour change follows the same rule.
Routine human acceptance is not a promotion gate; changing a commissioned
obligation still follows its owner's change process.

## Refine fakes through exploration

Exploratory testing against real providers and clients discovers behaviour that
the controlled model missed. Capture the observed exchanges, state transitions,
versions or observation date, environment and limits. Decide whether the mismatch
belongs in the fake, implementation or agreed expectation. An observed product
defect must not become the expected outcome merely to make a test green.

Update the owning fake and add a meaningful acceptance regression at the smallest
responsible boundary. Add Product coverage when the combined journey owns the
guarantee. Retain provenance and known fidelity gaps; use separately selectable
live comparisons where useful. Manual exploration improves automated protection
and happens outside routine promotion. It does not replace live-provider smoke.

Keep `4dev` fakes in the consuming component's repository and harness, alongside
its scenarios and fidelity checks. The simulated service's repository does not own
the fake. Consumer here means the component under test, including when the fake
acts as its client. Shared contract authority and real-provider conformance remain
separate. If reuse needs a published development artifact, its owning consumer
publishes it; packaging does not move ownership. Use lowercase fake names. The
optional `fake-external-services` skill provides implementation guidance.

## Separate candidate qualification from stable exploration

A mutable qualification environment receives PR candidates and can break while
infrastructure and real-provider assumptions are exercised. A stable exploration
environment receives the merged, qualified assembly. Promote the same identified
artifacts toward production with reviewed environment configuration. Use the same
deployment smoke in staging and production, parameterized for each environment's
endpoints, identities and fixtures. Local context names these roles and defines
recovery; retaining artifacts alone does not demonstrate rollback.

Preserve dedicated smoke identities, established client connections and minimal
shared resources across deployments and routine cleanup. Separate them from human
exploration identities and disposable run data. Provision, rotate, reauthorize or
replace them explicitly. Missing setup or expired authorization is a visible
failure, not an instruction to silently recreate the baseline and report success.
Smoke through a retained connection proves continued use, not fresh onboarding.

## Reserve shared environments for the whole execution

Use an **execution lease**, presented to users as an **environment reservation**,
independent of Terraform's state locks. CI and local developers acquire through
the same authority. Identify the product/component/environment scope and enforce
one execution at a time for each actual shared environment. Different scope labels
must not allow conflicting access to the same resources.

Acquisition is atomic and returns a unique owner token. Hold the reservation across
planning, deployment, tests, evidence collection or the manual session. The consumer
chooses a duration or deadline: a CI run might request 30 minutes and a manual run
the rest of the day. These are examples, not universal defaults. Heartbeats report
liveness without extending expiry; the owner can release early or explicitly extend
before expiry. An expired owner must acquire anew. CI waits for manual reservations.

Reject stale renewals and releases. Expiry revokes the old owner's permission but
cannot cancel an already-running Terraform or provider operation. Fence new writes
and drain or reconcile in-flight work before admitting conflicting execution;
uncertain environments remain blocked. Owner tokens alone do not fence provider
writes. Select the lease backend, enforcement and recovery mechanism explicitly.

## Adoption

Record the local coverage, candidate runner, smoke scope, fixture lifecycle,
environment reservations and remaining gaps before claiming compliance. This
guidance requires deployment evidence before merge and an automated promotion
path; consumers lacking these capabilities need a migration assessment. Treat
publication as a breaking guidance change under the shared release policy, not
as documentation-only housekeeping. Publication, pinned adoption and implementation
are distinct; do not silently revise commissioned criteria or historical verdicts.
