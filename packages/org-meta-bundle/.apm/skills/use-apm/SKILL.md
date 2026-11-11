---
name: use-apm
description: Use when creating or changing Agent Package Manager (APM) packages, manifests or dependencies, installing or refreshing packaged skills, compiling agent instructions, or validating and preparing marketplace publication. Not for application performance monitoring or ordinary application dependency management.
---

# Use APM

## Consult Cached Documentation

Check `apm --version` and search `.agent-cache/tool-docs/apm/<tag>/` before
using the network. This skill's `cached-docs.yml` caches the upstream README
and docs. Use the installed `use-cached-docs` skill to hydrate missing or stale
docs; prefer the repository's documented hydration Make target from the workspace root.
`version: latest` is resolved only when the hydrator runs, not on every read.
Compare the cached tag with the installed CLI version before using new flags.

Within the cache, start at `docs/src/content/docs/`:

- `reference/cli/install.md` and `compile.md` for installation and compilation.
- `reference/manifest-schema.md` and `lockfile-spec.md` for dependency declarations.
- `reference/targets-matrix.md` for supported primitives and deployment paths.
- `reference/cli/pack.md` and `producer/publish-to-a-marketplace.md` for distribution.

## Authoring

- Author package content under `.apm/`; do not edit generated deployment output.
- Put each skill in `.apm/skills/<skill-name>/SKILL.md` and keep its supporting scripts, references, and assets beside it.
- Keep package manifests in `apm.yml` with explicit name, version, description, and target selection.

## Codex Workflow

Run `make` first and prefer the repository's documented setup targets. When
adding APM setup, follow the shared Makefile guidance: list targets in the default
help output, use `.PHONY`, and preserve existing integrations. Name targets
`<area>[-<subject>]-<action>`: `apm-docs-hydrate` downloads documentation declared
by installed APM skills.

Where `use-cached-docs` is installed, expose installation → hydration → compilation
as one setup action, with hydration and compilation also callable independently:

```make
.PHONY: apm-install apm-update apm-docs-hydrate apm-compile

apm-install: ## Install pinned APM dependencies, hydrate docs and compile instructions.
	apm install --target codex
	$(MAKE) apm-docs-hydrate
	$(MAKE) apm-compile

apm-update: ## Refresh APM dependencies within declared refs, hydrate docs and compile.
	apm install --update --target codex
	$(MAKE) apm-docs-hydrate
	$(MAKE) apm-compile

apm-docs-hydrate: ## Download documentation declared by installed skills.
	uv run --script .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py

apm-compile: ## Compile Codex instructions without refreshing documentation.
	apm compile --target codex
```

Keep the ordered steps in recipes, not parallel prerequisites. Hydration requires
`uv` and network access; a failure stops compilation, but installation may already
have completed. Keep `.agent-cache/` ignored. Documentation versions come from
`cached-docs.yml`; `latest` resolves during hydration, independently of APM pins.
Without the hydrator, omit the hydration target and calls.

Before initial setup or intentional manifest/local-source changes, preview with
`apm install --target codex --dry-run`, then run `make apm-install`. For a workspace
that does not yet expose Make targets, the basic installation commands are:

```sh
apm install --target codex --dry-run
apm install --target codex
apm compile --target codex
```

A dry run can report an incomplete dependency preview when remote metadata is
unavailable; it is not proof that the live install will succeed.

For routine setup, use `apm install --target codex`, then compile. Commit explicit
release pins in `apm.yml`; ignore the generated `apm.lock.yaml`. Do not require
`--frozen` or commit lockfile refreshes. Direct pins do not freeze unpinned
transitive dependencies. Use `apm install --update --target codex` only for
deliberate refreshes within declared refs; adopting another release requires
changing its manifest pin.

Codex receives skills under `.agents/skills/` and agents as
`.codex/agents/<name>.toml`. Installation does not compile Codex instructions:
`apm compile --target codex` produces `AGENTS.md`. Edit package source instead
of generated output, and restart the agent session after refreshing it.

Resolve unmanaged file conflicts by inspecting ownership and adjusting names or
package selections. Do not use `--force` as a routine repair: it overwrites
collisions and bypasses the critical security-scan block.

## Workspace-Local Packages

Use a local package when its workflows, terminology, or tools only make sense
in one repository. Local `path:` dependencies MUST live below the repository
root that owns the declaring `apm.yml`; use a repository-relative path such as
`./local-apm-packages/follow-sdlc-principles`.

Do not use `../` paths, absolute paths, or paths into sibling repositories.
APM may support those forms, but they make a workspace depend on a machine-local
checkout. Put cross-repository workflows in a remote Git or marketplace package
instead.

Use lowercase, hyphen-separated package names that describe their purpose:

- `use-<tool>` for tool-use guidance, such as `use-obsidian`.
- `follow-<practice-or-principles>` for rules to follow, such as
  `follow-sdlc-principles`.
- A descriptive name such as `project-workflows` for a broader bundle that
  does not fit either prefix.

Keep the package directory basename and its `apm.yml` `name` identical by
convention. These prefixes and matching names are organization conventions,
not APM parser requirements.

Package names identify bundles, independently of the primitives inside them.
A skill has its own `.apm/skills/<skill-name>/SKILL.md`, with matching skill
folder and frontmatter `name`; it need not share the package name. Instruction
files use descriptive `.apm/instructions/<topic>.instructions.md` names and
do not need to match the package name. An instructions-only package needs no
skill folder or `SKILL.md`. The `follow-` prefix does not activate instructions;
their scope and compilation determine where they apply.

For example, keep repository-specific SDLC rules in this instructions-only
package:

```text
local-apm-packages/follow-sdlc-principles/
  apm.yml
  .apm/instructions/sdlc-principles.instructions.md
```

Its `apm.yml` declares:

```yaml
name: follow-sdlc-principles
version: 0.1.0
description: Repository-specific software delivery principles
target: codex
```

The instruction file uses `applyTo: "**"` for repository-wide scope:

```markdown
---
applyTo: "**"
---

# SDLC principles

Establish the delivery context, define observable acceptance criteria, and
preserve sustainable component boundaries throughout implementation.
```

Declare it as a regular dependency in the repository root's `apm.yml` so every
contributor receives the instructions:

```yaml
dependencies:
  apm:
    - path: ./local-apm-packages/follow-sdlc-principles
```

Use `devDependencies.apm` only for maintainer-only content, such as test
fixtures, debug agents, and release tooling. APM deploys both dependency groups
on a normal install, but excludes `devDependencies` from `apm pack` output.

Each local package needs its own `apm.yml` and `.apm/` source tree. Install it
from the workspace root after adding or changing a dependency:

```sh
apm install --target codex --dry-run
apm install --target codex
apm compile --target codex
```

A local package is versioned with the repository that owns it and should be
promoted into this organization package repository only when it has a clear
cross-repository use.

## Marketplace Workflow

Validate package versions before building the marketplace artifact:

```sh
apm pack --check-versions --dry-run
apm pack
```

Use local path dependencies while developing packages in the same repository. Install from the published marketplace only after the package release is available.

Bundle dependencies come from lockfile-attested deployed files and their hashes,
not directly from `apm_modules/`. Refresh installation after source changes before
packing. A successful pack creates local artifacts; publication is a separate step.
