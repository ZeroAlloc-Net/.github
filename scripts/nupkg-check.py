#!/usr/bin/env python3
"""Check that the packages a release produced carry the release version, and that they reached NuGet.

Used by .github/workflows/publish.yml. Two subcommands:

  verify DIR --version V --expect IDS_FILE --own-assemblies NAMES_FILE
      Reads every .nupkg in DIR and fails unless, for each one:
        - the nuspec <version> is V;
        - every dependency on another package of this release asks for exactly V, since
          a sibling that declares a version which was never built is what Blazor 7.7.7 and
          EventSourcing.Mediator 1.0.1 shipped;
        - every assembly built by this repository, under lib/, analyzers/, build/,
          buildTransitive/ or tools/, has assembly version V, since a correctly labelled
          package around a fallback assembly is how Results 1.2.1 and Authorization 2.1.0
          shipped;
      and the set of package ids equals IDS_FILE, so a project that discovery found but
      pack did not produce, or a package nobody expected, fails the release.

  await --version V --expect IDS_FILE --timeout-minutes N --download DIR
      Polls the nuget.org flat container until every id in IDS_FILE lists V, then
      downloads each published package into DIR. Fails when any id is still missing
      at the deadline. Run `verify` on DIR afterwards: only the published bytes show
      what consumers get, and --skip-duplicate means the push may have kept an older
      upload instead of this one.

Assembly versions are read by one pwsh call, since `AssemblyName.GetAssemblyName`
needs .NET; pwsh is preinstalled on GitHub's Ubuntu runners.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

FLAT_CONTAINER = "https://api.nuget.org/v3-flatcontainer"
ASSEMBLY_DIRS = ("lib/", "analyzers/", "build/", "buildTransitive/", "tools/")


def normalize(version: str) -> str:
    """NuGet compares versions case-insensitively and ignores build metadata."""
    return version.split("+", 1)[0].strip().lower()


def core_version(version: str) -> tuple[int, int, int]:
    """The numeric part of a SemVer string; the SDK derives AssemblyVersion from it."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise SystemExit(f"::error::'{version}' is not a SemVer version")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def range_floor(version_range: str) -> str:
    """The lower bound of a NuGet version range: '1.2.3', '[1.2.3]' and '[1.2.3, )' all give 1.2.3."""
    text = version_range.strip()
    if text[:1] in "[(":
        text = text[1:].split(",", 1)[0].rstrip("])")
    return text.strip()


def read_lines(path: str) -> list[str]:
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_nuspec(package: zipfile.ZipFile) -> tuple[str, str, list[tuple[str, str]]]:
    names = [n for n in package.namelist() if "/" not in n and n.lower().endswith(".nuspec")]
    if len(names) != 1:
        raise ValueError(f"expected one nuspec at the package root, found {len(names)}")
    root = ET.fromstring(package.read(names[0]))
    package_id = version = ""
    dependencies: list[tuple[str, str]] = []
    for element in root.iter():
        name = local_name(element.tag)
        if name == "id" and not package_id:
            package_id = (element.text or "").strip()
        elif name == "version" and not version:
            version = (element.text or "").strip()
        elif name == "dependency":
            dependencies.append((element.get("id", ""), element.get("version", "")))
    return package_id, version, dependencies


def assembly_versions(paths: list[Path]) -> dict[str, str]:
    if not paths:
        return {}
    script = (
        "$ErrorActionPreference='Stop';"
        "$r=@{};"
        "foreach($p in $input){$r[$p]=[System.Reflection.AssemblyName]::GetAssemblyName($p).Version.ToString()};"
        "$r|ConvertTo-Json -Compress"
    )
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script],
        input="\n".join(str(p) for p in paths),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"::error::reading assembly versions failed: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def summary(lines: list[str]) -> None:
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")


