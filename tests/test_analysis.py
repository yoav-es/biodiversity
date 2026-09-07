"""Tests for biodiversity.analysis helpers."""

import pandas as pd

from biodiversity.analysis import (
    at_risk_by_park,
    at_risk_observations,
    at_risk_species_df,
    conservation_pivot_by_category,
    filter_bats,
    get_at_risk_summary,
    get_unknown_status_by_category,
    observation_stats,
    species_stats,
    top_species_by_observations,
)


def test_observation_stats_and_top():
    obs = pd.DataFrame(
        {
            "park_name": ["P1", "P1", "P2"],
            "scientific_name": ["s1", "s1", "s2"],
            "observations": [2, 3, 1],
        }
    )
    stats = observation_stats(obs)
    assert stats["total_observations"] == 3
    assert stats["unique_species"] == 2
    top = top_species_by_observations(obs, n=1)
    assert top.iloc[0]["scientific_name"] == "s1"
    assert int(top.iloc[0]["observations"]) == 5


def test_species_stats_and_filters():
    species = pd.DataFrame(
        {
            "scientific_name": ["s1", "s2", "s3"],
            "category": ["Mammal", "Bird", "Mammal"],
            "conservation_status": [None, "Endangered", "Unknown"],
            "common_names": ["Little Bat", "Eagle", "Foo"],
        }
    )
    ss = species_stats(species)
    assert ss["num_species"] == 3
    assert ss["num_categories"] == 2
    ar = at_risk_species_df(species)
    assert "s2" in list(ar["scientific_name"])
    obs = pd.DataFrame(
        {
            "scientific_name": ["s2", "s3"],
            "park_name": ["P1", "P2"],
            "observations": [1, 2],
        }
    )
    aro = at_risk_observations(obs, species)
    assert aro.shape[0] == 1
    bats = filter_bats(species)
    assert bats.shape[0] == 1


def test_at_risk_summaries_and_pivot():
    species = pd.DataFrame(
        {
            "scientific_name": ["s1", "s2", "s3", "s4"],
            "category": ["A", "A", "B", "B"],
            "conservation_status": [
                "Endangered",
                "Species of Concern",
                "Unknown",
                "Threatened",
            ],
        }
    )
    summary = pd.DataFrame(get_at_risk_summary(species))
    assert "Endangered" in list(summary["conservation_status"])
    unknown = get_unknown_status_by_category(species)
    assert unknown["count"].sum() == 1
    pivot = conservation_pivot_by_category(species)
    assert "Endangered" in pivot.columns
