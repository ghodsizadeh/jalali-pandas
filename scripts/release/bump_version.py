"""Bump jalali-pandas version across metadata files."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
PROJECT_FILE = ROOT / "pyproject.toml"
VERSION_FILE = ROOT / "jalali_pandas" / "_version.py"

STAGE_LABELS = {"a": "alpha", "b": "beta", "rc": "candidate"}


@dataclass
class Version:
    major: int
    minor: int
    patch: int
    prerelease: str | None = None
    prerelease_num: int | None = None

    def __str__(self) -> str:  # pragma: no cover - trivial
        suffix = ""
        if self.prerelease:
            suffix = f"{self.prerelease}{self.prerelease_num or 0}"
        return f"{self.major}.{self.minor}.{self.patch}{suffix}"


VERSION_PATTERN = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:(?P<label>a|b|rc)(?P<num>\d+))?$"
)


def parse_version(version: str) -> Version:
    match = VERSION_PATTERN.match(version)
    if not match:
        raise ValueError(f"Invalid version: {version}")
    prerelease = match.group("label")
    prerelease_num = match.group("num")
    return Version(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        prerelease=prerelease,
        prerelease_num=int(prerelease_num) if prerelease_num else None,
    )


def format_version_info(version: Version) -> str:
    stage = STAGE_LABELS.get(version.prerelease or "", "final")
    number = version.prerelease_num or 0
    return (
        "( "
        f"{version.major}, {version.minor}, {version.patch}, \"{stage}\", {number} "
        ")"
    )


def replace_in_file(path: Path, patterns: Iterable[tuple[str, str]]) -> None:
    text = path.read_text()
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    path.write_text(text)


def update_pyproject(version: Version, dry_run: bool) -> None:
    patterns = [(r"^version\s*=\s*\".*\"", f'version = "{version}"')]
    if dry_run:
        return
    replace_in_file(PROJECT_FILE, patterns)


def update_version_file(version: Version, dry_run: bool) -> None:
    patterns = [
        (r'^__version__\s*=\s*".*"', f'__version__ = "{version}"'),
        (
            r'^__version_info__\s*=\s*\(.*\)$',
            f"__version_info__ = {format_version_info(version)}",
        ),
    ]
    if dry_run:
        return
    replace_in_file(VERSION_FILE, patterns)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bump project version")
    parser.add_argument("version", help="Target version (e.g. 1.2.3 or 1.2.3a1)")
    parser.add_argument(
        "--suffix",
        help="Prerelease suffix to append (e.g. a2, b1, rc1)",
        default=None,
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report changes without writing"
    )
    return parser.parse_args()


def build_version(args: argparse.Namespace) -> Version:
    base = args.version
    if args.suffix:
        base = f"{base}{args.suffix}"
    return parse_version(base)


def main() -> None:
    args = parse_args()
    version = build_version(args)
    update_pyproject(version, args.dry_run)
    update_version_file(version, args.dry_run)
    if args.dry_run:
        print(f"Would set version to {version}")


if __name__ == "__main__":
    main()
