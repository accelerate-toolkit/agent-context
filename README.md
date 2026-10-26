# agent-context

Codex-first APM packages for software projects in the accelerate-toolkit organization.
`org-meta-bundle` assumes a software development context. Non-software projects
are outside its scope; separate guidance can be forked when needed.

## Software development lifecycle

The bundle applies three continuous principles to planning, architecture,
implementation, testing and delivery: **Context**, **Feedback loops** and
**Trajectory**. Read the
[shared SDLC explanation](packages/org-meta-bundle/.apm/context/software-development-lifecycle.context.md).
The concise instruction applies to all files and links to this packaged reference;
APM rewrites the link when compiling consumer instructions.

Projects retain their own requirements, acceptance journeys and delivery decisions.
They should document how the shared principles apply locally without maintaining
a second copy of the shared guidance. Existing consumers adopt new guidance only
after installing a published release containing it.

## Onboard a Codex Workspace

Run these commands from the repository where you want Codex to use the
organization workflows.

1. Install APM, then confirm it is on your `PATH`:

   ```sh
   curl -sSL https://aka.ms/apm-unix | sh
   apm --version
   ```

   On macOS or Linux, Homebrew is an alternative:

   ```sh
   brew install microsoft/apm/apm
   ```

2. Bootstrap the workspace manifest. This creates `apm.yml`; choose Codex when
   prompted for a target.

   ```sh
   apm init
   ```

   For a non-interactive setup, use:

   ```sh
   apm init --yes --target codex
   ```

3. Install an explicitly versioned organization bundle. The example uses the
   existing `v0.2.0` release; select the published release you want to adopt:

   ```sh
   apm install accelerate-toolkit/agent-context/packages/org-meta-bundle#v0.2.0 --target codex
   apm compile --target codex
   ```

   This writes skills to `.agents/skills/`, compiles package instructions into
   `AGENTS.md`, and records the dependency in `apm.yml` and `apm.lock.yaml`.
   No marketplace registration or manual manifest editing is required.

4. Reload the Codex agent or start a new Codex session in the workspace. Codex
   reads the installed skills and generated `AGENTS.md` instructions when the
   session starts.

## Onboard Dependency Updates

