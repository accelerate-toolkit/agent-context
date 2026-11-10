# Requirements, delegation and evidence

A requirement states an obligation and how its satisfaction will be assessed.
There is one requirement entity at every layer. Business origin, product or
component scope, subject and ownership describe a requirement; they do not create
different entity types. Record provenance and rationale separately from who owns
the obligation and who delivers it.

For each requirement, its owner can decompose it into further requirements,
satisfy it directly, or delegate its delivery. These choices can be combined:
an owner can satisfy some subrequirements and delegate others. The receiving
party applies the same model within its scope, including further decomposition
and delegation. Local context identifies the parties and their commissioned scopes.

The core relationships are:

| Relationship | Meaning |
| --- | --- |
| Requirement decomposes into requirements | Subrequirements explain the obligations needed to satisfy their decomposition parent. Contributions to other requirements are separate supporting links. |
| Requirement is owned by a responsible party | The owner controls its meaning, assessment criteria and acceptance. |
| Requirement is delegated to another party | The recipient delivers against the commission; the commissioning owner retains authority over it. The recipient owns its further decomposition within that scope. |
| Evidence supports a requirement's assessment | Evidence establishes what was demonstrated against the identified requirement revision. The owner decides whether it is sufficient for acceptance. |

Decomposition and delegation alone do not establish satisfaction. Passing
subrequirement checks supports the parent assessment, but does not automatically
prove completeness or correct integration. The parent owner assesses whether
the decomposition and combined evidence satisfy the parent obligation, including
any verification needed at that boundary. A journey may exercise several
requirements, and a requirement may need several journeys or assertions.

## Minimum record and evidence

Keep useful scope, rationale, source references and commissioning context in the
requirement description itself. Acceptance criteria remain a separate section.
Do not add a standard "Scope and rationale" section, generic ownership/evidence
disclaimers or migration commentary. Include only context needed to understand or
fulfil this obligation; avoid repeating the parent when it adds no meaning.

Requirement and Evidence are the core concepts. A requirement needs a stable ID,
a statement of what must hold, acceptance criteria describing how satisfaction
is judged, and a lifecycle status. Ownership can be inherited from its containing
document or repository; provenance and shared baselines can be recorded at document
level rather than repeated on every requirement.

Add information as work requires it: parent links when decomposing, recipient and
agreed scope when delegating, evidence and assessment when verifying, and the
owner's decision when accepting. Keep required evidence, available evidence, and
missing or explicitly excluded evidence distinguishable. Exclusions record the
reason and owner's decision; they do not imply satisfaction or waive the obligation.

Tests, journeys, assertions and reviews define ways to obtain or assess evidence;
their definitions alone do not demonstrate satisfaction. A journey can produce
evidence for several requirements, and a requirement may need several evidence
sources. Evidence can be a lightweight reference to observations, results,
screenshots, transcripts or reviews, identifying what it demonstrates, the applicable
revision or situation, and its limitations. This model does not require a separate
Run entity, global evidence IDs or automatic execution capture. Specific acceptance
procedures can still require run records and provenance appropriate to their scope.

Evidence supports closing a subrequirement through acceptance by its owner. Missing
or unexecuted checks are not passes, and later changes do not rewrite historical
results. Delegation does not authorize a recipient to redefine the commissioned
requirement; proposed changes return to its owner.

## Keep product obligations separate from delivery practice

Product requirements state observable capabilities, quality constraints and shared
boundaries. Development rules, evidence handling, fixtures, release procedures and
assessment methods live in repository delivery policy and their owning
runbooks. Evidence reporting is an SDLC practice derived from requirements, their evidence
and assessments; it is not a separate product capability or dashboard commission.

Keep product constraints and shared contract guarantees at the commissioning
layer. Components own interaction wording, internal algorithms, storage choices
and detailed local capability requirements. Direct satisfaction needs no duplicate
child requirement. Acceptance criteria identify the relevant observations and
failure boundaries; test steps and actual results remain separate.

## Decompose to the appropriate level

Decompose only far enough to commission and accept meaningful work at the current
level. Define relevant outcomes, constraints and acceptance expectations, leaving
the implementing party room to research and specify the detailed requirements.
If further decomposition requires knowledge of the recipient's internal design,
delegate that decomposition to the recipient. Still specify mandatory shared
constraints and interfaces at their owning level.

For example, a commission could require following an agreed security guidance baseline. Its acceptance criteria would require the recipient to
identify applicable guidance and revisions, justify applicability and departures,
and supply evidence against the resulting security requirements. The recipient
owns the detailed security specification and verification; the commissioning owner
assesses whether these satisfy the commission. This example does not itself add
a security obligation or select a guidance baseline.

## Single ownership and allocation authority

Every requirement has exactly one accountable delivery owner. The owner either
satisfies it directly or delegates it to exactly one receiving owner. If delivery
needs multiple owners, decompose the requirement into separately owned children
before delegating them; do not assign one requirement jointly to several parties.
The parent owner remains accountable for the combined outcome and integration.

