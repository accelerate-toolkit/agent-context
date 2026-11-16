# Economical CI workflow review

Review date: 2026-11-16. Scope: agent-context issue #11; source inspection only.
The [workflow instructions](../../../packages/org-meta-bundle/.apm/instructions/github-workflows.instructions.md)
links verified official platform references and a reusable review checklist.
No workflow was dispatched and no measured savings are claimed.

## Inspected sources

- `accelerate-toolkit/delivery-tooling` at
  `ffc1d18c18c31a08978ff2968933d3395ef09481`:
  [check.yml](https://github.com/accelerate-toolkit/delivery-tooling/blob/ffc1d18c18c31a08978ff2968933d3395ef09481/.github/workflows/check.yml).
- `accelerate-toolkit/renovate-config` at
  `8911d6f6f36c97bcc52ed47f88b936ef1d9f0196`:
  [default.json](https://github.com/accelerate-toolkit/renovate-config/blob/8911d6f6f36c97bcc52ed47f88b936ef1d9f0196/default.json)
  and [groups.json](https://github.com/accelerate-toolkit/renovate-config/blob/8911d6f6f36c97bcc52ed47f88b936ef1d9f0196/groups.json).
  The default extends grouping; internal/external groups and concurrent PR limits
  do not cap workflow execution counts.

Sources were retrieved read-only through GitHub at those revisions. No sibling
checkout was inspected. Billing, run durations and branch protection were not
inspected; conclusions below concern workflow structure, not live acceptance.

## Delivery-tooling findings and proposed follow-up

| Area | Observed configuration | Disposition for the owning repository |
| --- | --- | --- |
| Triggers | PR, main push and manual dispatch; no branch-push validation | Retain main validation: plan depends on check and publish depends on plan. Manual dispatch should serve diagnosis/recovery, not polling. |
| Concurrency | Workflow-wide `delivery-${{ github.ref }}`, cancellation false | Candidate saving: cancel superseded PR checks only, using a PR-event condition. Keep main publication non-cancellable; review pending-run replacement and recovery before changing serialization. |
| Paths | All changes checked | Keep until dependency-aware selection and a conclusive required gate are demonstrated. No basis for blanket Markdown exclusion: shipped guidance can be behavior. |
| Matrix/runner | One Linux job per stage; no matrix | No matrix duplication to remove. Benchmark runner needs before changing size. |
| Setup/cache | Pinned uv/Node; uv cache explicitly disabled | Measure setup cost first. Do not enable caching merely by convention. |
| Timeouts | No explicit job timeouts | Collect check/plan/publish duration distributions, then propose limits with headroom and publication recovery. No arbitrary limit established here. |
| Artifacts | Release plan passed to publish with expected source commit | Preserve provenance checks. Review 90-day retention against recovery needs before reducing storage. |
| Retries/release | Check → plan/verify → publish | Preserve sequence. Diagnose locally and target failed work; avoid redispatch solely to show guidance works. |

These are proposed follow-ups for
[delivery-tooling #3](https://github.com/accelerate-toolkit/delivery-tooling/issues/3),
which remains the home for reusable tooling guidance and implementation. This
checkout adds concise workflow instructions and records the review; it does not
publish that repository's guide, change its workflow, or claim owner acceptance.
No cross-repository comment was posted. Budgets and rollout remain consumer-owned.

## Local application

Agent-context's `ci.yml` validates PRs and main pushes; `release.yml` separately
serializes publication with cancellation disabled. Preserve release validation
because preparation changes metadata before publication. PR-only cancellation is
a possible follow-up for CI; no workflow changes are needed to deliver this
instructional issue. Do not infer duplicate final-commit evidence from PR success.

## Local validation

- `make test release-check`: passed (15 release tests and 18 bundled-script tests;
  package/marketplace alignment passed).
- Changed source documents' relative links resolved; `git diff --check` passed.
- `make apm-compile`: succeeded and placed the checklist in
  `.github/workflows/AGENTS.md`; root `AGENTS.md` does not contain it. Root
  `AGENTS.md` remains ignored; the generated workflow file accompanies this change.
  APM 0.30.0 reported existing anchor-resolution warnings in
  `assembly-and-deployment.context.md` and `roadmaps-and-milestones.context.md`;
  neither reference was changed by this work.
- No dependency refresh, workflow execution, publication or consumer rollout was
  performed. The examples were reviewed as guidance, not exercised as live
  workflows. Platform facts were checked against the official sources linked in
  the instructions; monetary savings remain unmeasured.

CI guidance is activated by `github-workflows.instructions.md`, scoped to
`.github/workflows/**`, rather than the global APM update instructions. The existing
always-applicable `git-commits.instructions.md` remains the authoritative home for
`[no ci]` decisions; it already covers eligibility, shipped behavior, required
checks and release triggers. The workflow instructions defer to that policy rather than
duplicating it. The longer context reference was removed in favor of the scoped
checklist.
