# Release automation scripts

These helpers keep version numbers, changelog entries, and release artifacts in
sync. All commands should be run from the repository root and use `uv` for
reproducibility.

## Bump the version

```bash
uv run python scripts/release/bump_version.py 1.2.3
uv run python scripts/release/bump_version.py 1.2.3 --suffix a2
uv run python scripts/release/bump_version.py 1.2.3 --dry-run
```

The script updates `pyproject.toml` and `jalali_pandas/_version.py` so
`__version__` matches the published package. Prerelease suffixes (`a`, `b`,
`rc`) are supported via `--suffix`.

## Finalize the changelog

```bash
uv run python scripts/release/changelog.py 1.2.3
uv run python scripts/release/changelog.py 1.2.3 --date 2026-01-31 --dry-run
```

The command moves entries from **Unreleased** into a dated section and updates
links at the bottom of `CHANGELOG.md` to point to the new tag.

## Build artifacts

```bash
uv run python scripts/release/build.py
```

This cleans `dist/`, builds the sdist and wheel via `python -m build`, and runs
`twine check` to validate metadata.
