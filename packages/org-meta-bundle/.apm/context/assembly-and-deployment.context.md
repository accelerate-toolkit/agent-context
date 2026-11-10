# Component delivery and product assembly

Apply the [responsibility model](software-development-lifecycle.context.md) to
assembly as well as implementation. Identify the owning layer and its environment
boundaries in local context before changing deployment workflows. This guidance
does not authorize provisioning, teardown or migration of existing resources.

## Deliver artifacts and deployment interfaces

Components produce independently versioned artifacts and evidence from their own
testing loops. Deliverables can include images, binaries and reusable provisioning
modules, with contracts and usage instructions. A module describes provisioning;
it still needs an identified executable artifact. Modules and containers can be
complementary rather than mutually exclusive choices.

The assembling layer owns environment composition, wiring, deployment state and
credentials, promotion and integrated acceptance. Component-owned resource schemas,
runtime requirements and least-privilege policy definitions can remain with the
component's deployment interface. Keep infrastructure foundation responsibilities
explicit rather than silently assigning them to either party.

A decision to move deployment ownership is not evidence that migration occurred.
Inspect existing deployment roots and workflows, preserve infrastructure and state
identities, and plan the transition explicitly. Do not replace a running stack as
an incidental consequence of reorganizing repositories or documentation.

## Separate component sandboxes from integration

Component sandboxes serve component testing. Product assembly consumes versioned
artifacts, reusable modules and evidence, rather than depending on mutable component
sandbox services or test fixtures. Components can reset their sandboxes without
invalidating retained product acceptance setup.

The assembling layer maintains its integration environment with distinct runtime
endpoints, identity clients, credentials, application state and deployment state
where applicable. Integration, staging and preproduction can describe the same
role; those names do not require three environments. Local constraints determine
account, tenant, domain and state bindings; this method does not mandate a new
cloud account or a particular provider.

Exercise real component boundaries in integrated acceptance. Record substitutes
and missing integrations explicitly; component checks alone do not establish the
assembled user outcome. Retain verified shared setup independently of scenario
fixtures, following the [setup guidance](software-development-lifecycle.context.md#setup-as-a-reusable-feedback-loop).

## Identify candidate assemblies and actual deployments

Record the selected component versions in a versioned assembly description, using
existing project tooling where suitable. Identify exact source/release versions,
immutable executable identities such as image digests or archive checksums,
provisioning-module revisions and contract compatibility. Include client tools used
by acceptance journeys. Do not invent pins for unpublished artifacts or treat a
module version as sufficient executable identity.

An assembly revision identifies a candidate that evidence can assess. It does not
prove that candidate is running in any environment. Record each environment's
actual assembly revision, resolved artifacts, infrastructure/configuration revision
and last acceptance result. Test and production may intentionally run different
accepted revisions while a candidate is evaluated.

Keep environment-specific values and secret references separate from component
version selection. Promote identified, verified artifacts rather than rebuilding
unknown content at promotion time. If a dependency is still embedded in a consumer,
record that actual provenance; a separate manifest pin cannot change an already
built executable. A deployment record or successful provisioning run does not
replace integrated acceptance and the owning layer's acceptance decision.
