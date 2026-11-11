# Self-contained PDF extraction

Verified on 2026-11-11 for agent-context #7 using Python 3.14 and pypdf 7.0.1.
The candidate hydrator ran in a temporary workspace with an empty `PATH` and
fresh uv cache. An absolute uv executable and Python interpreter were supplied;
uv provisioned all three declared dependencies. No PDF executable was available
through `PATH`, and extraction invoked no subprocess or system PDF library.

Commands, from the temporary workspace:

```sh
uv run --python /path/to/python --script hydrate.py --manifest cached-docs.yml
uv run --python /path/to/python --script hydrate.py --manifest cached-docs.yml --check
```

The manifest selected the two public AWS PDFs recorded in
[provenance.json](provenance.json), preserving their bytes and SHA-256 hashes.

| Document | Pages | Extracted characters |
| --- | ---: | ---: |
| Cognito developer guide | 1,621 | 3,271,678 |
| Cognito user-pools API reference | 1,385 | 2,147,823 |

Both commands exited successfully; the offline check verified all seven snapshot
files. Spot checks of PKCE explanations and authentication API challenge fields
found readable text and preserved parameter names. This is representative text
quality evidence, not a complete layout audit. Unicode ligatures remain present.
No OCR is provided; encrypted PDFs and empty extracts fail.

The bundled suite passed all 18 tests, including actual multi-page PDF extraction,
byte preservation, text tamper detection, malformed/truncated/encrypted/empty
PDF rejection, retained snapshots, download-length checks and legacy Poppler
provenance verification. Release metadata validation and diff checks passed.
No APM or Make orchestration tests were added.

Publication and consumer adoption remain pending. The generated PDF/text cache
is local state and is not committed.
