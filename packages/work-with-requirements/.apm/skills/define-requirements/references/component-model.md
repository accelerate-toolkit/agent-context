# Components, derivation and allocation

A unit is a component, not a team, repository or requirement group. Component
containment and requirement decomposition are distinct structures connected by
allocation. Record definition authority and accountable delivery ownership
explicitly; neither follows automatically from a diagram box or repository path.

## One component view

Intent contains received obligations. Explicit derived requirement layers appear
below intent. These layers represent decisions owned by the current component;
several requirement levels can precede allocation to an immediate subcomponent.
Branches can have different depths. Component depth and requirement depth are
independent. No intermediate component is needed merely because an obligation
requires another level of refinement.

Derivation creates a new stable ID under the decomposition parent. Allocation
references the same requirement ID in a receiving component. It does not copy
or redefine the obligation. On zooming into that component, the allocated
requirements become its intent and its own derivation becomes visible.

A received requirement may be allocated directly. Direct satisfaction requires
no duplicate child. Components with children may also satisfy obligations locally.
Each allocated obligation has one accountable delivery owner; decompose shared
work into separately allocated contributions. Keep supporting links distinct
from the single decomposition parent.

The commissioning component defines interfaces between its immediate parts and
owns combined outcome assessment. Receiving components own internal design and
further derivation within their commissions. Changes to received obligations
return to their definition authority.

## Example

Storefront receives R1, customers can purchase products. It derives R1.1, select
products, and R1.2, complete purchase. Below those it derives R1.1.1, browse the
catalogue; R1.1.2, select quantities; R1.2.1, review the order; and R1.2.2, confirm
payment. All these derivation layers remain within Storefront's view.

Catalogue's box references R1.1.1; Basket's references R1.1.2 and R1.2.1;
Checkout's references R1.2.2. Zooming into Basket shows those same IDs as intent.
These example IDs illustrate relationships, not newly commissioned obligations.
Consumer registers retain their canonical namespace and existing IDs.

## Verification and evidence

The verification plan links planned demonstrations to received and locally
derived requirements, acceptance criteria and interfaces. Child coverage is
visible separately from the current boundary's coverage. Planning establishes
how an obligation will be assessed, not whether it has passed.

Actual observations, applicability to revisions and satisfaction assessments
belong in a separate evidence view and workflow. Do not label planned coverage
as implemented, accepted or passing. Whether to use a particular evidence status
schema or the phrase “closed loop” remains a local decision; the model does not
require the prototype's five-state result scheme.
