# Biodiversity in U.S. National Parks

This repository contains a reproducible analysis of species observations across U.S. National Parks. The primary artifact is a Jupyter notebook and a supporting Python package (`biodiversity/`) containing extracted helper modules for data processing, analysis, and visualization.

## Quick Highlights

- **Notebook**: `biodiversity.ipynb` - Primary interactive analysis and narrative report
- **Package**: `biodiversity/` - Supporting modules for data loading, processing, analysis, and visualization
- **Environment**: Python 3.11
- **Execution**: Local CLI, Docker Compose, and interactive shell/PowerShell scripts

## Overview

This project provides an empirical analysis of species observations and conservation statuses across U.S. National Parks. It aims to identify trends in species endangerment, park biodiversity levels, and observation counts to inform conservation insights using Python and common data science libraries.

## Features

- Modular Python package (`biodiversity/`) with helpers for data I/O, processing, and visualization.
- Automated report generation via `nbconvert` locally or in an isolated container.
- Comprehensive test suite with `pytest`.
- Pre-commit hooks for code formatting and linting (Black, Ruff, isort).
- Automated CI pipeline via GitHub Actions.
- Containerized Jupyter notebook server and report execution via Docker Compose.

## Project Structure

- `biodiversity.ipynb` — Primary analysis notebook (narrative + code)
- `biodiversity/` — Python package with helper modules (`data_io`, `processing`, `analysis`, `viz`)
- `tests/` — Unit and integration tests
- `scripts/` — Helper scripts (`run_report_docker.sh`, `run_report_docker.ps1`)
- `requirements.txt` / `pyproject.toml` — Runtime/dev dependencies and tool config
- `.github/workflows/ci.yml` — GitHub Actions CI pipeline
- `Dockerfile` / `docker-compose.yml` — Container setup files

## Prerequisites & Environment

- Python 3.11
- Core dependencies:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `jupyter`

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/username/biodiversity.git](https://github.com/username/biodiversity.git)
   cd biodiversity
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pip install -e .              # Optional: install biodiversity package in editable mode
   ```

## Development & Code Quality

### Testing

Run the test suite:

```bash
pytest -q
```

### Pre-commit & Formatting

Install pre-commit hooks configured with Black, Ruff, and isort:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Execution & Report Generation

### Local Execution

Generate the executed notebook and HTML report locally:

```bash
python -m nbconvert --to notebook --execute biodiversity.ipynb --output biodiversity-executed.ipynb
python -m nbconvert --to html biodiversity-executed.ipynb --output report.html
```

### Docker Execution (Isolated Environment)

Build and run using Docker Compose:

```bash
docker compose build
docker compose run --rm report
```

Or run via interactive helper scripts:

- **Linux / macOS / WSL**: `bash scripts/run_report_docker.sh`
- **Windows**: `powershell -ExecutionPolicy Bypass -File scripts/run_report_docker.ps1`

Outputs: `biodiversity-executed.ipynb`, `report.html`

## Usage & Workflow

Launch the interactive Jupyter notebook environment:

```bash
jupyter notebook biodiversity.ipynb
```

Typical analytical workflow:
1. **Data Review**: Load species and observation datasets to inspect schemas and missing values.
2. **Data Cleaning & Formatting**: Standardize species categories, merge observation logs, and clean null records.
3. **Exploratory Data Analysis (EDA)**: Evaluate species distributions and conservation status representations.
4. **Analysis & Modeling**: Examine observation frequencies across parks and evaluate endangered species patterns.
   - Which national parks have the highest species diversity and observation counts?
   - How are species conservation statuses distributed across categories (e.g., mammals, birds, plants)?
5. **Conclusions**: Synthesize findings regarding park biodiversity and document analytical limitations.

## Continuous Integration

CI pipelines are managed via GitHub Actions (`.github/workflows/ci.yml`), which automatically runs tests, checks code style, and executes the report build on repository updates.

## Data Source

This analysis utilizes the National Parks Biodiversity Data from the National Park Service.

- **Dataset**: [Biodiversity in National Parks](https://www.kaggle.com/datasets/nationalparkservice/park-biodiversity)
- **Required Files**:
  - `species_info.csv`: Species taxonomy and conservation status (`category`, `scientific_name`, `common_names`, `conservation_status`).
  - `observations.csv`: Species observation logs (`scientific_name`, `park_name`, `observations`).
- **Location**: Download and place both CSV files into the `data/` directory.
- **Repository Note**: Raw dataset files are ignored by git (`.gitignore`) and not committed to the repository to respect creator distribution rights.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.