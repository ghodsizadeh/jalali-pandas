# Prompt: Implement Phase 8 Release & Documentation Automation

You are tasked with implementing the Phase 8 automation scope defined in `plans/8-implementation-roadmap.md` and `plans/tasks/phase8-release-automation.md`. Follow these directives strictly.

## Objectives
- Automate packaging and publishing to TestPyPI/PyPI with trusted publishing.
- Automate versioning/changelog management and release-note generation.
- Automate docs build/versioning and publishing to GitHub Pages.
- Provide a release checklist for human verification.

## Constraints & Standards
- Use `uv` for dependency install and invocation where applicable.
- Keep version source of truth synchronized between `pyproject.toml` and `jalali_pandas/__init__.py`.
- Preserve Keep a Changelog format in `CHANGELOG.md`.
- Follow repo coding standards in `AGENTS.md` (Ruff formatting, 88-char lines, typed public APIs).

## Work Items
1. **Release Tooling (`scripts/release/`)**
   - Add `build.py` (or `build.sh`) to clean `dist/`, build sdist/wheel via `uv run python -m build`, and run `uv run twine check dist/*`.
   - Add `bump_version.py` to update both `pyproject.toml` and `jalali_pandas/__init__.py`; support prerelease suffixes and dry-run flag.
   - Add `changelog.py` helper to move "Unreleased" entries into a new version section with date when tagging.
   - Provide a `README.md` in `scripts/release/` explaining usage.

2. **CI Workflows**
   - Create `.github/workflows/release.yml` triggered on tags `v*` and manual `workflow_dispatch` with a `dry_run` input.
   - Steps: checkout with `fetch-depth: 0`; set up Python + uv cache; install deps; run `ruff check`, format check, `pytest`, type checks; build artifacts; run `twine check`; publish to TestPyPI for prerelease tags and PyPI for stable using trusted publishing; upload dist/ and logs as artifacts.
   - Add gate for release approval (required reviewer or environment protection) before publish job runs.
   - Add `.github/workflows/docs.yml` to build docs on PRs and publish to `gh-pages` on tags; include API reference generation and cache; host under `/latest/` and `/vX.Y.Z/`.
   - If using Release Drafter, add `.github/release-drafter.yml` and ensure workflow exists/updated.

3. **Docs Versioning & Execution**
   - Configure MkDocs with version switcher (e.g., `mkdocs-material` versioning plugin or static selector) to publish latest + tag paths.
   - Automate API docs with `mkdocs-gen-files`/`mkdocstrings` during CI; ensure config lives in `docs/` or `mkdocs.yml`.
   - Add CI validation for examples/notebooks (execute or sanity-check) to prevent stale content.

4. **Release Checklist**
   - Add `docs/release-checklist.md` (or update existing) covering: changelog completeness, version bump, lint/tests/docs build commands, signed tag creation (`git tag -s vX.Y.Z`), CI publish confirmation, docs deployment verification, announcement links.

## Acceptance Criteria
- Tagging a version triggers CI that lint/tests/builds/publishes artifacts and docs automatically; dry-run path available.
- Changelog and version numbers remain in sync across metadata and docs.
- Docs site publishes latest and tagged versions to GitHub Pages.
- Scripts include usage docs and support dry-run/validation.

## Delivery Instructions
- Update relevant docs (README, CHANGELOG, `plans/8-implementation-roadmap.md` if necessary) to reflect automation.
- Add tests/smoke checks for new scripts where feasible.
- Ensure commits are clean and CI configurations reference pinned tool versions.
