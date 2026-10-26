# Frontend documentation hydration trial

Observed 2026-10-26 against agent-context base
`7883f5516b459854c7b9a626b17fb85c845654b7` plus the local frontend package,
TLS-trust correction and multi-package release changes. This is local evidence,
not a published release or consumer adoption claim.

## Method and results

Installed both repository-local packages through APM 0.30.0 after dry-run, compiled
instructions, then ran the existing installed use-cached-docs hydrator. No direct
copy into generated skill directories and no npm installation were used.

The first dry-run reached pinned frontend entries but failed when requesting the
existing APM release metadata: its certifi-only SSL context did not trust the managed
network certificate. The tool now initializes default system/environment trust and
adds certifi roots. Certificate verification remains enabled; the installed copy
was refreshed through APM before retrying. A regression test covers this setup.

| Source | Hydrated files, including licenses | Approximate retained disk usage |
| --- | --- | --- |
| React | 143 | 3.2 MB |
| TypeScript | 22 | 376 KB |
| Vite | 8 | 148 KB |
| MDN selected browser/CSS/accessibility references | 12 | 328 KB |

All four source commits and selected paths are in the
[frontend manifest](../packages/frontend-react/.apm/skills/build-static-react/cached-docs.yml).
The normal all-manifest command also hydrated 150 existing APM documentation files
at v0.35.0 via the shared manifest's unchanged latest selector. That is documentation,
not an upgrade of the APM 0.30.0 execution tool. The new frontend sources all use
immutable commits. Two full runs succeeded; the second expanded MDN from 6 to 12 files.

`make frontend-docs-verify` passed without network calls, locating React effect
cleanup, TypeScript narrowing, Vite public environment variables, fetch response
checks/cancellation and upstream licenses. These are representative smoke checks,
not a completeness or compatibility claim for every upstream API.

`make test release-check` passed: 15 release tests and 6 bundled-script tests.
Coverage includes multi-package version synchronization, retained historical
marketplace contents before publication, metadata drift, publication recovery,
selected-path extraction and TLS setup. Shell syntax and whitespace checks passed.

## Limits and follow-through

The hydrator still downloads whole compressed archives and reads them in memory;
the retained sizes above are not transfer sizes or peak-memory measurements. MDN
is a large upstream. Real hydration succeeded here, but constrained environments
may warrant a separate targeted-download enhancement. No archive-size benchmark
or performance guarantee is claimed. Dry-run alone does not validate source paths.

APM install emitted an organization-policy discovery warning: the optional private
policy repository was unavailable. Installation and compilation completed, but no
claim is made that private organization policy was loaded.

APM marketplace dry-run listed both packages and reported metadata-enrichment HTTP
404 for frontend-react because it is not present at the existing published baseline.
The tracked published marketplace remains unchanged. The new package joins the next
lockstep release; historical v0.6.0 does not contain it. Remote version validation
and consumer installation must follow publication of a real new tag. No release,
Hub/Auth dependency update or deployment was performed.

Restart a consuming agent session after adopting the released package. Keep source
and generated lockfile changes together; generated skills and documentation caches
remain ignored. The new package contains reusable guidance and official-source
references, with no private consumer data or deployment configuration.
