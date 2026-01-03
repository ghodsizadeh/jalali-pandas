"""Build release artifacts for jalali-pandas."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = ROOT / "dist"


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(command)}\n"
            f"stdout:\n{result.stdout.decode()}\n"
            f"stderr:\n{result.stderr.decode()}"
        )


def clean_dist() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def build_artifacts() -> None:
    run(["uv", "run", "python", "-m", "build"])


def check_artifacts() -> None:
    artifacts = sorted(str(path) for path in DIST_DIR.glob("*"))
    if not artifacts:
        raise RuntimeError("No artifacts were produced in dist/")
    run(["uv", "run", "twine", "check", *artifacts])


def main() -> None:
    clean_dist()
    build_artifacts()
    check_artifacts()


if __name__ == "__main__":
    main()
