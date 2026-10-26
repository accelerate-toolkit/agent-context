#!/usr/bin/env bash
# Offline smoke checks for selected official references and upstream licenses.
set -euo pipefail
cd "$(dirname "$0")/.."
react_docs=.agent-cache/tool-docs/react/ae5e48074d4f73f1e349eda2a66841f9a959023e
ts_docs=.agent-cache/tool-docs/typescript/3b069fb7d66c9c69b590c18e5cb9f9fa92b16467
vite_docs=.agent-cache/tool-docs/vite/981f07fa4580fb88b333c4450431e4715d2a0b82
mdn_docs=.agent-cache/tool-docs/mdn-web/9de14917b151f7db567a65d44c2685cea754b12a
# These probes intentionally track the documented manifest pins; update together.
test -s "$react_docs/LICENSE-DOCS.md"
test -s "$ts_docs/LICENSE"
test -s "$ts_docs/LICENSE-CODE"
test -s "$vite_docs/LICENSE"
test -s "$mdn_docs/LICENSE.md"
rg -q 'cleanup' "$react_docs/src/content/reference/react/useEffect.md"
rg -q 'narrowing' "$ts_docs/packages/documentation/copy/en/handbook-v2/Narrowing.md"
rg -q 'VITE_' "$vite_docs/docs/guide/env-and-mode.md"
rg -q 'response.ok' "$mdn_docs/files/en-us/web/api/fetch_api/using_fetch/index.md"
rg -q 'AbortController' "$mdn_docs/files/en-us/web/api/fetch_api/using_fetch/index.md"
printf '%s\n' 'ok: React effects, TypeScript narrowing, Vite public variables, fetch cancellation/errors and licenses available offline'
