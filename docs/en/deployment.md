# Deployment

This project uses MkDocs + Material. A GitHub Actions workflow should:

1) Install docs dependencies
2) Build with `mkdocs build --strict`
3) Publish the `site/` directory to GitHub Pages

Example steps:

```bash
uv sync --extra docs
uv run mkdocs build --strict
```

Make sure the workflow adds a `.nojekyll` file in the published output.
