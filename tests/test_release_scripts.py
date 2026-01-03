from __future__ import annotations

from pathlib import Path

from scripts.release import bump_version, changelog


def test_bump_version_updates_files(tmp_path: Path, monkeypatch: object) -> None:
    project = tmp_path / "pyproject.toml"
    project.write_text("""[project]\nversion = \"0.1.0\"\n""")
    version_file = tmp_path / "_version.py"
    version_file.write_text(
        '__version__ = "0.1.0"\n__version_info__ = ( 0, 1, 0, "final", 0 )\n'
    )

    monkeypatch.setattr(bump_version, "PROJECT_FILE", project)
    monkeypatch.setattr(bump_version, "VERSION_FILE", version_file)

    version = bump_version.parse_version("1.2.3b2")
    bump_version.update_pyproject(version, False)
    bump_version.update_version_file(version, False)

    assert 'version = "1.2.3b2"' in project.read_text()
    body = version_file.read_text()
    assert '__version__ = "1.2.3b2"' in body
    assert '"beta"' in body


def test_changelog_promotes_unreleased(tmp_path: Path, monkeypatch: object) -> None:
    changelog_file = tmp_path / "CHANGELOG.md"
    changelog_file.write_text(
        """# Changelog\n\n## [Unreleased]\n\n### Added\n- Pending\n\n## [0.1.0] - 2023-01-01\n\n[Unreleased]: https://example.com/compare/v0.1.0...HEAD\n[0.1.0]: https://example.com/compare/v0.0.1...v0.1.0\n"""
    )
    monkeypatch.setattr(changelog, "CHANGELOG", changelog_file)

    output = changelog.finalize_changelog("0.2.0", date="2024-02-02", dry_run=True)
    assert output is not None
    assert "## [0.2.0] - 2024-02-02" in output
    assert "- Pending" in output
    assert "[Unreleased]: https://example.com/compare/v0.2.0...HEAD" in output
