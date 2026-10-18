---
description: Onboard dependency updates with shared Renovate presets and keep versioned APM installations current.
applyTo: "**"
---

# Dependency Management and APM Updates

## Repository onboarding

When onboarding dependency management, inspect the repository's existing Renovate
configuration and runner before adding anything. Reuse the organization's preset
when one is published. The shared baseline is
`github>accelerate-toolkit/renovate-config`; organizations can extend it with their own
policies, and projects should extend their organization preset. If no organization
preset exists, extend the shared baseline directly in `renovate.json`:

```json
{
  "extends": ["github>accelerate-toolkit/renovate-config"]
}
```

Keep project exceptions local rather than copying the shared rules. Unpinned
presets follow their default branch on each Renovate run; use an existing release
tag when a controlled, versioned rollout is required. Do not assume an example
organization preset or tag has been published.

A preset supplies policy, not a running bot. Each organization owns runner
onboarding, credentials, repository access, schedules, and merge policy. Validate
the configuration and verify an actual update PR before treating onboarding as
complete. Private target repositories still require organization-scoped access,
even when the shared preset and APM packages are public.

Keep Renovate configuration repositories independent of APM: no APM manifests,
lockfiles, installed skills, or APM bootstrap steps. A preset may describe APM
update rules without depending on APM. Tooling needed to refresh consumer
lockfiles belongs in the consumer update runner.

## Public repository portability

Keep shared modules, skills and instructions independent of private consumer
organizations. Use fictional names, example domains/mailboxes and placeholder
account IDs in examples. Do not carry consumer project names, private repository
links, local filesystem paths or deployment settings into public guidance.
Deployment-specific values belong in ignored local configuration or private
consumer repositories. Public package/preset coordinates and copyright notices
remain legitimate attribution; do not remove those as part of sanitizing examples.
Audit publication candidates as well as staged content, and distinguish this check
from an audit or rewrite of previously published Git history.

## New GitHub repository checklist

Onboard ordinary project repositories with both APM and Renovate. The Renovate
configuration-repository exception above still applies. Start by inspecting the
existing Makefile, agent instructions, APM manifests/lock, dependency configuration,
workflows, hooks and GitHub settings; preserve working integrations.

1. Add repository-specific `.apm/instructions/` and an `apm.yml` targeting the
   supported agent, with the published organization package pinned to a real
   release. Do not invent a tag or use a sibling-checkout path for shared skills.
   Preview installation, resolve the first lock, then compile instructions. Commit
   the manifest, lock and compiled instructions; ignore downloaded packages, tool
   caches and generated deployments. Do not introduce ontologies unless requested.
2. Expose setup/install, deliberate update, compilation and relevant local checks
   through documented Make targets. Normal setup uses the frozen lock; dependency
   updates are a separate reviewed operation. Install the advisory hooks described
   below without replacing existing hooks. Keep private deployment config, state,
   credentials and test artifacts ignored, with fictional public examples.
3. Extend the existing organization/shared Renovate preset. Configure a working
   runner or verify an existing GitHub App/shared runner; a preset alone is not
   execution. Pin runner tools, provide APM for lock regeneration, and include
   managers for all relevant dependency inputs. Check extraction, especially when
   inherited ignore rules exclude examples that are executable test deployments.
4. Apply the agreed automerge/check policy explicitly. Automerge may include major
   updates, but respect required checks; do not copy `ignoreTests: true` from a repo
   with no checks into a module that has checks. Dependency updates do not authorize
   infrastructure deployment. Keep module checks credential-free; cloud acceptance
   tests need their own explicitly authorized workflow.
5. Configure narrowly scoped GitHub-only bot access. Use repository secrets when
   organizational secrets are unavailable under the GitHub plan. Never expose
   token values in files, logs or messages; keep scope/expiry/rotation notes private.
   Do not add AWS credentials or deployment access to a dependency runner.
6. Validate locally, then distinguish prepared configuration from live onboarding.
   Confirm publication, runner authentication/extraction and a real dependency PR
   and expected merge before claiming completion. Record pending external steps.
   Repository publication/commits and messaging still follow the user's existing
   authorization; onboarding does not silently authorize exposing private content.

For changes to this shared guidance, update its source package and compile the
repository instructions. Existing consumers stay on their published package pin
until a new immutable release is available; do not point them at an unpublished
version or claim that editing this checkout updated all consumers.

## APM dependencies

Pin remote APM packages to explicit release versions, for example
`owner/repository/packages/package-name#v1.2.3`. Commit `apm.yml` and
`apm.lock.yaml` together. Repository-local `path:` dependencies remain versioned
with their owning repository.

Use a Renovate version with APM manager support to update version pins and the
lockfile together. Its execution environment needs the APM CLI available to
regenerate the lockfile. Unversioned dependencies are skipped. This package
provides adoption guidance; it does not install Renovate configuration or hooks.

During onboarding, integrate an advisory local check with the repository's
existing Git hooks without replacing them. After a successful merge (including
a fast-forward pull), or a rebase, detect whether `apm.yml` or `apm.lock.yaml`
changed across the operation. For rebase hooks, ignore amend events and compare
the pre-operation and resulting trees rather than only the last replayed commit.
When either file changed, print:

```text
APM dependencies changed.
Run make apm-install to refresh your skills and instructions.
```

The check must not access upstream services, install packages, change tracked
files, or fail the Git operation. Unchanged pulls stay quiet. No persistent
reminder state or shell wrapper is required. Hook installation is local to each
clone and must be included in that organization's onboarding workflow.

`make apm-install` installs the accepted dependency versions and recompiles
instructions. `make apm-update` deliberately resolves newer dependencies and
recompiles; review its lockfile changes. Restart the agent session after refreshing
its skills and instructions.
