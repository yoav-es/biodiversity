"""Tests for processing helpers."""

from pathlib import Path

import pandas as pd

from biodiversity.processing import (
    count_observations_by_species,
    observations_by_park,
    preprocess,
)


def test_count_observations_by_species() -> None:
    df = pd.DataFrame({"scientific_name": ["A", "A", "B"], "observations": [1, 2, 3]})
    counts = count_observations_by_species(df)
    assert counts.loc[counts["scientific_name"] == "A", "observations"].iloc[0] == 3


def test_observations_by_park() -> None:
    df = pd.DataFrame(
        {
            "park_name": ["P1", "P2", "P1"],
            "scientific_name": ["A", "B", "A"],
            "observations": [1, 2, 3],
        }
    )
    park_counts = observations_by_park(df)
    assert (
        park_counts.loc[park_counts["park_name"] == "P1", "observations"].iloc[0] == 4
    )


def test_preprocess(tmp_path: Path) -> None:
    # Synthetic small example
    species = pd.DataFrame(
        {
            "scientific_name": ["s1", "s2"],
            "category": ["bird", "mammal"],
            "conservation_status": [None, "Unknown"],
        }
    )
    observations = pd.DataFrame(
        {
            "park_name": ["P1", "P1"],
            "scientific_name": ["s1", "s1"],
            "observations": [2, 3],
        }
    )
    sp, obs = preprocess(species, observations)
    assert sp.loc[sp["scientific_name"] == "s1", "observations"].iloc[0] == 5
