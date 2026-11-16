---
description: Keep GitHub Actions validation economical while preserving merge and release guarantees.
applyTo: ".github/workflows/**"
---

# GitHub workflow efficiency

When creating, changing or reviewing workflows, use this checklist:

- **Triggers and paths:** Avoid duplicate branch-push and PR validation for the
  same candidate. Preserve checks for the actual merge/release commit. Select
  expensive suites by relevant changes, including shared tooling inputs, while
  keeping required checks conclusive; skipped workflows can leave checks pending.
- **Concurrency:** Cancel superseded PR validation only when it has no side
  effects. Keep publication and deployment protected from cancellation. For a
  workflow whose PR path only validates, use a workflow/PR-specific group and
  `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`. Review pending
  run replacement separately; disabling cancellation does not preserve every run.
- **Setup and matrices:** Run cheap checks first. Use the smallest suitable runner
  and matrix. Reuse setup/results only when inputs and provenance match; cache
  dependencies when measured savings justify restore/save and storage costs.
- **Timeouts and retries:** Set timeouts from observed duration with headroom.
  Inspect logs and reproduce failures locally first. Retry failed work after a fix
  or evidence of a transient failure; a rerun tests the original SHA, not a later
  fix. Do not use empty commits, forced rebases or full reruns to poll progress.
- **Dependency automation:** Inherit shared internal/external Renovate grouping;
  keep exceptions local. Let the hosted app handle discovery and follow-up merges.
  Avoid redundant runners, dashboard requests and manual dispatches. Separate
  updates, new versions and rebases mean two groups do not guarantee two CI runs
  or immediate merges. Hosted bot runtime limits are separate from Actions usage.
- **Merge and release safety:** Preserve applicable checks before merging or
  publishing. Repositories intentionally without CI need no ceremonial checks
  just for Renovate. Commit-time `[no ci]` decisions remain in the global commit
  instructions; a change needing no build may still need other validation.
- **Measurement:** Compare execution counts, attempts per SHA, job durations,
  runner usage and billing over comparable windows. Total job time differs from
  elapsed time; parallel jobs may finish sooner while consuming more minutes.
  Keep consumer budgets and rollout decisions in their owning repository.

Verify platform-specific behavior before changing workflows using the official
[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency),
[billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
and [hosted Renovate limits](https://docs.renovatebot.com/mend-hosted/overview/).
