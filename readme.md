# Biodiversity in U.S. National Parks

This repository contains a reproducible analysis of species observations across U.S. National Parks. The primary artifact is a Jupyter notebook (analysis) and a small Python package (`biodiversity/`) that contains extracted helpers for data loading, cleaning, analysis and visualization.

Quick highlights
- Notebook: `biodiversity.ipynb` (analysis + narrative)
- Package: `biodiversity/` (loaders, processing, analysis, viz)
- Tests: pytest-based unit tests under `tests/`
- CI: GitHub Actions workflow runs tests and executes the notebook
- Docker: image + compose to run the report without local dependency setup

Supported (recommended) environment
- Python 3.11
- See `requirements.txt` for pinned runtime/dev dependencies

Getting started (local)

1. Clone the repository

```sh
git clone <repo-url>
cd biodiversity
```

2. Create a virtual environment and install dependencies

```sh
python -m venv .venv
source .venv/bin/activate    # or .\\.venv\\Scripts\\Activate.ps1 on Windows PowerShell
pip install -r requirements.txt
```

3. Run tests

```sh
python -m pytest -q
```

4. Launch the notebook (optional)

```sh
jupyter notebook biodiversity.ipynb
```

Automated report generation (recommended)

- To execute the notebook end-to-end and produce an executed notebook:
  - Locally: `python -m nbconvert --to notebook --execute biodiversity.ipynb --output biodiversity-executed.ipynb`
  - With Docker (recommended, isolated): see Docker section below

Pre-commit and formatting

We provide a `.pre-commit-config.yaml` with Black, Ruff and isort hooks. Install locally with:

```sh
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Continuous Integration

- GitHub Actions workflow is configured at `.github/workflows/ci.yml`. It runs on pushes and PRs to `main`, `master` and `cursor-version`, installs requirements, runs the tests and executes the notebook.

Docker (run the report without local installs)

- Build the image:
  ```sh
  docker compose build
  ```
- Run the report (the executed notebook will be produced in the project directory as `biodiversity-executed.ipynb`):
  ```sh
  docker compose run --rm report
  ```

Project files

- `biodiversity.ipynb` — primary analysis notebook (narrative + code)
- `biodiversity/` — Python package with helper modules (data_io, processing, analysis, viz)
- `tests/` — unit tests
- `requirements.txt` — runtime/dev dependencies
- `.github/workflows/ci.yml` — CI pipeline
- `Dockerfile`, `docker-compose.yml` — containerized report runner
- `biodiversity-executed.ipynb` — last executed notebook (artifact)
Makefile

Makefile commands

If you prefer simple commands, a Makefile is provided. From the project root:

- Run tests:
  ```sh
  make test
  ```
- Execute the report locally (uses scripts/run_report.sh):
- Execute the report (runs in Docker for OS-independence):
  ```sh
  make run-report
  ```
- Build the Docker image:
  ```sh
  make docker-build
  ```
- Run the report in Docker (writes executed notebook to project directory):
  ```sh
  make docker-run
  ```

CHANGELOG

- See `CHANGELOG.md` for the recent changes and version notes.

License

This project is available under the MIT License. See the `LICENSE` file.