Cursor assistant prompt — change summary for this project

Use this prompt with Cursor (or any assistant) to generate a concise, actionable summary of changes made to a repository, and to extract the automation/scripts that were added so they can be applied to other projects.

Prompt:

You are a repository assistant. Given this project's working tree and git history, produce a concise, actionable summary that a developer can reuse to apply the same refactor/automation to another repository.

Answer the sections below using 2–8 short bullets each. Prefer Docker-based, OS-agnostic commands. Where relevant, mention file paths and exact commands.

1) What did you change in this project?
  - Extracted notebook logic into a small package `biodiversity/` with modules: `data_io.py`, `processing.py`, `analysis.py`, `viz.py`, and `__init__.py` (version 1.2.0).
  - Added unit tests under `tests/` (test_io.py, test_processing.py, test_analysis.py); 8 tests pass with pytest.
  - Added developer and CI infra: `requirements.txt`, `.pre-commit-config.yaml`, `pyproject.toml`, `.github/workflows/ci.yml` (runs tests and executes the notebook).
  - Added reproducible report tooling: `Dockerfile`, `docker-compose.yml`, interactive runners `scripts/run_report_docker.sh` and `scripts/run_report_docker.ps1`.
  - Updated README.md to document scripts, Docker-based commands, and removed Makefile references (Makefile deleted).
  - Added `CHANGELOG.md` tracking version history.
  - The notebook calls extracted package functions (14 imports from `biodiversity.*`) but some plotting cells were restored to inline code to preserve original visual output.
  - Configured `pyproject.toml` with `[project]` metadata, `[tool.setuptools.packages.find]`, and `setuptools.build_meta` so `pip install -e .` works.
  - Dataset CSVs (`observations.csv`, `species_info.csv`) are tracked with explicit `!` exceptions in `.gitignore`.
  - Generated artifacts (`biodiversity-executed.ipynb`, `report.html`) are now gitignored.

2) What did you add that might be problematic or worth reviewing?
  - Large Docker image install steps (build-essential, git, ipykernel) increase image size (~400MB+ for build-essential alone) — note trade-offs if you later add PDF export (TeX/Playwright).
  - Some notebook plotting cells were restored to verbose inline code (not calling package functions) because modularization altered the visual output; the package functions exist but aren't called for those cells.
  - (Resolved in 1.2.0) Linters were removed from `requirements.txt` and kept in `.pre-commit-config.yaml` only; ruff version fixed from invalid `v0.18.0` to `v0.15.0`; black updated to `26.1.0`.
  - (Resolved in 1.2.0) Generated artifacts gitignored; CSV dataset exceptions added; obsolete `version:` key removed from `docker-compose.yml`.

3) What required multiple fixes / iteration and why?
  - Notebook cell edits: the `EditNotebook` tool requires exact string matches on cell content; fragile replacements left orphaned code fragments. Solved by inserting new clean cells and archiving broken ones, using Python `repr()` / programmatic extraction to get exact cell content before editing.
  - Plot restoration: initial extraction of plotting code into `viz.py` functions changed graph appearance (axis order, colors, labels). User requested "restore" — solved by reverting specific plotting cells to original inline code while keeping the package functions available for reuse.
  - Kernel errors in Docker and CI: nbconvert failed with "No such kernel named python3". Fixed by installing `ipykernel` and registering a `python3` kernel in both the Dockerfile (`python -m ipykernel install --sys-prefix`) and CI (`python -m ipykernel install --user`).
  - Dockerfile parse error: multi-line `RUN apt-get install` with `\\` line continuations was parsed incorrectly by Docker; fixed by collapsing to a single-line command.
  - Linter version conflict: `ruff>=0.18.0` does not exist on PyPI (latest is 0.15.x); caused pip install failure in Docker. Fixed by removing ruff/isort from `requirements.txt`.
  - Test collection failure: `test_preprocess(tmp_path: Path = None)` caused `NameError: name 'Path' is not defined` at collection time. Fixed by adding `from pathlib import Path` import and removing the `= None` default (pytest injects `tmp_path` as a fixture).
  - Type checker warnings: `processing.py` had a type mismatch when mapping a Series; fixed by converting to `.to_dict()` before `.map()`.
  - PowerShell incompatibility: `&&` is not a valid statement separator in older PowerShell versions; all chained commands in scripts and docs must use `;` or separate lines.
  - Makefile added then removed: Makefile targets ran on the host (required `make` installed); user wanted everything inside Docker. Replaced with interactive shell/PS scripts. Makefile deleted.
  - Git push from agent environment: credential/network restrictions prevented pushing from the Cursor agent sandbox; user had to push manually.

