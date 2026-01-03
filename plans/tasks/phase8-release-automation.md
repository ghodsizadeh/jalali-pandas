# Task: Implement Phase 8 Release & Documentation Automation

## Objective
Deliver the automation and human-in-the-loop steps defined in Phase 8 of the implementation roadmap so releases can be cut, validated, and published with minimal manual effort.

## Scope
- Build tooling/scripts to automate version bumps, packaging, and publishing.
- Add CI workflows that validate, build, and deploy artifacts to TestPyPI/PyPI and GitHub Pages.
- Wire changelog/version management and documentation automation to keep releases consistent.

## Deliverables
- `scripts/release/` utilities to bump versions, clean artifacts, and build sdist/wheel.
- GitHub Actions workflows for release publishing and docs build/deploy with dry-run support.
- Automated changelog updates and release notes generation tied to version tags.
- Versioned documentation published to GitHub Pages (latest + tagged versions).
- Release checklist capturing the required manual verifications.

## Work Breakdown
1. **Packaging & Publishing Automation**
   - Create a consolidated release script (`scripts/release/build.py` or `release.sh`) that cleans `dist/` and builds artifacts via `uv run python -m build`.
   - Add a GitHub Actions release workflow triggered on `v*` tags that runs lint, tests, type checks, builds artifacts, runs `uv run twine check dist/*`, and publishes to TestPyPI for prereleases or PyPI for stable tags using trusted publishing.
   - Provide a manual `workflow_dispatch` dry-run path and upload build logs/artifacts for traceability.
   - Document required repository permissions/secrets and how to opt into trusted publishing.

2. **Versioning & Changelog Management**
   - Establish a single version source of truth (e.g., `jalali_pandas/__init__.py` synced with `pyproject.toml`) and add a helper to bump both.
   - Adopt or refine Keep a Changelog sections, wiring automation to move entries from Unreleased to release sections during tagging.
   - Configure Release Drafter (or similar) to assemble release notes from merged PRs/labels, and gate publishing on approval.

3. **Documentation Automation**
   - Add a docs workflow that runs `uv run mkdocs build --strict` on PRs and publishes to `gh-pages` on tags.
   - Implement docs versioning (latest + per-tag paths) and automate API reference generation with `mkdocs-gen-files`/`mkdocstrings`.
   - Validate or execute examples/notebooks in CI to prevent stale docs content.

4. **Release Checklist (Human-in-the-loop)**
   - Verify changelog completeness and version bumps before tagging.
   - Run `uv run pytest`, `uv run ruff check`, and docs build locally or via CI gates.
   - Create a signed tag (`git tag -s vX.Y.Z`), push, and confirm TestPyPI/PyPI uploads and docs deployment.
   - Publish announcement links once artifacts and docs are live.

## Success Criteria
- Tagging a release triggers CI that validates, builds, and publishes artifacts and docs without manual patching.
- Changelog entries and version numbers stay in sync across code, package metadata, and published docs.
- Dry-run workflows enable safe rehearsal of releases.
