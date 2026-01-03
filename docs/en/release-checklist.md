# Release checklist

Follow this checklist before tagging a new release.

1. **Finalize the changelog**
   - Fill out the *Unreleased* section in `CHANGELOG.md`.
   - Run `uv run python scripts/release/changelog.py <version>`.
2. **Bump the version**
   - Run `uv run python scripts/release/bump_version.py <version>`.
   - Confirm `pyproject.toml` and `jalali_pandas/_version.py` match.
3. **Run quality gates**
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - `uv run pytest`
   - `uv run mypy jalali_pandas`
   - `uv run pyright jalali_pandas`
   - `uv sync --extra docs --frozen && uv run mkdocs build --strict`
   - `uv run python -m compileall examples`
4. **Tag the release**
   - `git tag -s v<version> -m "Release v<version>"`
   - `git push origin v<version>`
5. **Verify CI publishing**
   - Confirm GitHub Actions release workflow publishes to
     TestPyPI (prerelease) or PyPI (stable).
   - Download build artifacts and review `twine check` output.
6. **Verify documentation**
   - Visit GitHub Pages and confirm `/latest/` points to the new release.
   - Confirm `/v<version>/` was published.
7. **Announce**
   - Draft release notes or announcements referencing the changelog.
   - Share links to the PyPI release and documentation.
