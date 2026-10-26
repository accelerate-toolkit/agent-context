# Official documentation map

The adjacent cached-docs.yml pins these upstream snapshots, inspected 2026-10-26.
Search `.agent-cache/tool-docs/<id>/<commit>/` after hydration. Upstream Markdown
contains site-specific links/macros; this is a searchable source cache, not an
offline rendered website. Follow official web links when context is absent.

| ID | Official source | Selected coverage | Snapshot |
| --- | --- | --- | --- |
| react | https://react.dev / https://github.com/reactjs/react.dev | Learn, React and React DOM reference | ae5e48074d4f73f1e349eda2a66841f9a959023e |
| typescript | https://www.typescriptlang.org/docs / https://github.com/microsoft/TypeScript-Website | Handbook, strict and indexed-access configuration | 3b069fb7d66c9c69b590c18e5cb9f9fa92b16467 |
| vite | https://vite.dev/guide / https://github.com/vitejs/vite | Getting started, features, build, assets, environment, static deployment and build configuration | 981f07fa4580fb88b333c4450431e4715d2a0b82 (v8.3.5 release target) |
| mdn-web | https://developer.mozilla.org / https://github.com/mdn/content | Fetch, abort, CSRF, CSP, CSS variables/reduced motion, native forms and keyboard/live-region accessibility | 9de14917b151f7db567a65d44c2685cea754b12a |

These are documentation pins, not npm dependency approvals. Check version support
before using APIs; React/TypeScript website snapshots may discuss features outside
a project's selected versions. The MDN subset is intentionally narrow, not a
complete CSS/accessibility reference. Use official CSS and HTML references for
missing topics and extend this manifest only after checking paths and size.

Preserve upstream licenses: React LICENSE-DOCS.md, TypeScript LICENSE and
LICENSE-CODE, Vite LICENSE, and MDN LICENSE.md are cached. Documentation licenses
differ from this package's MIT guidance license. Keep source attribution and
review licenses before redistributing content. No upstream documentation is
vendored in this package; local generated caches stay ignored.

The existing hydrator downloads a full compressed source archive before selecting
paths. Selection reduces retained content, not network transfer or peak memory.
MDN is particularly large. Hydration is an explicit setup/update action, not a
per-task or CI test prerequisite. Its dry-run reports intended sources but does
not verify paths, archive availability or extraction. A real run establishes those.
The current tool redownloads even existing entries on rerun.

Use the consumer's documented Make/APM hydration action, or from its workspace:

```sh
uv run .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py --dry-run
uv run .agents/skills/use-cached-docs/scripts/hydrate_cached_docs.py
rg -n 'AbortController|response.ok' .agent-cache/tool-docs/mdn-web
```

Install use-cached-docs from org-meta-bundle alongside frontend-react. Never copy
skills manually into generated output. Advance source pins deliberately: inspect
upstream ownership, resolve the commit, check paths and licensing, hydrate, perform
representative offline queries and record results. Do not use latest for these
reviewed references. Deployment-provider and identity-provider docs belong with
their respective guidance, not this framework package.
