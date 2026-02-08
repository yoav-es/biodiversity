# Changelog

All notable changes to this project are documented in this file.

## 1.2.0 - 2026-02-08
- Fixed `.pre-commit-config.yaml`: updated ruff from invalid `v0.18.0` to `v0.15.0`, black from `23.9.1` to `26.1.0`, corrected repo URL to `astral-sh/ruff-pre-commit`.
- Removed obsolete `version: '3.8'` key from `docker-compose.yml`.
- Gitignored generated artifacts (`biodiversity-executed.ipynb`, `report.html`) to avoid noisy diffs.
- Added `!observations.csv` and `!species_info.csv` exceptions to `.gitignore` so dataset intent is explicit.
- Added `[project]` metadata and `[tool.setuptools.packages.find]` to `pyproject.toml` so `pip install -e .` works.
- Bumped package version to 1.2.0.

## 1.1.2 - 2026-02-07
- CI: GitHub Actions workflow to run tests and execute the notebook.
- Added Docker support to run the report in an isolated container.
- Added pre-commit config and formatting tooling.
- Interactive runner scripts (`scripts/run_report_docker.sh`, `scripts/run_report_docker.ps1`).
- Updated README with Docker/script documentation; removed Makefile.

## 1.1.1 - 2026-02-07
- Restored bat plotting cell in notebook to preserve original visual behavior.
- Bumped package version to 1.1.1.
- Added CI, requirements, pre-commit config.

## 1.1.0 - prior
- Initial extraction of helpers into `biodiversity/` package.
- Unit tests added.
