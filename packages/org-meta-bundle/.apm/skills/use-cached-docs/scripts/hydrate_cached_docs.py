#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "certifi>=2025.0.0",
#   "pyyaml>=6.0.2",
# ]
# ///
"""Hydrate documentation manifests owned by installed agent skills."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from datetime import datetime, timezone
from uuid import uuid4
import io
import json
import re
import shutil
import ssl
import tarfile
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit
import urllib.request

import certifi
import yaml


USER_AGENT = "agent-context-hydrate-cached-docs"
def create_ssl_context() -> ssl.SSLContext:
    """Keep system/SSL_CERT_FILE trust (including managed proxies) plus certifi."""
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=certifi.where())
    return context


SSL_CONTEXT = create_ssl_context()
IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


@dataclass(frozen=True)
class HttpFile:
    url: str
    destination: PurePosixPath
    format: str
    text_destination: PurePosixPath | None = None


@dataclass(frozen=True)
class CachedDocsSource:
    identifier: str
    repository: str
    strategy_type: str
    version: str
    files: tuple[tuple[PurePosixPath, PurePosixPath], ...]
    folders: tuple[tuple[PurePosixPath, PurePosixPath], ...]
    configuration_path: Path
    http_files: tuple[HttpFile, ...] = ()


def request_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, context=SSL_CONTEXT) as response:
        return json.load(response)


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, context=SSL_CONTEXT) as response:
        return response.read()


def release_source(repository: str, version: str) -> tuple[str, str]:
    if version == "latest":
        url = f"https://api.github.com/repos/{repository}/releases/latest"
    else:
        url = (
            f"https://api.github.com/repos/{repository}/releases/tags/"
            f"{quote(version, safe='')}"
        )

    release = request_json(url)
    if release.get("draft") or release.get("prerelease"):
        raise RuntimeError(f"GitHub release {version!r} for {repository} is not stable")

    tag = release.get("tag_name")
    archive_url = release.get("tarball_url")
    if not isinstance(tag, str) or not isinstance(archive_url, str):
        raise RuntimeError(f"GitHub's release response for {repository} is missing a tag or source archive")
    return tag, archive_url


def required_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def source_identifier(value: object, label: str) -> str:
    identifier = required_string(value, label)
    if not IDENTIFIER_PATTERN.fullmatch(identifier):
        raise ValueError(f"{label} must contain lowercase letters, digits, dots, underscores, or hyphens")
    return identifier


def relative_folder(value: object, label: str) -> PurePosixPath:
    path = PurePosixPath(required_string(value, label))
    if path.is_absolute() or ".." in path.parts or path == PurePosixPath("."):
        raise ValueError(f"{label} must be a relative path without '..'")
    return path


def configured_paths(
    entry: Mapping[object, object],
    label: str,
    key: str,
) -> tuple[tuple[PurePosixPath, PurePosixPath], ...]:
    configured = entry.get(key, [])
    if not isinstance(configured, list):
        raise ValueError(f"{label}.{key} must be a list")

    paths: list[tuple[PurePosixPath, PurePosixPath]] = []
    destinations: set[PurePosixPath] = set()
    for index, path in enumerate(configured, start=1):
        if not isinstance(path, Mapping):
            raise ValueError(f"{label}.{key}[{index}] must be a mapping")
        source = relative_folder(path.get("source"), f"{label}.{key}[{index}].source")
        destination = relative_folder(
            path.get("destination", source.as_posix()),
            f"{label}.{key}[{index}].destination",
        )
        if destination in destinations:
            raise ValueError(f"{label}.{key} has duplicate destination {destination}")
        destinations.add(destination)
        paths.append((source, destination))
    return tuple(paths)


def load_sources(configuration_path: Path) -> list[CachedDocsSource]:
    with configuration_path.open() as configuration_file:
        configuration = yaml.safe_load(configuration_file)
    if not isinstance(configuration, Mapping):
        raise ValueError(f"{configuration_path} must contain a mapping")

    entries = configuration.get("cached_docs")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{configuration_path} must define at least one cached_docs entry")

    sources: list[CachedDocsSource] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, Mapping):
            raise ValueError(f"{configuration_path}: cached_docs entry {index} must be a mapping")
        identifier = source_identifier(entry.get("id"), f"{configuration_path}: cached_docs entry {index}.id")
        strategy = entry.get("strategy")
        if not isinstance(strategy, Mapping):
            raise ValueError(f"{configuration_path}: cached_docs entry {identifier}.strategy must be a mapping")
        strategy_type = required_string(strategy.get("type"), f"{configuration_path}: {identifier}.strategy.type")
        if strategy_type == "http-files":
            if entry.get("folders"):
                raise ValueError("http-files does not support folders")
            sources.append(CachedDocsSource(
                identifier, "", strategy_type, "", (), (), configuration_path,
                configured_http_files(entry),
            ))
            continue
        if strategy_type not in {"github-release-http", "github-archive-http"}:
            raise ValueError(
                f"{configuration_path}: cached_docs entry {identifier} must use github-release-http, github-archive-http or http-files"
            )

        repository = required_string(strategy.get("repository"), f"{configuration_path}: {identifier}.repository")
        version_key = "version" if strategy_type == "github-release-http" else "ref"
        version = required_string(strategy.get(version_key), f"{configuration_path}: {identifier}.{version_key}")
        if strategy_type == "github-archive-http" and not COMMIT_PATTERN.fullmatch(version):
            raise ValueError(f"{configuration_path}: {identifier}.ref must be a 40-character lowercase commit SHA")

        files = configured_paths(entry, f"{configuration_path}: {identifier}", "files")
        folders = configured_paths(entry, f"{configuration_path}: {identifier}", "folders")
        if not files and not folders:
            raise ValueError(f"{configuration_path}: {identifier} must define at least one file or folder")
        destinations = [destination for _source, destination in (*files, *folders)]
        if len(destinations) != len(set(destinations)):
            raise ValueError(f"{configuration_path}: {identifier} has duplicate file or folder destinations")

        sources.append(
            CachedDocsSource(identifier, repository, strategy_type, version, files, folders, configuration_path)
        )
    return sources


def discover_configuration_paths(workspace_root: Path) -> list[Path]:
    own_configuration = Path(__file__).resolve().parents[1] / "cached-docs.yml"
    installed_configurations = workspace_root.glob(".agents/skills/*/cached-docs.yml")
    configurations = [own_configuration, *installed_configurations]
    unique_configurations = {path.resolve() for path in configurations if path.is_file()}
    return sorted(unique_configurations)


def discover_sources(workspace_root: Path) -> list[CachedDocsSource]:
    sources_by_id: dict[str, CachedDocsSource] = {}
    for configuration_path in discover_configuration_paths(workspace_root):
        for source in load_sources(configuration_path):
            existing = sources_by_id.get(source.identifier)
            if existing:
                raise ValueError(
                    f"Duplicate cached docs ID {source.identifier!r} in "
                    f"{existing.configuration_path} and {source.configuration_path}"
                )
            sources_by_id[source.identifier] = source
    if not sources_by_id:
        raise ValueError("No cached-docs.yml files were found beside installed skills")
    return list(sources_by_id.values())


def source_archive(source: CachedDocsSource) -> tuple[str, str]:
    if source.strategy_type == "github-release-http":
        return release_source(source.repository, source.version)
    return source.version, f"https://api.github.com/repos/{source.repository}/tarball/{source.version}"


def extract_folders(
    archive: bytes,
    destination: Path,
    files: tuple[tuple[PurePosixPath, PurePosixPath], ...],
    folders: tuple[tuple[PurePosixPath, PurePosixPath], ...],
) -> tuple[dict[PurePosixPath, int], dict[PurePosixPath, int]]:
    files_written = {source: 0 for source, _ in files}
    folders_written = {source: 0 for source, _ in folders}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        for member in tar:
            if not member.isfile():
                continue

            archive_path = PurePosixPath(member.name)
            relative_path = archive_path.parts[1:]
            if not relative_path:
                continue
            archive_relative = PurePosixPath(*relative_path)
            for source_file, destination_file in files:
                if archive_relative != source_file:
                    continue
                target = destination / Path(*destination_file.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                archive_file = tar.extractfile(member)
                if archive_file is None:
                    raise RuntimeError(f"Could not extract {member.name}")
                with archive_file, target.open("wb") as output:
                    shutil.copyfileobj(archive_file, output)
                files_written[source_file] += 1
                break
            else:
                for source_folder, destination_folder in folders:
                    source_parts = source_folder.parts
                    if relative_path[: len(source_parts)] != source_parts:
                        continue
                    remaining_path = relative_path[len(source_parts) :]
                    if not remaining_path:
                        continue
                    target = destination / Path(*destination_folder.parts, *remaining_path)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    archive_file = tar.extractfile(member)
                    if archive_file is None:
                        raise RuntimeError(f"Could not extract {member.name}")
                    with archive_file, target.open("wb") as output:
                        shutil.copyfileobj(archive_file, output)
                    folders_written[source_folder] += 1
                    break
    return files_written, folders_written


def hydrate(source: CachedDocsSource, cache_root: Path, dry_run: bool) -> None:
    if source.strategy_type == "http-files":
        hydrate_http(source, cache_root, dry_run)
        return
    tag, source_url = source_archive(source)
    destination = cache_root / "tool-docs" / source.identifier / tag
    if dry_run:
        print(f"Would hydrate {source.repository} {tag} into {destination}")
        return

    archive = download(source_url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent, prefix=f".{source.identifier}-{tag}-") as temporary_dir:
        temporary_destination = Path(temporary_dir)
        files_written, folders_written = extract_folders(
            archive, temporary_destination, source.files, source.folders
        )
        missing_files = [file for file, count in files_written.items() if not count]
        missing_folders = [folder for folder, count in folders_written.items() if not count]
        if missing_files or missing_folders:
            missing = ", ".join(
                [*(file.as_posix() for file in missing_files), *(folder.as_posix() for folder in missing_folders)]
            )
            raise RuntimeError(f"{source.repository} {tag} did not contain configured paths: {missing}")

        if destination.exists():
            shutil.rmtree(destination)
        shutil.move(str(temporary_destination), destination)

    print(
        f"Hydrated {sum(files_written.values()) + sum(folders_written.values())} files "
        f"from {source.repository} {tag} into {destination}"
    )


def https_url(value: object) -> str:
    url = required_string(value, "url")
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username
            or parsed.password or parsed.fragment):
        raise ValueError("Documentation URLs must use HTTPS without credentials or fragments")
    return url


def configured_http_files(entry: Mapping) -> tuple[HttpFile, ...]:
    entries = entry.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("http-files requires a nonempty files list")
    files = []
    outputs = [PurePosixPath(name) for name in
               ("INDEX.md", "provenance.json", "SHA256SUMS", "cached-docs.yml")]
    for item in entries:
        if not isinstance(item, Mapping):
            raise ValueError("HTTP file must be a mapping")
        url = https_url(item.get("url"))
        destination = relative_folder(item.get("destination"), "destination")
        kind = item.get("format", "text")
        if kind not in {"text", "markdown", "pdf"}:
            raise ValueError("HTTP file format must be text, markdown or pdf")
        text_destination = None
        if "text_destination" in item:
            if kind != "pdf":
                raise ValueError("text_destination requires PDF format")
            text_destination = relative_folder(item["text_destination"], "text_destination")
        for output in (destination, text_destination):
            if output is None:
                continue
            if any(output == old or output in old.parents or old in output.parents for old in outputs):
                raise ValueError(f"Conflicting or reserved destination: {output}")
            if any(char in str(output) for char in "\n\r\\"):
                raise ValueError("Destinations must not contain newlines or backslashes")
            outputs.append(output)
        files.append(HttpFile(url, destination, kind, text_destination))
    return tuple(files)


class HTTPSRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        https_url(newurl)
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def download_http(url: str, destination: Path) -> dict:
    opener = urllib.request.build_opener(
        HTTPSRedirectHandler(), urllib.request.HTTPSHandler(context=SSL_CONTEXT)
    )
    request = urllib.request.Request(https_url(url), headers={"User-Agent": USER_AGENT})
    with opener.open(request, timeout=60) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
        return {"resolved_url": response.url,
                "headers": {key: response.headers[key] for key in
                            ("ETag", "Last-Modified", "Content-Type") if key in response.headers}}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def file_hash(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def hydrate_http(source: CachedDocsSource, cache_root: Path, dry_run: bool) -> None:
    parent = cache_root / "tool-docs" / source.identifier
    if dry_run:
        print(f"Would hydrate {len(source.http_files)} HTTPS files into {parent}/<snapshot>/")
        return
    extractor = None
    if any(item.text_destination for item in source.http_files):
        extractor = subprocess.run(["pdftotext", "-v"], check=True, capture_output=True,
                                   text=True).stderr.strip()
    parent.mkdir(parents=True, exist_ok=True)
    name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:12]
    destination = parent / name
    provenance = {"source_id": source.identifier, "strategy": "http-files",
                  "retrieval_started": utc_now(), "pdftotext_version": extractor, "files": []}
    index = ["# Documentation snapshot", "",
             "Upstream HTTP sources are mutable; this is a retrieval snapshot, not a release.",
             "See provenance.json and SHA256SUMS. Text extracts are local derivatives.",
             "Links inside upstream documents may refer to uncached pages.", ""]
    with tempfile.TemporaryDirectory(dir=parent, prefix=".download-") as temp:
        stage = Path(temp)
        shutil.copyfile(source.configuration_path, stage / "cached-docs.yml")
        for item in source.http_files:
            target = stage / item.destination
            target.parent.mkdir(parents=True, exist_ok=True)
            metadata = download_http(item.url, target)
            with target.open("rb") as stream:
                prefix = stream.read(1024)
            if not prefix:
                raise ValueError(f"Empty documentation: {item.url}")
            if item.format == "pdf":
                if not prefix.startswith(b"%PDF-"):
                    raise ValueError(f"Expected PDF: {item.url}")
            else:
                if re.search(rb"<!doctype\s+html|<html[\s>]", prefix, re.I):
                    raise ValueError(f"Unexpected HTML: {item.url}")
                target.read_text(encoding="utf-8")
            metadata.update(url=item.url, destination=str(item.destination),
                            retrieved_at=utc_now(), sha256=file_hash(target))
            index.append(f"- [{item.destination}]({quote(str(item.destination))}) — {item.url}")
            if item.text_destination:
                text_path = stage / item.text_destination
                text_path.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["pdftotext", "-layout", str(target), str(text_path)], check=True)
                if not text_path.stat().st_size:
                    raise ValueError(f"Empty PDF text extract: {item.url}")
                metadata.update(text_destination=str(item.text_destination),
                                text_sha256=file_hash(text_path))
                index.append(f"  - [Searchable text]({quote(str(item.text_destination))})")
            provenance["files"].append(metadata)
        provenance["retrieval_completed"] = utc_now()
        (stage / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        (stage / "INDEX.md").write_text("\n".join(index) + "\n")
        checksums = "".join(f"{file_hash(path)}  {path.relative_to(stage).as_posix()}\n"
                            for path in sorted(stage.rglob("*")) if path.is_file())
        (stage / "SHA256SUMS").write_text(checksums)
        stage.rename(destination)
    # Publish the pointer only after every download and extraction succeeded.
    pointer = parent / (".current-" + name)
    try:
        pointer.symlink_to(name, target_is_directory=True)
        pointer.replace(parent / "current")
    finally:
        pointer.unlink(missing_ok=True)
    print(f"Hydrated {len(source.http_files)} HTTP files into {destination}")


def check_http_cache(source: CachedDocsSource, cache_root: Path) -> None:
    if source.strategy_type != "http-files":
        raise ValueError("--check currently supports only http-files sources; select one with --source")
    current = cache_root / "tool-docs" / source.identifier / "current"
    lines = (current / "SHA256SUMS").read_text().splitlines()
    if not lines:
        raise ValueError("Empty checksum manifest")
    checked = set()
    for line in lines:
        digest, name = line.split("  ", 1)
        relative = relative_folder(name, "checksum path")
        path = current / relative
        if not path.resolve().is_relative_to(current.resolve()):
            raise ValueError(f"Checksum path leaves snapshot: {name}")
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or file_hash(path) != digest:
            raise ValueError(f"Checksum mismatch: {name}")
        checked.add(relative)
    required = {item.destination for item in source.http_files}
    required.update(item.text_destination for item in source.http_files if item.text_destination)
    if not required.issubset(checked):
        raise ValueError("Snapshot is missing configured files; refresh the cache")
    print(f"Verified {len(checked)} files offline in {current}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Resolve releases without downloading or writing files.")
    parser.add_argument("--source", action="append", help="Hydrate only this source ID (repeatable).")
    parser.add_argument("--manifest", type=Path, help="Read one explicit manifest instead of discovery.")
    parser.add_argument("--check", action="store_true", help="Verify selected HTTP snapshots offline.")
    args = parser.parse_args()
    if args.check and args.dry_run:
        parser.error("--check and --dry-run cannot be combined")
    return args


def main() -> None:
    args = parse_args()
    workspace_root = Path.cwd()
    cache_root = workspace_root / ".agent-cache"
    sources = load_sources(args.manifest) if args.manifest else discover_sources(workspace_root)
    if args.source:
        missing = set(args.source) - {source.identifier for source in sources}
        if missing:
            raise ValueError(f"Unknown source IDs: {', '.join(sorted(missing))}")
        sources = [source for source in sources if source.identifier in args.source]
    for source in sources:
        if args.check:
            check_http_cache(source, cache_root)
        else:
            hydrate(source, cache_root, args.dry_run)


if __name__ == "__main__":
    main()
