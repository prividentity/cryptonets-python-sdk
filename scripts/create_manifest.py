#!/usr/bin/env python3
"""
Create a YAML manifest for native artifacts.

Input directory layout (recommended):

native-artifacts/
  <build_version>/
    Linux/
      ubuntu/
        22.04/
          x86_64/
            libprivid_fhe.so
            libtensorflow-lite.so
          arm64/
            ...
        24.04/
          ...
    Darwin/
      universal/
        libprivid_fhe.dylib
    Windows/
      x86_64/
        privid_fhe.dll

This script walks the folder tree and emits a manifest following scripts/manifest_sample.yaml structure.
It also supports a fallback filename parsing strategy for flatter layouts when possible.

Usage:
  python scripts/create_manifest.py \
      --artifacts-root ./native-artifacts \
      --out scripts/manifest.yaml \
      --manifest-version 1.3.11 \
      --bucket cryptonets-python-sdk \
      --base-path privModules

Notes:
- If --latest is not provided, the latest version is inferred by lexicographically max folder name under artifacts root.
- upload_date_time is set to current local time in ISO 8601 with offset.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone
import yaml

# --------------------------- Helpers ---------------------------

def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _iso_now_with_tz() -> str:
    # Local time with timezone offset, e.g. 2025-04-21T18:11:48+02:00
    now = datetime.now().astimezone()
    return now.isoformat(timespec='seconds')


# Try to parse hints like: linux-ubuntu-22.04-x86_64-libprivid_fhe.so
_FILENAME_PATTERN = re.compile(
    r"(?i)^(linux|darwin|windows)[-_]?(?:([a-z0-9]+))?[-_]?([0-9]{2}\.[0-9]{2})?[-_]?((?:x86_64|amd64|arm64|aarch64|universal))?[-_]?.*$"
)


def _norm_arch(s: str | None) -> str | None:
    if not s:
        return s
    s = s.lower()
    if s in ("x86_64", "amd64"):
        return "x86_64"
    if s in ("arm64", "aarch64"):
        return "arm64"
    if s == "universal":
        return "universal"
    return s


def _walk_leaf_files(root: Path):
    """Yield (leaf_dir_relative_parts, file_path) where leaf_dir_relative_parts reflect OS/distro/version/arch.
    The function favors the directory structure. If not enough levels are present, we will attempt filename parsing later.
    """
    for dirpath, _, filenames in os.walk(root):
        dpath = Path(dirpath)
        if not filenames:
            continue
        rel = dpath.relative_to(root)
        parts = [p for p in rel.parts if p]
        for fn in filenames:
            yield parts, dpath / fn


def _insert_entry(manifest_versions: dict, version: str, os_name: str, distro: str | None, distro_ver: str | None, arch: str, filename: str, sha256: str):
    # Build nested dicts as needed according to manifest_sample.yaml
    os_node = manifest_versions.setdefault(version, {})
    # insert upload_date_time if not set
    os_node.setdefault('upload_date_time', _iso_now_with_tz())

    os_name = _canonical_os(os_name)
    os_map = os_node.setdefault(os_name, {})

    if os_name == 'Linux':
        if not distro:
            distro = 'ubuntu'  # default if unknown
        distro_map = os_map.setdefault(distro, {})
        if not distro_ver:
            # if missing, place under "unknown"
            distro_ver = 'unknown'
        ver_map = distro_map.setdefault(str(distro_ver), {})
        arch_list = ver_map.setdefault(arch, [])
        arch_list.append({'filename': filename, 'sha256': sha256})
    elif os_name == 'Darwin':
        # Darwin uses a direct arch (often "universal") mapping to list
        arch_list = os_map.setdefault(arch, [])
        arch_list.append({'filename': filename, 'sha256': sha256})
    elif os_name == 'Windows':
        arch_list = os_map.setdefault(arch, [])
        arch_list.append({'filename': filename, 'sha256': sha256})
    else:
        # Unknown OS bucket — put under its name similar to Windows/Darwin
        arch_list = os_map.setdefault(arch, [])
        arch_list.append({'filename': filename, 'sha256': sha256})


def _canonical_os(s: str) -> str:
    sl = s.lower()
    if sl.startswith('lin'):
        return 'Linux'
    if sl.startswith('dar') or sl.startswith('mac') or sl.startswith('osx'):
        return 'Darwin'
    if sl.startswith('win'):
        return 'Windows'
    # leave as-is with title case
    return s.title()


def _infer_from_parts(parts: list[str]) -> tuple[str | None, str | None, str | None, str | None]:
    """Return (os, distro, distro_version, arch) from directory parts when possible.
    Handles cases where Linux path segments are combined like 'ubuntu-22.04-arm64'.
    """
    os_name: str | None = None
    distro: str | None = None
    distro_ver: str | None = None
    arch: str | None = None

    if not parts:
        return None, None, None, None

    os_name = parts[0]

    # Quick path for non-Linux: expect direct arch under OS
    if not os_name.lower().startswith('lin'):
        if len(parts) >= 2:
            # parts[1] might already be arch (e.g., Windows/x86_64) or further dirs
            arch = _norm_arch(parts[1]) if _norm_arch(parts[1]) else arch
        if len(parts) >= 3 and not arch:
            arch = _norm_arch(parts[2])
        return os_name, None, None, arch

    # Linux: try to parse next 1-3 segments for distro, version, arch
    def apply_token(tok: str):
        nonlocal distro, distro_ver, arch
        t = tok.strip()
        if not t:
            return
        # version like 22.04
        if re.fullmatch(r"\d{2}\.\d{2}", t):
            if not distro_ver:
                distro_ver = t
            return
        # arch
        maybe_arch = _norm_arch(t)
        if maybe_arch in ("x86_64", "arm64", "universal"):
            if not arch:
                arch = maybe_arch
            return
        # distro (fallback)
        if not distro:
            distro = t

    # Consider up to next 3 path parts
    for i in range(1, min(len(parts), 4)):
        seg = parts[i]
        # split on dashes to catch combined segments; keep underscores intact (e.g., x86_64)
        tokens = re.split(r"-", seg)
        for tok in tokens:
            apply_token(tok)
        # If segment itself looks like a pure arch and we didn't get arch from tokens
        if not arch:
            arch = _norm_arch(seg)

    return os_name, distro, distro_ver, arch


def _infer_from_filename(filename: str) -> tuple[str | None, str | None, str | None, str | None]:
    m = _FILENAME_PATTERN.match(filename)
    if not m:
        return None, None, None, None
    os_name, distro, distro_ver, arch = m.groups()
    return os_name, distro, distro_ver, _norm_arch(arch)


def _determine_versions(artifacts_root: Path, latest: str | None) -> tuple[list[str], str | None]:
    versions = [p.name for p in artifacts_root.iterdir() if p.is_dir()]
    versions.sort()
    if latest:
        return versions, latest
    return versions, (versions[-1] if versions else None)


def build_manifest(artifacts_root: Path, manifest_version: str, bucket: str, base_path: str, latest: str | None = None) -> dict:
    versions, latest_final = _determine_versions(artifacts_root, latest)

    manifest: dict = {
        'metadata': {
            'manifest_version': str(manifest_version),
            's3_python_sdk_bucket': bucket,
            'base_path': base_path,
            'latest': latest_final or ''
        },
        'versions': {}
    }

    versions_map: dict = manifest['versions']

    allowed_exts = {'.so', '.dylib', '.dll'}
    for ver in versions:
        ver_root = artifacts_root / ver
        for parts, fpath in _walk_leaf_files(ver_root):
            # Skip files that are not shared libraries
            if fpath.suffix.lower() not in allowed_exts:
                continue
            # Respect structure: expecting parts like [OS, distro, distro_ver, arch, ...]
            os_name, distro, distro_ver, arch = _infer_from_parts(parts)
            if not arch:
                # try filename-based inference
                fos, fdistro, fdver, farch = _infer_from_filename(fpath.name)
                os_name = os_name or fos
                distro = distro or fdistro
                distro_ver = distro_ver or fdver
                arch = _norm_arch(farch) if farch else None
            else:
                arch = _norm_arch(arch)

            if not os_name:
                # default to Linux if nothing else can be determined
                os_name = 'Linux'

            # Apply sensible OS-specific default arch if still unknown
            if not arch:
                cos = _canonical_os(os_name)
                if cos == 'Darwin':
                    arch = 'universal'
                else:
                    # Windows/Linux and others default to x86_64
                    arch = 'x86_64'

            sha256 = _sha256_file(fpath)
            _insert_entry(versions_map, ver, os_name, distro, distro_ver, arch, fpath.name, sha256)

    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description='Create YAML manifest from native-artifacts directory.')
    ap.add_argument('--artifacts-root', default=str(Path(__file__).resolve().parents[1] / 'native-artifacts'),
                    help='Root path to native artifacts (default: ./native-artifacts)')
    ap.add_argument('--out', default=str(Path(__file__).resolve().parent / 'manifest.yaml'),
                    help='Output YAML file (default: scripts/manifest.yaml)')
    ap.add_argument('--manifest-version', default='1.3.11', help='Manifest version string')
    ap.add_argument('--bucket', default='cryptonets-python-sdk', help='S3 bucket name for python sdk')
    ap.add_argument('--base-path', default='privModules', help='Base path in the bucket')
    ap.add_argument('--latest', default=None, help='Explicit latest version (default: infer from directory names)')
    ap.add_argument('--dry-run', action='store_true', help='Do not write file, just print to stdout')

    args = ap.parse_args(argv)

    artifacts_root = Path(args.artifacts_root)
    if not artifacts_root.exists():
        print(f"Artifacts root does not exist: {artifacts_root}", file=sys.stderr)
        return 2

    manifest = build_manifest(artifacts_root, args.manifest_version, args.bucket, args.base_path, args.latest)

    if args.dry_run:
        yaml.safe_dump(manifest, sys.stdout, sort_keys=False)
        return 0

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open('w', encoding='utf-8') as f:
        yaml.safe_dump(manifest, f, sort_keys=False)
    print(f"Manifest written to {out_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