Distinguish the commissioning authority from the receiving delivery owner. The
commissioning authority retains control of the delegated obligation and accepts
the returned evidence; the recipient owns delivery and further decomposition
within that commission. Delegation does not create two competing authorities
over the requirement's meaning.

Record the delivery owner and, for delegated requirements, the commissioning
authority and delegation scope. Document-level ownership defaults are sufficient
only when they make the owner of every requirement unambiguous; record exceptions
explicitly. Parent links and delegation records must make it possible to identify
who delivers each requirement and who accepts the result. Slugs and
repository location alone must not be used to infer a delegated assignment.

The owner responsible for decomposing a requirement controls allocation of its
immediate child numbers. It allocates distinct children before delegating them to
different parties. Each recipient controls further child allocation beneath its
assigned requirements, within the delegated scope. Contributors request numbers
from that allocation owner rather than allocating competing children independently.

The commissioning authority maintains and approves the party registry. Use
canonical party names, such as ExampleProduct, Accounts and Catalog, directly
without separate lowercase keys. Each requirement has one registered delivery owner, never a list
or a shared owner. These parties represent durable responsibilities; individual
work assignees are separate. A component that needs a new receiving party must
request its configuration and approval from the registry owner before delegating. Until
approval and delegation, the existing delivery owner retains responsibility.

The authoritative repository establishes who maintains a requirement's definition.
A delivery owner can refine its locally maintained decomposition within the assigned
scope, but requests changes to the commissioned obligation in its maintainer's
repository. Refinement of the same obligation retains its ID; replacement by a
different obligation creates a new ID and supersedes the original. Retiring a
child must not silently remove an obligation of its parent.

## Repository requirement registers and local context

Use this shared register convention across collaborating repositories. During
adoption, map existing records without changing stable IDs or losing history:


```text
docs/workbench/requirements/
  README.md
  parties.md
  upstream/
    ExampleProduct/
      EXM.1/
        EXM.1.2.md
  owned/
    EXM.1/
      EXM.1.2/
        EXM.1.2.1.md
```

Paths and IDs above are illustrative. `owned/` contains authoritative definitions
maintained by this repository. `upstream/<MaintainingParty>/` contains copies of
assigned requirements maintained by that named party. Either kind can be satisfied
locally. An upstream requirement can be decomposed into owned requirements; an
owned requirement can be delegated further. There is no need to invent a child
merely to implement an upstream obligation directly. The folders distinguish
definition authority, not delivery routing.

A requirement with locally stored descendants uses a directory named
`<canonical-ID>-<slug>`, with its own content in `_index.md`. Leaf requirements
use `<canonical-ID>-<slug>.md`; they need no folder or index file. For example:

```text
owned/
  EXM.1-catalog/
    _index.md
    EXM.1.1-create.md
    EXM.1.2-search/
      _index.md
      EXM.1.2.1-fidelity.md
```

These slugs illustrate the convention; they do not allocate new obligations.
A slug is a short, lowercase, hyphen-separated navigation hint. It is distinct
from both the canonical ID and the requirement title: for example, ID `EXM.1.2`,
slug `search`, and title “Find catalog entries”. Choose it deliberately rather
than generating it from the title. It may be shorter than the title and does not
change automatically when wording or the title is refined. It is not a valid cross-repository reference by itself.

Keep slugs stable during ordinary edits. A proposed substantive slug change is
a signal that intent or scope may have changed: raise a new review ticket before
renaming it. The requirement maintainer decides whether this remains the same
obligation or requires a replacement requirement with a new ID and supersession
of the original. Correcting a typo does not by itself imply a new requirement.

The heading always repeats the canonical ID. `_index.md` distinguishes parent
content from child branches; exact display order depends on the listing tool.
Structural ancestor folders do not imply copying upstream ancestor definitions.
Use the same rule within each `upstream/<MaintainingParty>/` directory. An upstream
copy can be a leaf locally even when its authority maintains further descendants;
the requirement content and ID remain the same despite the different local path.

Cross-repository requirement references use canonical IDs,
not storage paths. Authority and the storage convention resolve those references;
local navigation links may point to files. Moving files does not change identity
or assignments.

Each heading begins with the canonical ID followed by a short,
descriptive title. Titles help scanning; statements and acceptance criteria carry
the precise obligation. Do not encode owners, lifecycle status or implementation
details in titles. A minimal owned definition is:

```markdown
---
id: EXM.1.2.1
status: Proposed
---

# EXM.1.2.1 — Session expiry

## Description

Statement of the obligation, with useful context and references.

## Acceptance criteria

How satisfaction will be judged.
```

YAML frontmatter is the metadata authority. Require `id` and `status`; the ID must
match the heading and storage path. Use `delivery_owner` for an explicit recipient
or an ownership exception; omission retains the repository default. Optional
`supports` and `superseded_by` are YAML lists of canonical requirement IDs, not
comma-separated strings. A Superseded requirement requires `superseded_by`.
Duplicate or unknown metadata keys are
invalid. Repository validation should use safe YAML parsing and check types and section order.
This guidance does not install a validator.
Description and Acceptance criteria must both be present and non-empty. Metadata
examples inside prose do not change the actual frontmatter values.