def verify(args: argparse.Namespace) -> int:
    want = normalize(args.version)
    want_core = core_version(want)
    expected = {i.lower(): i for i in read_lines(args.expect)}
    own = {n.lower() for n in read_lines(args.own_assemblies)}
    packages = sorted(p for p in Path(args.directory).glob("*.nupkg") if not p.name.lower().endswith(".snupkg"))
    errors: list[str] = []
    rows: list[str] = []

    if not packages:
        errors.append(f"no .nupkg files in {args.directory}")

    with tempfile.TemporaryDirectory() as scratch:
        found: dict[str, Path] = {}
        pending: list[tuple[str, str, Path]] = []
        details: dict[str, dict] = {}
        for path in packages:
            with zipfile.ZipFile(path) as package:
                try:
                    package_id, version, dependencies = read_nuspec(package)
                except (ValueError, ET.ParseError) as error:
                    errors.append(f"{path.name}: {error}")
                    continue
                key = package_id.lower()
                if key in found:
                    errors.append(f"{path.name}: package id {package_id} was produced twice")
                found[key] = path
                details[key] = {"id": package_id, "version": version, "deps": [], "assemblies": []}
                if normalize(version) != want:
                    errors.append(f"{package_id}: nuspec version is {version}, expected {args.version}")
                for dep_id, dep_range in dependencies:
                    if dep_id.lower() not in expected:
                        continue
                    floor = range_floor(dep_range)
                    details[key]["deps"].append(f"{dep_id} {dep_range}")
                    if normalize(floor) != want:
                        errors.append(
                            f"{package_id}: depends on {dep_id} {dep_range or '(no version)'}, "
                            f"expected {args.version}, the version this release built"
                        )
                for entry in package.namelist():
                    if not entry.lower().endswith(".dll") or not entry.startswith(ASSEMBLY_DIRS):
                        continue
                    if Path(entry).stem.lower() not in own:
                        continue
                    target = Path(scratch) / key / entry
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(package.read(entry))
                    pending.append((key, entry, target))

        versions = assembly_versions([t for _, _, t in pending])
        for key, entry, target in pending:
            actual = versions.get(str(target), "")
            parts = [int(x) for x in actual.split(".")] if actual else []
            details[key]["assemblies"].append(f"{entry} {actual}")
            if not parts or tuple(parts[:3]) != want_core or any(parts[3:]):
                errors.append(
                    f"{details[key]['id']}: {entry} has assembly version {actual or 'unreadable'}, "
                    f"expected {'.'.join(map(str, want_core))}.0"
                )

        for key, original in expected.items():
            if key not in found:
                errors.append(f"{original}: discovered as packable but no package was produced")
        for key in found:
            if key not in expected:
                errors.append(f"{details[key]['id']}: produced but not discovered as packable")

        rows.append(f"### Package check: {args.directory}, expecting {args.version}")
        rows.append("")
        rows.append("| Package | Version | Own assemblies checked | Sibling dependencies |")
        rows.append("|---|---|---|---|")
        for key in sorted(details):
            d = details[key]
            rows.append(f"| {d['id']} | {d['version']} | {len(d['assemblies'])} | {', '.join(d['deps']) or '-'} |")
            for line in d["assemblies"]:
                print(f"  {d['id']}: {line}")
            print(f"{d['id']} {d['version']}: {len(d['assemblies'])} assemblies, deps: {d['deps'] or '-'}")

    if errors:
        rows.append("")
        rows.extend(f"- :x: {e}" for e in errors)
    summary(rows)
    for error in errors:
        print(f"::error::{error}")
    if not errors:
        print(f"OK: {len(found)} package(s) carry {args.version}")
    return 1 if errors else 0


def fetch(url: str) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": "ZeroAlloc-Net publish check"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        print(f"  {url}: HTTP {error.code}, retrying")
        return None
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"  {url}: {error}, retrying")
        return None


def await_packages(args: argparse.Namespace) -> int:
    want = normalize(args.version)
    ids = read_lines(args.expect)
    deadline = time.monotonic() + args.timeout_minutes * 60
    missing = list(ids)
    while True:
        still = []
        for package_id in missing:
            body = fetch(f"{FLAT_CONTAINER}/{package_id.lower()}/index.json")
            versions = json.loads(body).get("versions", []) if body else []
            if want not in (normalize(v) for v in versions):
                still.append(package_id)
        missing = still
        if not missing:
            break
        if time.monotonic() >= deadline:
            for package_id in missing:
                print(f"::error::{package_id} {args.version} is not on nuget.org after {args.timeout_minutes} minutes")
            summary([f"- :x: not on nuget.org after {args.timeout_minutes} minutes: {', '.join(missing)}"])
            return 1
        print(f"Waiting for {len(missing)} of {len(ids)} package(s) to appear: {', '.join(missing)}")
        time.sleep(args.interval_seconds)
    print(f"All {len(ids)} package(s) list {args.version} on nuget.org")

    out = Path(args.download)
    out.mkdir(parents=True, exist_ok=True)
    for package_id in ids:
        lower = package_id.lower()
        body = None
        for _ in range(10):
            body = fetch(f"{FLAT_CONTAINER}/{lower}/{want}/{lower}.{want}.nupkg")
            if body:
                break
            time.sleep(args.interval_seconds)
        if not body:
            print(f"::error::{package_id} {args.version} is listed but its package could not be downloaded")
            return 1
        (out / f"{lower}.{want}.nupkg").write_bytes(body)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    v = sub.add_parser("verify")
    v.add_argument("directory")
    v.add_argument("--version", required=True)
    v.add_argument("--expect", required=True, help="file with one expected package id per line")
    v.add_argument("--own-assemblies", required=True, help="file with one assembly name built by this repo per line")

    a = sub.add_parser("await")
    a.add_argument("--version", required=True)
    a.add_argument("--expect", required=True)
    a.add_argument("--timeout-minutes", type=float, default=30)
    a.add_argument("--interval-seconds", type=float, default=30)
    a.add_argument("--download", required=True)

    args = parser.parse_args()
    return verify(args) if args.command == "verify" else await_packages(args)


if __name__ == "__main__":
    sys.exit(main())
