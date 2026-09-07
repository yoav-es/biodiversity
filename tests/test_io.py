"""Tests for data IO helpers."""

from pathlib import Path

import pandas as pd

from biodiversity.data_io import load_observations, load_species


def _write_csv(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def test_load_species(tmp_path: Path) -> None:
    p = tmp_path / "species.csv"
    _write_csv(p, "scientific_name,category,conservation_status\ns1,bird,Unknown\n")
    df = load_species(p)
    assert isinstance(df, pd.DataFrame)
    assert "scientific_name" in df.columns


def test_load_observations(tmp_path: Path) -> None:
    p = tmp_path / "obs.csv"
    _write_csv(p, "park_name,scientific_name,observations\nP1,s1,3\n")
    df = load_observations(p)
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "observations"] == 3
