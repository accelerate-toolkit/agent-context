# /// script
# requires-python = ">=3.11"
# dependencies = ["pypdf==6.21.4"]
# ///
"""Prepare a searchable, page-indexed reference from a local publisher PDF."""
import argparse
import hashlib
from pathlib import Path

import pypdf


def render_reference(source: Path, title: str, source_url: str, edition: str) -> str:
    reader = pypdf.PdfReader(source)
    pages = [(page.extract_text(extraction_mode="layout") or "").strip()
             for page in reader.pages]
    if not any(pages):
        raise ValueError("PDF has no extractable text; OCR or manual preparation is needed")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    lines = [f"# {title}", "", f"Source: {source_url}", f"Edition: {edition}",
             f"Source PDF SHA-256: `{digest}`",
             f"Extractor: pypdf {pypdf.__version__}, layout mode", "",
             "Local text derivative. Page numbers refer to PDF pages, not printed labels.",
             "Layout, tables and images may lose meaning; consult the original PDF when ambiguous.",
             "Source copyright and licence apply; see the accompanying sources.md.", "",
             "## Page index", ""]
    lines.extend(f"- [Page {n}](#page-{n})" for n in range(1, len(pages) + 1))
    for n, text in enumerate(pages, 1):
        lines.extend(["", f"## Page {n}", "", "```text",
                      text or "[No extractable text on this page.]", "```"])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="Local PDF; no network access is performed")
    parser.add_argument("output", type=Path, help="Markdown reference to create or replace")
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-url", required=True, help="Publisher URL for attribution")
    parser.add_argument("--edition", required=True, help="Publisher edition/date, not retrieval date")
    args = parser.parse_args()
    if args.pdf.resolve() == args.output.resolve():
        parser.error("Output must differ from the input PDF")
    rendered = render_reference(args.pdf, args.title, args.source_url, args.edition)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
