.DEFAULT_GOAL := help
export PYTHONDONTWRITEBYTECODE := 1
APM_VERSION ?= 0.30.0
APM ?= uv tool run --from apm-cli==$(APM_VERSION) apm

.PHONY: help apm-install apm-update test release-test release-plan release-check

help: ## List available repository actions.
	@awk 'BEGIN { FS = ":.*##" } /^[[:alnum:]_.-]+:.*##/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

apm-install: ## Install APM dependencies and compile Codex instructions.
	$(APM) install --target codex
	$(APM) compile --target codex

apm-update: ## Update APM dependencies and compile Codex instructions.
	$(APM) install --update --target codex
	$(APM) compile --target codex

release-plan: ## Preview the next version and write release notes under build/.
	uv run --script scripts/release/release.py plan

release-check: ## Validate package and marketplace version alignment.
	uv run --script scripts/release/release.py check

release-test: ## Test version planning and publication recovery.
	uv run --script scripts/release/test_release.py

test: release-test ## Test release tooling and bundled scripts.
	uv run --script scripts/test.py

.PHONY: apm-install-dry-run docs-hydrate-preview docs-hydrate frontend-docs-verify
apm-install-dry-run: ## Preview managed skill installation.
	$(APM) install --target codex --dry-run

docs-hydrate-preview: ## Preview sources selected by installed documentation manifests.
	uv run .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py --dry-run

docs-hydrate: ## Hydrate official references using the installed existing hydrator.
	uv run .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py

frontend-docs-verify: ## Check representative frontend references and licenses offline after hydration.
	bash scripts/verify_frontend_docs.sh
