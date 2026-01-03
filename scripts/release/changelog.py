"""Manage Keep a Changelog entries when tagging releases."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGELOG = ROOT / "CHANGELOG.md"

HEADER_PATTERN = re.compile(r"^## \[(?P<section>.+?)\]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finalize changelog for release")
    parser.add_argument("version", help="Version being released (e.g. 1.2.3)")
    parser.add_argument(
        "--date", default=None, help="Override release date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show updates without writing",
    )
    return parser.parse_args()


def find_sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    positions: dict[str, tuple[int, int]] = {}
    current: str | None = None
    start = 0
    for idx, line in enumerate(lines):
        match = HEADER_PATTERN.match(line)
        if match:
            if current is not None:
                positions[current] = (start, idx)
            current = match.group("section")
            start = idx
    if current is not None:
        positions[current] = (start, len(lines))
    return positions


def update_links(text: str, version: str, previous: str | None) -> str:
    base = "https://github.com/ghodsizadeh/jalali-pandas"
    for line in text.splitlines():
        if line.startswith("[Unreleased]:"):
            base = line.split(" ", 1)[1].split("/compare")[0]
            break
    unreleased = f"[Unreleased]: {base}/compare/v{version}...HEAD"
    new_version = (
        f"[{version}]: {base}/compare/v{previous}...v{version}" if previous else None
    )
    lines = text.rstrip().splitlines()
    updated: list[str] = []
    replaced_unreleased = False
    inserted_version = False
    for line in lines:
        if line.startswith("[Unreleased]:"):
            updated.append(unreleased)
            replaced_unreleased = True
            continue
        if new_version and not inserted_version and previous and line.startswith(
            f"[{previous}]"
        ):
            updated.append(new_version)
            inserted_version = True
        updated.append(line)
    if not replaced_unreleased:
        updated.append(unreleased)
    if not inserted_version and new_version:
        updated.append(new_version)
    return "\n".join(updated) + "\n"


def finalize_changelog(version: str, date: str | None = None, dry_run: bool = False) -> str | None:
    release_date = date or dt.date.today().isoformat()
    lines = CHANGELOG.read_text().splitlines()
    sections = find_sections(lines)
    if "Unreleased" not in sections:
        raise ValueError("CHANGELOG is missing an Unreleased section")

    unreleased_start, unreleased_end = sections["Unreleased"]
    next_section_starts = [
        start for name, (start, _) in sections.items() if name != "Unreleased"
    ]
    next_section_start = min(next_section_starts) if next_section_starts else len(lines)
    content_start = unreleased_start + 1
    content_end = next_section_start
    new_lines = lines[:unreleased_start + 1]
    new_lines.append("")
    new_lines.append(f"## [{version}] - {release_date}")
    new_lines.extend(lines[content_start:content_end])
    if new_lines[-1].strip():
        new_lines.append("")
    new_lines.extend(lines[unreleased_end:])

    previous_versions = [name for name in sections if name not in {"Unreleased"}]
    previous_versions.sort()
    previous = previous_versions[-1] if previous_versions else None

    updated_text = "\n".join(new_lines) + "\n"
    updated_text = update_links(updated_text, version, previous)

    if dry_run:
        return updated_text

    CHANGELOG.write_text(updated_text)
    return None


if __name__ == "__main__":
    parsed = parse_args()
    output = finalize_changelog(
        parsed.version, date=parsed.date, dry_run=parsed.dry_run
    )
    if output:
        print(output)
