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
pip install -e .              # optional: makes the biodiversity package importable everywhere
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
- `pyproject.toml` — project metadata and tool config (black, ruff, isort); supports `pip install -e .`
- `CHANGELOG.md` — version history

Scripts

Two convenience scripts are provided to run the report from the project root (they call Docker Compose so no local Python installs are required):

- Bash (Linux / macOS / WSL / Git Bash): `scripts/run_report_docker.sh`
- PowerShell (Windows): `scripts/run_report_docker.ps1`

Both scripts present a small interactive menu:

1. Create HTML report — builds the image (no-cache), executes the notebook, and exports `report.html` (and `biodiversity-executed.ipynb`) into the project root.
2. Open Jupyter Notebook — starts a containerized Jupyter server bound to localhost:8888.
3. Exit

Quick commands (no make)

If you don't want to use the interactive scripts, use these Docker Compose one-liners:

- Produce HTML report:
  ```sh
  docker compose run --rm report sh -c "python -m nbconvert --to notebook --execute biodiversity.ipynb --ExecutePreprocessor.timeout=600 --output biodiversity-executed.ipynb && python -m nbconvert --to html biodiversity-executed.ipynb --output report.html"
  ```

- Start a Jupyter server via container:
  ```sh
  docker compose run --service-ports --rm report sh -c "python -m notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''"
  ```

CHANGELOG

- See `CHANGELOG.md` for the recent changes and version notes.

License

This project is available under the MIT License. See the `LICENSE` file.