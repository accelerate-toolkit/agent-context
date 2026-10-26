# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Plan, prepare and publish lockstep APM releases. Only publish contacts GitHub."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

import yaml

VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
SUBJECT = re.compile(r"^(?P<type>[a-z]+)(?:\([^)]+\))?(?P<breaking>!)?: .+")
RELEASE = re.compile(r"^chore\(release\): v(\d+\.\d+\.\d+)$")
ROOT_MANIFEST = Path("apm.yml")
INDEX = Path(".claude-plugin/marketplace.json")


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).rstrip("\r\n")


def git(*args: str) -> str:
    return run("git", *args)


def version_tuple(value: str) -> tuple[int, ...]:
    if not VERSION.fullmatch(value):
        raise ValueError(f"invalid version: {value}")
    return tuple(map(int, value.split(".")))


def commits(start: str | None, end: str = "HEAD") -> list[dict]:
    raw = git("log", "--format=%H%x1f%s%x1f%b%x1e", f"{start}..{end}" if start else end)
    return [dict(zip(("sha", "subject", "body"), record.strip("\r\n").split("\x1f", 2)))
            for record in raw.split("\x1e") if record.strip("\r\n")]


def bump_type(changes: list[dict]) -> str | None:
    bump = None
    for change in changes:
        match = SUBJECT.match(change["subject"])
        if (match and match["breaking"]) or re.search(r"(?m)^BREAKING[ -]CHANGE: .+", change["body"]):
            return "major"
        if match and match["type"] == "feat":
            bump = "minor"
        elif match and match["type"] in {"fix", "perf"} and bump != "minor":
            bump = "patch"
    return bump


def notes(version: str, changes: list[dict]) -> str:
    lines = [f"# v{version}", ""]
    for change in reversed(changes):
        if RELEASE.fullmatch(change["subject"]):
            continue
        lines.append(f"- {change['subject']} ({change['sha'][:7]})")
        if change["body"].strip():
            lines.extend(["", *[f"  {line}" for line in change["body"].strip().splitlines()], ""])
    return "\n".join(lines) + "\n"


def plan(repo: str | None = None) -> dict:
    tags = [tag for tag in git("tag", "--merged", "HEAD", "--list", "v*").splitlines()
            if VERSION.fullmatch(tag[1:])]
    latest = max(tags, key=lambda tag: version_tuple(tag[1:]), default=None)
    if latest and repo:
        pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/releases?per_page=100"))
        published = any(item["tag_name"] == latest and not item["draft"]
                        for page in pages for item in page)
        release_commit = git("rev-parse", latest + "^{commit}")
        if not published and git("show", "-s", "--format=%s", release_commit) == f"chore(release): {latest}":
            previous = max((tag for tag in tags if tag != latest),
                           key=lambda tag: version_tuple(tag[1:]), default=None)
            return dict(version=latest[1:], commit=release_commit, prepare=False,
                        notes=notes(latest[1:], commits(previous, release_commit + "^")))
    changes = commits(latest)
    # A metadata commit pushed before a failed publication must finish first,
    # even when further work has subsequently reached main.
    pending = [change for change in reversed(changes) if RELEASE.fullmatch(change["subject"])]
    if pending:
        target = pending[0]
        version = RELEASE.fullmatch(target["subject"])[1]
        if latest and version_tuple(version) <= version_tuple(latest[1:]):
            raise ValueError("pending release does not advance the latest version")
        return dict(version=version, commit=target["sha"], prepare=False,
                    notes=notes(version, commits(latest, target["sha"] + "^")))
    # Recreate a missing release / finish a draft after its tag was pushed.
    if not repo and latest and git("rev-parse", latest + "^{commit}") == git("rev-parse", "HEAD"):
        subject = git("show", "-s", "--format=%s", "HEAD")
        if subject == f"chore(release): {latest}":
            previous = max((tag for tag in tags if tag != latest),
                           key=lambda tag: version_tuple(tag[1:]), default=None)
            return dict(version=latest[1:], commit=git("rev-parse", "HEAD"), prepare=False,
                        notes=notes(latest[1:], commits(previous, "HEAD^")))
    bump = bump_type(changes)
    if not bump:
        return {}
    major, minor, patch = version_tuple(latest[1:]) if latest else (0, 0, 0)
    version = {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0",
               "patch": f"{major}.{minor}.{patch + 1}"}[bump]
    return dict(version=version, commit=git("rev-parse", "HEAD"), prepare=True,
                notes=notes(version, changes))


def metadata() -> tuple[dict, list[dict]]:
    root = yaml.safe_load(ROOT_MANIFEST.read_text())
    packages = [yaml.safe_load((Path(entry["subdir"]) / "apm.yml").read_text())
                for entry in root["marketplace"]["packages"]]
    return root, packages


def marketplace(root: dict, packages: list[dict]) -> dict:
    return {"name": root["name"], "owner": root["marketplace"]["owner"], "plugins": [{
        "name": package["name"], "description": package["description"], "version": package["version"],
        "source": {"source": "git-subdir", "url": entry["source"], "path": entry["subdir"],
                   "ref": "v" + package["version"]}}
        for entry, package in zip(root["marketplace"]["packages"], packages, strict=True)]}


