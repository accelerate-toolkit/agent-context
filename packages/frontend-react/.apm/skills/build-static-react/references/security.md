# Dependency and browser security

Before adding a dependency, record purpose, exact registry coordinate and upstream
identity, direct/transitive scope, license, maintenance/security response, install
scripts and available provenance. Prefer established maintainers, but review the
specific release: popularity and signatures are not evidence of safe behavior.
Do not treat the technology shortlist as approval of every version or plugin.

Use one package manager, exact reviewed direct versions and a committed lockfile;
pin Node and package-manager versions. Use frozen installation in CI. Disable
lifecycle scripts by default where supported and document required exceptions.
Avoid unreviewed create-* or npx latest invocations. Inspect template output and
remove unnecessary dependencies before adoption. Do not automatically run audit
fixes that change the graph or make breaking upgrades.

Automated updates propose reviewed lockfile changes, including transitives. Choose
a documented release-age window and an expedited security-fix path; do not silently
inherit blanket major-version automerge. Scan the locked graph and retain an SBOM
or equivalent inventory per artifact. Triage findings and record exceptions with
owners and revisit conditions. Pin and review CI actions and downloaded tools too.

Dependency installation and build jobs must not receive deployment credentials.
Promote a previously built artifact through a separate least-privilege job. Prepare
a path to revoke/replace a compromised dependency and rebuild cleanly. Documentation
hydration fetches text; it must not execute upstream packages or project scripts.

Keep server authorization authoritative. Never put secrets in VITE_* variables,
static config, URLs or telemetry. Avoid localStorage for bearer tokens or source
credentials. Clear secret form fields after submission and do not echo stored
credentials. Private responses must not enter shared CDN caches. Limit CORS to the
reviewed origins and credential model; wildcard origins are not a substitute for
access control. Cookie-authenticated mutations need CSRF/origin controls.

Use text rendering by default. Review any dangerouslySetInnerHTML, Markdown/HTML
renderer, inline-script requirement, third-party analytics or remote script source.
A CSP helps constrain execution but does not make a compromised trusted bundle safe.
