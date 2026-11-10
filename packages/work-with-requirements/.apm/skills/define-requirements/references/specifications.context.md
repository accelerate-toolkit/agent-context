# Specifications, contracts and acceptance

Apply the [requirements model](requirements.context.md)
between product and components, between lower-level parts of a
component, and with external suppliers. Each owning layer decomposes its outcome
into obligations, defines the interfaces and acceptance criteria, and commissions
the lower layers to deliver them. Feedback flows upward; decisions and revised
specifications flow downward.

The layer that owns the decomposition and interfaces retains decision authority.
Suppliers own implementation within their assigned scope and may repeat the
pattern for their own internal decomposition. They cannot redefine higher-level
obligations or negotiate binding contract changes directly with other producers
or consumers. The commissioning layer owns interfaces between the parts it
commissions; each lower layer owns its internal design and subordinate interfaces
within that delegated scope.

## Delegate capability requirements at the appropriate level

The commissioning layer specifies product-specific outcomes, constraints, shared
interfaces and observable acceptance obligations. It does not reproduce the full
catalogue of standard requirements expected of a supplied capability. Delegate
research and definition of that capability's complete requirements, detailed
specification and verification to its owning component or supplier.

The receiving layer owns those derived requirements within its delegated scope,
including capability completeness beyond the journeys selected by the current
milestone. It records their rationale and traceability to the commission and owns
its detailed acceptance suite. Routine refinement within that scope does not
require higher-level decisions. A proposed change to a commissioned outcome,
constraint, acceptance obligation or shared interface must return to its owner;
producers and consumers cannot change those obligations by bilateral agreement.

This separates authority over the commission from authority over its decomposition.
Higher-level acceptance assesses the delivered capability and returned evidence;
it need not enumerate or duplicate every lower-level requirement or test.

## Requirements and technical contracts

Requirements explain the context, why a capability is needed, what must be delivered,
constraints and observable acceptance. They may impose interface constraints but do
not substitute for a technical exchange definition.

A shared contract specifies the exchange itself: protocol and transport profile,
operations, request/response or event schemas, field meanings, authentication and
correlation, error representation, ordering/retry/recovery interactions and compatibility.
Include only details that parties need to exchange information correctly; link to the
requirements for rationale and acceptance. A narrative list of behavioral obligations
is not a complete technical contract.

The commissioning repository manages the authoritative technical contracts between
its commissioned parts, including schemas and protocol bindings. It defines, reviews,
versions and publishes them. Components may contribute proposals and feedback here;
they do not independently publish binding interpretations or negotiate changes between
themselves. External standards remain owned by their providers; this repository owns
the selected profile and product-specific extensions or mappings.

Components own internal design, storage schemas, algorithms, adapters and test harnesses.
They implement producer and consumer tests against the same published technical
contract. An exchange schema is not an internal implementation detail simply because
it is technical. Generated bindings and local copies identify their exact authoritative
source; they are not separate authorities.

Keep requirement editions and technical contracts separate and cross-reference them.
A component edition states its required outcomes and the exact contracts it must provide
or consume. Context-only material is labelled separately. Publishing requirements can
commission assessment and independent work, but interoperability work with a missing
technical contract remains explicitly blocked pending owner publication; components
must not fill that gap through private agreement. Record draft, published, deprecated
and superseded status explicitly, preserving immutable historical tags and assignments.

## Versioned specifications, contracts and context

Publish independently versioned component specification
**editions as browsable Markdown**, not downloadable specification packs. Each
component has an index identifying its applicable requirements, interfaces,
observable acceptance criteria, scope and necessary rationale. Link to
authoritative material rather than maintaining copied requirements. Preserve
stable requirement IDs and exact source provenance. Acceptance test-suite versions
can be identified independently where needed; matching software/specification
version numbers do not establish conformity.

## Semantic versioning

