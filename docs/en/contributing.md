# Contributing

Thanks for contributing to jalali_pandas.

## Development setup

```bash
uv sync --extra dev
```

## Tests

```bash
uv run pytest
uv run pytest --cov=jalali_pandas --cov-report=xml
```

## Linting and formatting

```bash
uv run ruff check jalali_pandas tests
uv run ruff format --check jalali_pandas tests
```

## Type checking

```bash
uv run mypy jalali_pandas
uv run pyright jalali_pandas
```

## Docs build

```bash
uv sync --extra docs
uv run mkdocs build --strict
```

## Notes

- Keep public APIs typed.
- Follow Ruff formatting rules (88 chars).
- Add tests for accessors/offsets and type behavior.
