# Benchmarks

The repository no longer ships ASV benchmarks by default. If you want to track
performance, you can reintroduce ASV in your fork:

1) Add `asv` to optional dependencies in `pyproject.toml`.
2) Add an `asv.conf.json` config and a `benchmarks/` directory.
3) Run `uv run asv run --quick`.

For ad-hoc performance checks, you can use:

- `scripts/profile_conversion.py`

If benchmarks are reintroduced, document the workflow here.