The repository's `README.md` declares its canonical party, scope and shared
conventions. Lifecycle status is mandatory in every requirement file. An omitted
delivery owner in `owned/` defaults to the repository's declared party. Delegation
requires an explicit `delivery_owner` naming the approved recipient. The recipient
preserves that field in its upstream copy; defaults do not reassign copied
requirements.

Keep evidence and assessments separate from requirement definitions. Acceptance
criteria describe the required demonstration; actual results, evidence references
and acceptance decisions evolve independently and identify the revisions assessed.
Their storage remains flexible and a current view may be generated dynamically.
An automated latest-pass view is not an owner's acceptance decision.

Delivery owners take stock of incoming assignments locally, including their
decomposition or direct delivery approach, progress, evidence and outstanding gaps.
The upstream tree makes assigned definitions locally readable without turning
them into independently editable obligations. Copy each assigned requirement
directly from its authoritative repository's `owned/` directory, never through
another consumer's upstream copy. The maintaining-party directory records source
authority; no separate provenance index or commit field is required in each copy.
Git history and cross-repository handoffs retain the assignment/change history;
evidence still identifies the exact revision it assessed.

The commissioning repository's `parties.md` is the authoritative party registry. Other
repositories retain complete synchronized copies obtained directly from that authority,
so agents can interpret assignments and owners locally. They request
registry changes from the authority rather than edit competing definitions. Keep the
shared requirements convention available locally through APM context. Registry
copies and applicable context refresh with assignments that depend on changes.

## Assignment notification and refresh

The requirement maintainer initiates notification whenever an assignment changes,
using the `collaborate-cross-repos` communication protocol. Identify the requirement,
previous and new assigned baselines, what changed, and effects on scope, acceptance
or delivery ownership. Publication alone is neither notification nor adoption.

On notification, the recipient refreshes its upstream copy directly from authority
and reconciles its local register, decomposition and required work. Copies represent
the current assignment rather than independently selected versions. A pending
refresh must remain visible until reconciliation completes; do not silently assume
a notified but unprocessed copy is current. Refresh supporting registry/context
copies when the changed assignment needs them. Retain historical evidence rather
than relabel it as satisfying the new revision.

Copy only explicitly assigned requirements, not their ancestors or unrelated
branches. Each commission includes enough rationale and scope to be understood
and fulfilled locally; parent references support deeper exploration. If an ancestor
change affects a delegated obligation, its maintainer propagates the change through
the affected requirements and notifies their delivery owners. Unaffected assignments
need no refresh. Local context must be sufficient to fulfil the assignment without
creating untracked ancestor copies that can become stale.

## Requirement identity, hierarchy and slugs

Choose a stable project namespace. Canonical IDs use that prefix followed by dot-separated,
unpadded positive integers, such as `EXM.1`, `EXM.1.1` and `EXM.1.1.2`.
Numeric segments describe recursive requirement decomposition. Decompose by
intent or concern, independently of component allocation; assignment to an implementing party is recorded separately. A requirement
has one decomposition parent; supporting relationships do not introduce additional
ID paths. Reassigning delivery does not change its identity or hierarchy.

IDs are immutable references, not document section positions. Do not renumber
them to reorder a document, close gaps or reorganize implementation. Dropped
requirements retain their IDs and records; never reuse them. A change to the
decomposition that replaces a requirement retains its original record and links
the replacement rather than changing the original ID.

Canonical IDs are the references used in metadata and across repositories. Short
slugs make files and folders readable; they do not create another namespace or
replace identity. For example, `EXM.1.2-search.md` stores requirement `EXM.1.2`.
Use the canonical ID to locate the current file independently of its slug.

Lifecycle status is separate from delivery progress and satisfaction:

| Status | Meaning |
| --- | --- |
| Proposed | Awaiting agreement. |
| Active | An agreed obligation, whether or not its implementation has been accepted. |
| Retired | No longer required; preserve the reason and decision. |
| Superseded | Replaced; preserve links to replacement requirements, including splits or merges. |

## Delivery state and satisfaction assessment

Record delivery progress separately from demonstrated satisfaction. For example,
not started, implementing and ready for acceptance describe progress; implemented
does not by itself mean accepted or that the desired quality has been achieved.

Each requirement defines its assessment method:

| Assessment | What must be defined |
| --- | --- |
| Binary conformity | The observable condition that must hold and the evidence needed to establish it. |
| Quantitative quality | The measure, units, observation method and any agreed target or mandatory acceptance threshold. |
| Graduated assessment | The dimensions, defined levels, evidence needed for each level and the desired or required level. |

Requirement category and assessment method are independent. A security objective
may be assessed across graduated dimensions while a subrequirement such as
rejecting expired credentials has a binary result. A performance requirement may
have a measured value and a mandatory pass/fail threshold. Do not treat every
functional requirement as binary or every non-functional requirement as graduated.

Record the demonstrated value or level separately from the target and acceptance
decision. Define criteria before verification; do not invent thresholds after
seeing results. Missing evidence means unassessed, not the lowest measured value
or a pass. A graduated parent assessment cannot waive mandatory subrequirements.
