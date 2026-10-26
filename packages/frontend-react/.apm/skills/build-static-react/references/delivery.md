# Static delivery and verification

Deploy built HTML/JS/CSS to static storage/CDN. Do not run vite dev or vite preview
as a production server. Cache content-hashed assets immutably, revalidate the HTML
shell, and retain prior assets so open clients survive rollout/rollback. Scope SPA
fallbacks to UI routes: missing assets and API errors must not become HTML 200s.
Treat route identifiers and query strings as untrusted input.

Keep personalized data behind authenticated APIs with shared caching disabled.
Choose runtime public config or build-time config deliberately; neither may hold
secrets. If configuration is injected at deployment, record its identity alongside
the artifact and verify cache behavior. Frontend/backend releases must tolerate
old browser bundles or provide a deliberate unsupported-version recovery path.

Verify type checking and production build separately. Exercise loading, empty,
error, denied, expired-session and stale-request states. Test failed mutation and
retry semantics, duplicate submissions, identity changes and cross-user isolation.
Use real browser checks for keyboard/focus behavior, screen-reader announcements,
responsive layout, direct links, refresh and back/forward. Agree support/contrast
criteria; automated checks alone do not establish accessibility.

Check actual hosting rules: static requests avoid application compute, API failures
remain API failures, cache headers match their data class and older assets remain
available. Verify CSP and credential redaction. Measure bundle sizes, cold/warm API
latency and representative cost against agreed budgets; do not invent thresholds.
Do not turn every visual detail into a unit test or substitute mocked journeys for
integrated acceptance. Record versions, artifacts, environment, substitutions and
pass/fail/blocked/unrun outcomes. A rollback changes served code, not past mutations.
