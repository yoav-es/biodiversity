"""Data loading utilities for the biodiversity project."""
from pathlib import Path
from typing import Any

import pandas as pd


def _ensure_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Expected a file path, got: {path!r}")


def load_species(path: Any) -> pd.DataFrame:
    """Load species CSV into a DataFrame."""
    p = Path(path)
    _ensure_file(p)
    return pd.read_csv(p)


def load_observations(path: Any) -> pd.DataFrame:
    """Load observations CSV into a DataFrame."""
    p = Path(path)
    _ensure_file(p)
    return pd.read_csv(p)