4) Automation, CI/CD, Docker, and helper scripts added (path, purpose, exact command)
  - `.github/workflows/ci.yml` — CI that installs deps, registers ipykernel, runs tests, executes notebook.
    - Trigger: push / pull_request to main, master, cursor-version.
  - `Dockerfile` — Python 3.11-slim image; installs build-essential, git, runtime deps, ipykernel; registers `python3` kernel.
    - Build: `docker compose build`
  - `docker-compose.yml` — defines `report` service that mounts project into `/app` and runs nbconvert.
    - Run default (execute notebook): `docker compose run --rm report`
    - Run report + HTML one-liner: `docker compose run --rm report sh -c "python -m nbconvert --to notebook --execute biodiversity.ipynb --ExecutePreprocessor.timeout=600 --output biodiversity-executed.ipynb && python -m nbconvert --to html biodiversity-executed.ipynb --output report.html"`
  - `scripts/run_report_docker.sh` (bash) — interactive menu: (1) create HTML report, (2) open Jupyter, (3) exit.
    - Use: `bash scripts/run_report_docker.sh`
  - `scripts/run_report_docker.ps1` (PowerShell) — Windows interactive menu (same options).
    - Use: `powershell -ExecutionPolicy Bypass -File .\scripts\run_report_docker.ps1`
  - `requirements.txt` — runtime deps only (pandas, matplotlib, seaborn, pytest, nbconvert, black); linters kept in `.pre-commit-config.yaml`.
  - `.pre-commit-config.yaml` — hooks for black, ruff, isort (dev-only, not installed in Docker runtime image).
  - `pyproject.toml` — tool config for black, ruff, isort; build-system metadata.
  - Local report generation (without Docker):
    - `python -m nbconvert --to notebook --execute biodiversity.ipynb --output biodiversity-executed.ipynb`
    - `python -m nbconvert --to html biodiversity-executed.ipynb --output report.html`

5) Checklist to apply same improvements to another repository
  - 1) Create small package folder and extract reusable functions (data_io, processing, analysis, viz); add `__init__.py` with `__version__`.
  - 2) Add unit tests (pytest). Run locally; fix imports and fixtures (`from pathlib import Path`, correct `tmp_path` usage — no default value).
  - 3) Add `requirements.txt` (runtime only) and `.pre-commit-config.yaml` for black/ruff/isort; do NOT put linters in runtime requirements (causes Docker install failures with version mismatches).
  - 4) Add `pyproject.toml` with tool config and `[build-system]`; optionally add `[tool.setuptools.packages.find]` so `pip install -e .` works if needed.
  - 5) Add `Dockerfile` (python:3.11-slim) and `docker-compose.yml`; install runtime deps and `ipykernel`; register a `python3` kernel with `python -m ipykernel install --sys-prefix`. Keep apt-get commands on a single line to avoid Dockerfile parse errors.
  - 6) Add interactive scripts: `run_report_docker.sh` (bash) and `run_report_docker.ps1` (PowerShell) that call `docker compose` to execute notebook and export HTML.
  - 7) Add CI workflow (`.github/workflows/ci.yml`): checkout, setup-python, pip install -r requirements.txt, install ipykernel + register kernel, run pytest, execute notebook with nbconvert.
  - 8) Ensure dataset files are committed: if `.gitignore` has `*.csv`, add exceptions like `!observations.csv`.
  - 9) Remove `version:` key from `docker-compose.yml` (obsolete warning).
  - 10) Decide how to handle executed artifacts: commit them, gitignore them, or upload as CI artifacts.
  - 11) Use `;` instead of `&&` in PowerShell commands and scripts; avoid heredocs in PowerShell.
  - 12) Update README to document scripts and Docker commands; keep instructions OS-agnostic.

Constraints reminder:
- Keep answers concise when generating the summary.
- Prefer Docker-based commands for cross-platform compatibility.
- Flag trade-offs for large installs (TeX/Playwright).

Use this updated prompt with Cursor to produce the final change-summary you asked for when applying this pattern to other projects.