Use Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`) across independently released
software, specification editions, shared contracts, and separately published
acceptance suites or agent-context packages. Each has its own version sequence
and declares the public interface or obligations against which compatibility is
assessed. Version numbers need not match across artifacts; matching numbers do
not prove conformity or compatibility.

| Change | Version increment |
| --- | --- |
| Incompatible change to a public interface, commissioned obligation or observable acceptance criterion | Major |
| Backward-compatible functionality or optional capability added without invalidating existing supported use or conformity | Minor |
| Backward-compatible defect correction; for specifications, clarification that does not change required behavior or acceptance obligations | Patch |

For specifications, adding a mandatory obligation that invalidates a previously
conforming delivery is a breaking change, even if the text is purely additive.
For contracts, assess both producer and consumer obligations; a change compatible
with only one side is not automatically backward-compatible. A clarification that
changes required behavior is not a patch. The owning layer records the rationale
and impact of the version increment.

The first binding specification and contract editions start at `1.0.0`. This does
not assert implementation readiness or reset existing software release sequences.
SemVer permits `0.y.z` for initial development and prerelease identifiers for
unstable releases; these must not be presented as stable compatibility promises.
Published versions are immutable. Build metadata does not change version precedence
or replace exact artifact identity.

Assignments and assemblies pin exact versions and commits or artifact digests.
A compatible version increment does not automatically reassign work, establish
conformance or authorize an assembly upgrade. Producer/consumer evidence and the
commissioning owner's acceptance remain required under the assigned baseline.

## Component editions and immutable references

Declare independent tag namespaces for specifications and contracts. For example:

| Specification | Tag convention |
| --- | --- |
| Component | `<component>-spec/v<version>` |
| Shared contract | `contract/<contract-name>/v<version>` |

The component index at the tagged revision defines that edition's scope. Although
a tag captures the entire repository, publishing one component specification tag
declares only that component edition; it does not publish or assign editions for
other components.
Components can therefore remain assigned different specification versions.
Software release versions are separate from specification edition versions.

Published specification and contract tags must never move or identify different
content. Record both the tag and its resolved full commit in assignments, deliveries and acceptance
records. Link directly to the index at that tagged revision; do not use `main` as
a binding baseline. Use the full commit reference when an exact immutable target
is needed. Normal editing on the default branch does not revise a published edition.

An edition's same-revision relative links resolve within its tagged snapshot.
References to independently versioned shared contracts must explicitly name the
contract tag and commit, with a version-pinned link. Review all normative links
for complete scope and fixed versions before publication; an unpinned external
link must not silently change an assigned obligation.

Shared interface contracts have one authoritative definition. Component editions
state whether they provide or consume each exact contract version. A producer edition requires provision of an identified contract version; consumer
editions require consumption of that same version. The layer owning the interface
owns its authoritative technical definition, including schemas, and approval and
publication of changes. Components can contribute proposals in the commissioning
repository but cannot independently define the shared exchange or change its meaning.

## Separate agent context

APM manages product purpose, wider specification context, rationale, architecture
and working guidance for agents. An assignment may identify both a binding
component edition and a product-context baseline. Context helps understanding but
does not silently add or change obligations. Any contextual document intended to
be binding must be explicitly incorporated by the formal specification at an exact
version. APM updates do not automatically revise component assignments.

External suppliers can browse the same versioned Markdown without APM. No package
registry or archive download is required for the specification handoff; executable
acceptance checks can be checked out at their assigned revisions. Their execution
prerequisites remain explicit. A future documentation site may present the same
source without becoming another authority.

Publication requires complete edition scope and fixed normative references under
the semantic versioning rules above. The repository edition directory
records published baselines separately from software conformity and assignments.
Automation of publication or assignment issues is not a prerequisite for a manually
reviewed edition.

## Assignment, delivery and acceptance

Use GitHub issues for component work assignments and returned delivery evidence.
Issues reference the exact published component edition index, tag and commit and applicable contract
versions rather than maintain copied requirements. Include the required outcome,
deliverables, dependencies and open questions. A supplier outside GitHub can use
an equivalent record without changing the pattern.

The lower layer reviews its current implementation, designs the solution and
implements/tests against the assigned baseline. Delivery through the issue identifies
software artifacts and their exact versions/digests, the specification and contract
versions claimed, executed acceptance results and evidence, and deviations or
remaining limitations. Keep failed, blocked, skipped and unrun checks distinct.

The commissioning owner records accepted, rejected or incomplete against the
assigned criteria. A closed implementation issue, a supplier's conformity claim
or passing producer tests alone is not an acceptance decision. Product binds
accepted software releases to specification/contract versions in its assembly
and verifies the integrated product journey. Producer conformance and
consumer contract tests use the same formal contract; neither replaces product
acceptance or authorizes bilateral contract changes.

## Observable obligations and component-owned verification

The specification owner defines observable acceptance obligations: what a delivery
must demonstrate at its boundary, not the detailed test procedure or implementation.
Components own their acceptance harnesses, fixtures, fakes, detailed acceptance
cases, integration/unit/regression tests and coverage strategy. Test sketches live
in component repositories as starting material, not prescribed product procedures.
Components maintain those suites alongside implementation and trace their evidence
to the assigned requirements/contracts. Product retains assembled user-journey
acceptance and decides whether returned evidence demonstrates conformity.

A shared contract defines observable obligations on both sides. Producer and
consumer own their respective test implementations against that same definition;
neither can weaken it to make tests pass. Missing or ambiguous required behavior
returns to the owner for decision. Missing test detail belongs to the component.

## Fakes within component test harnesses

Each component maintains its own dependency fakes within its test harness and
owns their scenarios and fidelity checks. Fakes follow the published contracts
consumed by that component; they are not shared deliverables and need no separate
publication process or prescribed framework.

For detailed fake design, the separately installable `fake-external-services`
package provides the method. Adopt a published release explicitly when needed;
this package does not install that optional skill. Component ownership and
acceptance obligations remain as defined here.

Passing against fakes supports component acceptance. Real integration evidence
is still required to establish agreement between components.

## Component conformity and milestone coverage are separate

A product milestone selects user outcomes and assembled acceptance journeys; it
does not define the complete set of component obligations. A component capability
can be required and need component-owned acceptance coverage even when no current
milestone journey exercises it.

Record component requirement applicability and component acceptance separately
from milestone journey coverage. Absence from a milestone journey is not a waiver or deferral of
an agreed component requirement. Only an explicit decision by the requirement
owner changes its obligation. Component editions must distinguish requirements
from the subset exercised by a particular milestone; no component-wide conformance claim follows
from that milestone subset alone.

## Specification changes trigger work

Follow the [specification change workflow](specification-change-workflow.context.md)
for decisions, validation, immutable publication and assignment handoffs.

Publishing a changed component specification triggers an assignment to the
affected component, identifying its previous and new required versions and the
changed obligations. Track required specification version separately from the
accepted version demonstrated by the component. A difference exposes outstanding
work; publication alone does not establish adoption.

Required work can be implementation changes, new verification, or evidence that
existing behavior already conforms. A changed edition cannot be silently ignored,
but does not necessarily require a code change. Context-only updates do not
change component obligations. Record explanatory versus behavioral changes so
the impact is explicit.

A changed shared contract triggers owner assessment of all affected producers
and consumers. Publish affected component specification editions with exact contract
references and issue updated assignments. Do not silently advance existing work
to a new baseline or relabel historical evidence as passing the revised contract.

## Implementation feedback and controlled change

When implementation surfaces a new need, raise a change request to the contract
or requirement owner against the exact assigned version. Explain the need,
affected criteria/consumers, evidence, proposed change and impact of leaving the
baseline unchanged. Producers and consumers may supply analysis and proposals;
only the owning layer decides whether to clarify, change, defer or retain the
obligation. No private agreement changes the authoritative contract.

If approved, the owner publishes a revised contract/specification baseline,
identifies affected component editions, and issues revised assignments. Components
return conformity evidence against those versions; the owner accepts delivery
and updates the compatible assembly. Until explicitly reassigned, the existing
baseline remains binding. Report blocked work explicitly and continue independent
work. Preserve prior baselines, acceptance decisions and evidence.
