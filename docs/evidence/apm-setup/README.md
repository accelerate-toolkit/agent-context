# APM setup verification

Verified on 2026-11-11 for [issue #5](https://github.com/accelerate-toolkit/agent-context/issues/5),
using APM CLI 0.30.0 and the local org-meta-bundle source at version 0.15.1.

- A temporary consumer started without installed skills, a lockfile or documentation
  cache. It declared a repository-local copy of org-meta-bundle and used the root
  Makefile. `make -j8 apm-install` installed the skills, downloaded 150 files from
  microsoft/apm v0.35.0, then generated `AGENTS.md`. A second run also succeeded.
- This repository's `make apm-install` hydrated all five declared documentation
  sources and compiled instructions successfully.
- `make apm-test` verifies install/update ordering and repeat execution under
  parallel Make, nonzero failures that prevent subsequent steps, and standalone
  compilation without hydration. External commands are faked in these tests.
- `make test release-check` passed: 15 release tests, 19 bundled-script tests,
  and package metadata checks. Generated cache and lockfile paths remain ignored.

Both real setup runs reported the two existing context-link compilation warnings.
The existing checkout also reported unmanaged installed files and unavailable
organization policy discovery; the fresh consumer had no unmanaged-file conflicts.

This verifies the local source workflow. Publication of an immutable package
release and adoption by pinned consumers remain outstanding.
