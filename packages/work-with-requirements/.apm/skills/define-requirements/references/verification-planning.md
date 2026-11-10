# Verification planning and coverage

Plan how to cover obligations before execution. Ask whether each requirement is
observable or measurable, how it will be assessed, and what remains uncovered.
A plan is distinct from actual evidence and acceptance.

## Planned check

Describe four things, using the project's existing format:

- Demonstration: what the check will establish.
- Method: how to observe it, such as a scenario, measurement, inspection or study.
- Assessment criteria: references to the requirement's criteria and any agreed
  thresholds; do not invent new criteria inside the plan.
- Coverage links: the requirements, individual criteria or interface obligations
  addressed, including explicit partial scope.

Do not prescribe test frameworks, fixtures or internal implementation at the
commissioning boundary. The receiving component owns its detailed harness.
A metric without an agreed threshold can establish a baseline; distinguish that
purpose from a pass/fail demonstration.

For safe payment retries, a check could repeat confirmation after a lost response
and observe one charge plus recovery of the order outcome. These criteria must
already be agreed in the requirement or be proposed there for approval.

## Review coverage

Every requirement needs an assessment route, not necessarily a unique check.
One journey may cover several obligations, and several checks may jointly cover
one requirement. Requirement-level links claim full coverage only when the
planned demonstrations address all required criteria.

Review three boundaries: incoming and derived requirement coverage; provider and
consumer conformance to interface obligations; and the combined component outcome.
These are relationships, not mandatory separate suites. Child plans cannot alone
establish complete parent coverage. A parent may reference a suitable existing
integrated check rather than duplicate it, but must explain how that check covers
the parent's own criteria at its boundary.

Expose gaps explicitly:

| Gap | Interpretation |
| --- | --- |
| No planned check | No method explains how to assess the obligation. |
| Partial coverage | Planned checks address only some required criteria. |
| Unclear criteria | The intended demonstration cannot be judged yet. |
| Unobservable or unmeasurable statement | Refine the requirement or observation method. |
| Missing integration coverage | Parts have plans but their combined outcome does not. |

Distinguish structural validation from semantic review. A missing link can be
found mechanically. A link to a latency check does not establish that catalogue
search returns correct products, even if both share a requirement ID.

Return reasons and affected IDs for coverage judgments. Coverage completeness
means a sufficient plan has been articulated; it does not imply a check has been
implemented, executed, passed or accepted. Keep those concerns in evidence
assessment. Show child gaps without replacing the current component's own plan
with an aggregate child percentage.