def check(*, release_ready: bool = False) -> None:
    root, packages = metadata()
    version_tuple(root["version"])
    entries = root["marketplace"]["packages"]
    if len({entry["name"] for entry in entries}) != len(entries):
        raise ValueError("duplicate marketplace package names")
    for entry, package in zip(entries, packages, strict=True):
        if entry["name"] != package["name"] or not root["version"] == package["version"] == entry["version"]:
            raise ValueError("root, packages and marketplace versions/names must agree")
    index = json.loads(INDEX.read_text())
    expected = marketplace(root, packages)
    if index != expected and not release_ready:
        # The published index may omit packages added since its tagged release.
        old_version = index["plugins"][0]["version"]
        if version_tuple(old_version) <= version_tuple(root["version"]):
            tag = "v" + old_version
            historical_root = yaml.safe_load(git("show", f"{tag}:{ROOT_MANIFEST.as_posix()}"))
            historical = [yaml.safe_load(git("show", f"{tag}:{entry['subdir']}/apm.yml"))
                          for entry in historical_root["marketplace"]["packages"]]
            expected = marketplace(historical_root, historical)
            for actual, plugin in zip(index["plugins"], expected["plugins"]):
                if "sha" in actual["source"]:
                    plugin["source"]["sha"] = git("rev-parse", tag + "^{commit}")
    if index != expected:
        raise ValueError("marketplace index does not match package metadata")


def sync(version: str) -> None:
    version_tuple(version)
    root, _ = metadata()
    paths = [(ROOT_MANIFEST, 1 + len(root["marketplace"]["packages"]))]
    paths.extend((Path(entry["subdir"]) / "apm.yml", 1) for entry in root["marketplace"]["packages"])
    for path, expected in paths:
        text, count = re.subn(r"(?m)^(\s*version:) .+$", lambda m: f"{m[1]} {version}", path.read_text())
        if count != expected:
            raise ValueError(f"unexpected version fields in {path}")
        path.write_text(text)
    root, packages = metadata()
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps(marketplace(root, packages), indent=2) + "\n")
    check(release_ready=True)


def prepare(version: str) -> None:
    expected = plan()
    if not expected.get("prepare") or expected.get("version") != version:
        raise ValueError("requested version does not match the release plan")
    sync(version)


def gh(*args: str) -> str:
    return run("gh", *args)


def publish(repo: str, version: str, commit: str, notes_path: Path) -> None:
    version_tuple(version)
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("repository and full commit SHA are required")
    if git("rev-parse", "HEAD") != commit or git("show", "-s", "--format=%s", commit) != f"chore(release): v{version}":
        raise ValueError("checkout must be the planned release metadata commit")
    check(release_ready=True)
    if metadata()[0]["version"] != version:
        raise ValueError("release version differs from manifests")
    if not notes_path.is_file():
        raise ValueError("release notes are missing")
    tag = "v" + version
    refs = json.loads(gh("api", f"repos/{repo}/git/matching-refs/tags/{tag}"))
    if any(ref["ref"] == f"refs/tags/{tag}" for ref in refs):
        actual = json.loads(gh("api", f"repos/{repo}/commits/{tag}"))["sha"]
        if actual != commit:
            raise ValueError(f"refusing to move published tag {tag}")
    else:
        gh("api", "--method", "POST", f"repos/{repo}/git/refs", "-f", f"ref=refs/tags/{tag}", "-f", f"sha={commit}")
    pages = json.loads(gh("api", "--paginate", "--slurp", f"repos/{repo}/releases?per_page=100"))
    release = next((item for page in pages for item in page if item["tag_name"] == tag), None)
    if release and not release["draft"]:
        print(f"{tag} is already published; left unchanged")
        return
    if not release:
        gh("release", "create", tag, "--repo", repo, "--verify-tag", "--draft",
           "--title", tag, "--notes-file", str(notes_path))
    gh("release", "edit", tag, "--repo", repo, "--notes-file", str(notes_path), "--draft=false", "--latest")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    command = sub.add_parser("plan", help="Preview version and write notes under build/release")
    command.add_argument("--repo", help="CI: query GitHub to recover an unpublished tag before newer work")
    sub.add_parser("check", help="Validate lockstep manifests and generated marketplace index")
    command = sub.add_parser("prepare", help="Synchronize metadata for the computed release; does not commit")
    command.add_argument("--version", required=True)
    command = sub.add_parser("publish", help="Create remote tag and GitHub release from a prepared commit")
    command.add_argument("--version", required=True)
    command.add_argument("--commit", required=True)
    command.add_argument("--repo", required=True)
    command.add_argument("--notes", type=Path, default=Path("build/release/notes.md"))
    args = parser.parse_args()
    if args.action == "plan":
        result = plan(args.repo)
        if result:
            Path("build/release").mkdir(parents=True, exist_ok=True)
            Path("build/release/notes.md").write_text(result.pop("notes"))
        print(json.dumps(result, indent=2))
        if output := os.environ.get("GITHUB_OUTPUT"):
            with open(output, "a") as stream:
                stream.write(f"release={'true' if result else 'false'}\n")
                for key, value in result.items():
                    stream.write(f"{key}={str(value).lower() if isinstance(value, bool) else value}\n")
    elif args.action == "check":
        check()
    elif args.action == "prepare":
        prepare(args.version)
    else:
        publish(args.repo, args.version, args.commit, args.notes)


if __name__ == "__main__":
    main()