For a new GitHub repository, follow the complete
[APM and Renovate onboarding checklist](packages/org-meta-bundle/.apm/instructions/apm-updates.instructions.md#new-github-repository-checklist).
It covers local setup, frozen locks, advisory hooks, runner credentials and
verification of an actual update PR/merge. Prepared files alone are not live onboarding.

Inspect existing Renovate configuration and runner setup. Projects should extend
their organization's published preset; when none exists, add this baseline to
`renovate.json`:

```json
{
  "extends": ["github>accelerate-toolkit/renovate-config"]
}
```

The public [shared preset](https://github.com/accelerate-toolkit/renovate-config)
centralizes dependency rules. Organization presets add local policy, and project
configs retain exceptions. An unpinned preset follows its default branch on each
run; use a published tag when a versioned rollout is needed.

A preset does not run Renovate. The organization must onboard the project into a
runner with suitable repository access and verify an update PR. APM consumers
also need the APM CLI in that runner to refresh `apm.lock.yaml` alongside version
pins. Renovate config repositories themselves remain independent of APM: no APM
manifest, installation, or dependency on agent-context.

See [organization rollout](docs/releases.md#organization-rollout) for runner
responsibilities and the local post-pull reminder. Installing this bundle does
not install Renovate configuration or Git hooks.

## Makefile Convention

Every repository should use its `Makefile` as the discoverable catalogue of
standard project actions that work without caller-supplied parameters, such as
`make test`, `make build`, or `make docs-check`. Running `make` must list the
available targets and concise descriptions. Declare action targets `.PHONY`
and keep recipes short, delegating substantial logic to scripts.

For operations requiring inputs or options, document the script directly and
provide useful `--help`. Avoid Make targets that mainly forward `INPUT=...`,
`VERSION=...`, or `ARGS=...`. A target may supply fixed arguments that define a
standard project action.

For example, a repository with a documentation checker could expose its usual
check through Make and document custom inputs through the script:

```make
.PHONY: docs-check
docs-check: ## Check the project's documentation.
	uv run --script scripts/check_docs.py --root docs
```

```sh
uv run --script scripts/check_docs.py --help
uv run --script scripts/check_docs.py --root other-docs
```

Prefer an existing Make target when it matches the intended action; otherwise,
use the documented script interface. Include these standard APM targets:

```make
.DEFAULT_GOAL := help

.PHONY: help apm-install apm-update

help: ## List available repository actions.
	@awk 'BEGIN { FS = ":.*##" } /^[[:alnum:]_.-]+:.*##/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

apm-install: ## Install APM dependencies and compile Codex instructions.
	apm install --target codex
	apm compile --target codex

apm-update: ## Update APM dependencies and compile Codex instructions.
	apm install --update --target codex
	apm compile --target codex
```

To review the planned files before writing them, add `--dry-run` to the install
command.

## Scripting Convention

Use Bash for straightforward command sequences, simple checks, redirects, and
pipelines. Use Python when a script grows substantial branching, structured-data
processing, retries, cleanup handling, or orchestration. Complexity and purpose
determine the choice, rather than a line limit. Shell integration and bootstrap
code can stay in the appropriate shell.

Run standalone Python scripts with `uv run --script` and declare their runtime
and dependencies using PEP 723. For example, a standard-library-only entry point
can start with:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
```

Choose the Python requirement for the script; this example does not prescribe
an organization-wide version. Declare third-party dependencies in the same
block, including those used by imported local helpers. Helper modules do not
need their own metadata. Tooling that depends on an established Python project
environment should use that environment's conventions.

Keep substantial logic importable and the CLI entry point small. Scripts with
substantial logic or consequential side effects should have behavioral tests,
covering relevant failures and repeat execution where appropriate. Prefer
`unittest`, temporary fixtures, and fake external interactions, following the
repository's existing test layout and isolation rules. Add integration tests
where real process or service interaction matters.

Expose focused test suites through documented Make actions and include them in
the appropriate aggregate suite. Keep live integration checks separately
selectable. Standalone test entry points also use uv and PEP 723; importing the
script under test does not install its inline dependencies. Declare the test
environment's dependencies so intended tests run without ambient packages or
missing-dependency skips. Existing project-managed suites retain their own
environment conventions.

## Releases and Dependency Updates

Use Conventional Commits and Semantic Versioning for released artifacts. This
repository uses an automatic release model: eligible commits on
`main` produce a tested, immutable release with synchronized package metadata.
Skills and instructions are shipped functionality, so classify their changes by
consumer impact rather than automatically using `docs` for Markdown.

See [release operations and organization rollout](docs/releases.md) for version
rules, preview commands, recovery, and repository setup requirements. The shared
bundle carries release and APM update guidance. Each organization owns its
Renovate configuration and consumer hook installation.

Renovate updates pinned APM versions and their lockfile together. When a pull
brings changes to either dependency file, local merge/rebase hooks should remind
you to run `make apm-install`. The reminder performs no upstream check or update.

## Structure

- `packages/` contains separately selectable APM packages released in lockstep.
- `packages/frontend-react/` provides optional static React guidance and pinned official references; see its [adoption notes](packages/frontend-react/README.md).
- `packages/org-meta-bundle/` provides the organization-wide Codex workflows.
- `.agent-cache/` is generated local documentation state.

## Maintain This Repository

This repository installs `org-meta-bundle` from its local package path. Run:

```sh
make
make apm-install
apm run hydrate-cached-docs
```

Use `make apm-update` to refresh APM dependencies before recompiling the
Codex instructions. `make` lists the supported repository actions.

After a release tag exists remotely, preview and build APM marketplace artifacts
from the repository root (the release workflow validates local metadata before
the new tag exists):

```sh
apm pack --check-versions --dry-run
apm pack --marketplace-path claude=build/claude-marketplace.json --marketplace-path codex=build/codex-marketplace.json
```

## Licence

The scripts and guidance in this repository are available under the
[MIT licence](LICENCE).

## Frontend documentation trial

For the optional frontend package, run `make apm-install-dry-run`, then
`make apm-install`, `make docs-hydrate-preview`, `make docs-hydrate` and
`make frontend-docs-verify`. The root maintainer install includes both local
packages; consumers opt into frontend-react separately. No npm packages are
installed by this workflow. Hydration uses the existing shared tool and downloads
full upstream archives before selecting paths. The offline smoke check requires rg.

See [hydration evidence](docs/frontend-hydration.md) for observed results and limits.
