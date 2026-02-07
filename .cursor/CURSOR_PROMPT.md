Cursor assistant prompt — change summary for this project

Use this prompt with Cursor (or any assistant) to generate a concise, actionable summary of changes made to a repository, and to extract the automation/scripts that were added so they can be applied to other projects.

Prompt:

You are a repository assistant. Given this project's working tree and git history, produce a concise, actionable summary that a developer can reuse to apply the same refactor/automation to another repository.

Answer the sections below using 2–8 short bullets each. Prefer Docker-based, OS-agnostic commands. Where relevant, mention file paths and exact commands.

1) What did you change in this project?
  - Extracted notebook logic into a small package `biodiversity/` with modules: `data_io.py`, `processing.py`, `analysis.py`, `viz.py`, and `__init__.py` (version bumped to 1.1.2).
  - Added unit tests under `tests/` (tests/test_io.py, tests/test_processing.py, tests/test_analysis.py) and fixed test signatures/imports so pytest collects correctly.
  - Added developer and CI infra: `requirements.txt`, `.pre-commit-config.yaml`, `pyproject.toml`, `.github/workflows/ci.yml` (runs tests and executes the notebook).
  - Added reproducible report tooling: `Dockerfile`, `docker-compose.yml`, interactive runners `scripts/run_report_docker.sh` and `scripts/run_report_docker.ps1`, plus `scripts/run_report_docker.sh` exports `report.html`.
  - Updated README.md to document the scripts and Docker-based, OS-agnostic commands; removed Makefile references and deleted the Makefile.
  - Created artifacts during work: `biodiversity-executed.ipynb` and `report.html`.

2) What did you add that might be problematic or worth reviewing?
  - Initial inclusion of linters in `requirements.txt` (ruff/isort) caused Docker install failures; moved linters to pre-commit or dev-only places to avoid runtime install issues.
  - Large Docker image install steps (build-essential, ipykernel, optional Playwright/TeX) increase image size—note trade-offs if you later add PDF export.
  - Executed artifacts (`biodiversity-executed.ipynb`, `report.html`) are committed/produced — consider adding them to `.gitignore` or uploading as CI artifacts instead of committing.

3) What required multiple fixes / iteration and why?
  - Notebook cell edits: JSON cell content and indices caused fragile notebook edits; solved by inserting clean cells and archiving fragments rather than trying fragile in-place replacements.
  - Kernel errors in CI: nbconvert failed with "No such kernel named python3"; fixed by installing `ipykernel` and registering a `python3` kernel in the Dockerfile and CI.
  - Type/import/test issues: tests expected `Path` and tmp_path usage; fixed test imports and signatures to be pytest-compatible.
  - Linter/runtime conflicts: earlier attempts to run linters in CI or install linters in the runtime image caused version/compat issues; moved linters to pre-commit and dev flows.

4) Automation, CI/CD, Docker, and helper scripts added (path, purpose, exact command)
  - `.github/workflows/ci.yml` — CI that installs deps, runs tests, registers kernel, executes notebook.
    - Trigger: push / pull_request to main, master, cursor-version.
  - `Dockerfile` — image used to run/execute notebook and produce report; installs runtime deps and `ipykernel`.
    - Build: `docker compose build`
  - `docker-compose.yml` — defines `report` service that mounts project and runs commands.
    - Run report one-liner: `docker compose run --rm report sh -c "python -m nbconvert --to notebook --execute biodiversity.ipynb --ExecutePreprocessor.timeout=600 --output biodiversity-executed.ipynb && python -m nbconvert --to html biodiversity-executed.ipynb --output report.html"`
  - `scripts/run_report_docker.sh` (bash) — interactive runner: build, execute notebook, export HTML; use: `bash scripts/run_report_docker.sh`
  - `scripts/run_report_docker.ps1` (PowerShell) — Windows interactive runner (same actions); use: `powershell -ExecutionPolicy Bypass -File .\scripts\run_report_docker.ps1`
  - `requirements.txt` — runtime deps for CI/Docker (moved linters out of runtime to avoid install failures).

5) Checklist to apply same improvements to another repository
  - 1) Create small package folder and extract reusable functions (data_io, processing, analysis, viz); add `__init__.py` and set package version.
  - 2) Add unit tests (pytest). Run locally; fix imports and fixtures (`from pathlib import Path`, correct tmp_path usage).
  - 3) Add `requirements.txt` (runtime only) and `.pre-commit-config.yaml` for black/ruff/isort; avoid installing linters in runtime image.
  - 4) Add `Dockerfile` and `docker-compose.yml` that install runtime deps and `ipykernel`; register a `python3` kernel (for nbconvert).
  - 5) Add interactive scripts: `run_report_docker.sh` and `run_report_docker.ps1` that call `docker compose` one-liners to execute the notebook and export HTML.
  - 6) Add CI workflow: checkout, setup-python, pip install -r requirements.txt, (install ipykernel and register python3), run pytest, execute notebook with nbconvert.
  - 7) Run CI locally with a container first; iterate until nbconvert/kernel/test issues are resolved.
  - 8) Decide how to handle executed artifacts: commit, ignore, or upload as CI artifacts.

Constraints reminder:
- Keep answers concise when generating the summary.
- Prefer Docker-based commands for cross-platform compatibility.
- Flag trade-offs for large installs (TeX/Playwright).

Use this updated prompt with Cursor to produce the final change-summary you asked for when applying this pattern to other projects.

