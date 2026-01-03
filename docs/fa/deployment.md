# انتشار

مستندات با MkDocs + Material ساخته می‌شود و در GitHub Pages منتشر می‌شود.

مراحل کلی:

```bash
uv sync --extra docs
uv run mkdocs build --strict
```

در گردش‌کار انتشار باید فایل `.nojekyll` به خروجی اضافه شود.
