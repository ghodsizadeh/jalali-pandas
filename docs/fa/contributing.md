# مشارکت

از مشارکت شما در jalali_pandas خوشحال می‌شویم.

## راه‌اندازی توسعه

```bash
uv sync --extra dev
```

## تست‌ها

```bash
uv run pytest
uv run pytest --cov=jalali_pandas --cov-report=xml
```

## لینت و فرمت

```bash
uv run ruff check jalali_pandas tests
uv run ruff format --check jalali_pandas tests
```

## بررسی نوع‌ها

```bash
uv run mypy jalali_pandas
uv run pyright jalali_pandas
```

## ساخت مستندات

```bash
uv sync --extra docs
uv run mkdocs build --strict
```
