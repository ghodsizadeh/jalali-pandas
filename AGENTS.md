# Repository Guidelines

## Project Structure & Module Organization
- `jalali_pandas/` contains the core library (accessors, offsets, core types).
- `tests/` holds pytest suites (unit tests for series, dataframe, timestamp behavior).
- `docs/` is MkDocs documentation content and assets.
- `examples/` includes usage notebooks and sample code.
- `plans/` contains internal design/roadmap notes.

## Build, Test, and Development Commands
Use `uv` when available (aligned with CI); pip works too.
- `uv sync --all-extras` installs dev/docs/benchmark extras.
- `uv run pytest` runs the test suite.
- `uv run pytest --cov=jalali_pandas --cov-report=xml` runs tests with coverage.
- `uv run ruff check jalali_pandas tests` runs linting.
- `uv run ruff format --check jalali_pandas tests` verifies formatting.
- `uv run mypy jalali_pandas` and `uv run pyright jalali_pandas` run type checks.
- `uv sync --extra docs` then `uv run mkdocs build --strict` builds docs.

## Coding Style & Naming Conventions
- Python 3.9+ with type hints; keep public APIs typed.
- Formatting and linting are enforced by Ruff with 88-char lines.
- Use snake_case for functions/variables, PascalCase for classes, and `test_` names for tests.
- Keep imports sorted (Ruff isort rules) and prefer explicit, local imports.

## Testing Guidelines
- Framework: pytest; configured in `pyproject.toml`.
- Test files may be `test_*.py` or `*_test.py` (both are used).
- Add focused unit tests for new accessors/offsets and type behavior.
- Make sure test coverage is above 90%.

## Commit & Pull Request Guidelines
- Commit subjects are short and descriptive; prefixes like `Phase N:`, `CI:`, or `Update` are common.
- PRs should include: summary of behavior changes, test coverage notes, and linked issues when relevant.
- Add screenshots only for docs or example output changes.
