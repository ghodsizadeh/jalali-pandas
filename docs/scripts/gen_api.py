"""Generate API reference stubs for MkDocs."""

from __future__ import annotations

from pathlib import Path

import mkdocs_gen_files

PACKAGE_ROOT = Path("jalali_pandas")
API_ROOT = Path("en/api")

SECTIONS: dict[str, dict[str, list[str] | str]] = {
    "api": {
        "title": "Public API",
        "modules": [
            "jalali_pandas.api.conversion",
            "jalali_pandas.api.date_range",
            "jalali_pandas.api.grouper",
        ],
    },
    "core": {
        "title": "Core",
        "modules": [
            "jalali_pandas.core.timestamp",
            "jalali_pandas.core.dtypes",
            "jalali_pandas.core.arrays",
            "jalali_pandas.core.indexes",
            "jalali_pandas.core.calendar",
            "jalali_pandas.core.conversion",
        ],
    },
    "offsets": {
        "title": "Offsets",
        "modules": [
            "jalali_pandas.offsets",
            "jalali_pandas.offsets.aliases",
            "jalali_pandas.offsets.base",
            "jalali_pandas.offsets.month",
            "jalali_pandas.offsets.quarter",
            "jalali_pandas.offsets.year",
            "jalali_pandas.offsets.week",
        ],
    },
    "accessors": {
        "title": "Accessors",
        "modules": [
            "jalali_pandas.accessors.series",
            "jalali_pandas.accessors.dataframe",
        ],
        "legacy": [
            "jalali_pandas.df_handler",
            "jalali_pandas.serie_handler",
        ],
    },
}


for name, config in SECTIONS.items():
    doc_path = API_ROOT / f"{name}.md"
    with mkdocs_gen_files.open(doc_path, "w") as fd:
        fd.write(f"# {config['title']}\n\n")
        for module in config["modules"]:
            fd.write(f"::: {module}\n\n")
        if "legacy" in config:
            fd.write("## Legacy accessors\n\n")
            for module in config["legacy"]:  # type: ignore[index]
                fd.write(f"::: {module}\n\n")
    mkdocs_gen_files.set_edit_path(doc_path, str(PACKAGE_ROOT / "__init__.py"))
