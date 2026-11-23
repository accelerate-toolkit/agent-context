.DEFAULT_GOAL := help
export PYTHONDONTWRITEBYTECODE := 1
APM_VERSION ?= 0.38.0
RENOVATE_IMAGE := ghcr.io/renovatebot/renovate:44.257.9
APM ?= uv tool run --from apm-cli==$(APM_VERSION) apm

.PHONY: help apm-install apm-update apm-compile test release-test release-plan release-check

.PHONY: renovate-check
renovate-check: ## Validate dependency update configuration without bot credentials.
	docker run --rm -v "$(CURDIR)/renovate.json:/config/renovate.json:ro" --entrypoint renovate-config-validator $(RENOVATE_IMAGE) --strict --no-global /config/renovate.json

help: ## List available repository actions.
	@awk 'BEGIN { FS = ":.*##" } /^[[:alnum:]_.-]+:.*##/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

apm-install: ## Install APM dependencies, hydrate docs and compile instructions.
	$(APM) install --target codex
	$(MAKE) apm-docs-hydrate
	$(MAKE) apm-compile

apm-update: ## Refresh APM dependencies, hydrate docs and compile instructions.
	$(APM) install --update --target codex
	$(MAKE) apm-docs-hydrate
	$(MAKE) apm-compile

apm-compile: ## Compile instructions without refreshing documentation.
	$(APM) compile --target codex

release-plan: ## Preview the next version and write release notes under build/.
	uv run --script scripts/release/release.py plan

release-check: ## Validate package and marketplace version alignment.
	uv run --script scripts/release/release.py check

release-test: ## Test version planning and publication recovery.
	uv run --script scripts/release/test_release.py

test: release-test ## Test release tooling and bundled scripts.
	uv run --script scripts/test.py

.PHONY: apm-install-dry-run apm-docs-hydrate-preview apm-docs-hydrate frontend-docs-verify
apm-install-dry-run: ## Preview managed skill installation.
	$(APM) install --target codex --dry-run

apm-docs-hydrate-preview: ## Preview sources selected by installed documentation manifests.
	uv run --script .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py --dry-run

apm-docs-hydrate: ## Hydrate official references using the installed existing hydrator.
	uv run --script .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py

frontend-docs-verify: ## Check representative frontend references and licenses offline after hydration.
	bash scripts/verify_frontend_docs.sh
