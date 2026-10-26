# Frontend React guidance

Optional APM package for projects that have chosen a minimal, statically delivered
React application. It supplies build-static-react and a manifest for pinned official
React, TypeScript, Vite and selected MDN documentation. It installs guidance, not
npm dependencies or an application template. Product architecture remains local.

See [the skill](.apm/skills/build-static-react/SKILL.md) and
[documentation map](.apm/skills/build-static-react/references/documentation.md).

## Adoption

This package is a new, unreleased addition. The manifest version follows repository
lockstep metadata; it does not imply this package exists in the historical v0.6.0
tag. After publication, select the first real release that includes this directory
and declare `accelerate-toolkit/agent-context/packages/frontend-react` with that
explicit release pin. Install org-meta-bundle alongside it for use-cached-docs.
Do not point consumers at a sibling checkout or invent a release tag.

Preview APM installation, resolve and review the manifest/lock together, install,
compile instructions and restart the consuming agent session. Hydrate through the
existing installed tool; keep .agent-cache ignored. Source pin changes are deliberate
reviews, independent of npm dependency updates. Review package and documentation
licenses before redistribution.

Repository maintainers develop this package using the root's local devDependency;
normal org-meta-bundle consumers do not receive frontend guidance or its downloads
unless they explicitly install frontend-react.
